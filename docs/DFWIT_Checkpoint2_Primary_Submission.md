# DFWIT AI & Startup Competition 2026

# Checkpoint 2 Primary Submission

## Project Title

**OncoReconcile AI**

### AI-Powered Precision Oncology Data Quality, Governance & Interoperability Platform

**Team:** Variant Vanguard

**Submission Branch:** startup-platform

**Repository:**
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

---

# Executive Summary

OncoReconcile AI is an AI-powered biomedical data quality, governance, and interoperability platform designed to improve the consistency, explainability, and AI-readiness of oncology and clinical genomics data.

The platform reconciles heterogeneous disease names, genes, and genomic variants into standardized canonical representations using:

* AI-assisted entity resolution
* Evidence retrieval
* Confidence scoring
* Explainable recommendations
* Human review workflows
* Standards-aligned exports

Rather than forcing uncertain mappings, the system surfaces supporting evidence and routes ambiguous cases through expert review.

The result is trustworthy, explainable, and reusable oncology data suitable for precision medicine, clinical research, healthcare analytics, and future AI applications.

---

# Problem Statement

Precision oncology data is fragmented across multiple sources:

* Electronic Health Records (EHR)
* Molecular Diagnostic Laboratories
* Clinical Trials
* Research Databases
* Real-World Evidence Platforms
* Healthcare Analytics Systems

The same biological concept frequently appears under different names.

| Input    | Canonical Representation         |
| -------- | -------------------------------- |
| HER2     | ERBB2                            |
| HER1     | EGFR                             |
| p53      | TP53                             |
| NSCLC    | Lung Non-Small Cell Carcinoma    |
| Ex19del  | EGFR Exon 19 Deletion            |
| FLT3 ITD | FLT3 Internal Tandem Duplication |

These inconsistencies create challenges for:

* Biomarker analytics
* Cohort generation
* Clinical trial matching
* Data integration
* AI model development
* Healthcare interoperability

Organizations often spend substantial effort manually harmonizing data before it becomes useful.

---

# Why This Matters

Healthcare organizations are increasingly adopting AI.

However:

**Trustworthy AI requires trustworthy data.**

Poorly standardized oncology data can lead to:

* Reduced data quality
* Increased manual effort
* Inconsistent analytics
* Lower interoperability
* Reduced confidence in AI systems

OncoReconcile AI focuses on improving data quality before downstream analytics and AI workflows.

---

# Solution Overview

```text
Disease / Gene / Variant Input
                |
                v
       Entity Resolution
                |
                v
       Evidence Retrieval
                |
                v
       Confidence Scoring
                |
                v
       Governance Decision
        /       |        \
AUTO_RECONCILE REVIEW_REQUIRED CANNOT_RECONCILE
                |
                v
         Human Review
                |
                v
          Curated Output
                |
                v
     FHIR / OMOP / Analytics
```

---

# Core Platform Capabilities

## Reconciliation Engine

* Disease reconciliation
* Gene reconciliation
* Variant reconciliation
* Alias normalization
* Fuzzy matching
* Compound disease-gene-variant reasoning

## Evidence Intelligence

* Local oncology catalogs
* MyVariant.info integration
* ClinVar integration
* CIViC integration
* ClinGen reference support

## Explainable AI

* Confidence scores
* Audit trails
* Evidence packages
* Alternative candidate suggestions
* Provenance tracking

## Human Governance

* Review queue
* Reviewer decisions
* Adjudication workflow
* Review reopening
* Governance metrics

## Interoperability

* FHIR export
* OMOP export
* Knowledge graph export
* VRS-inspired structures
* Cat-VRS-inspired structures
* VA-Spec-inspired provenance

## Analytics

* Evaluation dashboard
* Benchmark reporting
* Safety reporting
* Review metrics
* Data quality metrics

---

# Technical Architecture

```text
Clinical Data Sources
Genomic Data Sources
Laboratory Data Sources

            |
            v

    Normalization Layer

            |
            v

   Entity Resolution Layer

            |
            v

    Evidence Retrieval

            |
            v

     Confidence Engine

            |
            v

     Governance Engine

            |
            v

      Human Review

            |
            v

    FHIR / OMOP Export

            |
            v

 Analytics & AI Applications
```

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

Current pipeline components:

1. **MyGene.info** — gene alias collection and gene-symbol support through [`download_gene_aliases_from_mygene.py`](../scripts/download_gene_aliases_from_mygene.py), producing [`raw_gene_alias_candidates.json`](../data/raw/raw_gene_alias_candidates.json) and [`gene_aliases.json`](../data/gene_aliases.json).
2. **CIViC** — cancer-variant candidate collection through [`download_variant_candidates_from_civic_graphql.py`](../scripts/download_variant_candidates_from_civic_graphql.py), producing [`civic_variant_candidates.csv`](../data/raw/civic_variant_candidates.csv).
3. **Disease aliases** — [`disease_aliases.json`](../data/disease_aliases.json), the manually curated MVP disease-normalization knowledge base.
4. **Disease-gene catalog** — [`disease_gene_catalog.csv`](../data/disease_gene_catalog.csv), a curated/static source of disease-gene context.
5. **Gene-variant catalog** — built through [`create_gene_variant_catalog.py`](../scripts/create_gene_variant_catalog.py), [`create_expanded_gene_variant_catalog.py`](../scripts/create_expanded_gene_variant_catalog.py), or [`create_curated_catalog_from_review.py`](../scripts/create_curated_catalog_from_review.py), producing [`gene_variant_catalog.csv`](../data/gene_variant_catalog.csv).
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

