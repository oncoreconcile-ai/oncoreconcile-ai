# OncoReconcile AI

# Architecture Documentation

## Overview

OncoReconcile AI is a biomedical data quality, governance, and interoperability platform designed to standardize oncology disease, gene, and variant data while maintaining explainability, traceability, and human oversight.

The platform combines:

* Biomedical entity resolution
* Evidence retrieval
* Confidence scoring
* Human governance workflows
* Interoperability exports
* Benchmark-driven validation

The architecture is intentionally designed to support trustworthy AI by ensuring uncertain recommendations are reviewed by human experts.

---

# High-Level Architecture

```text
Clinical Data Sources
Genomic Data Sources
Laboratory Data Sources
Research Data Sources

            |
            v

     Normalization Layer

            |
            v

   Entity Resolution Layer

            |
            v

    Evidence Retrieval Layer

            |
            v

     Confidence Engine

            |
            v

     Governance Engine

            |
            v

      Human Review Layer

            |
            v

    Interoperability Layer

            |
            v

Analytics & AI Applications
```

---

# Data Sources

The platform is designed to process oncology data originating from multiple systems.

Examples include:

## Clinical Sources

* Electronic Health Records (EHR)
* Cancer Registries
* Clinical Trial Systems

## Molecular Sources

* Molecular Diagnostic Reports
* Next-Generation Sequencing Platforms
* Clinical Genomics Pipelines

## Research Sources

* Research Databases
* Real-World Evidence Platforms
* Precision Oncology Programs

---

# Normalization Layer

The normalization layer standardizes incoming values before reconciliation.

Examples:

| Input        | Normalized   |
| ------------ | ------------ |
| HER2         | her2         |
| HER-2        | her2         |
| HER 2        | her2         |
| EGFR Ex19del | egfr ex19del |

Functions include:

* Case normalization
* Punctuation normalization
* Whitespace normalization
* Synonym preparation

This stage reduces variation prior to matching.

---

# Entity Resolution Layer

The entity resolution layer converts raw inputs into canonical biomedical concepts.

Supported entities:

* Disease
* Gene
* Variant

Resolution strategies include:

## Exact Matching

Example:

```text id="r4a1ko"
EGFR → EGFR
```

---

## Alias Matching

Example:

```text id="c4ay6m"
HER1 → EGFR
HER2 → ERBB2
p53 → TP53
```

---

## Fuzzy Matching

Used when exact and alias matching fail.

Examples:

```text id="7e95li"
non small cell lung ca
     →
Lung Non-Small Cell Carcinoma
```

---

## Context-Aware Resolution

The platform evaluates:

* Disease context
* Gene context
* Variant context

to improve reconciliation quality.

---

# Evidence Retrieval Layer

Evidence retrieval provides supporting information for reconciliation decisions.

Sources currently include:

## Local Knowledge Sources

* Disease catalogs
* Gene catalogs
* Variant catalogs

---

## External Knowledge Sources

* MyVariant.info
* ClinVar
* CIViC
* ClinGen resources

---

# Evidence Package Generation

Evidence packages provide:

* Supporting evidence
* Provenance
* Auditability
* Reviewer context

These packages help reviewers make informed decisions.

---

# Confidence Engine

The confidence engine evaluates reconciliation quality.

Factors include:

| Factor              | Purpose                        |
| ------------------- | ------------------------------ |
| Match Type          | Exact vs Alias vs Fuzzy        |
| Source Authority    | Evidence quality               |
| Similarity Score    | String similarity              |
| Context Consistency | Disease-gene-variant coherence |
| Catalog Coverage    | Curated support                |

Outputs:

* Confidence Score
* Confidence Category

Examples:

```text id="44xt1i"
HIGH
MEDIUM
LOW
```

---

# Governance Engine

The governance engine determines the appropriate workflow.

Possible outcomes:

## AUTO_RECONCILE

High-confidence mappings.

Characteristics:

* Strong evidence
* Consistent context
* Low ambiguity

---

## REVIEW_REQUIRED

Ambiguous mappings requiring expert review.

Characteristics:

* Multiple candidates
* Limited evidence
* Potential ambiguity

---

## CANNOT_RECONCILE

Insufficient evidence.

Characteristics:

* No reliable mapping
* Missing context
* Unknown terminology

---

# Human Review Layer

Human governance is a core platform feature.

The platform intentionally avoids forcing uncertain decisions.

Capabilities include:

## Review Queue

Stores cases requiring review.

---

## Reviewer Decisions

Supported actions:

* Approve
* Reject
* Edit
* Reopen

---

## Adjudication

Senior reviewers can resolve disagreements.

---

## Governance Metrics

Examples:

* Review rates
* Agreement rates
* Adjudication rates
* Reviewer productivity

---

# Interoperability Layer

The interoperability layer prepares standardized outputs.

## FHIR Export

Supports future healthcare interoperability.

Potential resources include:

* Patient
* Condition
* Observation
* DiagnosticReport

---

## OMOP Export

Supports:

* Research workflows
* Real-world evidence studies
* Cohort generation

---

## Knowledge Graph Export

Supports graph-based analytics.

Examples:

```text id="a7o4hf"
Disease
   |
Gene
   |
Variant
   |
Evidence
```

---

# Analytics Layer

The analytics layer provides operational visibility.

