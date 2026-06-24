import csv
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import ReconcileRequest
from app.reconcile import reconcile_record
from app import reconcile as reconcile_module
from app import external_lookup
from app import review_store


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = ROOT / "data" / "benchmark_cases.csv"
client = TestClient(app)


@pytest.fixture(autouse=True)
def isolate_review_queue_and_live_lookup(monkeypatch):
    original_review_queue = (
        review_store.REVIEW_QUEUE_PATH.read_text(encoding="utf-8")
        if review_store.REVIEW_QUEUE_PATH.exists()
        else None
    )
    monkeypatch.setattr(reconcile_module, "lookup_all_external_sources", lambda gene, variant: [])
    review_store.clear_queue()
    yield
    review_store.clear_queue()
    if original_review_queue is None:
        review_store.REVIEW_QUEUE_PATH.unlink(missing_ok=True)
    else:
        review_store.REVIEW_QUEUE_PATH.write_text(original_review_queue, encoding="utf-8")
    review_store._store.clear()
    review_store._load_store()


def load_benchmark_cases():
    with BENCHMARK_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def expected_optional_gene(row):
    if row["expected_gene"] in {"REVIEW_REQUIRED", "CANNOT_RECONCILE"}:
        return None
    return row["expected_gene"]


def expected_optional_disease(row):
    if row["expected_disease"] == "CANNOT_RECONCILE":
        return None
    return row["expected_disease"]


def expected_optional_variant(row):
    if row["expected_variant"] == "CANNOT_RECONCILE":
        return None
    return row["expected_variant"]


def test_benchmark_cases_file_is_well_formed():
    rows = load_benchmark_cases()
    assert len(rows) == 191
    assert {row["expected_status"] for row in rows} == {
        "AUTO_RECONCILE",
        "REVIEW_REQUIRED",
        "CANNOT_RECONCILE",
    }


def test_all_benchmark_cases_reconcile_to_expected_status_and_concepts():
    failures = []
    for row in load_benchmark_cases():
        result = reconcile_record(
            ReconcileRequest(
                case_id=row["case_id"],
                cancer_type=row["input_disease"],
                gene=row["input_gene"],
                variant=row["input_variant"],
            )
        )
        expected_gene = expected_optional_gene(row)
        expected_variant = expected_optional_variant(row)

        checks = {
            "disease": result.canonical.cancer_type == expected_optional_disease(row),
            "gene": (
                result.canonical.gene == expected_gene
                or row["expected_gene"] == "REVIEW_REQUIRED"
            ),
            "variant": result.canonical.variant == expected_variant,
            "status": result.review_status == row["expected_status"],
        }
        if not all(checks.values()):
            failures.append(
                {
                    "case_id": row["case_id"],
                    "checks": checks,
                    "actual": (
                        result.canonical.cancer_type,
                        result.canonical.gene,
                        result.canonical.variant,
                        result.review_status,
                    ),
                    "expected": (
                        row["expected_disease"],
                        expected_gene,
                        expected_variant,
                        row["expected_status"],
                    ),
                }
            )

    assert failures == []


def test_review_required_trk_fusion_does_not_guess_specific_ntrk_gene():
    req = ReconcileRequest(cancer_type="NSCLC", gene="TRK", variant="pan-trk fusion")
    result = reconcile_record(req)
    assert result.review_status == "REVIEW_REQUIRED"
    assert result.confidence == "MEDIUM"
    assert result.canonical.cancer_type == "Lung Non-Small Cell Carcinoma"
    assert result.canonical.gene is None
    assert result.canonical.variant == "Categorical NTRK Fusion (NTRK1/NTRK2/NTRK3)"
    assert "multiple NTRK-family genes" in " ".join(result.notes)
    assert any(item.evidence_type == "cat_vrs_style_ambiguity" for item in result.evidence)
    assert {item["name"] for item in result.alternatives[:3]} == {
        "NTRK1 Fusion",
        "NTRK2 Fusion",
        "NTRK3 Fusion",
    }
    assert {item["categorical_variant"] for item in result.alternatives[:3]} == {
        "Categorical NTRK Fusion (NTRK1/NTRK2/NTRK3)"
    }


def test_review_required_trk_bare_fusion_preserves_family_variant():
    req = ReconcileRequest(cancer_type="NSCLC", gene="TRK", variant="fusion")
    result = reconcile_record(req)

    assert result.review_status == "REVIEW_REQUIRED"
    assert result.canonical.gene is None
    assert result.canonical.variant == "Categorical NTRK Fusion (NTRK1/NTRK2/NTRK3)"
    assert "categorical NTRK fusion ambiguity" in result.explanation


def test_catalog_review_required_variant_generates_governance_evidence_and_candidates():
    req = ReconcileRequest(cancer_type="Melanoma", gene="BRAF", variant="V600")
    result = reconcile_record(req)

    assert result.review_status == "REVIEW_REQUIRED"
    assert result.canonical.gene == "BRAF"
    assert result.canonical.variant == "BRAF V600 Mutation"
    assert any(item.evidence_type == "cat_vrs_style_ambiguity" for item in result.evidence)
    assert any(item.type == "variant_review_required" for item in result.evidence)
    assert {item["name"] for item in result.alternatives[:2]} == {
        "BRAF V600E",
        "BRAF V600K",
    }


