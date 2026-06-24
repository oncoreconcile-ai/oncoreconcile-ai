"""
Unified Evidence Model & Federation
─────────────────────────────────
Common schema for all evidence sources (ClinVar, CIViC, Local Catalog, MyVariant.info).
Provides evidence ranking, weighting for confidence score enhancement, and source-grouped
display formatting.
"""
from datetime import datetime, timezone
from typing import Optional
from .canonical_hgvs import get_canonical_hgvs
from .evidence_clinvar import search_clinvar_all
from .evidence_civic import search_civic_all


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Unified Evidence Schema ──────────────────────────────────────────────────

UNIFIED_EVIDENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "source": {"type": "string", "description": "ClinVar | CIViC | Local Catalog | MyVariant.info"},
        "source_label": {"type": "string", "description": "Human-readable source display label"},
        "source_badge": {"type": "string", "description": "Badge key for frontend display"},
        "variant": {"type": "string", "description": "Variant identifier used in the query"},
        "evidence_type": {"type": "string", "description": "Type of evidence (clinical_significance, predictive, etc.)"},
        "summary": {"type": "string", "description": "Human-readable summary of the evidence"},
        "confidence": {"type": "number", "description": "Numeric confidence 0.0–1.0"},
        "url": {"type": "string", "description": "Link to the source record"},
        "metadata": {"type": "object", "description": "Source-specific details"},
        "retrieval_mode": {"type": "string", "description": "How the evidence was retrieved"},
        "timestamp": {"type": "string", "format": "date-time"},
    },
    "required": ["source", "summary", "confidence"],
}


# ── Evidence weighting for confidence score enhancement ────────────────────

EVIDENCE_WEIGHT_CONFIG = {
    "ClinVar": {
        "base_weight": 0.25,
        "pathogenic_multiplier": 1.2,
        "review_status_bonus": {
            "practice guideline": 0.15,
            "reviewed by expert panel": 0.12,
            "criteria provided": 0.08,
            "conflicting": 0.0,
            "no assertion": -0.10,
        },
    },
    "CIViC": {
        "base_weight": 0.25,
        "level_weights": {
            "A": 0.15,
            "B": 0.10,
            "C": 0.05,
            "D": 0.0,
            "E": -0.05,
        },
        "predictive_bonus": 0.08,
        "direction_bonus": {"Supports": 0.05, "Does Not Support": -0.05},
    },
    "Local Catalog": {
        "base_weight": 0.20,
        "auto_reconcile_bonus": 0.10,
    },
    "MyVariant.info": {
        "base_weight": 0.10,
    },
}


def compute_evidence_boost(unified_evidence: list[dict]) -> dict:
    """
    Compute confidence score boost from evidence sources.

    Returns:
    {
        "evidence_boost": float (0.0–0.5 added to base confidence),
        "breakdown": {source: float},
        "details": [str] (human-readable explanation of each contribution)
    }
    """
    total_boost = 0.0
    breakdown = {}
    details = []

    for ev in unified_evidence:
        source = ev.get("source", "")
        config = EVIDENCE_WEIGHT_CONFIG.get(source, {})
        base = config.get("base_weight", 0.10)
        boost = base

        if source == "ClinVar":
            meta = ev.get("metadata", {})
            sig = (meta.get("clinical_significance") or "").lower()
            review_status = (meta.get("review_status") or "").lower()

            # Pathogenic/likely_pathogenic
            if "pathogenic" in sig:
                boost *= config.get("pathogenic_multiplier", 1.2)
                details.append(f"ClinVar: Pathogenic designation → +{boost:.3f}")
            elif "benign" in sig:
                boost *= 0.5
                details.append(f"ClinVar: Benign designation → reduced weight")

            # Review status bonus
            for status, bonus in config.get("review_status_bonus", {}).items():
                if status in review_status:
                    boost += bonus
                    details.append(f"ClinVar: Review status '{status}' → +{bonus:.3f}")
                    break

        elif source == "CIViC":
            meta = ev.get("metadata", {})
            level = (meta.get("evidence_level") or "").upper()
            ev_type = (meta.get("evidence_type") or "").lower()
            direction = (meta.get("evidence_direction") or "").lower()

            # Level weight
            for lvl, w in config.get("level_weights", {}).items():
                if level == lvl:
                    boost += w
                    details.append(f"CIViC: Level {level} weight → +{w:.3f}")
                    break

            # Predictive bonus
            if ev_type == "predictive":
                boost += config.get("predictive_bonus", 0.08)
                details.append(f"CIViC: Predictive evidence bonus → +0.080")

            # Direction bonus
            direction_lower = {k.lower(): v for k, v in config.get("direction_bonus", {}).items()}
            if direction in direction_lower:
                boost += direction_lower[direction]
                details.append(f"CIViC: Direction '{direction}' → {direction_lower[direction]:+.3f}")

        elif source == "Local Catalog":
            meta = ev.get("metadata", {})
            if meta.get("mvp_status") == "AUTO_RECONCILE":
                boost += config.get("auto_reconcile_bonus", 0.10)
                details.append(f"Local Catalog: AUTO_RECONCILE status → +0.100")

        total_boost += boost
        breakdown[source] = round(boost, 3)

    # Cap total boost at 0.5
    total_boost = min(total_boost, 0.5)

    return {
        "evidence_boost": round(total_boost, 3),
        "breakdown": breakdown,
        "details": details,
    }


