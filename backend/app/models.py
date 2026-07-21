from datetime import datetime, timezone
from typing import List, Optional, Any
from pydantic import BaseModel, Field


class ReconcileRequest(BaseModel):
    case_id: Optional[str] = None
    cancer_type: Optional[str] = None
    gene: str
    variant: str


class EvidenceItem(BaseModel):
    source: str
    type: str
    description: str
    evidence_type: Optional[str] = None
    confidence_weight: Optional[str] = None
    retrieval_mode: Optional[str] = None
    external_id: Optional[str] = None
    url: Optional[str] = None
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    governance_standard: Optional[str] = "VA-Spec-inspired"


class CanonicalHGVS(BaseModel):
    canonical_variant: Optional[str] = None
    protein_hgvs: Optional[str] = None
    coding_hgvs: Optional[str] = None
    genomic_hgvs: Optional[str] = None
    vrs_id: Optional[str] = None                # future GA4GH VRS
    vrs_ready: bool = False                     # future GA4GH VRS


class CanonicalConcept(BaseModel):
    cancer_type: Optional[str] = None
    gene: Optional[str] = None
    variant: Optional[str] = None


class UnifiedEvidenceItem(BaseModel):
    """Common schema for all evidence sources."""
    source: str                                  # ClinVar | CIViC | Local Catalog | MyVariant.info
    source_label: Optional[str] = None
    source_badge: Optional[str] = None
    variant: Optional[str] = None
    evidence_type: Optional[str] = None
    summary: str
    confidence: float = 0.0
    url: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    retrieval_mode: Optional[str] = None
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class EvidenceBoost(BaseModel):
    """Confidence score boost from evidence sources."""
    evidence_boost: float = 0.0
    breakdown: dict = Field(default_factory=dict)
    details: List[str] = Field(default_factory=list)


class FederationResult(BaseModel):
    """Aggregated result from all evidence sources."""
    unified_evidence: List[UnifiedEvidenceItem] = Field(default_factory=list)
    by_source: dict = Field(default_factory=dict)
    hgvs: CanonicalHGVS = Field(default_factory=CanonicalHGVS)
    evidence_count: int = 0
    evidence_boost: EvidenceBoost = Field(default_factory=EvidenceBoost)
    errors: List[str] = Field(default_factory=list)


class ReconcileResponse(BaseModel):
    case_id: Optional[str] = None
    input: dict
    canonical: CanonicalConcept
    canonical_hgvs: Optional[CanonicalHGVS] = None   # new: HGVS representations
    evidence: List[EvidenceItem]
    unified_evidence: List[UnifiedEvidenceItem] = Field(default_factory=list)  # new
    federation: Optional[FederationResult] = None    # new: aggregate evidence
    explanation: str
    confidence: str                              # HIGH | MEDIUM | LOW
    confidence_score: float = 0.0               # 0.0–1.0 numeric score
    score_breakdown: dict = Field(default_factory=dict)  # per-signal weights
    evidence_score_breakdown: Optional[dict] = None     # new: evidence weighting details
    review_status: str
    alternatives: List[Any] = Field(default_factory=list)  # other candidates considered
    notes: List[str] = Field(default_factory=list)
    audit_trail: List[str] = Field(default_factory=list)
    curation_metadata: Optional[dict] = None


class BatchRequest(BaseModel):
    records: List[ReconcileRequest]


class BatchResponse(BaseModel):
    results: List[ReconcileResponse]
    summary: dict


# ── Review queue models ───────────────────────────────────────────────────────

class ReviewDecision(BaseModel):
    case_id: str
    decision: str           # "approve" | "reject" | "edit" | "override" | "reopen"
    curator_id: Optional[str] = None
    override_canonical: Optional[CanonicalConcept] = None
    notes: Optional[str] = None
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class ReviewDecisionRecord(BaseModel):
    decision: str
    curator_id: Optional[str] = None
    role: str = "reviewer"
    canonical: Optional[CanonicalConcept] = None
    notes: Optional[str] = None
    timestamp: str


class ReviewQueueItem(BaseModel):
    case_id: str
    input: dict
    canonical: CanonicalConcept
    confidence: str
    confidence_score: float
    score_breakdown: dict
    review_status: str
    explanation: str
    evidence: List[EvidenceItem]
    alternatives: List[Any] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    audit_trail: List[str] = Field(default_factory=list)
    curation_metadata: Optional[dict] = None
    decision: Optional[str] = None        # null until reviewed
    curator_id: Optional[str] = None
    curator_notes: Optional[str] = None
    decision_timestamp: Optional[str] = None
    review_history: List[ReviewDecisionRecord] = Field(default_factory=list)
    adjudication_status: str = "NOT_REQUIRED"
    adjudicated_by: Optional[str] = None
    adjudication_timestamp: Optional[str] = None
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class ReviewQueueResponse(BaseModel):
    items: List[ReviewQueueItem]
    total: int
    pending: int
    reviewed: int