def test_local_catalog_gene_with_scoped_variant_auto_reconciles():
    req = ReconcileRequest(cancer_type="Breast Cancer", gene="PIK3CA", variant="E545K")
    result = reconcile_record(req)

    assert result.review_status == "AUTO_RECONCILE"
    assert result.confidence == "HIGH"
    assert result.canonical.cancer_type == "Breast Invasive Carcinoma"
    assert result.canonical.gene == "PIK3CA"
    assert result.canonical.variant == "PIK3CA E545K"
    assert any(item.evidence_type == "local_gene_catalog_match" for item in result.evidence)


def test_cross_context_variant_candidate_routes_to_human_review():
    req = ReconcileRequest(cancer_type="NSCLC", gene="PIK3CA", variant="E545K")
    result = reconcile_record(req)

    assert result.review_status == "REVIEW_REQUIRED"
    assert result.confidence == "MEDIUM"
    assert result.canonical.cancer_type == "Lung Non-Small Cell Carcinoma"
    assert result.canonical.gene == "PIK3CA"
    assert result.canonical.variant == "PIK3CA E545K"
    assert any(item.evidence_type == "local_gene_catalog_candidate" for item in result.evidence)
    assert any(item.evidence_type == "external_candidate_evidence" for item in result.evidence)
    assert "External candidate fallback requires human review" in " ".join(result.audit_trail)


def test_unknown_gene_routes_to_cannot_reconcile():
    req = ReconcileRequest(cancer_type="NSCLC", gene="unknown_gene", variant="unknown_variant")
    result = reconcile_record(req)
    assert result.review_status == "CANNOT_RECONCILE"
    assert result.confidence == "LOW"
    assert result.canonical.gene is None
    assert result.canonical.variant is None
    assert "CANNOT_RECONCILE" in result.explanation


def test_empty_cancer_type_still_reconciles_gene_and_variant():
    req = ReconcileRequest(cancer_type=None, gene="HER2", variant="Amplification")
    result = reconcile_record(req)
    assert result.canonical.gene == "ERBB2"
    assert result.canonical.variant == "ERBB2 Amplification"
    assert result.review_status == "AUTO_RECONCILE"


def test_explanation_always_non_empty():
    req = ReconcileRequest(cancer_type="NSCLC", gene="FAKE_GENE_XYZ", variant="FAKE_VARIANT_XYZ")
    result = reconcile_record(req)
    assert result.explanation


def test_audit_trail_present_and_non_empty():
    req = ReconcileRequest(cancer_type="NSCLC", gene="HER2", variant="Amplification")
    result = reconcile_record(req)
    assert result.audit_trail
    assert "Confidence score" in " ".join(result.audit_trail)


def test_evidence_has_metadata_fields():
    req = ReconcileRequest(cancer_type="NSCLC", gene="HER2", variant="Amplification")
    result = reconcile_record(req)
    assert result.evidence
    for item in result.evidence:
        assert item.evidence_type
        assert item.retrieval_mode
        assert item.timestamp
        assert item.governance_standard


def test_external_evidence_sources_are_added_for_catalog_matches():
    req = ReconcileRequest(cancer_type="NSCLC", gene="EGFR", variant="Ex19del")
    result = reconcile_record(req)

    sources = {item.source for item in result.evidence}
    assert {"ClinVar", "CIViC", "OncoKB"}.issubset(sources)
    assert "External evidence references added" in " ".join(result.audit_trail)


def test_myvariant_lookup_success_returns_evidence(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "hits": [
                    {
                        "_id": "chr7:g.55181378A>T",
                        "clinvar": {"rcv": []},
                        "dbsnp": {"rsid": "rs123"},
                    }
                ]
            }

    monkeypatch.setattr(external_lookup.httpx, "get", lambda *args, **kwargs: FakeResponse())

    evidence = external_lookup.lookup_myvariant("EGFR", "C797S")

    assert len(evidence) == 1
    assert evidence[0]["source"] == "MyVariant.info"
    assert evidence[0]["evidence_type"] == "external_lookup"
    assert evidence[0]["retrieval_mode"] == "live_myvariant_api"
    assert evidence[0]["external_id"] == "chr7:g.55181378A>T"


def test_myvariant_lookup_failure_returns_error_evidence(monkeypatch):
    def fail_request(*args, **kwargs):
        raise RuntimeError("network unavailable")

    monkeypatch.setattr(external_lookup.httpx, "get", fail_request)

    evidence = external_lookup.lookup_myvariant("EGFR", "C797S")

    assert len(evidence) == 1
    assert evidence[0]["evidence_type"] == "external_lookup_error"
    assert evidence[0]["retrieval_mode"] == "live_myvariant_api_error"
    assert "network unavailable" in evidence[0]["description"]


