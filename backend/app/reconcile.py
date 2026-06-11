import json
import csv
from pathlib import Path
from .models import ReconcileRequest, ReconcileResponse, CanonicalConcept, EvidenceItem
from .explain import build_explanation

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

def load_json(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_disease_aliases() -> dict:
    aliases = load_json("cancer_aliases.json")
    aliases.update(load_json("disease_aliases.json"))
    return aliases


def load_variant_catalog() -> list[dict]:
    path = DATA_DIR / "gene_variant_catalog.csv"
    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as f:
        return [
            row
            for row in csv.DictReader(f)
            if row.get("gene") and row.get("variant")
        ]


def index_variant_catalog(rows: list[dict]) -> dict[tuple[str, str], list[dict]]:
    index = {}
    for row in rows:
        aliases = [row["variant"]]
        aliases.extend(
            alias.strip()
            for alias in row.get("variant_aliases", "").split(";")
            if alias.strip()
        )
        for alias in aliases:
            key = (row["gene"].strip(), alias.strip())
            index.setdefault(key, []).append(row)
            index.setdefault((key[0], key[1].lower()), []).append(row)
    return index


CANCER_ALIASES = load_disease_aliases()
GENE_ALIASES = load_json("gene_aliases.json")
GENE_REVIEW_REQUIRED = load_json("gene_review_required.json")
VARIANT_ALIASES = load_json("variant_aliases.json")
VARIANT_CATALOG = load_variant_catalog()
VARIANT_CATALOG_INDEX = index_variant_catalog(VARIANT_CATALOG)
REVIEW_REQUIRED_GENE_TERMS = {
    term
    for term, canonical in GENE_ALIASES.items()
    if canonical == "REVIEW_REQUIRED"
}
REVIEW_REQUIRED_GENE_TERMS.update({"TRK", "trk", "NTRK", "ntrk", "REVIEW_REQUIRED"})
CANNOT_RECONCILE_GENE_TERMS = {
    term
    for term, canonical in GENE_ALIASES.items()
    if canonical == "CANNOT_RECONCILE"
}
CANNOT_RECONCILE_GENE_TERMS.update({"CANNOT_RECONCILE"})


def normalize_cancer_type(value: str | None):
    if not value:
        return None, None
    raw = value.strip()
    canonical = (
        CANCER_ALIASES.get(value)
        or CANCER_ALIASES.get(raw)
        or CANCER_ALIASES.get(raw.lower())
    )
    return canonical, "Cancer type alias match" if canonical else None


def normalize_gene(value: str):
    raw = value.strip()
    canonical = GENE_ALIASES.get(value) or GENE_ALIASES.get(raw) or GENE_ALIASES.get(raw.lower())
    if canonical in {"REVIEW_REQUIRED", "CANNOT_RECONCILE"}:
        return None, None
    return canonical, "Gene alias match" if canonical else None


def get_gene_review_required(value: str):
    raw = value.strip()
    review = GENE_REVIEW_REQUIRED.get(value) or GENE_REVIEW_REQUIRED.get(raw)
    if review:
        return review
    if raw in REVIEW_REQUIRED_GENE_TERMS:
        return {
            "reason": (
                f"{raw} may refer to multiple NTRK-family genes and requires "
                "human review before selecting a canonical gene."
            )
        }
    return None


def get_gene_cannot_reconcile(value: str):
    return value.strip() in CANNOT_RECONCILE_GENE_TERMS


def find_catalog_variant(value: str, canonical_gene: str | None, gene_review_required: bool):
    raw = value.strip()
    candidate_genes = []
    if canonical_gene:
        candidate_genes.append(canonical_gene)
    if gene_review_required:
        candidate_genes.append("REVIEW_REQUIRED")
    candidate_genes.append("CANNOT_RECONCILE")

    for gene in candidate_genes:
        matches = (
            VARIANT_CATALOG_INDEX.get((gene, raw))
            or VARIANT_CATALOG_INDEX.get((gene, raw.lower()))
        )
        if matches:
            return matches[0], "Variant catalog match"

    return None, None


def normalize_variant(value: str, canonical_gene: str | None, gene_review_required: bool = False):
    catalog_row, catalog_reason = find_catalog_variant(
        value,
        canonical_gene,
        gene_review_required,
    )
    if catalog_row:
        return catalog_row["variant"], catalog_reason, catalog_row

    raw = value.strip()
    mapped = VARIANT_ALIASES.get(raw)
    if not mapped:
        return None, None, None

    if "{gene}" in mapped:
        if canonical_gene:
            mapped = mapped.replace("{gene}", canonical_gene)
        else:
            return None, None, None

    if " " in mapped:
        mapped_gene = mapped.split(" ", 1)[0]
        if mapped_gene.isupper() and canonical_gene != mapped_gene:
            return None, None, None

    return mapped, "Variant synonym match", None


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
    audit_trail = ["Input received"]

    audit_trail.append("Cancer alias lookup attempted")
    canonical_cancer, cancer_reason = normalize_cancer_type(req.cancer_type)
    audit_trail.append("Gene alias lookup attempted")
    canonical_gene, gene_reason = normalize_gene(req.gene)
    audit_trail.append("Gene review-required lookup attempted")
    gene_review_required = get_gene_review_required(req.gene)
    gene_cannot_reconcile = get_gene_cannot_reconcile(req.gene)
    if gene_review_required:
        canonical_gene = None
        gene_reason = None
    if gene_cannot_reconcile:
        canonical_gene = None
        gene_reason = None
    audit_trail.append("Variant synonym lookup attempted")
    canonical_variant, variant_reason, variant_catalog_row = normalize_variant(
        req.variant,
        canonical_gene,
        bool(gene_review_required),
    )

    evidence = []
    if cancer_reason:
        audit_trail.append("Cancer type alias match found")
        evidence.append(EvidenceItem(
            source="Seed Knowledge Base",
            type="cancer_type_alias",
            description=f"{req.cancer_type} was mapped to {canonical_cancer}.",
            evidence_type="alias_dictionary_match",
            confidence_weight="MEDIUM",
            retrieval_mode="local_seed_alias"
        ))
    if gene_reason:
        audit_trail.append("Gene alias match found")
        evidence.append(EvidenceItem(
            source="Seed Knowledge Base / HGNC-inspired",
            type="gene_alias",
            description=f"{req.gene} was mapped to {canonical_gene}.",
            evidence_type="alias_dictionary_match",
            confidence_weight="HIGH",
            retrieval_mode="local_seed_alias"
        ))
    if gene_review_required:
        audit_trail.append("Gene ambiguity requiring review found")
        evidence.append(EvidenceItem(
            source="Seed Knowledge Base / HGNC-inspired",
            type="gene_review_required",
            description=(
                f"{req.gene} may refer to NTRK1, NTRK2, or NTRK3. "
                "Rather than guessing, the system recommends human review."
            ),
            evidence_type="requires_human_review",
            confidence_weight="MEDIUM",
            retrieval_mode="local_review_required"
        ))
    if variant_reason:
        audit_trail.append("Variant synonym match found")
        source = "Curated Gene Variant Catalog" if variant_catalog_row else "Seed Knowledge Base"
        confidence_weight = "MEDIUM" if variant_catalog_row and variant_catalog_row.get("mvp_status") != "AUTO_RECONCILE" else "HIGH"
        evidence.append(EvidenceItem(
            source=source,
            type="variant_synonym",
            description=f"{req.variant} was mapped to {canonical_variant}.",
            evidence_type="alias_dictionary_match",
            confidence_weight=confidence_weight,
            retrieval_mode="local_variant_catalog" if variant_catalog_row else "local_seed_alias"
        ))
    if not evidence:
        audit_trail.append("No alias/synonym evidence found")

    confidence = get_confidence(bool(canonical_cancer), bool(canonical_gene), bool(canonical_variant))
    review_status = get_review_status(confidence, canonical_gene, canonical_variant)
    if gene_cannot_reconcile:
        canonical_variant = None
        confidence = "LOW"
        review_status = "CANNOT_RECONCILE"
    if gene_review_required:
        confidence = "MEDIUM"
        review_status = "REVIEW_REQUIRED"
    if variant_catalog_row:
        catalog_status = variant_catalog_row.get("mvp_status")
        if catalog_status in {"REVIEW_REQUIRED", "CANNOT_RECONCILE"}:
            review_status = catalog_status
            confidence = "MEDIUM" if catalog_status == "REVIEW_REQUIRED" else "LOW"
            if catalog_status == "CANNOT_RECONCILE":
                canonical_variant = None
        elif catalog_status == "AUTO_RECONCILE" and canonical_gene and canonical_variant:
            confidence = "HIGH"
            review_status = "AUTO_RECONCILE"
    audit_trail.append(f"Confidence computed: {confidence}")
    audit_trail.append(f"Review status decided: {review_status}")

    evidence_dicts = [e.model_dump() for e in evidence]
    explanation = build_explanation(evidence_dicts, confidence, review_status)
    audit_trail.append("Explanation generated")

    notes = []
    if gene_review_required:
        notes.append(gene_review_required.get("reason", "Gene requires human review."))
        audit_trail.append("Gene marked for human review")
    if not canonical_gene:
        notes.append("Gene could not be reconciled.")
        audit_trail.append("Gene unresolved")
    if not canonical_variant:
        notes.append("Variant could not be reconciled.")
        audit_trail.append("Variant unresolved")

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
        audit_trail=audit_trail,
    )
