"""
Canonical HGVS Layer
───────────────────
Generates canonical HGVS representations (protein, coding, genomic) for
reconciled gene + variant pairs. Uses a curated reference map for known
variants and falls back to pattern-based generation for well-known formats.

Extension points (future):
  - GA4GH VRS: vrs_id, vrs_ready fields
  - ClinGen Allele Registry: look up canonical HGVS
"""
import json
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

# Cache for reference map
_HGVS_MAP: dict | None = None


def _load_hgvs_map() -> dict:
    global _HGVS_MAP
    if _HGVS_MAP is not None:
        return _HGVS_MAP
    path = DATA_DIR / "hgvs_reference_map.json"
    if path.exists():
        _HGVS_MAP = json.loads(path.read_text(encoding="utf-8"))
    else:
        _HGVS_MAP = {}
    return _HGVS_MAP


def get_canonical_hgvs(gene: str | None, variant: str | None) -> dict:
    """
    Look up canonical HGVS representations for a gene/variant pair.

    Returns dict with keys:
      - canonical_variant: str (best canonical representation)
      - protein_hgvs: str | None
      - coding_hgvs: str | None
      - genomic_hgvs: str | None
      - vrs_id: str | None (future GA4GH VRS)
      - vrs_ready: bool (future GA4GH VRS)

    If no HGVS is known, returns the variant name as canonical_variant
    and all HGVS fields as None.
    """
    if not gene or not variant:
        return {
            "canonical_variant": variant,
            "protein_hgvs": None,
            "coding_hgvs": None,
            "genomic_hgvs": None,
            "vrs_id": None,
            "vrs_ready": False,
        }

    gene_upper = gene.strip().upper()
    variant_stripped = variant.strip()

    # Look up in reference map
    ref_map = _load_hgvs_map()
    gene_map = ref_map.get(gene_upper, {})
    if variant_stripped in gene_map:
        entry = gene_map[variant_stripped]
        # Clean variant name: prefer the mapped canonical_variant if present
        canonical = entry.get("canonical_variant") or variant_stripped
        return {
            "canonical_variant": canonical,
            "protein_hgvs": entry.get("protein_hgvs"),
            "coding_hgvs": entry.get("coding_hgvs"),
            "genomic_hgvs": entry.get("genomic_hgvs"),
            "vrs_id": entry.get("vrs_id"),           # future GA4GH VRS
            "vrs_ready": bool(entry.get("vrs_id")),   # future GA4GH VRS
        }

    # Try also with full variant name (gene + variant) as key
    full_key = f"{gene_upper} {variant_stripped}"
    for gene_key, variants in ref_map.items():
        # Case-insensitive gene key
        if gene_key.upper() != gene_upper:
            continue
        if full_key in variants:
            entry = variants[full_key]
            canonical = entry.get("canonical_variant") or variant_stripped
            return {
                "canonical_variant": canonical,
                "protein_hgvs": entry.get("protein_hgvs"),
                "coding_hgvs": entry.get("coding_hgvs"),
                "genomic_hgvs": entry.get("genomic_hgvs"),
                "vrs_id": entry.get("vrs_id"),
                "vrs_ready": bool(entry.get("vrs_id")),
            }

    # Known pattern generation for common formats
    hgvs = _generate_hgvs_pattern(gene_upper, variant_stripped)
    if hgvs:
        return hgvs

    return {
        "canonical_variant": variant_stripped,
        "protein_hgvs": None,
        "coding_hgvs": None,
        "genomic_hgvs": None,
        "vrs_id": None,
        "vrs_ready": False,
    }


def _generate_hgvs_pattern(gene: str, variant: str) -> dict | None:
    """
    Pattern-based HGVS generation for well-known variant formats.
    This is a best-effort generation and NOT a substitution for proper
    HGVS validation (HGVS nomenclator, Mutalyzer, etc.).
    """
    import re

    # Protein-level: e.g., V600E → p.Val600Glu
    aa_map = {
        "A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys",
        "Q": "Gln", "E": "Glu", "G": "Gly", "H": "His", "I": "Ile",
        "L": "Leu", "K": "Lys", "M": "Met", "F": "Phe", "P": "Pro",
        "S": "Ser", "T": "Thr", "W": "Trp", "Y": "Tyr", "V": "Val",
    }
    protein_match = re.fullmatch(r"[A-Z][a-z]?(\d{1,5})[A-Z][a-z]?", variant)
    if protein_match:
        pos = protein_match.group(1)
        ref_aa = variant[0].upper()
        alt_aa = variant[-1].upper()
        ref_name = aa_map.get(ref_aa, f"X{ref_aa}")
        alt_name = aa_map.get(alt_aa, f"X{alt_aa}")
        protein_hgvs = f"p.{ref_name}{pos}{alt_name}"
        return {
            "canonical_variant": f"{gene} {variant}",
            "protein_hgvs": protein_hgvs,
            "coding_hgvs": None,
            "genomic_hgvs": None,
            "vrs_id": None,
            "vrs_ready": False,
        }

    return None


# ── Future extension points (design only) ─────────────────────────────────

# GA4GH VRS extension point:
#   def to_vrs_allele(canonical_hgvs: dict) -> dict:
#       """Convert canonical HGVS to GA4GH VRS Allele object."""
#       raise NotImplementedError("GA4GH VRS integration — future milestone")

# ClinGen Allele Registry extension point:
#   def lookup_clingen_allele(protein_hgvs: str) -> dict | None:
#       """Resolve canonical HGVS to ClinGen Allele Registry CA ID."""
#       raise NotImplementedError("ClinGen Allele Registry — future milestone")

# OncoKB extension point:
#   def lookup_oncokb(gene: str, variant: str) -> dict | None:
#       """Query OncoKB for oncogenicity and actionability."""
#       raise NotImplementedError("OncoKB integration — future milestone")

# gnomAD extension point:
#   def lookup_gnomad(variant: str) -> dict | None:
#       """Query gnomAD for population frequency."""
#       raise NotImplementedError("gnomAD integration — future milestone")
