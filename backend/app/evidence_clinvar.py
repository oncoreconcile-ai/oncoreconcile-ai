"""
ClinVar Evidence Service
──────────────────────
Retrieves clinical significance, review status, variation ID, accession,
and citations from NCBI ClinVar using canonical HGVS when available.

Uses NCBI E-utilities (esearch/esummary) for ClinVar queries.
Falls back to gene + variant text search when HGVS is not available.
"""
import time
import httpx
from datetime import datetime, timezone
from typing import Optional

NCBI_EUTILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CLINVAR_URL = "https://www.ncbi.nlm.nih.gov/clinvar/variation"

# Rate limiting: NCBI requires 3 requests/second max without API key
_REQUEST_INTERVAL = 0.35  # seconds between requests
_last_request_time: float = 0.0


def _rate_limit():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _REQUEST_INTERVAL:
        time.sleep(_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.time()


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def search_clinvar_by_hgvs(
    protein_hgvs: str | None = None,
    coding_hgvs: str | None = None,
    genomic_hgvs: str | None = None,
) -> list[dict]:
    """
    Query ClinVar using HGVS notation. Tries protein_hgvs first, then
    coding_hgvs, then genomic_hgvs. Returns list of evidence items.
    """
    for hgvs in [protein_hgvs, coding_hgvs, genomic_hgvs]:
        if not hgvs:
            continue
        results = _search_clinvar(hgvs)
        if results:
            return results
    return []


def search_clinvar_by_text(gene: str | None, variant: str | None) -> list[dict]:
    """Fallback: query ClinVar using gene + variant text."""
    if not gene or not variant:
        return []
    query = f"{gene.strip()} {variant.strip()}"
    return _search_clinvar(query)


def _search_clinvar(query: str) -> list[dict]:
    """
    Execute ClinVar search via NCBI E-utilities.
    Returns structured evidence items.
    """
    _rate_limit()
    try:
        # Step 1: esearch to find ClinVar IDs
        search_response = httpx.get(
            f"{NCBI_EUTILS_URL}/esearch.fcgi",
            params={
                "db": "clinvar",
                "term": query,
                "retmode": "json",
                "retmax": 5,
            },
            timeout=10,
        )
        search_response.raise_for_status()
        search_data = search_response.json()
        identifiers = search_data.get("esearchresult", {}).get("idlist", [])
        if not identifiers:
            return []
    except Exception as exc:
        return [{
            "source": "ClinVar",
            "retrieval_mode": "live_clinvar_api",
            "evidence_type": "external_lookup_error",
            "description": f"ClinVar search failed for '{query}': {exc}",
            "confidence": 0.0,
            "url": None,
            "metadata": {"query": query, "error": str(exc)},
            "timestamp": _timestamp(),
        }]

    _rate_limit()
    try:
        # Step 2: esummary to get details
        summary_response = httpx.get(
            f"{NCBI_EUTILS_URL}/esummary.fcgi",
            params={
                "db": "clinvar",
                "id": ",".join(identifiers[:5]),
                "retmode": "json",
            },
            timeout=10,
        )
        summary_response.raise_for_status()
        results = summary_response.json().get("result", {})
    except Exception as exc:
        return [{
            "source": "ClinVar",
            "retrieval_mode": "live_clinvar_api",
            "evidence_type": "external_lookup_error",
            "description": f"ClinVar summary failed for IDs {identifiers}: {exc}",
            "confidence": 0.0,
            "url": None,
            "metadata": {"query": query, "identifiers": identifiers, "error": str(exc)},
            "timestamp": _timestamp(),
        }]

    evidence = []
    for identifier in identifiers[:5]:
        summary = results.get(str(identifier), {})
        variation_name = (
            summary.get("variation_name")
            or summary.get("title")
            or ""
        )

        # Extract clinical significance and review status
        clinical_significance = summary.get("clinical_significance", {})
        if isinstance(clinical_significance, str):
            description = clinical_significance
        else:
            description = clinical_significance.get("description", "") if clinical_significance else ""

        review_status = summary.get("review_status", {})
        if isinstance(review_status, str):
            review_status_text = review_status
        elif isinstance(review_status, dict):
            review_status_text = review_status.get("description", "")
        else:
            review_status_text = ""

        # Extract citations if available
        supporting_submissions = summary.get("supporting_submissions", [])
        citations_count = len(supporting_submissions) if isinstance(supporting_submissions, list) else 0

        # Confidence based on review status
        confidence = _confidence_from_review_status(review_status_text)

        accession = summary.get("accession") or f"VCV{identifier}" if identifier else None

        evidence.append({
            "source": "ClinVar",
            "retrieval_mode": "live_clinvar_api",
            "evidence_type": "clinical_significance",
            "description": (
                f"ClinVar clinical significance for {query}: {description or variation_name}. "
                f"Review status: {review_status_text}."
            ),
            "confidence": confidence,
            "url": f"{CLINVAR_URL}/{identifier}/" if identifier else None,
            "metadata": {
                "variation_id": identifier,
                "accession": accession,
                "variation_name": variation_name,
                "clinical_significance": description,
                "review_status": review_status_text,
                "citations_count": citations_count,
                "query": query,
            },
            "timestamp": _timestamp(),
        })

    return evidence


def _confidence_from_review_status(status: str) -> float:
    """Map ClinVar review status to numeric confidence."""
    status_lower = (status or "").lower()
    if "practice guideline" in status_lower:
        return 0.95
    if "reviewed by expert panel" in status_lower:
        return 0.90
    if "criteria provided" in status_lower and "multiple" in status_lower:
        return 0.80
    if "criteria provided" in status_lower:
        return 0.75
    if "conflicting" in status_lower or "conflict" in status_lower:
        return 0.50
    if "no assertion" in status_lower:
        return 0.30
    return 0.60


def search_clinvar_all(
    gene: str | None,
    variant: str | None,
    protein_hgvs: str | None = None,
    coding_hgvs: str | None = None,
    genomic_hgvs: str | None = None,
) -> list[dict]:
    """
    Comprehensive ClinVar search: try HGVS first, fall back to text.
    Returns list of evidence items from all found results.
    """
    results = search_clinvar_by_hgvs(protein_hgvs, coding_hgvs, genomic_hgvs)
    if not results:
        results = search_clinvar_by_text(gene, variant)
    return results


# ── Future extension points (design only) ─────────────────────────────────

# GA4GH Beacon extension point:
#   def query_clinvar_beacon(hgvs: str) -> dict | None:
#       """Query GA4GH Beacon-compatible ClinVar endpoint."""
#       raise NotImplementedError("GA4GH Beacon integration — future milestone")

# GA4GH Phenopackets extension point:
#   def clinvar_to_phenopacket(evidence: dict) -> dict:
#       """Convert ClinVar evidence to GA4GH Phenopacket."""
#       raise NotImplementedError("Phenopackets integration — future milestone")
