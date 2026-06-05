"""
Rule-based pre-processing for oncology entity normalization.

Purpose: clean formatting noise from raw input so that downstream alias
dictionary lookups have the best possible chance of finding a match.

This module handles STRUCTURAL normalization only:
  - punctuation/whitespace variants (hyphens, underscores, extra spaces)
  - case normalization where safe
  - common abbreviation expansions (shorthand → full term)
  - token reordering (e.g. "del19" → "exon 19 deletion")

It does NOT handle semantic synonyms — that is the alias dictionary's job.
Example: "HER-2" → "HER2" is normalization (formatting).
         "HER2"  → "ERBB2" is aliasing (meaning).

Each entity type has its own function because the noise patterns differ
significantly between genes, variants, and cancer types. Shared helpers
live at the bottom of the file.

Expanding coverage: add new patterns to the relevant _REPLACEMENTS list
or the entity-specific function. Keep each rule small and commented with
a real example from the benchmark or hard-case data.
"""

import re


# ---------------------------------------------------------------------------
# Variant normalization
# ---------------------------------------------------------------------------

# Ordered list of (pattern, replacement) tuples applied sequentially.
# Order matters — more specific patterns should come before general ones.
# Each entry: (compiled_regex, replacement_string, comment_for_humans)
_VARIANT_REPLACEMENTS: list[tuple[re.Pattern, str, str]] = [
    # "exon20ins" / "exon19del" → expand digits and suffix
    # benchmark: case_009 exon20ins, case_015 del19, case_001 Ex19del
    (re.compile(r"\bex(?:on)?[\s\-_]?(\d+)[\s\-_]?del\b", re.IGNORECASE),
     r"exon \1 deletion", "exon N del → exon N deletion"),

    (re.compile(r"\bdel[\s\-_]?(\d+)\b", re.IGNORECASE),
     r"exon \1 deletion", "del19 → exon 19 deletion"),

    (re.compile(r"\bex(?:on)?[\s\-_]?(\d+)[\s\-_]?ins\b", re.IGNORECASE),
     r"exon \1 insertion", "exon N ins → exon N insertion"),

    # "copy gain" / "copy number gain" variants
    # benchmark: case_020 "copy gain"
    (re.compile(r"\bcopy[\s\-_]?gain\b", re.IGNORECASE),
     "copy number gain", "copy gain → copy number gain"),

    # "amp" → "amplification"
    # benchmark: case_007 "amp"
    (re.compile(r"\bamp\b", re.IGNORECASE),
     "amplification", "amp → amplification"),

    # underscore as range separator in protein notation: E746_A750del → E746_A750del
    # Already handled correctly by alias; normalize spacing around underscore only
    (re.compile(r"\b([A-Z]\d+)_([A-Z]\d+)(del|ins)\b", re.IGNORECASE),
     r"\1_\2\3", "preserve protein range notation, strip surrounding noise"),

    # Collapse multiple spaces
    (re.compile(r"  +"), " ", "collapse whitespace"),
]


def normalize_variant_text(raw: str) -> str:
    """
    Apply rule-based normalization to a raw variant string.

    Returns the cleaned string. If no rules match, returns the original
    stripped of leading/trailing whitespace. Never returns None.

    The result is passed to the alias dictionary lookup, not returned
    directly as a canonical value.
    """
    text = raw.strip()
    for pattern, replacement, _ in _VARIANT_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text.strip()


# ---------------------------------------------------------------------------
# Gene normalization
# ---------------------------------------------------------------------------

# Gene symbols are tightly constrained — we only fix punctuation noise.
# Semantic aliasing (HER2 → ERBB2, p53 → TP53) stays in gene_aliases.json.
_GENE_REPLACEMENTS: list[tuple[re.Pattern, str, str]] = [
    # Hyphens in gene symbols: HER-2 → HER2, ERB-B2 → ERBB2
    # benchmark: case_007 "HER-2"
    # Rin's planned additions: ERB-B2, c-met
    (re.compile(r"([A-Za-z]+)-([A-Za-z0-9]+)"),
     r"\1\2", "remove hyphen from gene symbol"),

    # Underscores used as separators: unknown_gene → unknown gene (won't alias, but cleaner)
    (re.compile(r"([A-Za-z]+)_([A-Za-z]+)"),
     r"\1 \2", "underscore separator → space"),
]


def normalize_gene_text(raw: str) -> str:
    """
    Apply rule-based normalization to a raw gene string.

    Conservative: only removes punctuation noise. Does not change case
    because gene symbol casing is clinically significant (e.g. "MET" vs
    "met" mean the same thing, but "BRAF" vs "braf" — we preserve the
    input and let the alias dict handle case variants explicitly).
    """
    text = raw.strip()
    for pattern, replacement, _ in _GENE_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text.strip()


# ---------------------------------------------------------------------------
# Cancer type normalization
# ---------------------------------------------------------------------------

_CANCER_REPLACEMENTS: list[tuple[re.Pattern, str, str]] = [
    # Hyphen variants: "non-small cell" / "non small cell"
    # Rin's planned additions: "non small cell lung cancer"
    (re.compile(r"\bnon[\s\-]small[\s\-]cell\b", re.IGNORECASE),
     "non-small cell", "normalise spacing/hyphen in NSCLC phrase"),

    # "ca" as abbreviation for carcinoma
    # Rin's planned additions: "lung adeno ca"
    (re.compile(r"\bca\b", re.IGNORECASE),
     "carcinoma", "ca → carcinoma"),

    # Collapse multiple spaces
    (re.compile(r"  +"), " ", "collapse whitespace"),
]


def normalize_cancer_type_text(raw: str) -> str:
    """
    Apply rule-based normalization to a raw cancer type string.

    More aggressive than gene normalization because cancer type free-text
    is the messiest input class. Downstream fuzzy matching (RapidFuzz,
    Checkpoint 2) will benefit from cleaner input here.
    """
    if not raw:
        return raw
    text = raw.strip()
    for pattern, replacement, _ in _CANCER_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text.strip()
