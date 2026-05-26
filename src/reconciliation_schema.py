"""
Canonical schema for gene/variant reconciliation results.

- original_input: Raw input as received.
- source_text: Extracted text (if different from original_input).
- canonical_gene: Normalized gene symbol.
- canonical_variant: Normalized variant (HGVS, etc).
- confidence: Deterministic or model-based confidence score.
- evidence_sources: List of evidence references (ClinVar, CIViC, etc).
- explainability: Human-readable explanation of normalization/decision.
- requires_human_review: True if human review is needed.
- cannot_reconcile: True if reconciliation is not possible.
- audit_trail: List of steps, sources, and decisions for traceability.

Notes:
- Deterministic normalization is always attempted before AI reasoning.
- Evidence sources are references, not clinical recommendations.
- Extraction (OCR, parsing) is separate from semantic interpretation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class ReconciliationResult:
    original_input: str
    source_text: Optional[str] = None
    canonical_gene: Optional[str] = None
    canonical_variant: Optional[str] = None
    confidence: Optional[float] = None
    evidence_sources: List[str] = field(default_factory=list)
    explainability: Optional[str] = None
    requires_human_review: bool = False
    cannot_reconcile: bool = False
    audit_trail: List[Any] = field(default_factory=list)
