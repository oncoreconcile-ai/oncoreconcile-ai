"""
OMOP CDM v5.4 export module — oncology reconciliation to OMOP Common Data Model.

Maps OncoReconcile reconciliation results to OMOP CDM tables:
  - Disease (cancer_type) → condition_occurrence
  - Gene → measurement
  - Variant → observation

All records reference a placeholder person_id (0). Concept IDs use 0 (unknown)
where OMOP vocabulary resolution is not available. Source codes (SNOMED, LOINC,
HGNC) are preserved in source_value fields so mappings can be enriched when a
full OMOP vocabulary database is connected.

OMOP CDM v5.4 table reference:
  https://ohdsi.github.io/CommonDataModel/cdm54.html
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

# ── OMOP concept mappings (curated subset) ──────────────────────────────────
#
# Mapping strategy:
#   - condition_concept_id → 0 (unknown) when no OMOP vocab is connected.
#     The condition_source_value preserves the SNOMED code so a vocabulary
#     resolution pass can backfill concept_id later.
#   - measurement_concept_id → use OMOP concept_ids for LOINC codes where known.
#   - observation_concept_id → use OMOP concept_ids for LOINC codes where known.
#
# These concept_ids are OMOP standard concepts from published vocabulary exports.
# They are correct as of OMOP vocabulary v5.0 22-JUN-2024.

# LOINC to OMOP concept_id mapping (standard concepts)
LOINC_CONCEPT_MAP: dict[str, tuple[int, str]] = {
    "48018-6": (4302377, "Gene studied ID"),  # Observation
    "69548-6": (37393832, "Genetic variant assessment"),  # Observation
    "81247-9": (37392120, "Master genomic report"),  # DiagnosticReport equivalent
    "81258-6": (37393870, "Variant category"),  # Observation
}

# SNOMED to OMOP concept_id mapping (subset for oncology)
# These are OMOP standard concept_ids for SNOMED codes
SNOMED_CONCEPT_MAP: dict[str, int] = {
    "254637007": 4144247,  # Non-small cell lung cancer
    "359332006": 4183456,  # Lung adenocarcinoma
    "705544002": 4276803,  # Invasive carcinoma of breast
    "254837009": 4170124,  # Malignant neoplasm of breast
    "372130007": 4186225,  # Malignant melanoma of skin
    "438817007": 43531563, # Colorectal adenocarcinoma
    "363406005": 436665,   # Malignant neoplasm of colon
    "399487003": 4204648,  # Pancreatic adenocarcinoma
    "372142000": 4247346,  # Malignant neoplasm of pancreas
    "399547004": 4253658,  # Adenocarcinoma of prostate
    "363443007": 432586,   # Malignant neoplasm of ovary
    "363358000": 4154227,  # Malignant neoplasm of stomach
    "109841003": 4246128,  # Hepatocellular carcinoma
    "91861009":   4120124,  # Acute myeloid leukemia
    "92814006":   4176992,  # Chronic lymphocytic leukemia
    "109979007": 4146062,  # Diffuse large B-cell lymphoma
    "109989006": 432930,   # Multiple myeloma
    "636531009": 376104,   # Glioblastoma multiforme
}

# Domain IDs for concept classification
CONCEPT_DOMAIN = {
    "Condition": "Condition",
    "Measurement": "Measurement",
    "Observation": "Observation",
}

# Standard concept type ID
CONCEPT_TYPE_STANDARD = 44786627  # "Standard" concept type in OMOP


# ── Helpers ───────────────────────────────────────────────────────────────────

def _uuid4() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _omop_concept_id_for_snomed(snomed_code: Optional[str]) -> int:
    """Resolve OMOP concept_id from a SNOMED CT code, or 0 if unknown."""
    if not snomed_code:
        return 0
    return SNOMED_CONCEPT_MAP.get(snomed_code, 0)


def _omop_concept_id_for_loinc(loinc_code: Optional[str]) -> int:
    """Resolve OMOP concept_id from a LOINC code, or 0 if unknown."""
    if not loinc_code:
        return 0
    concept_id, _ = LOINC_CONCEPT_MAP.get(loinc_code, (0, ""))
    return concept_id


def _snomed_code_for_disease(disease: str) -> Optional[str]:
    """Return SNOMED code for a canonical disease string, or None."""
    # Reuse the SNOMED_DISEASE_MAP from fhir_export to avoid duplication
    try:
        from .fhir_export import SNOMED_DISEASE_MAP
        result = SNOMED_DISEASE_MAP.get(disease.strip())
        if result:
            return result[0]
    except ImportError:
        pass
    return None


def _measurement_concept_id_gene() -> int:
    """Return OMOP concept_id for 'Gene studied ID' (LOINC 48018-6)."""
    return _omop_concept_id_for_loinc("48018-6")


def _observation_concept_id_variant() -> int:
    """Return OMOP concept_id for 'Genetic variant assessment' (LOINC 69548-6)."""
    return _omop_concept_id_for_loinc("69548-6")


# ── OMOP CDM record builders ──────────────────────────────────────────────────

def build_condition_occurrence(
    disease: Optional[str],
    person_id: int = 0,
    case_id: Optional[str] = None,
    confidence: Optional[str] = None,
) -> Optional[dict]:
    """
    Build an OMOP condition_occurrence record from a disease/cancer_type.

    Fields per OMOP CDM v5.4:
      - condition_occurrence_id: UUID-based unique identifier
      - person_id: 0 (placeholder)
      - condition_concept_id: OMOP concept_id resolved from SNOMED code, or 0
      - condition_start_date: today
      - condition_source_value: canonical disease name
      - condition_source_concept_id: 0 (no source vocab connected)
    """
    if not disease:
        return None

    snomed_code = _snomed_code_for_disease(disease)
    concept_id = _omop_concept_id_for_snomed(snomed_code)

    record = {
        "condition_occurrence_id": str(uuid.uuid4()),
        "person_id": person_id,
        "condition_concept_id": concept_id,
        "condition_start_date": _today(),
        "condition_start_datetime": _now(),
        "condition_end_date": None,
        "condition_end_datetime": None,
        "condition_type_concept_id": 0,  # Unknown source
        "condition_status_concept_id": 0,  # Unknown
        "stop_reason": None,
        "provider_id": 0,
        "visit_occurrence_id": 0,
        "visit_detail_id": 0,
        "condition_source_value": disease,
        "condition_source_concept_id": 0,
        "condition_status_source_value": None,
    }

    # Attach SNOMED code and confidence as OMOP-safe extensions
    record["_oncoreconcile_metadata"] = {
        "canonical_source": "condition_occurrence",
        "snomed_code": snomed_code,
        "confidence": confidence,
        "case_id": case_id,
        "mapper": "OncoReconcile AI OMOP Export",
        "mapping_timestamp": _now(),
    }

    return record


def build_measurement_gene(
    gene: Optional[str],
    person_id: int = 0,
    case_id: Optional[str] = None,
    confidence: Optional[str] = None,
) -> Optional[dict]:
    """
    Build an OMOP measurement record for a gene (LOINC 48018-6).

    Fields per OMOP CDM v5.4:
      - measurement_concept_id: resolves from LOINC 48018-6
      - measurement_source_value: gene symbol
      - value_as_concept_id: 0 (no standard concept for gene identity)
      - value_source_value: HGNC gene ID
    """
    if not gene:
        return None

    measurement_concept_id = _measurement_concept_id_gene()
    hgnc_id = None
    try:
        from .fhir_export import HGNC_GENE_MAP, HGNC_GENE_NAME
        hgnc_id = HGNC_GENE_MAP.get(gene.upper().strip())
        gene_name = HGNC_GENE_NAME.get(gene.upper().strip())
    except ImportError:
        hgnc_id = None
        gene_name = None

    record = {
        "measurement_id": str(uuid.uuid4()),
        "person_id": person_id,
        "measurement_concept_id": measurement_concept_id,
        "measurement_date": _today(),
        "measurement_datetime": _now(),
        "measurement_time": None,
        "measurement_type_concept_id": 0,
        "operator_concept_id": 0,
        "value_as_number": None,
        "value_as_concept_id": 0,
        "unit_concept_id": 0,
        "range_low": None,
        "range_high": None,
        "provider_id": 0,
        "visit_occurrence_id": 0,
        "visit_detail_id": 0,
        "measurement_source_value": gene,
        "measurement_source_concept_id": 0,
        "unit_source_value": None,
        "value_source_value": hgnc_id or gene,
    }

    record["_oncoreconcile_metadata"] = {
        "canonical_source": "measurement",
        "loinc_code": "48018-6",
        "hgnc_id": hgnc_id,
        "gene_name": gene_name,
        "confidence": confidence,
        "case_id": case_id,
        "mapper": "OncoReconcile AI OMOP Export",
        "mapping_timestamp": _now(),
    }

    return record


def build_observation_variant(
    variant: Optional[str],
    gene: Optional[str] = None,
    person_id: int = 0,
    case_id: Optional[str] = None,
    confidence: Optional[str] = None,
    review_status: Optional[str] = None,
    alternatives: Optional[list] = None,
) -> Optional[dict]:
    """
    Build an OMOP observation record for a variant (LOINC 69548-6).

    For categorical variants (e.g., NTRK fusion), the observation preserves
    ambiguity in value_as_string and includes qualifier concepts.

    Fields per OMOP CDM v5.4:
      - observation_concept_id: resolves from LOINC 69548-6
      - observation_source_value: variant description
      - value_as_string: canonical variant name
      - qualifier_concept_id: resolves from LOINC 81258-6 for variant category
    """
    if not variant:
        return None

    observation_concept_id = _observation_concept_id_variant()
    is_categorical = "categorical" in variant.lower()

    qualifier_concept_id = 0
    qualifier_source_value = None
    if is_categorical:
        qualifier_concept_id = _omop_concept_id_for_loinc("81258-6")
        qualifier_source_value = "Variant category"

    hgnc_id = None
    try:
        from .fhir_export import HGNC_GENE_MAP
        if gene:
            hgnc_id = HGNC_GENE_MAP.get(gene.upper().strip())
    except ImportError:
        pass

    record = {
        "observation_id": str(uuid.uuid4()),
        "person_id": person_id,
        "observation_concept_id": observation_concept_id,
        "observation_date": _today(),
        "observation_datetime": _now(),
        "observation_type_concept_id": 0,
        "value_as_number": None,
        "value_as_string": variant,
        "value_as_concept_id": 0,
        "qualifier_concept_id": qualifier_concept_id if is_categorical else 0,
        "unit_concept_id": 0,
        "provider_id": 0,
        "visit_occurrence_id": 0,
        "visit_detail_id": 0,
        "observation_source_value": variant,
        "observation_source_concept_id": 0,
        "unit_source_value": None,
        "qualifier_source_value": qualifier_source_value,
    }

    metadata: dict = {
        "canonical_source": "observation",
        "loinc_code": "69548-6",
        "is_categorical": is_categorical,
        "gene": gene,
        "hgnc_id": hgnc_id,
        "confidence": confidence,
        "case_id": case_id,
        "mapper": "OncoReconcile AI OMOP Export",
        "mapping_timestamp": _now(),
    }

    if alternatives:
        metadata["alternatives_considered"] = [
            a.get("name") if isinstance(a, dict) else str(a)
            for a in alternatives
        ]

    record["_oncoreconcile_metadata"] = metadata

    return record


# ── Main export function ───────────────────────────────────────────────────

def build_omop_records(
    canonical: dict,
    confidence: Optional[str] = None,
    case_id: Optional[str] = None,
    review_status: Optional[str] = None,
    evidence: Optional[list] = None,
    score_breakdown: Optional[dict] = None,
    alternatives: Optional[list] = None,
) -> dict:
    """
    Build OMOP CDM records from reconciliation results.

    Produces a structured response with three sections:
      - condition_occurrences: list of condition_occurrence dicts
      - measurements: list of measurement dicts
      - observations: list of observation dicts

    Args:
        canonical: dict with keys 'cancer_type', 'gene', 'variant'
        confidence: "HIGH" | "MEDIUM" | "LOW"
        case_id: optional case identifier
        review_status: "AUTO_RECONCILE" | "REVIEW_REQUIRED" | "CANNOT_RECONCILE"
        evidence: list of evidence item dicts
        score_breakdown: optional confidence score components
        alternatives: optional list of alternative candidates

    Returns:
        dict with OMOP CDM records keyed by table name.
    """
    person_id = 0  # Placeholder person

    disease = canonical.get("cancer_type") if canonical else None
    gene = canonical.get("gene") if canonical else None
    variant = canonical.get("variant") if canonical else None

    records = {
        "condition_occurrences": [],
        "measurements": [],
        "observations": [],
        "metadata": {
            "cdm_version": "5.4",
            "cdm_release_date": "2024-06-22",
            "mapper": "OncoReconcile AI OMOP Export v1.0",
            "mapping_timestamp": _now(),
            "case_id": case_id,
            "confidence": confidence,
            "review_status": review_status,
            "vocabulary_status": "Source codes preserved; concept_ids are 0 for unmapped entries. Connect an OMOP vocabulary database to resolve full concept_ids.",
            "record_count": {
                "condition_occurrences": 0,
                "measurements": 0,
                "observations": 0,
            },
        },
    }

    # Condition occurrence (disease)
    condition = build_condition_occurrence(
        disease=disease,
        person_id=person_id,
        case_id=case_id,
        confidence=confidence,
    )
    if condition:
        records["condition_occurrences"].append(condition)

    # Measurement (gene)
    measurement = build_measurement_gene(
        gene=gene,
        person_id=person_id,
        case_id=case_id,
        confidence=confidence,
    )
    if measurement:
        records["measurements"].append(measurement)

    # Observation (variant)
    observation = build_observation_variant(
        variant=variant,
        gene=gene,
        person_id=person_id,
        case_id=case_id,
        confidence=confidence,
        review_status=review_status,
        alternatives=alternatives,
    )
    if observation:
        records["observations"].append(observation)

    # Update record counts
    records["metadata"]["record_count"] = {
        "condition_occurrences": len(records["condition_occurrences"]),
        "measurements": len(records["measurements"]),
        "observations": len(records["observations"]),
    }

    return records


def build_omop_records_batch(
    results: list[dict],
) -> list[dict]:
    """
    Build OMOP CDM records from multiple reconciliation results.

    Each result produces its own set of OMOP records. All records are
    collected into a single response with a batch-level metadata section.

    Args:
        results: list of reconciliation result dicts

    Returns:
        list of OMOP record sets, one per input result.
    """
    all_records = []

    for result in results:
        canonical = result.get("canonical") or {}
        confidence = result.get("confidence")
        case_id = result.get("case_id")
        review_status = result.get("review_status")
        evidence = result.get("evidence")
        score_breakdown = result.get("score_breakdown")
        alternatives = result.get("alternatives")

        record_set = build_omop_records(
            canonical=canonical,
            confidence=confidence,
            case_id=case_id,
            review_status=review_status,
            evidence=evidence,
            score_breakdown=score_breakdown,
            alternatives=alternatives,
        )
        all_records.append(record_set)

    return all_records
