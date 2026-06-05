"""
Stub: Embedding-based semantic similarity fallback.

Background:
  An embedding model converts text into a vector of numbers such that
  semantically similar phrases produce vectors that are close together
  in that space. Closeness is measured with cosine similarity (a value
  between 0 and 1, where 1 = identical direction).

  At query time:
    1. Encode the input term → query vector.
    2. Compare against pre-computed vectors for all known canonical terms.
    3. Return the canonical term with the highest similarity score,
       if it exceeds a confidence threshold.

Intended role in the pipeline (last resort before CANNOT_RECONCILE):
  Called after alias dict, VICC, and LLM extraction all fail to resolve
  a term. Returns a MEDIUM-confidence suggestion requiring human review —
  never AUTO_RECONCILE.

Model candidates (biomedical domain recommended):
  - pritamdeka/S-PubMedBert-MS-MARCO  (retrieval-tuned, good for short phrases)
  - dmis-lab/biobert-base-cased-v1.2  (general biomedical, widely validated)

Requires: sentence-transformers (not yet in requirements.txt).
  Add when ready to implement:  pip install sentence-transformers

See docs/decisions.md for the architectural rationale around embedding
confidence and auditability constraints.
"""

from __future__ import annotations


# Similarity score below which we distrust the result and return None.
# Needs calibration against the benchmark hard cases once implemented.
SIMILARITY_THRESHOLD = 0.80


class EmbeddingMatch:
    """Result of an embedding similarity search."""

    def __init__(self, canonical: str, score: float):
        self.canonical = canonical
        self.score = score  # cosine similarity, 0.0–1.0


def find_similar_variant(
    normalized_variant: str,
    canonical_gene: str | None,
) -> EmbeddingMatch | None:
    """
    Find the closest canonical variant via embedding similarity.

    Args:
        normalized_variant: Variant string after rule-based normalization.
        canonical_gene: Canonical gene symbol, used to scope the search
                        index and to provide context to the model.

    Returns:
        EmbeddingMatch if similarity >= SIMILARITY_THRESHOLD, else None.
        Callers must treat a non-None result as MEDIUM confidence only.
    """
    # TODO: load model (once at startup, not per call).
    # TODO: build or load pre-computed index of canonical variant vectors.
    # TODO: encode normalized_variant, run cosine similarity, threshold filter.
    #
    # Implementation sketch:
    #   from sentence_transformers import SentenceTransformer, util
    #   model = SentenceTransformer("pritamdeka/S-PubMedBert-MS-MARCO")
    #   query_vec = model.encode(normalized_variant, convert_to_tensor=True)
    #   scores = util.cos_sim(query_vec, canonical_index_vectors)
    #   best_idx = scores.argmax()
    #   if scores[best_idx] >= SIMILARITY_THRESHOLD:
    #       return EmbeddingMatch(canonical_terms[best_idx], float(scores[best_idx]))
    return None


def find_similar_gene(normalized_gene: str) -> EmbeddingMatch | None:
    """
    Find the closest canonical gene symbol via embedding similarity.

    Less likely to be useful than variant similarity (gene symbols are
    short and structural — alias lookup and VICC should cover most cases).
    Included for completeness and future experimentation.
    """
    # TODO: same pattern as find_similar_variant.
    return None


def find_similar_cancer_type(normalized_cancer_type: str) -> EmbeddingMatch | None:
    """
    Find the closest canonical cancer type via embedding similarity.

    Likely the highest-value use of embeddings: cancer type free-text is
    the messiest entity class and has the widest vocabulary of synonyms,
    abbreviations, and clinical shorthands.
    """
    # TODO: same pattern as find_similar_variant.
    return None
