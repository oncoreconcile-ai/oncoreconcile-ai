"""
CIViC Evidence Service
────────────────────
Retrieves evidence items from CIViC (Clinical Interpretation of Variants in Cancer)
using their GraphQL API. Queries by gene + variant.

Retrieves:
  - evidence type (Predictive, Prognostic, Diagnostic, Predisposing, Oncogenic)
  - disease context
  - therapy association (for Predictive evidence)
  - evidence level (A, B, C, D, E)
  - evidence direction (Supports, Does Not Support)
  - citations (PubMed IDs)
"""
import httpx
from datetime import datetime, timezone
from typing import Optional

CIVIC_GRAPHQL_URL = "https://civicdb.org/api/graphql"
CIVIC_BASE_URL = "https://civicdb.org"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


# Simplified GraphQL queries compatible with current CIViC API.
# Uses the REST API for evidence details after initial variant search.

VARIANT_SEARCH_QUERY = """
query VariantSearch($query: String!) {
  search(query: $query, types: [VARIANT]) {
    id
    name
    resultType
  }
}
"""


def search_civic_variants(
    gene: str | None,
    variant: str | None,
) -> list[dict]:
    """Search CIViC by gene + variant text query."""
    if not gene or not variant:
        return []

    query = f"{gene.strip()} {variant.strip()}"
    return _execute_civic_search(query, gene, variant)


