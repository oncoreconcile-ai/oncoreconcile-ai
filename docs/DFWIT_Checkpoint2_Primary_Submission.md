# DFWIT AI & Startup Competition 2026

# Checkpoint 2 Primary Submission

## Project Title

**OncoReconcile AI**

### AI-Powered Precision Oncology Data Quality, Governance & Interoperability Platform

**Team:** Variant Vanguard

**Submission Branch:** startup-platform

**Repository:**
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

**Demo Video:** [Google Drive demo video](https://drive.google.com/file/d/12k0wm4KthaTWYMj6u33mElQiiQ2KhR7p/view)

---

# Team Information

| Field | Information |
| ----- | ----------- |
| Team Name | Variant Vanguard |
| Project | OncoReconcile AI |
| Competition | DFWIT AI & Startup Competition 2026 |
| Checkpoint | Checkpoint 2 |
| Submission Branch | `startup-platform` |

Demo video: [Google Drive demo video](https://drive.google.com/file/d/12k0wm4KthaTWYMj6u33mElQiiQ2KhR7p/view).

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

# Official Judging Alignment

This submission is organized to align with the DFWIT judging dimensions:

* **Innovation, Business Value & Social Impact:** Applies AI-assisted reconciliation to precision-oncology data quality, a high-friction healthcare data problem that affects analytics, research, interoperability, and trustworthy AI readiness.
* **Tech Solution, Quality & User Experience:** Provides a working FastAPI + React application with guided single-record demos, CSV batch reconciliation, human review, benchmark dashboards, evidence display, and standards-inspired export prototypes.
* **Business Development:** Positions the product as a biomedical data quality layer for cancer centers, molecular labs, healthcare data platforms, AI teams, and pharma analytics groups, with future services, SaaS, and API paths.
* **Presentation:** Uses a judge-friendly GUI flow: reconcile a record, show evidence and governance, process a CSV batch, review ambiguous cases, and explain benchmark results from the dashboard.

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

# GUI Demonstration Workflow

The current frontend is organized into five judge-facing tabs:

| GUI Tab | What Judges Can See |
| ------- | ------------------- |
| Single Record | Manual disease/gene/variant input, featured demo case, guided examples, canonical output, confidence score, evidence badges, decision rationale, alternatives, audit trail, and standards/export actions. |
| CSV Upload | Sample CSV, downloadable demo CSV, upload-and-reconcile workflow, batch status summary, and expandable result cards for each row. |
| Review Queue | Seeded review examples, pending/reviewed filters, curator ID, evidence/candidate indicators, approve/reject/edit/reopen actions, review history, and adjudication support. |
| Benchmark | Accuracy, coverage, review rate, total cases, status counts, evidence counts, review-decision counts, and benchmark-source explanation. |
| Evaluation | Visual KPI cards, status distribution, accuracy/coverage chart, review-rate chart, false auto-accept rate, evidence-source chart, reviewer agreement, review-decision chart, and failure breakdown. |

This workflow directly supports the presentation score because the demo can move from a messy oncology input to a governed, explainable, benchmarked output without requiring judges to inspect code.

---

# Screenshots

The primary submission includes the current GUI screenshots stored under `docs/screenshots/`.

## Platform Homepage

![OncoReconcile AI homepage](screenshots/01-homepage.png)

## Single Record Reconciliation

![High-confidence single record reconciliation](screenshots/02-single-record-reconciliation.png)

## Review-Required Decision

![Ambiguous TRK fusion routed to human review](screenshots/03-review-required.png)

## Human Review Queue

![Human review queue and curator workflow](screenshots/04-review-queue.png)

## Evaluation Dashboard

![Benchmark evaluation and safety metrics](screenshots/05-evaluation-dashboard.png)

## Knowledge Graph Export

![JSON-LD knowledge graph export](screenshots/06-knowledge-graph-export.png)

## Interactive API Documentation

![FastAPI OpenAPI documentation](screenshots/07-api-docs.png)

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

# User Experience & Product Quality

The Checkpoint 2 GUI is designed to make the system understandable in a short live demo:

* The Single Record tab includes curated example pathways for `AUTO_RECONCILE`, `REVIEW_REQUIRED`, and `CANNOT_RECONCILE`.
* The result view separates canonical output, confidence, evidence, decision rationale, audit trail, alternatives, and standards/export actions.
* The CSV Upload tab demonstrates a repeatable batch workflow using the same reconciliation engine.
* The Review Queue tab shows how uncertain records become human-governed decisions instead of silent automated guesses.
* The Benchmark and Evaluation tabs make quality, safety, and remaining gaps visible through metrics and charts.

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

Precision oncology generates growing volumes of clinical and genomic information, while healthcare organizations face pressure to improve data quality, reduce manual curation, support AI initiatives, and exchange data through standards-based interfaces.

OncoReconcile AI addresses this market as a biomedical data quality layer rather than a standalone terminology lookup tool. Its combination of reconciliation, evidence, governance, interoperability, and benchmark-driven validation creates a path toward enterprise services, SaaS deployment, and API licensing.

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

Checkpoint 2 demonstration includes:

* Single Record Reconciliation tab
* CSV Upload tab
* Human Review Queue tab
* Benchmark tab
* Evaluation Dashboard tab
* Evidence package and audit-trail display
* Provenance export
* Knowledge graph export
* FHIR export prototype
* OMOP export prototype

Suggested live demo order:

1. Run the featured single-record demo and explain evidence, confidence, and review status.
2. Open detailed evidence to show local evidence, live external evidence, safe API error handling, governance evidence, and audit trail.
3. Use the standards/export buttons to show provenance, knowledge graph, VRS-ready, Cat-VRS-ready, VA-Spec-ready, and FHIR JSON outputs.
4. Upload or use the sample CSV to show repeatable batch reconciliation.
5. Seed and review an ambiguous case in the Human Review Queue.
6. Close with Benchmark and Evaluation dashboards to show measured quality, safety-aware status accuracy, and false auto-accept rate.

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
