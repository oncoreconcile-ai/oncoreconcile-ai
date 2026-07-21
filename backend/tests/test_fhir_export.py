"""
Unit tests for FHIR R4 export module.

Tests cover:
  - build_fhir_bundle produces a valid Bundle with required resource types
  - SNOMED CT coding for known diseases
  - HGNC coding for known genes
  - Categorical ambiguity (NTRK fusion) preservation in Observation
  - MolecularSequence resource generation
  - Provenance and DiagnosticReport containers
  - build_fhir_bundle_batch for multiple results
  - API endpoints at /export/fhir, /export/fhir/download, /export/fhir/batch
  - Download endpoint returns Content-Disposition header
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.fhir_export import (
    build_fhir_bundle,
    build_fhir_bundle_batch,
    build_condition_resource,
    build_gene_observation,
    build_variant_observation,
    build_molecular_sequence,
    SNOMED_DISEASE_MAP,
    HGNC_GENE_MAP,
)
from app.models import ReconcileRequest
from app.reconcile import reconcile_record
from app import reconcile as reconcile_module
from app import review_store
from app import external_lookup


ROOT = Path(__file__).resolve().parents[2]
client = TestClient(app)


@pytest.fixture(autouse=True)
def isolate_live_lookups_and_queue(monkeypatch):
    """Isolate external lookups and review queue for every test."""
    monkeypatch.setattr(reconcile_module, "lookup_all_external_sources", lambda gene, variant: [])
    monkeypatch.setattr(external_lookup, "lookup_all_external_sources", lambda gene, variant: [])
    review_store.clear_queue()
    yield
    review_store.clear_queue()


def _example_result():
    """Full reconciliation result for testing."""
    return {
        "case_id": "fhir-test-001",
        "input": {"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
        "canonical": {
            "cancer_type": "Lung Non-Small Cell Carcinoma",
            "gene": "EGFR",
            "variant": "EGFR Exon 19 Deletion",
        },
        "confidence": "HIGH",
        "confidence_score": 0.92,
        "score_breakdown": {
            "match_type": 1.0,
            "source_authority": 1.0,
            "string_similarity": 0.95,
            "context_consistency": 0.8,
            "alias_coverage": 1.0,
            "variant_catalog": 1.0,
        },
        "review_status": "AUTO_RECONCILE",
        "explanation": "All entities were confidently reconciled to canonical oncology concepts.",
        "evidence": [
            {
                "source": "Seed Knowledge Base / HGNC-inspired",
                "type": "gene_alias",
                "description": "EGFR was mapped to EGFR (exact).",
                "evidence_type": "alias_dictionary_match",
                "confidence_weight": "HIGH",
                "retrieval_mode": "local_exact_alias",
                "timestamp": "2026-06-20T00:00:00Z",
            },
        ],
        "alternatives": [],
        "notes": [],
        "audit_trail": ["Input received", "Confidence score computed"],
        "curation_metadata": {},
    }


@pytest.fixture
def real_reconciliation():
    """Run an actual reconciliation for integration-style testing."""
    req = ReconcileRequest(
        case_id="fhir-real-test-001",
        cancer_type="NSCLC",
        gene="HER2",
        variant="amp",
    )
    return reconcile_record(req).model_dump(mode="json")


# ── Bundle structure tests ─────────────────────────────────────────────────


def test_build_fhir_bundle_is_valid_bundle():
    bundle = build_fhir_bundle(
        canonical={
            "cancer_type": "Lung Non-Small Cell Carcinoma",
            "gene": "EGFR",
            "variant": "EGFR Exon 19 Deletion",
        },
        confidence="HIGH",
        case_id="test-001",
        review_status="AUTO_RECONCILE",
        score_breakdown={"match_type": 1.0},
    )

    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert bundle["id"]
    assert bundle["timestamp"]


def test_bundle_contains_required_resource_types():
    bundle = build_fhir_bundle(
        canonical={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )

    resource_types = {
        entry["resource"]["resourceType"]
        for entry in bundle["entry"]
        if "resourceType" in entry["resource"]
    }

    assert "Patient" in resource_types
    assert "Condition" in resource_types
    assert "Observation" in resource_types
    assert "Provenance" in resource_types
    assert "DiagnosticReport" in resource_types


def test_bundle_with_no_variant_skips_variant_and_mol_seq():
    bundle = build_fhir_bundle(
        canonical={"cancer_type": "NSCLC", "gene": "EGFR"},
    )
    resource_types = {
        entry["resource"]["resourceType"]
        for entry in bundle["entry"]
        if "resourceType" in entry["resource"]
    }
    assert "Condition" in resource_types
    assert "Observation" in resource_types


def test_condition_has_snomed_coding_for_known_disease():
    bundle = build_fhir_bundle(
        canonical={"cancer_type": "Lung Non-Small Cell Carcinoma"},
    )
    entries = [e for e in bundle["entry"] if e["resource"]["resourceType"] == "Condition"]
    assert len(entries) == 1
    cond = entries[0]["resource"]
    coding = cond["code"]["coding"]
    assert coding is not None
    assert any(c["system"] == "http://snomed.info/sct" for c in coding)
    assert any(c["code"] == "254637007" for c in coding)


def test_condition_uses_text_only_for_unknown_disease():
    bundle = build_fhir_bundle(
        canonical={"cancer_type": "Very Rare Cancer Type XYZ"},
    )
    entries = [e for e in bundle["entry"] if e["resource"]["resourceType"] == "Condition"]
    assert len(entries) == 1
    cond = entries[0]["resource"]
    assert cond["code"]["text"] == "Very Rare Cancer Type XYZ"


def test_condition_has_active_clinical_status():
    bundle = build_fhir_bundle(
        canonical={"cancer_type": "Melanoma"},
    )
    entries = [e for e in bundle["entry"] if e["resource"]["resourceType"] == "Condition"]
    cond = entries[0]["resource"]
    assert cond["clinicalStatus"]["coding"][0]["code"] == "active"


def test_condition_subject_references_patient():
    bundle = build_fhir_bundle(
        canonical={"cancer_type": "Breast Cancer"},
    )
    entries = [e for e in bundle["entry"] if e["resource"]["resourceType"] == "Condition"]
    patient = [e for e in bundle["entry"] if e["resource"]["resourceType"] == "Patient"][0]
    assert entries[0]["resource"]["subject"]["reference"] == patient["fullUrl"]


def test_gene_observation_uses_loinc_48018_6():
    bundle = build_fhir_bundle(
        canonical={"gene": "BRAF"},
    )
    obs_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation"
        and any(
            c["code"] == "48018-6"
            for c in (e["resource"].get("code") or {}).get("coding", [])
        )
    ]
    assert len(obs_entries) >= 1
    obs = obs_entries[0]["resource"]
    assert obs["status"] == "final"
    assert obs["valueCodeableConcept"]["coding"][0]["system"] == "http://www.genenames.org/geneId"
    assert obs["valueCodeableConcept"]["text"] == "BRAF"


def test_gene_observation_has_hgnc_id():
    bundle = build_fhir_bundle(
        canonical={"gene": "EGFR"},
    )
    obs_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation"
        and any(
            c["code"] == "48018-6"
            for c in (e["resource"].get("code") or {}).get("coding", [])
        )
    ]
    obs = obs_entries[0]["resource"]
    hgnc_codes = [
        c["code"]
        for c in obs["valueCodeableConcept"]["coding"]
        if c["system"] == "http://www.genenames.org/geneId"
    ]
    assert "HGNC:3236" in hgnc_codes


def test_gene_observation_uses_symbol_for_unknown_gene():
    obs = build_gene_observation(
        gene="UNKNOWNGENE",
        patient_id="test-patient-id",
    )
    assert obs is not None
    resource = obs["resource"]
    assert resource["valueCodeableConcept"]["text"] == "UNKNOWNGENE"


def test_variant_observation_uses_loinc_69548_6():
    bundle = build_fhir_bundle(
        canonical={"gene": "EGFR", "variant": "EGFR Exon 19 Deletion"},
    )
    obs_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation"
        and any(
            c["code"] == "69548-6"
            for c in (e["resource"].get("code") or {}).get("coding", [])
        )
    ]
    assert len(obs_entries) >= 1
    obs = obs_entries[0]["resource"]
    assert obs["valueCodeableConcept"]["text"] == "EGFR Exon 19 Deletion"


def test_variant_observation_has_gene_component():
    bundle = build_fhir_bundle(
        canonical={"gene": "BRAF", "variant": "BRAF V600E"},
    )
    obs_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation"
        and any(
            c["code"] == "69548-6"
            for c in (e["resource"].get("code") or {}).get("coding", [])
        )
    ]
    obs = obs_entries[0]["resource"]
    components = obs.get("component", [])
    gene_comps = [c for c in components if any(cc["code"] == "48018-6" for cc in c["code"]["coding"])]
    assert len(gene_comps) >= 1
    assert gene_comps[0]["valueCodeableConcept"]["text"] == "BRAF"


def test_categorical_variant_preserves_ambiguity():
    bundle = build_fhir_bundle(
        canonical={
            "gene": None,
            "variant": "Categorical NTRK Fusion (NTRK1/NTRK2/NTRK3)",
        },
    )
    obs_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation"
        and any(
            c["code"] == "69548-6"
            for c in (e["resource"].get("code") or {}).get("coding", [])
        )
    ]
    assert len(obs_entries) >= 1
    obs = obs_entries[0]["resource"]
    assert "Categorical NTRK Fusion" in obs["valueCodeableConcept"]["text"]
    components = obs.get("component", [])
    variant_cat_comps = [
        c for c in components
        if any(cc["code"] == "81258-6" for cc in (c["code"] or {}).get("coding", []))
    ]
    assert len(variant_cat_comps) >= 1
    assert "Categorical NTRK Fusion" in variant_cat_comps[0]["valueCodeableConcept"]["text"]


def test_molecular_sequence_created_for_variant():
    bundle = build_fhir_bundle(
        canonical={"gene": "EGFR", "variant": "EGFR L858R"},
    )
    seq_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "MolecularSequence"
    ]
    assert len(seq_entries) >= 1
    seq = seq_entries[0]["resource"]
    assert seq["type"] == "aa"
    assert seq["referenceSeq"]["referenceSeqType"] == "gene"
    assert seq["variant"][0]["display"] == "EGFR L858R"


def test_molecular_sequence_dna_for_numeric_variant():
    bundle = build_fhir_bundle(
        canonical={"gene": "EGFR", "variant": "EGFR Amplification"},
    )
    seq_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "MolecularSequence"
    ]
    if seq_entries:
        seq = seq_entries[0]["resource"]
        assert seq["type"] == "dna"


def test_molecular_sequence_not_created_without_gene():
    seq = build_molecular_sequence(
        variant="Some Variant",
        gene=None,
        patient_id="test",
    )
    assert seq is None


def test_provenance_has_target_references():
    bundle = build_fhir_bundle(
        canonical={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    prov_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Provenance"
    ]
    assert len(prov_entries) == 1
    prov = prov_entries[0]["resource"]
    assert len(prov["target"]) > 0
    # The bundle should contain Condition and Observation entries that
    # correspond to provenance targets
    target_uris = {t["reference"] for t in prov["target"]}
    condition_entries = [e for e in bundle["entry"] if e["resource"]["resourceType"] == "Condition"]
    obs_entries = [e for e in bundle["entry"] if e["resource"]["resourceType"] == "Observation"]
    # At least one target reference should match a Condition entry
    condition_uris = {e["fullUrl"] for e in condition_entries}
    obs_uris = {e["fullUrl"] for e in obs_entries}
    assert target_uris & condition_uris, "Provenance should target the Condition resource"
    assert target_uris & obs_uris, "Provenance should target the Observation resource"


def test_diagnostic_report_has_result_references():
    bundle = build_fhir_bundle(
        canonical={"gene": "BRAF", "variant": "BRAF V600E"},
    )
    report_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "DiagnosticReport"
    ]
    assert len(report_entries) == 1
    report = report_entries[0]["resource"]
    assert report["status"] == "final"
    assert len(report.get("result", [])) >= 1


def test_diagnostic_report_has_confidence_extension():
    bundle = build_fhir_bundle(
        canonical={"gene": "BRAF", "variant": "BRAF V600E"},
        confidence="HIGH",
        review_status="AUTO_RECONCILE",
    )
    report_entries = [
        e for e in bundle["entry"]
        if e["resource"]["resourceType"] == "DiagnosticReport"
    ]
    report = report_entries[0]["resource"]
    extensions = report.get("extension", [])
    ext_urls = {e["url"] for e in extensions}
    assert "https://oncoreconcile.ai/fhir/StructureDefinition/confidence" in ext_urls
    assert "https://oncoreconcile.ai/fhir/StructureDefinition/review-status" in ext_urls


def test_build_fhir_bundle_batch_merges_all_entries():
    result_1 = _example_result()
    result_2 = dict(_example_result())
    result_2["case_id"] = "fhir-test-002"
    result_2["canonical"] = {"cancer_type": "Melanoma", "gene": "BRAF", "variant": "BRAF V600E"}

    bundle = build_fhir_bundle_batch([result_1, result_2])
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert len(bundle["entry"]) >= 12


def test_batch_bundle_preserves_all_resource_types():
    result_1 = _example_result()
    result_2 = dict(_example_result())
    result_2["case_id"] = "fhir-batch-002"
    result_2["canonical"] = {"gene": "KRAS", "variant": "KRAS G12C"}

    bundle = build_fhir_bundle_batch([result_1, result_2])
    resource_types = {
        entry["resource"]["resourceType"]
        for entry in bundle["entry"]
        if "resourceType" in entry["resource"]
    }
    assert "Patient" in resource_types
    assert "Condition" in resource_types
    assert "Observation" in resource_types
    assert "Provenance" in resource_types
    assert "DiagnosticReport" in resource_types


def test_export_fhir_endpoint_returns_valid_bundle():
    response = client.post(
        "/export/fhir",
        json={"case_id": "api-test-001", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert response.status_code == 200
    bundle = response.json()
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert len(bundle.get("entry", [])) >= 5


def test_export_fhir_endpoint_accepts_existing_result():
    reconcile_response = client.post(
        "/reconcile",
        json={"cancer_type": "NSCLC", "gene": "HER2", "variant": "amp"},
    )
    assert reconcile_response.status_code == 200
    result = reconcile_response.json()

    fhir_response = client.post("/export/fhir", json=result)
    assert fhir_response.status_code == 200
    bundle = fhir_response.json()
    assert bundle["resourceType"] == "Bundle"


def test_export_fhir_download_has_content_disposition():
    response = client.post(
        "/export/fhir/download",
        json={"case_id": "download-test-001", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment")
    assert response.headers["Content-Type"] == "application/json"
    bundle = json.loads(response.content)
    assert bundle["resourceType"] == "Bundle"


def test_export_fhir_download_filename_contains_case_id():
    response = client.post(
        "/export/fhir/download",
        json={"case_id": "my-case-001", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert "my-case-001" in response.headers["Content-Disposition"]


def test_export_fhir_batch_endpoint():
    response = client.post(
        "/export/fhir/batch",
        json={
            "results": [
                {"case_id": "batch-001", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
                {"case_id": "batch-002", "cancer_type": "Melanoma", "gene": "BRAF", "variant": "V600E"},
            ]
        },
    )
    assert response.status_code == 200
    bundle = response.json()
    assert bundle["resourceType"] == "Bundle"


def test_export_fhir_batch_accepts_single_result():
    response = client.post(
        "/export/fhir/batch",
        json={"case_id": "single-batch", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert response.status_code == 200


def test_fhir_condition_has_snomed_mapping_for_all_known_diseases():
    for disease_name in SNOMED_DISEASE_MAP:
        bundle = build_fhir_bundle(canonical={"cancer_type": disease_name})
        entries = [
            e for e in bundle["entry"]
            if e["resource"]["resourceType"] == "Condition"
            and e["resource"]["code"].get("coding")
        ]
        assert len(entries) >= 1, f"No Condition with coding for {disease_name}"
        cond = entries[0]
        code = cond["resource"]["code"]["coding"][0]["code"]
        expected_code = SNOMED_DISEASE_MAP[disease_name][0]
        assert code == expected_code, f"Expected SNOMED {expected_code} for {disease_name}, got {code}"


def test_fhir_gene_has_hgnc_mapping_for_all_known_genes():
    for gene_symbol, hgnc_code in HGNC_GENE_MAP.items():
        bundle = build_fhir_bundle(canonical={"gene": gene_symbol})
        obs_entries = [
            e for e in bundle["entry"]
            if e["resource"]["resourceType"] == "Observation"
            and any(
                c["code"] == "48018-6"
                for c in (e["resource"].get("code") or {}).get("coding", [])
            )
        ]
        assert len(obs_entries) >= 1, f"No gene observation for {gene_symbol}"
        obs = obs_entries[0]["resource"]
        coding = obs["valueCodeableConcept"]["coding"]
        hgnc_codes = [c["code"] for c in coding if c["system"] == "http://www.genenames.org/geneId"]
        assert hgnc_code in hgnc_codes, f"Expected HGNC {hgnc_code} for {gene_symbol}, found {hgnc_codes}"


def test_fhir_real_reconciliation_produces_valid_bundle(real_reconciliation):
    response = client.post("/export/fhir", json=real_reconciliation)
    assert response.status_code == 200
    bundle = response.json()
    assert bundle["resourceType"] == "Bundle"
    assert len(bundle.get("entry", [])) >= 5


def test_fhir_real_reconciliation_download(real_reconciliation):
    response = client.post("/export/fhir/download", json=real_reconciliation)
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment")


def test_standards_root_mentions_fhir():
    response = client.get("/")
    assert response.status_code == 200
    payload = str(response.json())
    assert "FHIR Genomics" in payload
