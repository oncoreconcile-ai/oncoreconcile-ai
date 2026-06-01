from app.models import ReconcileRequest
from app.reconcile import reconcile_record


def test_her2_amplification():
    req = ReconcileRequest(
        case_id="case_001",
        cancer_type="NSCLC",
        gene="HER2",
        variant="Amplification",
    )
    result = reconcile_record(req)
    assert result.canonical.gene == "ERBB2"
    assert result.canonical.variant == "ERBB2 Amplification"
    assert result.review_status == "AUTO_RECONCILE"


def test_p53_r175h():
    req = ReconcileRequest(
        case_id="case_002",
        cancer_type="LUAD",
        gene="p53",
        variant="R175H",
    )
    result = reconcile_record(req)
    assert result.canonical.gene == "TP53"
    assert result.canonical.variant == "TP53 p.R175H"
