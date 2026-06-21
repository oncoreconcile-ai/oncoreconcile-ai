"""
Unit tests for OMOP CDM v5.4 export module.

Tests cover:
  - build_omop_records produces valid OMOP records
  - condition_occurrence from disease with SNOMED→OMOP concept_id resolution
  - measurement from gene with LOINC→OMOP concept_id resolution
  - observation from variant with LOINC→OMOP concept_id resolution
  - Categorical ambiguity preservation (NTRK fusion)
  - Unmapped disease/gene falls back to concept_id=0 with source_value preserved
  - Batch export (build_omop_records_batch)
  - API endpoints at /export/omop, /export/omop/download, /export/omop/batch
  - Download endpoint returns Content-Disposition header
"""

import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.omop_export import (
    build_omop_records,
    build_omop_records_batch,
    build_condition_occurrence,
    build_measurement_gene,
    build_observation_variant,
    SNOMED_CONCEPT_MAP,
)
from app.models import ReconcileRequest
from app.reconcile import reconcile_record
from app import reconcile as reconcile_module
from app import review_store
from app import external_lookup


client = TestClient(app)


@pytest.fixture(autouse=True)
def isolate_live_lookups_and_queue(monkeypatch):
    """Isolate external lookups and review queue for every test."""
    monkeypatch.setattr(reconcile_module, "lookup_all_external_sources", lambda gene, variant: [])
    monkeypatch.setattr(external_lookup, "lookup_all_external_sources", lambda gene, variant: [])
    review_store.clear_queue()
    yield
    review_store.clear_queue()


# ── OMOP record structure tests ─────────────────────────────────────────────