# ── Evidence Federation ──────────────────────────────────────────────────────

def fetch_federated_evidence(
    gene: str | None,
    variant: str | None,
    canonical_gene: str | None = None,
    canonical_variant: str | None = None,
    local_evidence: list[dict] | None = None,
) -> dict:
    """
    Fetch evidence from all configured sources and merge into unified format.

    Returns:
    {
        "unified_evidence": [...],
        "by_source": {"ClinVar": [...], "CIViC": [...], "Local Catalog": [...], "MyVariant.info": [...]},
        "hgvs": {...},
        "evidence_count": int,
        "evidence_boost": {...},
        "errors": [str]
    }
    """
    # Resolve canonical HGVS
    hgvs = get_canonical_hgvs(canonical_gene or gene, canonical_variant or variant)

    # Gather evidence from all sources
    clinvar_results = search_clinvar_all(
        gene=canonical_gene or gene,
        variant=canonical_variant or variant,
        protein_hgvs=hgvs.get("protein_hgvs"),
        coding_hgvs=hgvs.get("coding_hgvs"),
        genomic_hgvs=hgvs.get("genomic_hgvs"),
    )

    civic_results = search_civic_all(
        gene=canonical_gene or gene,
        variant=canonical_variant or variant,
    )

    # Normalize local evidence to unified format
    local_unified = _normalize_local_evidence(local_evidence or [])

    # Merge and deduplicate by source + metadata variation ID / evidence ID
    all_evidence = []
    seen_keys = set()

    unified_by_source = {
        "ClinVar": [],
        "CIViC": [],
        "Local Catalog": [],
        "MyVariant.info": [],
    }

    errors = []

    for ev in clinvar_results:
        if ev.get("evidence_type") == "external_lookup_error":
            errors.append(f"ClinVar: {ev.get('description', '')}")
            continue
        dedup_key = _dedup_key(ev)
        if dedup_key not in seen_keys:
            seen_keys.add(dedup_key)
            unified = _to_unified(ev, "ClinVar")
            all_evidence.append(unified)
            unified_by_source["ClinVar"].append(unified)

    for ev in civic_results:
        if ev.get("evidence_type") == "external_lookup_error":
            errors.append(f"CIViC: {ev.get('description', '')}")
            continue
        dedup_key = _dedup_key(ev)
        if dedup_key not in seen_keys:
            seen_keys.add(dedup_key)
            unified = _to_unified(ev, "CIViC")
            all_evidence.append(unified)
            unified_by_source["CIViC"].append(unified)

    for ev in local_unified:
        dedup_key = _dedup_key(ev)
        if dedup_key not in seen_keys:
            seen_keys.add(dedup_key)
            unified = _to_unified(ev, "Local Catalog")
            all_evidence.append(unified)
            unified_by_source["Local Catalog"].append(unified)
            # Also check for MyVariant.info in local evidence
            if "myvariant" in (ev.get("retrieval_mode") or "").lower():
                unified_by_source["MyVariant.info"].append(unified)

    # Compute evidence boost
    boost = compute_evidence_boost(all_evidence)

    return {
        "unified_evidence": all_evidence,
        "by_source": unified_by_source,
        "hgvs": hgvs,
        "evidence_count": len(all_evidence),
        "evidence_boost": boost,
        "errors": errors,
    }


