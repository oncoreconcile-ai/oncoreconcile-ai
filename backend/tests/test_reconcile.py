import csv
from pathlib import Path

import pytest

from app.models import ReconcileRequest
from app.reconcile import reconcile_record


BENCHMARK_CSV = Path(__file__).resolve().parents[2] / "data" / "nsclc_benchmark.csv"

# Cases that cannot pass yet due to missing alias data.
# key: case_id, value: reason for xfail
KNOWN_GAPS = {
    "case_017": "E545K missing from variant_aliases.json — awaiting Rin's P0 data update",
}


def _load_benchmark_cases():
    params = []
    with BENCHMARK_CSV.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            case_id = row["case_id"]
            marks = []
            if case_id in KNOWN_GAPS:
                marks.append(pytest.mark.xfail(reason=KNOWN_GAPS[case_id], strict=True))
            params.append(pytest.param(
                row["cancer_type"],
                row["gene"],
                row["variant"],
                row["expected_cancer_type"] or None,
                row["expected_gene"] or None,
                row["expected_variant"] or None,
                id=case_id,
                marks=marks,
            ))
    return params


# review_status is not asserted here because it is fully derived from confidence, which is
# derived from the canonical outputs. Correct canonicals imply correct review_status by
# construction. See docs/decisions.md Decision 006 if this assumption ever needs revisiting.
@pytest.mark.parametrize(
    "cancer_type,gene,variant,exp_cancer_type,exp_gene,exp_variant",
    _load_benchmark_cases(),
)
def test_benchmark_reconciliation(cancer_type, gene, variant, exp_cancer_type, exp_gene, exp_variant):
    req = ReconcileRequest(cancer_type=cancer_type, gene=gene, variant=variant)
    result = reconcile_record(req)

    assert result.canonical.cancer_type == exp_cancer_type
    assert result.canonical.gene == exp_gene
    assert result.canonical.variant == exp_variant
