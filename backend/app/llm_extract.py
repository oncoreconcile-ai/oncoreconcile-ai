"""
Stub: LLM-based structured entity extraction.

Intended role in the pipeline (Checkpoint 2+):
  When rule-based normalization + alias lookup + VICC all fail to resolve
  an input, this module sends the raw input to an LLM with a narrow,
  structured prompt that asks only for entity extraction — not for a
  canonical output.

  The LLM's job is to parse messy free-text into structured fields:
    { "gene": "...", "variant": "...", "cancer_type": "..." }

  Those structured fields are then passed back into the alias lookup and
  VICC connector. The LLM never produces the canonical output directly —
  it only bridges the gap between unstructured input and structured lookup.

  This preserves the auditability story: the LLM's extraction is logged as
  an intermediate step, and the final canonical output always comes from a
  deterministic source (alias dict or VICC).

Assigned to: Hao (deferred — target start Jun 30, 2026, after deterministic
pipeline is stable). See docs/team_tasks.md.
"""

from __future__ import annotations


class LLMExtractionResult:
    """Structured output from the LLM extraction step."""

    def __init__(
        self,
        gene: str | None = None,
        variant: str | None = None,
        cancer_type: str | None = None,
        raw_llm_output: str | None = None,
    ):
        self.gene = gene
        self.variant = variant
        self.cancer_type = cancer_type
        self.raw_llm_output = raw_llm_output  # logged for auditability


def extract_entities_llm(
    raw_gene: str,
    raw_variant: str,
    raw_cancer_type: str | None,
) -> LLMExtractionResult | None:
    """
    Use an LLM to extract structured oncology entities from messy free-text.

    Args:
        raw_gene: Original gene input, after rule-based normalization failed.
        raw_variant: Original variant input, after rule-based normalization failed.
        raw_cancer_type: Original cancer type input (optional).

    Returns:
        LLMExtractionResult with parsed fields, or None if the stub is not
        yet implemented. Callers must handle None gracefully.

    Notes:
        - The LLM output is intermediate only. Results are passed back to
          alias lookup, not returned as canonical values.
        - raw_llm_output should always be logged regardless of parse success,
          to support audit trail construction in reconcile_record().
    """
    # TODO (Hao, Jun 30+): implement LLM extraction call.
    # Suggested approach:
    #   1. Build a structured prompt asking for JSON output only:
    #      { "gene": "...", "variant": "...", "cancer_type": "..." }
    #   2. Send to Anthropic/OpenAI with low temperature (0.0–0.1).
    #   3. Parse response, populate LLMExtractionResult.
    #   4. Log raw_llm_output to audit trail before returning.
    #   5. Return None if parsing fails — never raise from this function.
    return None
