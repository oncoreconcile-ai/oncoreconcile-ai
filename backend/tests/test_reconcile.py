import csv
from pathlib import Path

from app.models import ReconcileRequest
from app.reconcile import reconcile_record


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = ROOT / "data" / "benchmark_cases.csv"


def load_benchmark_cases():
    with BENCHMARK_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def expected_optional_gene(row):
    if row["expected_gene"] in {"REVIEW_REQUIRED", "CANNOT_RECONCILE"}:
        return None
    return row["expected_gene"]


def expected_optional_variant(row):
    if row["expected_variant"] == "CANNOT_RECONCILE":
        return None
    return row["expected_variant"]


def test_benchmark_cases_file_is_well_formed():
    rows = load_benchmark_cases()
    assert len(rows) == 156
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
            "disease": result.canonical.cancer_type == row["expected_disease"],
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
    assert result.canonical.variant == "TRK Fusion"
    assert "multiple NTRK-family genes" in " ".join(result.notes)


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
    assert "Confidence computed" in " ".join(result.audit_trail)


def test_evidence_has_metadata_fields():
    req = ReconcileRequest(cancer_type="NSCLC", gene="HER2", variant="Amplification")
    result = reconcile_record(req)
    assert result.evidence
    for item in result.evidence:
        assert item.evidence_type == "alias_dictionary_match"
        assert item.retrieval_mode in {"local_seed_alias", "local_variant_catalog"}
