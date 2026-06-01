import json
from pathlib import Path
from .models import ReconcileRequest, ReconcileResponse, CanonicalConcept, EvidenceItem

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT.parent / "data"

def load_json(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

CANCER_ALIASES = load_json("cancer_aliases.json")
GENE_ALIASES = load_json("gene_aliases.json")
VARIANT_ALIASES = load_json("variant_aliases.json")


def normalize_cancer_type(value: str | None):
    if not value:
        return None, None
    canonical = CANCER_ALIASES.get(value) or CANCER_ALIASES.get(value.strip())
    return canonical, "Cancer type alias match" if canonical else None


def normalize_gene(value: str):
    canonical = GENE_ALIASES.get(value) or GENE_ALIASES.get(value.strip())
    return canonical, "Gene alias match" if canonical else None


def normalize_variant(value: str, canonical_gene: str | None):
    raw = value.strip()
    mapped = VARIANT_ALIASES.get(raw)
    if not mapped:
        return None, None

    if "{gene}" in mapped:
        if canonical_gene:
            mapped = mapped.replace("{gene}", canonical_gene)
        else:
            return None, None

    return mapped, "Variant synonym match"


def get_confidence(cancer_ok: bool, gene_ok: bool, variant_ok: bool):
    if gene_ok and variant_ok:
        return "HIGH"
    if gene_ok or variant_ok or cancer_ok:
        return "MEDIUM"
    return "LOW"


def get_review_status(confidence: str, canonical_gene: str | None, canonical_variant: str | None):
    if confidence == "HIGH":
        return "AUTO_RECONCILE"
    if canonical_gene or canonical_variant:
        return "REVIEW_REQUIRED"
    return "CANNOT_RECONCILE"


def reconcile_record(req: ReconcileRequest) -> ReconcileResponse:
    canonical_cancer, cancer_reason = normalize_cancer_type(req.cancer_type)
    canonical_gene, gene_reason = normalize_gene(req.gene)
    canonical_variant, variant_reason = normalize_variant(req.variant, canonical_gene)

    evidence = []
    if cancer_reason:
        evidence.append(EvidenceItem(
            source="Seed Knowledge Base",
            type="cancer_type_alias",
            description=f"{req.cancer_type} was mapped to {canonical_cancer}."
        ))
    if gene_reason:
        evidence.append(EvidenceItem(
            source="Seed Knowledge Base / HGNC-inspired",
            type="gene_alias",
            description=f"{req.gene} was mapped to {canonical_gene}."
        ))
    if variant_reason:
        evidence.append(EvidenceItem(
            source="Seed Knowledge Base",
            type="variant_synonym",
            description=f"{req.variant} was mapped to {canonical_variant}."
        ))

    confidence = get_confidence(bool(canonical_cancer), bool(canonical_gene), bool(canonical_variant))
    review_status = get_review_status(confidence, canonical_gene, canonical_variant)

    if evidence:
        explanation = " ".join([item.description for item in evidence])
    else:
        explanation = "No reliable reconciliation evidence was found. Human review is recommended."

    notes = []
    if not canonical_gene:
        notes.append("Gene could not be reconciled.")
    if not canonical_variant:
        notes.append("Variant could not be reconciled.")

    return ReconcileResponse(
        case_id=req.case_id,
        input=req.model_dump(),
        canonical=CanonicalConcept(
            cancer_type=canonical_cancer,
            gene=canonical_gene,
            variant=canonical_variant,
        ),
        evidence=evidence,
        explanation=explanation,
        confidence=confidence,
        review_status=review_status,
        notes=notes,
    )