The data-source roadmap includes NCIt, OncoTree, COSMIC, OncoKB, SEER, TCGA, AACR GENIE, GA4GH VRS, GA4GH Cat-VRS, GA4GH VA-Spec, FHIR Genomics, and OMOP Oncology. These are future expansion targets, not claims of current clinical validation.

This governed data pipeline demonstrates that OncoReconcile AI is building a reusable biomedical knowledge asset and data quality infrastructure, not just a one-off reconciliation demo.

---

# Validation & Quality

Current platform status:

| Metric                 | Result      |
| ---------------------- | ----------- |
| Backend Test Suite    | 102 Passing |
| Frontend Build         | Passing     |
| Evaluation Dashboard   | Operational |
| Review Queue           | Operational |
| Evidence Package       | Operational |
| FHIR Export            | Operational |
| OMOP Export            | Operational |
| Knowledge Graph Export | Operational |

---

# Benchmark Framework

The platform includes a benchmark evaluation framework supporting:

* Alias normalization testing
* Ambiguous terminology testing
* Review-required scenarios
* Negative control safety testing
* Regression testing

Current benchmark coverage:

* 500 benchmark cases

Representative results:

| Metric                       | Result |
| ---------------------------- | ------ |
| Disease Accuracy             | 68.6%  |
| Gene Accuracy                | 96.6%  |
| Variant Accuracy             | 94.6%  |
| Safety-Aware Status Accuracy | 89.8%  |
| False Auto-Accept Rate       | 0%     |
| Negative Control Safety Rate | 100%   |

The benchmark intentionally includes difficult ambiguity scenarios to evaluate governance and safety behavior.

---

# Innovation

## Human-Governed AI

Rather than forcing automatic decisions, uncertain cases are escalated to human reviewers.

## Explainable Reconciliation

Every recommendation includes:

* Evidence
* Confidence score
* Audit trail
* Provenance

## Governance-First Design

The platform prioritizes transparency, reproducibility, and trust.

## Biomedical Specialization

Unlike general-purpose entity resolution systems, OncoReconcile AI is purpose-built for precision oncology workflows.

---

# Target Users

| User Type                 | Example Use Cases     |
| ------------------------- | --------------------- |
| Cancer Centers            | Data harmonization    |
| Molecular Laboratories    | Variant normalization |
| Pharmaceutical Companies  | Biomarker analytics   |
| Clinical Researchers      | Cohort generation     |
| Healthcare AI Teams       | AI-ready datasets     |
| Healthcare Data Platforms | Interoperability      |

---

# Business Opportunity

Potential future offerings include:

### Professional Services

* Oncology data harmonization
* FHIR implementation
* OMOP implementation
* Clinical genomics consulting

### SaaS Platform

* Individual subscriptions
* Team subscriptions
* Enterprise deployments

### Enterprise APIs

* Reconciliation API
* Evidence API
* Governance API
* FHIR Quality API

---

# Demonstration Assets

Checkpoint 2 Demonstration Includes:

* Single Record Reconciliation
* Batch Reconciliation
* Human Review Queue
* Evaluation Dashboard
* Evidence Package Generation
* FHIR Export
* OMOP Export

---

# Social Impact

Higher-quality oncology data can support:

* Better clinical research
* Safer healthcare AI
* Improved biomarker analytics
* Faster cohort discovery
* Greater interoperability

The platform promotes trustworthy AI by ensuring uncertain recommendations receive human review.

---

# Long-Term Vision

OncoReconcile AI aims to become the biomedical data quality and interoperability layer for precision oncology.

Future directions include:

* Multi-cancer support
* Enterprise APIs
* Biomedical Knowledge Graphs
* AI-Assisted Curation
* Clinical Trial Harmonization
* Precision Oncology Intelligence Platforms

---

# Repository

Primary Submission Branch:

**startup-platform**

https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

---

## Additional Resources

* **Repository:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform
* **README:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/README.md
* **Architecture:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/architecture.md
* **Architecture Diagrams:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/architecture_diagrams.md
* **Commercial Strategy:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/commercial_strategy.md
* **Roadmap:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/roadmap.md

---

# Disclaimer

OncoReconcile AI is a biomedical data harmonization and governance platform.

It is not a clinical decision support system and does not provide diagnosis, treatment recommendations, or medical advice.