def test_clinvar_lookup_success_returns_evidence(monkeypatch):
    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    responses = iter([
        FakeResponse({"esearchresult": {"idlist": ["123", "456"]}}),
        FakeResponse({
            "result": {
                "123": {"title": "EGFR C797S"},
                "456": {"title": "EGFR p.Cys797Ser"},
            }
        }),
    ])
    monkeypatch.setattr(external_lookup.httpx, "get", lambda *args, **kwargs: next(responses))

    evidence = external_lookup.lookup_clinvar("EGFR", "C797S")

    assert len(evidence) == 2
    assert evidence[0]["source"] == "ClinVar"
    assert evidence[0]["retrieval_mode"] == "live_clinvar_api"
    assert evidence[0]["external_id"] == "123"


def test_clinvar_lookup_failure_returns_error_evidence(monkeypatch):
    monkeypatch.setattr(
        external_lookup.httpx,
        "get",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("clinvar unavailable")),
    )

    evidence = external_lookup.lookup_clinvar("EGFR", "C797S")

    assert evidence[0]["retrieval_mode"] == "live_clinvar_api_error"
    assert "clinvar unavailable" in evidence[0]["description"]


def test_civic_lookup_success_returns_evidence(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "data": {
                    "search": [{"id": 12, "name": "V600E", "resultType": "VARIANT"}]
                }
            }

    monkeypatch.setattr(external_lookup.httpx, "post", lambda *args, **kwargs: FakeResponse())

    evidence = external_lookup.lookup_civic("BRAF", "V600E")

    assert len(evidence) == 1
    assert evidence[0]["source"] == "CIViC"
    assert evidence[0]["retrieval_mode"] == "live_civic_api"
    assert evidence[0]["external_id"] == "12"


def test_civic_lookup_failure_returns_error_evidence(monkeypatch):
    monkeypatch.setattr(
        external_lookup.httpx,
        "post",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("civic unavailable")),
    )

    evidence = external_lookup.lookup_civic("BRAF", "K601E")

    assert evidence[0]["retrieval_mode"] == "live_civic_api_error"
    assert "civic unavailable" in evidence[0]["description"]


def test_clingen_lookup_success_returns_evidence(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "@id": "https://reg.genome.network/allele/CA123456",
                "communityStandardTitle": "NM_005228.5(EGFR):c.2390G>C",
            }

    monkeypatch.setattr(external_lookup.httpx, "get", lambda *args, **kwargs: FakeResponse())

    evidence = external_lookup.lookup_clingen_allele_registry("EGFR", "C797S")

    assert len(evidence) == 1
    assert evidence[0]["retrieval_mode"] == "live_clingen_allele_registry_api"
    assert evidence[0]["external_id"] == "CA123456"


def test_clingen_lookup_failure_is_graceful(monkeypatch):
    monkeypatch.setattr(
        external_lookup.httpx,
        "get",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("registry unavailable")),
    )

    evidence = external_lookup.lookup_clingen_allele_registry("EGFR", "C797S")

    assert evidence[0]["retrieval_mode"] == "live_clingen_allele_registry_api_error"


def test_unknown_local_variant_triggers_external_lookup(monkeypatch):
    def fake_lookup(gene, variant):
        return [{
            "source": "MyVariant.info",
            "type": "external_variant_lookup",
            "description": f"External evidence candidate found for {gene} {variant}.",
            "evidence_type": "external_lookup",
            "confidence_weight": "LOW",
            "retrieval_mode": "live_myvariant_api",
            "external_id": "myvariant:EGFR-C797S",
            "timestamp": "2026-06-17T00:00:00+00:00",
        }]

    monkeypatch.setattr(reconcile_module, "external_variant_candidate_lookup", lambda gene, variant: [])
    monkeypatch.setattr(reconcile_module, "lookup_all_external_sources", fake_lookup)

    result = reconcile_record(ReconcileRequest(cancer_type="NSCLC", gene="EGFR", variant="C797S"))

    assert result.review_status == "REVIEW_REQUIRED"
    assert any(item.retrieval_mode == "live_myvariant_api" for item in result.evidence)
    assert "Live external evidence lookup started" in " ".join(result.audit_trail)
    assert "Live external evidence lookup completed: 1 evidence item(s)" in " ".join(result.audit_trail)


def test_external_evidence_turns_cannot_reconcile_into_review_required(monkeypatch):
    def fake_lookup(gene, variant):
        return [{
            "source": "MyVariant.info",
            "type": "external_variant_lookup",
            "description": f"External evidence candidate found for {gene} {variant}.",
            "evidence_type": "external_lookup",
            "confidence_weight": "LOW",
            "retrieval_mode": "live_myvariant_api",
            "external_id": "myvariant:unknown",
            "timestamp": "2026-06-17T00:00:00+00:00",
        }]

    monkeypatch.setattr(reconcile_module, "external_variant_candidate_lookup", lambda gene, variant: [])
    monkeypatch.setattr(reconcile_module, "lookup_all_external_sources", fake_lookup)

    response = client.post(
        "/reconcile",
        json={"case_id": "myvariant-review-1", "cancer_type": "NSCLC", "gene": "unknown_gene", "variant": "C797S"},
    )
    assert response.status_code == 200
    payload = response.json()

    assert payload["review_status"] == "REVIEW_REQUIRED"
    assert any(item["retrieval_mode"] == "live_myvariant_api" for item in payload["evidence"])
    assert "External evidence retrieved from live sources" in " ".join(payload["audit_trail"])
    assert "External evidence is advisory and requires human review." in payload["notes"]

    persisted = json.loads(review_store.REVIEW_QUEUE_PATH.read_text(encoding="utf-8"))
    assert any(item["case_id"] == "myvariant-review-1" for item in persisted["items"])