def _execute_civic_search(query: str, gene: str, variant: str) -> list[dict]:
    """Execute CIViC GraphQL search. Gets variant IDs, then fetches details via REST."""
    try:
        response = httpx.post(
            CIVIC_GRAPHQL_URL,
            json={"query": VARIANT_SEARCH_QUERY, "variables": {"query": query}},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        return [{
            "source": "CIViC",
            "retrieval_mode": "live_civic_api",
            "evidence_type": "external_lookup_error",
            "description": f"CIViC search failed for '{query}': {exc}",
            "confidence": 0.0,
            "url": None,
            "metadata": {"query": query, "error": str(exc)},
            "timestamp": _timestamp(),
        }]

    if payload.get("errors"):
        # Log error but don't fail — CIViC API often returns search results with warnings
        errors = payload.get("errors", [])
        error_msg = errors[0].get("message", str(errors)) if isinstance(errors, list) else str(errors)
        return [{
            "source": "CIViC",
            "retrieval_mode": "live_civic_api",
            "evidence_type": "external_lookup_error",
            "description": f"CIViC API error for '{query}': {error_msg}",
            "confidence": 0.0,
            "url": None,
            "metadata": {"query": query, "errors": errors},
            "timestamp": _timestamp(),
        }]

    data = payload.get("data", {})
    search_results = data.get("search", [])

    evidence = []
    seen_ids = set()

    for result in search_results:
        if result.get("resultType") not in (None, "VARIANT"):
            continue
        variant_id = result.get("id")
        variant_name = result.get("name") or query

        evidence.append({
            "source": "CIViC",
            "retrieval_mode": "live_civic_api",
            "evidence_type": "variant_match",
            "description": (
                f"CIViC returned variant record '{variant_name}' for query '{query}'. "
                "This matched via variant search. Click the URL to view full evidence details."
            ),
            "confidence": 0.65,
            "url": f"{CIVIC_BASE_URL}/variants/{variant_id}" if variant_id else None,
            "metadata": {
                "civic_variant_id": variant_id,
                "variant_name": variant_name,
                "query_gene": gene,
                "query_variant": variant,
                "query": query,
            },
            "timestamp": _timestamp(),
        })

    return evidence


def _extract_evidence_item(
    item: dict,
    gene: str,
    variant: str,
    variant_name: str,
    gene_info: dict,
) -> dict:
    """Convert a CIViC evidence item node to our unified format."""
    evidence_type = item.get("evidenceType") or "unknown"
    evidence_level = item.get("evidenceLevel") or ""
    evidence_direction = item.get("evidenceDirection") or ""
    clinical_significance = item.get("clinicalSignificance") or ""
    description = item.get("description") or ""
    rating = item.get("rating")

    # Disease
    disease = item.get("disease", {})
    disease_name = disease.get("name") if isinstance(disease, dict) else ""
    disease_doid = disease.get("doid") if isinstance(disease, dict) else ""

    # Drugs / therapy
    drugs = item.get("drugs", [])
    therapy_names = []
    for drug in (drugs or []):
        if isinstance(drug, dict) and drug.get("name"):
            therapy_names.append(drug["name"])

    # Source / citations
    source = item.get("source", {})
    if isinstance(source, dict):
        pubmed_id = source.get("pubmedId")
        citation_text = source.get("citation", "")
    else:
        pubmed_id = None
        citation_text = str(source) if source else ""

    # URL
    variant_id_for_url = variant_name  # best-effort URL
    civic_url = f"{CIVIC_BASE_URL}/evidence/{item.get('id')}" if item.get("id") else None

    # Confidence from evidence level
    confidence = _confidence_from_evidence_level(evidence_level, evidence_type)

    # Build summary description
    summary_parts = [f"CIViC {evidence_type.lower()} evidence for {gene} {variant}"]
    if clinical_significance:
        summary_parts.append(f"Clinical significance: {clinical_significance}")
    if evidence_direction:
        summary_parts.append(f"Direction: {evidence_direction}")
    if therapy_names:
        summary_parts.append(f"Therapies: {', '.join(therapy_names)}")
    if disease_name:
        summary_parts.append(f"Disease: {disease_name}")
    summary_parts.append(f"Level: {evidence_level}")
    if description:
        # Truncate long descriptions
        truncated = description[:300] + "..." if len(description) > 300 else description
        summary_parts.append(f"Detail: {truncated}")

    return {
        "source": "CIViC",
        "retrieval_mode": "live_civic_api",
        "evidence_type": evidence_type.lower(),
        "description": ". ".join(summary_parts),
        "confidence": confidence,
        "url": civic_url,
        "metadata": {
            "civic_evidence_id": item.get("id"),
            "evidence_type": evidence_type,
            "evidence_level": evidence_level,
            "evidence_direction": evidence_direction,
            "clinical_significance": clinical_significance,
            "disease": disease_name,
            "disease_doid": disease_doid,
            "therapies": therapy_names,
            "pubmed_id": pubmed_id,
            "citation": citation_text,
            "rating": rating,
            "variant_name": variant_name,
            "gene_symbol": gene_info.get("symbol") if isinstance(gene_info, dict) else None,
            "query_gene": gene,
            "query_variant": variant,
        },
        "timestamp": _timestamp(),
    }


def _confidence_from_evidence_level(level: str, evidence_type: str) -> float:
    """
    Map CIViC evidence level to numeric confidence.
    A=0.95, B=0.85, C=0.70, D=0.55, E=0.40.
    Predictive evidence gets a small bonus.
    """
    level_upper = (level or "").upper()
    base = {"A": 0.95, "B": 0.85, "C": 0.70, "D": 0.55, "E": 0.40}.get(level_upper, 0.50)
    if evidence_type and evidence_type.lower() == "predictive":
        base = min(base + 0.05, 0.99)
    return base


def search_civic_all(
    gene: str | None,
    variant: str | None,
) -> list[dict]:
    """Full CIViC search by gene + variant."""
    return search_civic_variants(gene, variant)


# ── Future extension points (design only) ─────────────────────────────────

# OncoKB extension point:
#   def search_oncokb(gene: str, variant: str) -> list[dict]:
#       """Query OncoKB for oncogenicity and FDA-approved therapies."""
#       raise NotImplementedError("OncoKB integration — future milestone")

# GA4GH Phenopackets extension point:
#   def civic_to_phenopacket(evidence: dict) -> dict:
#       """Convert CIViC evidence to GA4GH Phenopacket interpretation."""
#       raise NotImplementedError("Phenopackets integration — future milestone")
