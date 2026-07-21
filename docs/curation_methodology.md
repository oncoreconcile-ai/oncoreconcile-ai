# Curation Methodology

## Purpose

The OncoReconcile AI benchmark dataset was created to evaluate oncology entity reconciliation workflows.

The benchmark is intended to test:

* Cancer type reconciliation
* Gene reconciliation
* Variant reconciliation
* Confidence scoring
* Review recommendations
* Cannot Reconcile workflows
* Explainability
* Auditability

The benchmark is not intended to represent clinical truth or a comprehensive oncology knowledgebase.

---

## Data Sources

The benchmark was curated using:

* Public oncology knowledge resources
* HGNC nomenclature
* CIViC concepts
* ClinVar terminology
* OncoKB concepts
* Molecular diagnostics terminology
* Team domain expertise

No patient-identifiable information was used.

---

## Curation Principles

### Clinical Realism

Benchmark cases prioritize terminology commonly encountered in oncology workflows.

Preferred examples:

* HER2
* HER-2
* ERBB2
* EGFR Ex19del
* KRAS G12C

Avoided:

* Rare historical aliases
* Obsolete nomenclature
* Extremely uncommon reporting terminology

---

### Representative Coverage

The benchmark includes:

#### Disease Aliases

* NSCLC
* Non-Small Cell Lung Cancer
* LUAD
* Lung Adenocarcinoma

#### Gene Aliases

* HER2 → ERBB2
* HER-2 → ERBB2
* p53 → TP53

#### Variant Synonyms

* Ex19del
* del19
* E746_A750del

#### Fusions

* ALK Fusion
* RET Fusion
* ROS1 Rearrangement

#### Copy Number Alterations

* Amplification
* Copy Gain

---

### Difficulty Stratification

#### EASY

Canonical terminology.

Examples:

* EGFR L858R
* KRAS G12C

#### MEDIUM

Alias normalization required.

Examples:

* HER2 Amplification
* p53 R175H

#### DIFFICULT

Ambiguous terminology.

Examples:

* Unknown Gene
* ALK Positive
* Copy Gain

---

### Human Review

The benchmark intentionally contains review-required scenarios.

Examples:

* Ambiguous diseases
* Ambiguous variants
* Missing context
* Unknown entities

These scenarios support evaluation of:

* Confidence scoring
* Review recommendations
* Cannot Reconcile outcomes

---

## Data Collection Pipeline

The benchmark is generated from curated oncology knowledge assets maintained by the OncoReconcile AI platform.

These assets include:

* Disease aliases
* Gene aliases
* Disease-gene relationships
* Gene-variant catalogs
* Human-reviewed benchmark cases

The complete data collection, governance, and catalog generation process is documented in:

```text
docs/data_curation_pipeline.md
```

The benchmark relies on governed biomedical knowledge assets rather than purely AI-generated mappings. Downloaded candidate data is reviewed before promotion into production catalogs, and ambiguous concepts are intentionally preserved for REVIEW_REQUIRED evaluation scenarios.

---

## Benchmark Promotion Rules

Generated candidate cases may be promoted if they are:

* Clinically meaningful
* Traceable to authoritative resources
* Useful for reconciliation testing
* Consistent with oncology reporting terminology

Otherwise they may be classified as:

* Needs Review
* Rejected
* Synthetic Negative Control

---

## Provenance

Every benchmark case should be traceable to:

* Public source
* Manual seed rule
* Generated experiment
* Team curation decision

Future versions will expand provenance tracking using:

* GA4GH VA-Spec-inspired structures
* Evidence lineage
* Review history
* Audit metadata
* Standards-aligned provenance records

---

## Summary

The benchmark balances:

* Clinical realism
* Explainability
* Provenance
* Reproducibility
* Validation coverage

while maintaining transparency regarding how benchmark truth was established.

The goal is not simply high accuracy, but trustworthy evaluation of biomedical entity reconciliation systems operating under human governance.
