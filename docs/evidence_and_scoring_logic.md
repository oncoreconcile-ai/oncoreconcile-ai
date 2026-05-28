# Evidence and Scoring Logic: Current State and Future Improvements

---

## Canonical Reconciliation Schema (2026 MVP)

All evidence, scoring, and review logic now aligns with the canonical schema in `src/reconciliation_schema.py`. This schema standardizes the following output fields:

- `original_input`: Raw input as received
- `source_text`: Extracted text (if different from original_input)
- `canonical_gene`: Normalized gene symbol
- `canonical_variant`: Normalized variant (HGVS, etc)
- `confidence`: Deterministic or model-based confidence score
- `evidence_sources`: List of evidence references (ClinVar, CIViC, etc)
- `explainability`: Human-readable explanation of normalization/decision
- `requires_human_review`: True if human review is needed
- `cannot_reconcile`: True if reconciliation is not possible
- `audit_trail`: List of steps, sources, and decisions for traceability

See `data/examples/` for sample outputs covering high-confidence, requires-human-review, and cannot-reconcile cases.

All future evidence and scoring logic should use these field names for consistency and auditability.

## 1. Current Evidence Logic
- **Evidence Sources:**
  - Each variant in the knowledge base (KB) can have linked evidence (e.g., ClinVar, CIViC, NCCN, literature).
  - Evidence is stored as a list of objects with fields like source, title, and sometimes a link or description.
- **Usage:**
  - When a candidate variant is retrieved, its evidence is included in the output for review or reasoning.
  - Evidence count is sometimes used as a proxy for confidence.

## 2. Current Scoring Logic
- **Deterministic Score:**
  - 1.0 for exact canonical match (e.g., direct mapping from CSV or KB).
- **Semantic Score:**
  - Based on string similarity or embedding similarity (placeholder for now).
- **LLM Score:**
  - Confidence estimated by the reasoning agent, based on evidence count, clinical significance, and approval history.
- **Historical Score:**
  - Based on prior approvals/rejections for a variant in the KB.
- **Overall Confidence:**
  - Often a weighted combination of the above, or a simple rule (e.g., 1.0 for exact match, 0.7 for semantic match, 0.0 if no match).

## 3. Limitations
- Evidence is not weighted by quality, recency, or source.
- No evidence provenance or audit trail.
- Scoring is mostly rule-based, not data-driven.
- No explicit uncertainty quantification.
- LLM confidence is heuristic, not calibrated.

## 4. Recommendations for Improvement
1. **Evidence Weighting:**
   - Assign weights to evidence based on source, recency, or expert review.
   - Use evidence level (guideline, clinical trial, case report) to influence confidence.
2. **Provenance and Audit Trails:**
   - Track who added/approved evidence, when, and with what rationale.
   - Allow for evidence to be challenged or updated.
3. **Advanced Scoring Models:**
   - Use a more sophisticated formula or ML model to combine scores.
   - Calibrate LLM confidence using real-world validation or expert review.
4. **Uncertainty Modeling:**
   - Explicitly flag ambiguous or conflicting cases.
   - Provide a confidence interval or “needs review” status.
5. **Explainability:**
   - Always show which evidence, rules, or mappings contributed to the score.
   - Provide a reasoning chain or summary for each reconciliation.
6. **Continuous Improvement:**
   - Use human-in-the-loop feedback to refine evidence weights and scoring logic over time.

---

## 5. Actionable Improvements for the Competition

The following improvements can be realistically implemented within the competition timeframe:

1. **Evidence Weighting:**
  - Assign higher weights to evidence from trusted sources (e.g., NCCN, ClinVar) and lower to less reliable or older sources.
  - Add a simple “evidence_level” field (e.g., guideline, clinical trial, case report) and use it in scoring.

2. **Explainability:**
  - Display which evidence items contributed to each decision.
  - Show the reasoning chain and confidence calculation for each reconciliation.

3. **Provenance/Audit Trail:**
  - Track who added or approved evidence and when (even if just a username and timestamp).
  - Log manual review decisions for ambiguous cases.

4. **Uncertainty Handling:**
  - Flag cases with conflicting or insufficient evidence as “needs review.”
  - Add a “confidence interval” or “uncertainty” field to the output.

5. **Continuous Feedback:**
  - Allow reviewers to mark evidence as “strong,” “weak,” or “irrelevant,” and use this feedback to adjust future scoring.

6. **Documentation:**
  - Clearly document the evidence and scoring logic, so judges and team members understand how decisions are made.

These improvements are practical, do not require major refactoring, and will make the system more robust, transparent, and competitive.

---

*This document should be updated as the evidence and scoring logic evolves and new capabilities are added.*