def _dedup_key(ev: dict) -> str:
    """Generate a deduplication key for an evidence item."""
    source = ev.get("source", "")
    meta = ev.get("metadata", {}) or {}
    civic_id = meta.get("civic_evidence_id")
    var_id = meta.get("variation_id")
    pubmed = meta.get("pubmed_id")
    description = ev.get("description", "")[:80]
    # Use source + unique identifier or description prefix
    unique_id = civic_id or var_id or pubmed or description
    return f"{source}|{unique_id}"


def _to_unified(ev: dict, source_label: str) -> dict:
    """Convert any evidence format to the unified schema."""
    badge_map = {
        "ClinVar": "ClinVar",
        "CIViC": "CIViC",
        "Local Catalog": "Local Catalog",
        "MyVariant.info": "MyVariant",
    }
    return {
        "source": source_label,
        "source_label": source_label,
        "source_badge": badge_map.get(source_label, source_label),
        "variant": ev.get("variant", ""),
        "evidence_type": ev.get("evidence_type", "unknown"),
        "summary": ev.get("description", ""),
        "confidence": ev.get("confidence", 0.5),
        "url": ev.get("url"),
        "metadata": ev.get("metadata", {}),
        "retrieval_mode": ev.get("retrieval_mode", ""),
        "timestamp": ev.get("timestamp", _timestamp()),
    }


def _normalize_local_evidence(local_evidence: list[dict]) -> list[dict]:
    """Normalize local catalog evidence items to unified format."""
    unified = []
    for item in local_evidence:
        if isinstance(item, dict):
            source = item.get("source", "Local Catalog")
            # Map EvidenceItem type objects from reconcile.py
            confidence_weight = item.get("confidence_weight", "")
            if confidence_weight == "HIGH":
                confidence = 0.85
            elif confidence_weight == "MEDIUM":
                confidence = 0.60
            elif confidence_weight == "LOW":
                confidence = 0.35
            else:
                confidence = 0.50

            unified.append({
                "source": "Local Catalog",
                "type": item.get("type", ""),
                "description": item.get("description", ""),
                "evidence_type": item.get("evidence_type", ""),
                "confidence": confidence,
                "url": item.get("url"),
                "retrieval_mode": item.get("retrieval_mode", ""),
                "metadata": {
                    "original_source": source,
                    "confidence_weight": confidence_weight,
                    "type": item.get("type"),
                    "governance_standard": item.get("governance_standard"),
                },
                "timestamp": item.get("timestamp", _timestamp()),
            })
    return unified


# ── Ranking ─────────────────────────────────────────────────────────────────

def rank_evidence(unified_evidence: list[dict]) -> list[dict]:
    """
    Rank unified evidence items by confidence (descending).
    ClinVar and CIViC evidence with higher confidence appears first.
    """
    return sorted(unified_evidence, key=lambda x: x.get("confidence", 0), reverse=True)


def group_by_source(unified_evidence: list[dict]) -> dict:
    """Group evidence by source for frontend display."""
    grouped = {}
    for item in unified_evidence:
        source = item.get("source", "Other")
        grouped.setdefault(source, []).append(item)
    return grouped


def get_source_ordering() -> list[str]:
    """Preferred display order for evidence sources."""
    return ["ClinVar", "CIViC", "Local Catalog", "MyVariant.info"]
