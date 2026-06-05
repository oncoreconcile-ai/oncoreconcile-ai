"""
Stub: VICC API normalization connector.

The Variant Interpretation for Cancer Consortium (VICC) publishes a suite
of open-source normalization services backed by HGNC, Ensembl, CIViC, and
OncoKB:
  - gene-normalization:      https://github.com/cancervariants/gene-normalization
  - variation-normalization: https://github.com/cancervariants/variation-normalization
  - disease-normalization:   https://github.com/cancervariants/disease-normalization

Intended role in the pipeline (Checkpoint 2+):
  Called after alias dictionary lookup fails. Passes the pre-normalized
  term to the appropriate VICC service and returns a canonical string if
  a match is found, or None if not.

  This positions VICC as an authoritative fallback rather than the primary
  lookup, preserving our ability to override or supplement its output with
  project-specific aliases.

See docs/decisions.md for the architectural rationale.
"""

from __future__ import annotations


def lookup_gene_vicc(normalized_gene: str) -> str | None:
    """
    Query the VICC gene-normalization service for a canonical gene symbol.

    Args:
        normalized_gene: Gene string after rule-based normalization.

    Returns:
        Canonical HGNC gene symbol, or None if no confident match found.
    """
    # TODO (Checkpoint 2): implement HTTP call to VICC gene-normalization API.
    # Expected endpoint: GET /gene/normalize?q={normalized_gene}
    # Return response.normalized_id mapped to HGNC symbol.
    return None


def lookup_variant_vicc(normalized_variant: str, canonical_gene: str | None) -> str | None:
    """
    Query the VICC variation-normalization service for a canonical variant.

    Args:
        normalized_variant: Variant string after rule-based normalization.
        canonical_gene: Canonical gene symbol (improves match accuracy).

    Returns:
        Canonical variant string (e.g. "EGFR p.L858R"), or None if not found.
    """
    # TODO (Checkpoint 2): implement HTTP call to VICC variation-normalization API.
    # Expected endpoint: GET /variant/normalize?q={normalized_variant}&gene={canonical_gene}
    return None


def lookup_disease_vicc(normalized_cancer_type: str) -> str | None:
    """
    Query the VICC disease-normalization service for a canonical disease name.

    Args:
        normalized_cancer_type: Cancer type string after rule-based normalization.

    Returns:
        Canonical disease name (e.g. "Non-Small Cell Lung Cancer"), or None.
    """
    # TODO (Checkpoint 2): implement HTTP call to VICC disease-normalization API.
    # Expected endpoint: GET /disease/normalize?q={normalized_cancer_type}
    return None
