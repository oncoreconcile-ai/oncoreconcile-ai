from typing import List, Optional
from pydantic import BaseModel


class ReconcileRequest(BaseModel):
    case_id: Optional[str] = None
    cancer_type: Optional[str] = None
    gene: str
    variant: str


class EvidenceItem(BaseModel):
    source: str
    type: str
    description: str


class CanonicalConcept(BaseModel):
    cancer_type: Optional[str] = None
    gene: Optional[str] = None
    variant: Optional[str] = None


class ReconcileResponse(BaseModel):
    case_id: Optional[str] = None
    input: dict
    canonical: CanonicalConcept
    evidence: List[EvidenceItem]
    explanation: str
    confidence: str
    review_status: str
    notes: List[str] = []


class BatchRequest(BaseModel):
    records: List[ReconcileRequest]


class BatchResponse(BaseModel):
    results: List[ReconcileResponse]
    summary: dict