def test_auto_reconcile_does_not_run_external_lookup(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("AUTO_RECONCILE should not call live MyVariant lookup")

    monkeypatch.setattr(reconcile_module, "lookup_all_external_sources", fail_if_called)

    result = reconcile_record(ReconcileRequest(cancer_type="NSCLC", gene="EGFR", variant="Ex19del"))

    assert result.review_status == "AUTO_RECONCILE"
    assert not any(item.retrieval_mode == "live_myvariant_api" for item in result.evidence)


def test_llm_suggestion_is_review_required_only(monkeypatch):
    def fake_disambiguate(entity_type, input_value, candidates, context):
        return {
            "best_match": "NTRK1 Fusion",
            "confidence": 0.62,
            "rationale": "TRK fusion may map to an NTRK-family fusion.",
            "alternatives_considered": candidates,
            "provider": "test",
        }

    monkeypatch.setattr(reconcile_module.llm, "disambiguate", fake_disambiguate)

    result = reconcile_record(ReconcileRequest(cancer_type="NSCLC", gene="TRK", variant="fusion"))

    assert result.review_status == "REVIEW_REQUIRED"
    assert result.canonical.gene is None
    assert any(item.evidence_type == "llm_suggestion_review_required" for item in result.evidence)
    assert "LLM suggestion added for human review" in " ".join(result.audit_trail)


def test_llm_is_not_called_for_auto_reconcile(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("LLM should not be called for AUTO_RECONCILE")

    monkeypatch.setattr(reconcile_module.llm, "disambiguate", fail_if_called)

    result = reconcile_record(ReconcileRequest(cancer_type="NSCLC", gene="HER2", variant="amp"))

    assert result.review_status == "AUTO_RECONCILE"
    assert not any(item.evidence_type == "llm_suggestion_review_required" for item in result.evidence)


def test_benchmark_endpoint_reports_mvp_metrics():
    response = client.get("/benchmark")
    assert response.status_code == 200
    payload = response.json()

    assert payload["total_cases"] == 191
    assert payload["accuracy"] >= 0.90
    assert payload["coverage"] >= 0.95
    assert "review_rate" in payload
    assert payload["target_status"]["accuracy"] is True
    assert payload["target_status"]["coverage"] is True
    assert payload["counts"]["total_records"] == 191
    assert "candidate_evidence_cases" in payload["counts"]
    assert "approved_review_cases" in payload["counts"]


def test_review_queue_edit_decision_records_audit_trail():
    reconcile_response = client.post(
        "/reconcile",
        json={"case_id": "review-edit-1", "cancer_type": "NSCLC", "gene": "TRK", "variant": "fusion"},
    )
    assert reconcile_response.status_code == 200

    decision_response = client.post(
        "/review-queue/review-edit-1/decision",
        json={
            "case_id": "review-edit-1",
            "decision": "edit",
            "curator_id": "curator-test",
            "override_canonical": {
                "cancer_type": "Lung Non-Small Cell Carcinoma",
                "gene": "NTRK1",
                "variant": "NTRK1 Fusion",
            },
            "notes": "Edited after human review.",
        },
    )
    assert decision_response.status_code == 200
    item = decision_response.json()["item"]

    assert item["decision"] == "edit"
    assert item["canonical"]["gene"] == "NTRK1"
    assert item["decision_timestamp"]
    assert any("Human review decision: edit" in entry for entry in item["audit_trail"])


def test_review_queue_items_and_decisions_are_persisted_to_file():
    reconcile_response = client.post(
        "/reconcile",
        json={"case_id": "persist-review-1", "cancer_type": "AML", "gene": "IDH2", "variant": "R172K"},
    )
    assert reconcile_response.status_code == 200
    assert reconcile_response.json()["review_status"] == "REVIEW_REQUIRED"

    persisted = json.loads(review_store.REVIEW_QUEUE_PATH.read_text(encoding="utf-8"))
    persisted_item = next(item for item in persisted["items"] if item["case_id"] == "persist-review-1")
    assert persisted_item["canonical"]["variant"] == "IDH2 R172K"
    assert persisted_item["decision"] is None

    decision_response = client.post(
        "/review-queue/persist-review-1/decision",
        json={
            "case_id": "persist-review-1",
            "decision": "approve",
            "curator_id": "curator-test",
            "notes": "Approved after curator review.",
        },
    )
    assert decision_response.status_code == 200

    persisted = json.loads(review_store.REVIEW_QUEUE_PATH.read_text(encoding="utf-8"))
    persisted_item = next(item for item in persisted["items"] if item["case_id"] == "persist-review-1")
    assert persisted_item["decision"] == "approve"
    assert persisted_item["curator_id"] == "curator-test"
    assert persisted_item["created_at"]
    assert persisted_item["updated_at"]
    assert any("Human review decision: approve" in entry for entry in persisted_item["audit_trail"])


def test_review_queue_uses_stable_key_and_avoids_duplicates():
    payload = {"cancer_type": "AML", "gene": "IDH2", "variant": "R172K"}

    first = client.post("/reconcile", json=payload)
    second = client.post("/reconcile", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    queue = client.get("/review-queue?status=all").json()
    assert queue["total"] == 1
    assert queue["items"][0]["case_id"].startswith("review-")


def test_promote_to_catalog_is_an_explicit_disabled_stub():
    client.post(
        "/reconcile",
        json={"case_id": "promote-stub-1", "cancer_type": "AML", "gene": "IDH2", "variant": "R172K"},
    )

    response = client.post("/review-queue/promote-stub-1/promote")

    assert response.status_code == 200
    assert response.json()["status"] == "not_implemented"
    assert "do not modify" in response.json()["message"].lower()


def test_standards_alignment_endpoint_is_explicitly_non_compliant():
    response = client.get("/standards/alignment")

    assert response.status_code == 200
    payload = response.json()
    assert payload["product_positioning"] == "AI-assisted oncology curation and harmonization"
    assert "AI-Assisted Curation" in payload["aligned_use_cases"]
    assert "not an official GA4GH compliant implementation" in payload["disclaimer"]


def test_provenance_export_accepts_original_case_input():
    response = client.post(
        "/export/provenance",
        json={"cancer_type": "NSCLC", "gene": "HER2", "variant": "amp"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "PROV-O-inspired"
    assert payload["entity"]["canonical"]["gene"] == "ERBB2"
    assert payload["activity"]["name"] == "oncology_entity_reconciliation"
    assert payload["generated_at"]


def test_export_endpoints_accept_an_existing_reconciliation_result():
    reconciliation = client.post(
        "/reconcile",
        json={"cancer_type": "NSCLC", "gene": "HER2", "variant": "amp"},
    ).json()

    response = client.post("/export/provenance", json=reconciliation)

    assert response.status_code == 200
    assert response.json()["entity"]["canonical"]["gene"] == "ERBB2"


def test_knowledge_graph_export_contains_canonical_and_evidence_nodes():
    response = client.post(
        "/export/knowledge-graph",
        json={"case_id": "graph-1", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["export_status"] == "JSON-LD knowledge graph prototype"
    assert payload["@context"]
    node_types = {node["@type"] for node in payload["@graph"]}
    assert "onco:ReconciliationActivity" in node_types
    assert "onco:CanonicalGene" in node_types
    assert "onco:EvidenceRecord" in node_types
    assert "not an official" in payload["note"]


def test_vrs_ready_export_is_clearly_a_stub():
    response = client.post(
        "/export/vrs-ready",
        json={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "Ex19del"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "VRS-ready-stub"
    assert payload["variant"] == "EGFR Exon 19 Deletion"
    assert "not an official GA4GH VRS object" in payload["note"]


def test_cat_vrs_ready_export_preserves_ntrk_ambiguity():
    response = client.post(
        "/export/cat-vrs-ready",
        json={"cancer_type": "NSCLC", "gene": "TRK", "variant": "fusion"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "Cat-VRS-ready-stub"
    assert payload["ambiguity_preserved"] is True
    assert set(payload["members"][:3]) == {
        "NTRK1 Fusion",
        "NTRK2 Fusion",
        "NTRK3 Fusion",
    }


def test_va_spec_ready_export_contains_evidence_and_provenance():
    response = client.post(
        "/export/va-spec-ready",
        json={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "C797S"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "VA-Spec-ready-stub"
    assert payload["review_status"] == "REVIEW_REQUIRED"
    assert payload["evidence"]
    assert payload["provenance"]["type"] == "PROV-O-inspired"


def test_reconciliation_output_includes_curation_metadata():
    response = client.post(
        "/reconcile",
        json={"cancer_type": "NSCLC", "gene": "HER2", "variant": "amp"},
    )

    assert response.status_code == 200
    metadata = response.json()["curation_metadata"]
    assert metadata["curation_stage"] == "harmonize"
    assert metadata["human_governance_required"] is False
    assert metadata["catalog_promotion_candidate"] is False


def test_review_candidate_curation_metadata_requires_governance_and_promotion_review():
    response = client.post(
        "/reconcile",
        json={"cancer_type": "NSCLC", "gene": "EGFR", "variant": "C797S"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["review_status"] == "REVIEW_REQUIRED"
    assert payload["curation_metadata"]["human_governance_required"] is True
    assert payload["curation_metadata"]["catalog_promotion_candidate"] is True


def test_curation_report_combines_result_provenance_and_standards_stubs():
    response = client.post(
        "/curation/report",
        json={"case_id": "curation-report-1", "cancer_type": "NSCLC", "gene": "EGFR", "variant": "C797S"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["reconciliation_result"]["review_status"] == "REVIEW_REQUIRED"
    assert payload["provenance_export"]["type"] == "PROV-O-inspired"
    assert payload["knowledge_graph_export"]["export_status"] == "JSON-LD knowledge graph prototype"
    assert payload["standards_ready_exports"]["vrs_ready"]["type"] == "VRS-ready-stub"
    assert payload["standards_ready_exports"]["cat_vrs_ready"]["type"] == "Cat-VRS-ready-stub"
    assert payload["standards_ready_exports"]["va_spec_ready"]["type"] == "VA-Spec-ready-stub"
    assert payload["governance_summary"]["requires_human_review"] is True
    assert payload["governance_summary"]["candidate_for_catalog_promotion"] is True


def test_review_queue_reopen_moves_item_back_to_pending():
    reconcile_response = client.post(
        "/reconcile",
        json={"case_id": "review-reopen-1", "cancer_type": "NSCLC", "gene": "TRK", "variant": "fusion"},
    )
    assert reconcile_response.status_code == 200

    approve_response = client.post(
        "/review-queue/review-reopen-1/decision",
        json={
            "case_id": "review-reopen-1",
            "decision": "approve",
            "curator_id": "curator-test",
        },
    )
    assert approve_response.status_code == 200
    assert approve_response.json()["item"]["decision"] == "approve"

    reopen_response = client.post(
        "/review-queue/review-reopen-1/decision",
        json={
            "case_id": "review-reopen-1",
            "decision": "reopen",
            "curator_id": "curator-test",
            "notes": "Reopened after curator reconsideration.",
        },
    )
    assert reopen_response.status_code == 200
    item = reopen_response.json()["item"]

    assert item["decision"] is None
    assert any("Human review reopened" in entry for entry in item["audit_trail"])

    pending_response = client.get("/review-queue?status=pending")
    assert pending_response.status_code == 200
    assert any(row["case_id"] == "review-reopen-1" for row in pending_response.json()["items"])


# ── Evidence Upgrade Tests ────────────────────────────────────────────────


def test_canonical_hgvs_for_egfr_c797s():
    """Verify canonical HGVS resolution for EGFR C797S."""
    from app.canonical_hgvs import get_canonical_hgvs
    hgvs = get_canonical_hgvs("EGFR", "C797S")
    assert hgvs["canonical_variant"] == "EGFR C797S"
    assert hgvs["protein_hgvs"] == "p.Cys797Ser"
    assert hgvs["coding_hgvs"] == "c.2390G>C"
    assert hgvs["genomic_hgvs"] == "chr7:g.55249192G>C"
    assert hgvs["vrs_ready"] is False


def test_canonical_hgvs_for_braf_v600e():
    """Verify pattern-based HGVS generation for BRAF V600E."""
    from app.canonical_hgvs import get_canonical_hgvs
    hgvs = get_canonical_hgvs("BRAF", "V600E")
    assert hgvs["protein_hgvs"] == "p.Val600Glu"
    assert hgvs["canonical_variant"] == "BRAF V600E"


def test_canonical_hgvs_for_kras_g12c():
    """Verify HGVS from reference map for KRAS G12C."""
    from app.canonical_hgvs import get_canonical_hgvs
    hgvs = get_canonical_hgvs("KRAS", "G12C")
    assert hgvs["protein_hgvs"] == "p.Gly12Cys"
    assert hgvs["coding_hgvs"] == "c.34G>T"
    assert hgvs["genomic_hgvs"] == "chr12:g.25245350G>T"


def test_canonical_hgvs_unknown_variant_graceful():
    """Unknown variant with protein-like syntax uses pattern fallback gracefully."""
    from app.canonical_hgvs import get_canonical_hgvs
    hgvs = get_canonical_hgvs("UNKNOWN", "X999Z")
    # X999Z matches the protein pattern regex, so pattern fallback generates a HGVS
    assert hgvs["protein_hgvs"] is not None  # Pattern fallback works
    assert isinstance(hgvs["canonical_variant"], str)
    assert hgvs["vrs_ready"] is False


def test_canonical_hgvs_null_inputs():
    """Null gene/variant returns sensible defaults."""
    from app.canonical_hgvs import get_canonical_hgvs
    hgvs = get_canonical_hgvs(None, None)
    assert hgvs["canonical_variant"] is None
    assert hgvs["protein_hgvs"] is None
    assert hgvs["vrs_ready"] is False


def test_reconcile_response_includes_canonical_hgvs():
    """Reconcile response should contain canonical_hgvs field for known variants."""
    req = ReconcileRequest(case_id="hgvs-test", cancer_type="NSCLC", gene="EGFR", variant="L858R")
    result = reconcile_record(req)
    assert result.canonical_hgvs is not None
    assert result.canonical_hgvs.protein_hgvs == "p.Leu858Arg"
    assert result.canonical_hgvs.coding_hgvs == "c.2573T>G"
    assert result.canonical_hgvs.vrs_ready is False


def test_reconcile_response_includes_unified_evidence():
    """Reconcile response should include unified_evidence and federation."""
    req = ReconcileRequest(case_id="federation-test", cancer_type="NSCLC", gene="EGFR", variant="C797S")
    result = reconcile_record(req)
    assert result.unified_evidence is not None
    assert result.federation is not None
    assert len(result.unified_evidence) >= 5  # ClinVar + Local = at least 5


def test_unified_evidence_grouped_by_source():
    """Federated evidence should be grouped by source."""
    req = ReconcileRequest(case_id="source-group-test", cancer_type="NSCLC", gene="EGFR", variant="C797S")
    result = reconcile_record(req)
    by_source = result.federation.by_source
    assert "ClinVar" in by_source
    assert "Local Catalog" in by_source
    assert len(by_source["ClinVar"]) >= 1


def test_unified_evidence_boost_computed():
    """Evidence boost should be computed and included in response."""
    req = ReconcileRequest(case_id="boost-test", cancer_type="NSCLC", gene="EGFR", variant="C797S")
    result = reconcile_record(req)
    assert "evidence_boost" in result.evidence_score_breakdown
    assert result.evidence_score_breakdown["evidence_boost"] > 0


def test_evidence_boost_breakdown_has_details():
    """Evidence boost breakdown should contain per-source weights."""
    req = ReconcileRequest(case_id="boost-detail", cancer_type="NSCLC", gene="EGFR", variant="L858R")
    result = reconcile_record(req)
    breakdown = result.evidence_score_breakdown
    assert "evidence_breakdown" in breakdown
    assert len(breakdown["evidence_breakdown"]) >= 1


def test_clinvar_evidence_service_returns_structured_data(monkeypatch):
    """ClinVar service should return structured evidence items."""
    from app.evidence_clinvar import search_clinvar_by_text

    class FakeResponse:
        def raise_for_status(self): pass
        def json(self): return {"esearchresult": {"idlist": ["123"]}}

    class FakeSummaryResponse:
        def raise_for_status(self): pass
        def json(self):
            return {
                "result": {
                    "123": {
                        "variation_name": "NM_005228.5(EGFR):c.2390G>C",
                        "title": "EGFR C797S",
                        "clinical_significance": {"description": "Pathogenic"},
                        "review_status": {"description": "criteria provided, multiple submitters"},
                        "accession": "VCV000123",
                        "supporting_submissions": [{"submitter": "Lab A"}],
                    }
                }
            }

    responses = iter([FakeResponse(), FakeSummaryResponse()])
    monkeypatch.setattr("app.evidence_clinvar.httpx.get", lambda *args, **kwargs: next(responses))

    evidence = search_clinvar_by_text("EGFR", "C797S")
    assert len(evidence) >= 1
    assert evidence[0]["source"] == "ClinVar"
    assert evidence[0]["metadata"]["clinical_significance"] == "Pathogenic"
    assert evidence[0]["metadata"]["review_status"] == "criteria provided, multiple submitters"
    assert evidence[0]["metadata"]["citations_count"] == 1
    assert evidence[0]["confidence"] > 0.7  # Pathogenic + criteria provided → high confidence


def test_civic_evidence_service_returns_structured_data(monkeypatch):
    """CIViC service should return structured evidence items."""
    from app.evidence_civic import search_civic_variants

    class FakeResponse:
        def raise_for_status(self): pass
        def json(self):
            return {
                "data": {
                    "search": [
                        {"id": 42, "name": "V600E", "resultType": "VARIANT"}
                    ]
                }
            }

    monkeypatch.setattr("app.evidence_civic.httpx.post", lambda *args, **kwargs: FakeResponse())

    evidence = search_civic_variants("BRAF", "V600E")
    assert len(evidence) >= 1
    assert evidence[0]["source"] == "CIViC"
    assert evidence[0]["metadata"]["civic_variant_id"] == 42
    assert evidence[0]["confidence"] > 0


def test_federated_evidence_endpoint_returns_federation_result():
    """POST /evidence/federated should return full federation result."""
    response = client.post("/evidence/federated", json={"gene": "EGFR", "variant": "C797S"})
    assert response.status_code == 200
    payload = response.json()
    assert "unified_evidence" in payload
    assert "by_source" in payload
    assert "hgvs" in payload
    assert payload["evidence_count"] > 0
    assert payload["hgvs"]["protein_hgvs"] == "p.Cys797Ser"


def test_hgvs_resolve_endpoint():
    """POST /hgvs/resolve should return canonical HGVS."""
    response = client.post("/hgvs/resolve", json={"gene": "KRAS", "variant": "G12C"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["protein_hgvs"] == "p.Gly12Cys"
    assert payload["coding_hgvs"] == "c.34G>T"


def test_evidence_boost_endpoint():
    """POST /evidence/boost should compute boost from unified evidence."""
    sample_evidence = [
        {
            "source": "ClinVar",
            "summary": "Pathogenic variant",
            "confidence": 0.85,
            "metadata": {"clinical_significance": "Pathogenic", "review_status": "criteria provided, multiple submitters"}
        },
        {
            "source": "CIViC",
            "summary": "Predictive evidence",
            "confidence": 0.75,
            "metadata": {"evidence_level": "B", "evidence_type": "Predictive", "evidence_direction": "Supports"}
        },
    ]
    response = client.post("/evidence/boost", json={"unified_evidence": sample_evidence})
    assert response.status_code == 200
    payload = response.json()
    assert payload["evidence_boost"] > 0
    assert "ClinVar" in payload["breakdown"]
    assert "CIViC" in payload["breakdown"]


def test_reconcile_egfr_c797s_has_correct_hgvs_and_evidence():
    """End-to-end: EGFR C797S should produce correct HGVS and federated evidence."""
    req = ReconcileRequest(case_id="e2e-c797s", cancer_type="NSCLC", gene="EGFR", variant="C797S")
    result = reconcile_record(req)
    assert result.canonical_hgvs.protein_hgvs == "p.Cys797Ser"
    assert result.canonical_hgvs.coding_hgvs == "c.2390G>C"
    assert len(result.unified_evidence) >= 5
    assert result.federation.evidence_count > 0
    assert result.federation.evidence_boost.evidence_boost > 0


def test_reconcile_egfr_l858r_auto_reconcile_with_hgvs():
    """EGFR L858R should auto-reconcile and include HGVS."""
    req = ReconcileRequest(case_id="e2e-l858r", cancer_type="NSCLC", gene="EGFR", variant="L858R")
    result = reconcile_record(req)
    assert result.review_status == "AUTO_RECONCILE"
    assert result.canonical_hgvs.protein_hgvs == "p.Leu858Arg"
    assert result.canonical_hgvs.coding_hgvs == "c.2573T>G"
    assert len(result.unified_evidence) >= 3


def test_reconcile_kras_g12c_auto_reconcile_with_hgvs():
    """KRAS G12C should auto-reconcile and include HGVS."""
    req = ReconcileRequest(case_id="e2e-g12c", cancer_type="NSCLC", gene="KRAS", variant="G12C")
    result = reconcile_record(req)
    assert result.review_status == "AUTO_RECONCILE"
    assert result.canonical_hgvs.protein_hgvs == "p.Gly12Cys"
    assert result.canonical_hgvs.coding_hgvs == "c.34G>T"


def test_reconcile_braf_v600e_auto_reconcile_with_hgvs():
    """BRAF V600E should auto-reconcile and include HGVS."""
    req = ReconcileRequest(case_id="e2e-v600e", cancer_type="Melanoma", gene="BRAF", variant="V600E")
    result = reconcile_record(req)
    assert result.review_status == "AUTO_RECONCILE"
    assert result.canonical_hgvs.protein_hgvs == "p.Val600Glu"
    assert result.canonical_hgvs.coding_hgvs == "c.1799T>A"
    assert len(result.unified_evidence) >= 3


def test_reconcile_ntrk_fusion_review_required_with_hgvs():
    """NTRK fusion should be REVIEW_REQUIRED with categorical variant."""
    req = ReconcileRequest(case_id="e2e-ntrk", cancer_type="NSCLC", gene="TRK", variant="fusion")
    result = reconcile_record(req)
    assert result.review_status == "REVIEW_REQUIRED"
    assert result.canonical.gene is None
    assert "Categorical NTRK Fusion" in (result.canonical.variant or "")
    # TRK fusion → gene not resolved, so canonical_hgvs should have gene=None
    assert result.canonical_hgvs is not None


def test_federated_evidence_deduplication():
    """Federated evidence should not have duplicates within the same source (by URL)."""
    req = ReconcileRequest(case_id="dedup-test", cancer_type="NSCLC", gene="EGFR", variant="C797S")
    result = reconcile_record(req)
    # Check no duplicate source+url keys in unified_evidence
    # Source records from ClinVar each have unique URLs with variation IDs
    seen = set()
    for item in result.unified_evidence:
        # Use url + source as dedup key (each record has a unique URL)
        dedup_key = f"{item.source}|{item.url}"
        # Source records with no URL use summary prefix instead
        if not item.url:
            dedup_key = f"{item.source}|{item.evidence_type}|{item.summary[:40]}"
        assert dedup_key not in seen, f"Duplicate evidence: {dedup_key}"
        seen.add(dedup_key)


def test_evidence_boost_weight_config():
    """Evidence weight config should have expected structure."""
    from app.evidence_unified import EVIDENCE_WEIGHT_CONFIG
    assert "ClinVar" in EVIDENCE_WEIGHT_CONFIG
    assert "CIViC" in EVIDENCE_WEIGHT_CONFIG
    assert "Local Catalog" in EVIDENCE_WEIGHT_CONFIG
    assert "MyVariant.info" in EVIDENCE_WEIGHT_CONFIG
    assert EVIDENCE_WEIGHT_CONFIG["ClinVar"]["base_weight"] == 0.25
    assert EVIDENCE_WEIGHT_CONFIG["CIViC"]["base_weight"] == 0.25


def test_canonical_hgvs_vrs_future_fields():
    """Canonical HGVS should include VRS future fields."""
    from app.canonical_hgvs import get_canonical_hgvs
    hgvs = get_canonical_hgvs("EGFR", "L858R")
    assert "vrs_id" in hgvs
    assert "vrs_ready" in hgvs
    assert hgvs["vrs_id"] is None  # Not implemented yet
    assert hgvs["vrs_ready"] is False