def test_build_omop_records_has_all_sections():
    records = build_omop_records(
        canonical={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert "condition_occurrences" in records
    assert "measurements" in records
    assert "observations" in records
    assert "metadata" in records


def test_build_omop_records_has_metadata_with_cdm_version():
    records = build_omop_records(
        canonical={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert records["metadata"]["cdm_version"] == "5.4"
    assert records["metadata"]["record_count"]["condition_occurrences"] >= 1
    assert records["metadata"]["record_count"]["measurements"] >= 1
    assert records["metadata"]["record_count"]["observations"] >= 1


def test_build_omop_records_empty_canonical_returns_empty_sections():
    records = build_omop_records(canonical={})
    assert records["condition_occurrences"] == []
    assert records["measurements"] == []
    assert records["observations"] == []


def test_build_omop_records_no_variant_skips_observation():
    records = build_omop_records(
        canonical={"cancer_type": "NSCLC", "gene": "EGFR"},
    )
    assert len(records["condition_occurrences"]) == 1
    assert len(records["measurements"]) == 1
    assert len(records["observations"]) == 0


# ── condition_occurrence tests ───────────────────────────────────────────────


def test_condition_occurrence_has_required_fields():
    record = build_condition_occurrence(disease="Lung Non-Small Cell Carcinoma")
    assert record is not None
    assert "condition_occurrence_id" in record
    assert record["person_id"] == 0
    assert record["condition_concept_id"] == 4144247  # OMOP concept for SNOMED 254637007
    assert record["condition_source_value"] == "Lung Non-Small Cell Carcinoma"
    assert record["condition_start_date"] is not None


def test_condition_occurrence_unknown_disease_uses_concept_id_0():
    record = build_condition_occurrence(disease="Rare Unknown Cancer")
    assert record is not None
    assert record["condition_concept_id"] == 0
    assert record["condition_source_value"] == "Rare Unknown Cancer"


def test_condition_occurrence_none_disease_returns_none():
    record = build_condition_occurrence(disease=None)
    assert record is None


def test_condition_occurrence_snomed_resolution_for_all_mapped_diseases():
    """Verify that all SNOMED mapped diseases resolve to the correct OMOP concept_id."""
    for snomed_code, expected_concept_id in SNOMED_CONCEPT_MAP.items():
        # Find a disease name that maps to this SNOMED code
        from app.omop_export import _snomed_code_for_disease
        from app.fhir_export import SNOMED_DISEASE_MAP
        found = False
        for disease_name, (code, _) in SNOMED_DISEASE_MAP.items():
            if code == snomed_code:
                record = build_condition_occurrence(disease=disease_name)
                assert record is not None
                assert record["condition_concept_id"] == expected_concept_id, (
                    f"Disease '{disease_name}' (SNOMED {snomed_code}) should map to OMOP "
                    f"concept_id {expected_concept_id}, got {record['condition_concept_id']}"
                )
                found = True
                break
        assert found, f"No disease name found for SNOMED code {snomed_code}"


# ── measurement (gene) tests ────────────────────────────────────────────────


def test_measurement_has_required_fields():
    record = build_measurement_gene(gene="EGFR")
    assert record is not None
    assert "measurement_id" in record
    assert record["person_id"] == 0
    assert record["measurement_concept_id"] == 4302377  # OMOP concept for LOINC 48018-6
    assert record["measurement_source_value"] == "EGFR"
    assert record["value_source_value"] == "HGNC:3236"


def test_measurement_unknown_gene_uses_symbol_as_source():
    record = build_measurement_gene(gene="UNKNOWNGENE")
    assert record is not None
    assert record["measurement_concept_id"] == 4302377  # LOINC 48018-6 still applies
    assert record["measurement_source_value"] == "UNKNOWNGENE"
    assert record["value_source_value"] == "UNKNOWNGENE"


def test_measurement_none_gene_returns_none():
    record = build_measurement_gene(gene=None)
    assert record is None


# ── observation (variant) tests ─────────────────────────────────────────────


def test_observation_has_required_fields():
    record = build_observation_variant(variant="EGFR L858R", gene="EGFR")
    assert record is not None
    assert "observation_id" in record
    assert record["person_id"] == 0
    assert record["observation_concept_id"] == 37393832  # OMOP concept for LOINC 69548-6
    assert record["observation_source_value"] == "EGFR L858R"
    assert record["value_as_string"] == "EGFR L858R"


def test_observation_categorical_variant_has_qualifier():
    """Categorical fusions should have qualifier_concept_id set."""
    record = build_observation_variant(
        variant="Categorical NTRK Fusion (NTRK1/NTRK2/NTRK3)",
        gene=None,
    )
    assert record is not None
    assert record["qualifier_concept_id"] == 37393870  # LOINC 81258-6
    assert record["qualifier_source_value"] == "Variant category"
    assert "Categorical NTRK Fusion" in record["value_as_string"]


def test_observation_standard_variant_no_qualifier():
    """Non-categorical variants should have qualifier_concept_id=0."""
    record = build_observation_variant(variant="BRAF V600E", gene="BRAF")
    assert record is not None
    assert record["qualifier_concept_id"] == 0
    assert record["qualifier_source_value"] is None


def test_observation_none_variant_returns_none():
    record = build_observation_variant(variant=None)
    assert record is None


# ── Batch export tests ──────────────────────────────────────────────────────


def test_build_omop_records_batch_returns_list():
    records = build_omop_records_batch([])
    assert records == []


def test_build_omop_records_batch_with_multiple_results():
    results = [
        {
            "case_id": "batch-001",
            "canonical": {"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
        },
        {
            "case_id": "batch-002",
            "canonical": {"cancer_type": "Melanoma", "gene": "BRAF", "variant": "V600E"},
        },
    ]
    all_records = build_omop_records_batch(results)
    assert len(all_records) == 2
    for record_set in all_records:
        assert "condition_occurrences" in record_set
        assert "measurements" in record_set
        assert "observations" in record_set


# ── API endpoint tests ──────────────────────────────────────────────────────


def test_export_omop_endpoint_returns_valid_structure():
    response = client.post(
        "/export/omop",
        json={"case_id": "omop-test-001", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert response.status_code == 200
    records = response.json()
    assert "condition_occurrences" in records
    assert "measurements" in records
    assert "observations" in records
    assert "metadata" in records
    assert len(records["condition_occurrences"]) == 1
    assert len(records["measurements"]) == 1


def test_export_omop_endpoint_accepts_existing_result():
    reconcile_response = client.post(
        "/reconcile",
        json={"cancer_type": "NSCLC", "gene": "HER2", "variant": "amp"},
    )
    assert reconcile_response.status_code == 200
    result = reconcile_response.json()

    omop_response = client.post("/export/omop", json=result)
    assert omop_response.status_code == 200
    records = omop_response.json()
    assert "condition_occurrences" in records
    assert "measurements" in records


def test_export_omop_download_has_content_disposition():
    response = client.post(
        "/export/omop/download",
        json={"case_id": "omop-dl-001", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment")
    assert response.headers["Content-Type"] == "application/json"
    records = json.loads(response.content)
    assert "condition_occurrences" in records


def test_export_omop_download_filename_contains_case_id():
    response = client.post(
        "/export/omop/download",
        json={"case_id": "my-omop-case", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert "my-omop-case" in response.headers["Content-Disposition"]


def test_export_omop_batch_endpoint():
    response = client.post(
        "/export/omop/batch",
        json={
            "results": [
                {"case_id": "omop-batch-001", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
                {"case_id": "omop-batch-002", "cancer_type": "Melanoma", "gene": "BRAF", "variant": "V600E"},
            ]
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "omop_records" in data
    assert data["total_records"] == 2


def test_export_omop_batch_accepts_single_result():
    response = client.post(
        "/export/omop/batch",
        json={"case_id": "single-omop", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 1


def test_export_omop_structure_matches_cdm_v54_schema():
    """Verify OMOP record has all fields from CDM v5.4 table definitions."""
    response = client.post(
        "/export/omop",
        json={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )
    assert response.status_code == 200
    records = response.json()

    # condition_occurrence fields
    co = records["condition_occurrences"][0]
    for field in [
        "condition_occurrence_id", "person_id", "condition_concept_id",
        "condition_start_date", "condition_source_value",
    ]:
        assert field in co, f"Missing CDM field: {field}"

    # measurement fields
    m = records["measurements"][0]
    for field in [
        "measurement_id", "person_id", "measurement_concept_id",
        "measurement_date", "measurement_source_value",
    ]:
        assert field in m, f"Missing CDM field: {field}"

    # observation fields
    o = records["observations"][0]
    for field in [
        "observation_id", "person_id", "observation_concept_id",
        "observation_date", "observation_source_value", "value_as_string",
    ]:
        assert field in o, f"Missing CDM field: {field}"


def test_real_reconciliation_omop_endpoint():
    """Integration test: real reconcile → OMOP export."""
    req = ReconcileRequest(
        case_id="omop-integration-001",
        cancer_type="NSCLC",
        gene="HER2",
        variant="amp",
    )
    result = reconcile_record(req).model_dump(mode="json")

    response = client.post("/export/omop", json=result)
    assert response.status_code == 200
    records = response.json()
    assert len(records["condition_occurrences"]) == 1
    assert len(records["measurements"]) == 1
    assert len(records["observations"]) == 1


def test_real_reconciliation_omop_download():
    """Integration test: real reconcile → downloadable OMOP."""
    req = ReconcileRequest(
        case_id="omop-dl-integration",
        cancer_type="NSCLC",
        gene="HER2",
        variant="amp",
    )
    result = reconcile_record(req).model_dump(mode="json")

    response = client.post("/export/omop/download", json=result)
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment")


def test_standards_root_mentions_omop():
    """Root endpoint should mention OMOP CDM as implemented."""
    response = client.get("/")
    assert response.status_code == 200
    payload = str(response.json())
    assert "OMOP CDM v5.4 Export" in payload
