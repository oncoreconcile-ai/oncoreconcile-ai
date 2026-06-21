# DFWIT AI & Startup Competition 2026

# Checkpoint 2 Primary Submission

## Project Title

**OncoReconcile AI**

Human-Governed Biomedical Entity Resolution Platform for Precision Oncology

**Team:** Variant Vanguard

**Repository:**
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

---

# Executive Summary

OncoReconcile AI is a human-governed AI platform that reconciles fragmented oncology disease, gene, and variant terminology into standardized canonical representations.

Precision oncology data originates from multiple sources including electronic health records, molecular testing reports, research databases, clinical trials, and real-world evidence platforms. These sources often use inconsistent naming conventions, aliases, abbreviations, and partial representations that prevent reliable downstream analytics and AI applications.

OncoReconcile AI addresses this challenge through a reconciliation pipeline that combines curated biomedical knowledge, evidence retrieval, confidence scoring, and human governance workflows.

The platform produces explainable reconciliation decisions with provenance, confidence scores, and explicit review recommendations.

---

# Problem Statement

Precision oncology datasets frequently contain inconsistent biomedical terminology.

Examples include:

| Input    | Canonical Representation             |
| -------- | ------------------------------------ |
| NSCLC    | Non-Small Cell Lung Carcinoma        |
| HER2     | ERBB2                                |
| HER1     | EGFR                                 |
| Ex19del  | EGFR c.2235_2249del15                |
| FLT3 ITD | Standardized FLT3 ITD representation |

These inconsistencies create challenges for:

* Precision oncology programs
* Clinical research
* Clinical trial matching
* Biomarker analytics
* Real-world evidence studies
* AI model development
* Healthcare interoperability

Current workflows often require substantial manual review and expert curation.

---

# Solution

OncoReconcile AI provides a human-governed reconciliation framework that standardizes oncology entities while preserving transparency and auditability.

Core capabilities include:

* Disease reconciliation
* Gene reconciliation
* Variant reconciliation
* Evidence retrieval
* Confidence scoring
* Human review governance
* Provenance tracking
* Benchmark evaluation

The platform does not provide diagnosis or treatment recommendations.

---

# System Architecture

```text
User Input
     |
     v
Normalization Engine
     |
     +--> Alias Matching
     +--> Fuzzy Matching
     +--> Catalog Matching
     |
     v
Evidence Retrieval Layer
     |
     +--> Local Catalog
     +--> MyVariant.info
     +--> ClinVar
     +--> CIViC
     +--> ClinGen Allele Registry
     |
     v
Confidence Scoring
     |
     v
Governance Engine
     |
     +--> AUTO_RECONCILE
     +--> REVIEW_REQUIRED
     +--> CANNOT_RECONCILE
     |
     v
Review Queue
     |
     v
Benchmarking & Analytics
```

Additional technical details are provided in:

* docs/architecture.md
* docs/architecture_diagrams.md

---

# Implemented Features

## Reconciliation Engine

* Exact matching
* Alias matching
* Fuzzy matching
* Compound disease-gene-variant matching
* Canonical entity normalization

## Governance Framework

* AUTO_RECONCILE
* REVIEW_REQUIRED
* CANNOT_RECONCILE

## Evidence Sources

* Local curated knowledge base
* MyVariant.info integration
* ClinVar integration
* CIViC integration
* ClinGen Allele Registry integration

## Human Review Workflow

* Persistent review queue
* Curator review support
* Senior curator adjudication
* Reviewer agreement metrics
* Cohen's kappa calculation

## Export Foundations

* Provenance exports
* JSON-LD exports
* Knowledge graph foundations
* Standards-inspired VRS and VA-Spec structures

---

# Evaluation & Validation

Current platform validation results:

| Metric                    | Result     |
| ------------------------- | ---------- |
| Backend Tests             | 102 Passed |
| Benchmark Cases           | 191        |
| Frontend Production Build | Passed     |

The platform includes a dedicated evaluation dashboard that supports:

* Accuracy reporting
* Benchmark analysis
* Review-rate monitoring
* False auto-accept monitoring

---

# Demonstration Workflow

A typical workflow includes:

1. User submits disease, gene, and variant inputs.
2. Reconciliation engine identifies canonical candidates.
3. Evidence retrieval gathers supporting information.
4. Confidence scoring evaluates reconciliation quality.
5. Governance engine determines reconciliation status.
6. Ambiguous cases are routed to human review.
7. Provenance and analytics outputs are generated.

---

# Innovation

Key innovations include:

### Human-Governed AI

Rather than forcing automatic decisions, uncertain cases are explicitly escalated to expert review.

### Explainable Reconciliation

Every decision includes:

* Evidence
* Confidence score
* Audit trail
* Provenance

### Governance-First Design

The platform prioritizes trust, transparency, and reproducibility.

### Biomedical Focus

Unlike general-purpose entity resolution tools, OncoReconcile AI is designed specifically for precision oncology workflows.

---

# Target Users

Potential users include:

| User Type                 | Use Case                   |
| ------------------------- | -------------------------- |
| Cancer Centers            | Data harmonization         |
| Pharmaceutical Companies  | Biomarker analytics        |
| Clinical Researchers      | Data standardization       |
| Registries                | Terminology reconciliation |
| AI Teams                  | High-quality training data |
| Healthcare Data Platforms | Interoperability support   |

---

# Startup Potential

The long-term vision is to become the biomedical entity resolution layer for precision oncology.

Future development areas include:

* FHIR interoperability
* OMOP interoperability
* Biomedical knowledge graphs
* Enterprise APIs
* Multi-cancer support
* AI-assisted curation
* Clinical trial harmonization

By addressing one of the most persistent data-quality challenges in oncology, OncoReconcile AI has the potential to reduce manual curation effort, improve interoperability, and accelerate AI adoption in healthcare.

---

# Repository

Primary Submission Branch:

**startup-platform**

Repository:

https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

---

# Disclaimer

OncoReconcile AI is a biomedical data harmonization and governance platform.

It is not a clinical decision support system and does not provide diagnosis, treatment recommendations, or medical advice.