Current capabilities include:

## Evaluation Dashboard

Tracks:

* Benchmark performance
* Accuracy metrics
* Safety metrics

---

## Governance Analytics

Tracks:

* Review rates
* Reviewer activity
* Escalation rates

---

## Data Quality Metrics

Tracks:

* Reconciliation success
* Ambiguous cases
* Coverage

---

# Validation Framework

The platform includes automated validation capabilities.

Current validation includes:

* Automated test suite
* Benchmark framework
* Negative control testing
* Safety-aware evaluation

Current benchmark coverage:

* 500 benchmark cases

Representative metrics:

* Disease Accuracy
* Gene Accuracy
* Variant Accuracy
* Safety-Aware Accuracy
* False Auto-Accept Rate

---

# Security & Governance Principles

The platform follows several design principles.

## Human Oversight

Humans remain responsible for final decisions.

---

## Explainability

Every recommendation includes:

* Evidence
* Confidence score
* Provenance
* Audit trail

---

## Transparency

The platform avoids hidden decision-making.

---

## Reproducibility

Results can be reproduced using the same inputs and evidence.

---

## Data Collection & Curation Pipeline

```text
Public Biomedical Sources
          ↓
Automated Collection Scripts
          ↓
Candidate Data
          ↓
Human Review / Curation
          ↓
Curated Knowledge Catalogs
          ↓
Benchmark Generation
          ↓
Reconciliation Engine
          ↓
Evaluation & Governance
```

The architecture separates automated collection from production curation. Current pipeline components include:

1. **MyGene.info** — collects gene aliases and supports gene-symbol normalization through [`download_gene_aliases_from_mygene.py`](../scripts/download_gene_aliases_from_mygene.py), producing [`raw_gene_alias_candidates.json`](../data/raw/raw_gene_alias_candidates.json) and [`gene_aliases.json`](../data/gene_aliases.json).
2. **CIViC** — collects cancer-variant candidates through [`download_variant_candidates_from_civic_graphql.py`](../scripts/download_variant_candidates_from_civic_graphql.py), producing [`civic_variant_candidates.csv`](../data/raw/civic_variant_candidates.csv).
3. **Disease aliases** — [`disease_aliases.json`](../data/disease_aliases.json) is the manually curated MVP knowledge base for disease terminology normalization.
4. **Disease-gene catalog** — [`disease_gene_catalog.csv`](../data/disease_gene_catalog.csv) provides curated, static disease-to-gene context.
5. **Gene-variant catalog** — [`create_gene_variant_catalog.py`](../scripts/create_gene_variant_catalog.py), [`create_expanded_gene_variant_catalog.py`](../scripts/create_expanded_gene_variant_catalog.py), and [`create_curated_catalog_from_review.py`](../scripts/create_curated_catalog_from_review.py) produce the canonical mappings in [`gene_variant_catalog.csv`](../data/gene_variant_catalog.csv).
6. **Benchmark generation** — [`generate_benchmark_cases_from_catalogs.py`](../scripts/generate_benchmark_cases_from_catalogs.py) produces [`benchmark_cases.csv`](../data/benchmark_cases.csv). The newer [`benchmark_v2.csv`](../data/benchmark_v2.csv) is the current benchmark and contains 500 cases.

| Data Source | Purpose | Current Status |
|---|---|---|
| MyGene.info | Gene aliases | Integrated |
| CIViC | Variant candidates | Integrated |
| ClinVar | Evidence support | Integrated |
| MyVariant.info | Evidence retrieval | Integrated |
| HGNC | Gene nomenclature support | Curated / integrated |
| ClinGen Allele Registry | Variant reference support | Integrated |
| Internal Curated Catalogs | Production mappings | Active |

Downloaded candidate data is not blindly promoted into production. Candidate aliases and variants are reviewed before becoming curated catalog entries. Ambiguous terms such as `TRK` should route to `REVIEW_REQUIRED`; unknown terms should route to `CANNOT_RECONCILE`.

Future source and standards expansion includes NCIt, OncoTree, COSMIC, OncoKB, SEER, TCGA, AACR GENIE, GA4GH VRS, GA4GH Cat-VRS, GA4GH VA-Spec, FHIR Genomics, and OMOP Oncology. These are roadmap targets, not claims of current clinical validation or complete standards compliance.

This governed data pipeline demonstrates that OncoReconcile AI is building a reusable biomedical knowledge asset and data quality infrastructure, not just a one-off reconciliation demo.

---

# Future Architecture Evolution

Planned future enhancements include:

## Patient Journey Analytics

```text id="6otdxq"
Diagnosis
      ↓
Biomarker Testing
      ↓
Treatment
      ↓
Progression
      ↓
Outcome
```

---

## Biomedical Knowledge Graphs

Expanded relationship modeling.

---

## Enterprise APIs

* Reconciliation API
* Evidence API
* Governance API
* Interoperability API

---

## AI-Assisted Curation

Future reviewer assistance capabilities while preserving human oversight.

---

# Architectural Philosophy

OncoReconcile AI is built around a simple principle:

**Trustworthy AI requires trustworthy data.**

The platform combines AI-assisted reconciliation with human governance to create explainable, auditable, and interoperable oncology data suitable for precision medicine, clinical research, and future healthcare AI applications.
