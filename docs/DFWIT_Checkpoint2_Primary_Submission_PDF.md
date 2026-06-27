---
header-includes:
  - \usepackage{xcolor}
  - \usepackage{graphicx}
  - \usepackage{fancyhdr}
  - \setlength{\headheight}{90pt}
  - \setlength{\headsep}{14pt}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyhead[C]{\includegraphics[width=3.6in,height=1.15in,keepaspectratio]{images/oncoreconcile_logo.png}}
  - \fancyfoot[L]{\textcolor{blue}{\textbf{OncoReconcile AI}}}
  - \fancyfoot[R]{\textcolor{blue}{\textbf{page \thepage}}}
  - \renewcommand{\headrulewidth}{0.4pt}
  - \renewcommand{\footrulewidth}{0.4pt}
  - \AtBeginDocument{\pagestyle{fancy}}
---

<div align="center">

# OncoReconcile AI

## AI-Powered Precision Oncology Data Quality, Governance & Interoperability Platform

### DFWIT AI & Startup Competition 2026

### Checkpoint 2 Primary Submission

**Team:** Variant Vanguard

**Submission Date:** June 27, 2026

**Demo Video:** https://drive.google.com/file/d/12k0wm4KthaTWYMj6u33mElQiiQ2KhR7p/view

</div>

---

## Executive Summary

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

## Checkpoint 2 Deliverables

* Human-governed reconciliation engine
* Single-record reconciliation
* Batch reconciliation
* Evidence retrieval
* Review queue and reviewer governance workflow
* 500-case benchmark evaluation
* Evaluation dashboard
* FHIR export prototype
* OMOP export prototype
* Knowledge graph export prototype
* Data collection and curation pipeline
* PDF-ready documentation package
* Screenshots and demo assets

---

## Official Judging Alignment

This submission is organized to align with the DFWIT judging dimensions:

* **Innovation, Business Value & Social Impact:** Applies AI-assisted reconciliation to precision-oncology data quality, a high-friction healthcare data problem that affects analytics, research, interoperability, and trustworthy AI readiness.
* **Tech Solution, Quality & User Experience:** Provides a working FastAPI + React application with guided single-record demos, CSV batch reconciliation, human review, benchmark dashboards, evidence display, and standards-inspired export prototypes.
* **Business Development:** Positions the product as a biomedical data quality layer for cancer centers, molecular labs, healthcare data platforms, AI teams, and pharma analytics groups, with future services, SaaS, and API paths.
* **Presentation:** Uses a judge-friendly GUI flow: reconcile a record, show evidence and governance, process a CSV batch, review ambiguous cases, and explain benchmark results from the dashboard.

---

## Problem Statement

Precision oncology data is fragmented across multiple sources:

* Electronic Health Records (EHR)
* Molecular Diagnostic Laboratories
* Clinical Trials
* Research Databases
* Real-World Evidence Platforms
* Healthcare Analytics Systems

The same biological concept frequently appears under different names.

| Input | Canonical Representation |
|---|---|
| HER2 | ERBB2 |
| HER1 | EGFR |
| p53 | TP53 |
| NSCLC | Lung Non-Small Cell Carcinoma |
| Ex19del | EGFR Exon 19 Deletion |
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

## Why This Matters

Healthcare organizations are increasingly adopting AI. However:

> **Trustworthy AI requires trustworthy data.**

Poorly standardized oncology data can lead to:

* Reduced data quality
* Increased manual effort
* Inconsistent analytics
* Lower interoperability
* Reduced confidence in AI systems

OncoReconcile AI focuses on improving data quality before downstream analytics and AI workflows.

---

## Solution Overview

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

<div align="center">

![](screenshots/02-single-record-reconciliation.png){width=5.8in}

**Figure 1. Single Record Reconciliation**

</div>

---

## Core Platform Capabilities

### Reconciliation Engine

* Disease reconciliation
* Gene reconciliation
* Variant reconciliation
* Alias normalization
* Fuzzy matching
* Compound disease-gene-variant reasoning

### Evidence Intelligence

* Local oncology catalogs
* MyVariant.info integration
* ClinVar integration
* CIViC integration
* ClinGen reference support

### Explainable AI

* Confidence scores
* Audit trails
* Evidence packages
* Alternative candidate suggestions
* Provenance tracking

### Human Governance

* Review queue
* Reviewer decisions
* Adjudication workflow
* Review reopening
* Governance metrics

### Interoperability

* FHIR export
* OMOP export
* Knowledge graph export
* VRS-inspired structures
* Cat-VRS-inspired structures
* VA-Spec-inspired provenance

### Analytics

* Evaluation dashboard
* Benchmark reporting
* Safety reporting
* Review metrics
* Data quality metrics

---

## GUI Demonstration Workflow

The current frontend is organized into five judge-facing tabs:

| GUI Tab | What Judges Can See |
|---|---|
| Single Record | Manual disease/gene/variant input, featured demo case, guided examples, canonical output, confidence score, evidence badges, decision rationale, alternatives, audit trail, and standards/export actions. |
| CSV Upload | Sample CSV, downloadable demo CSV, upload-and-reconcile workflow, batch status summary, and expandable result cards for each row. |
| Review Queue | Seeded review examples, pending/reviewed filters, curator ID, evidence/candidate indicators, approve/reject/edit/reopen actions, review history, and adjudication support. |
| Benchmark | Accuracy, coverage, review rate, total cases, status counts, evidence counts, review-decision counts, and benchmark-source explanation. |
| Evaluation | Visual KPI cards, status distribution, accuracy/coverage chart, review-rate chart, false auto-accept rate, evidence-source chart, reviewer agreement, review-decision chart, and failure breakdown. |

This workflow directly supports the presentation score because the demo can move from a messy oncology input to a governed, explainable, benchmarked output without requiring judges to inspect code.

---

## Technical Architecture

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

The architecture separates deterministic normalization, evidence discovery, confidence assessment, governance, and export. This separation supports traceability and allows enterprise teams to integrate the platform into existing oncology data pipelines without making automated clinical decisions.

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

The current governed pipeline includes:

1. **MyGene.info** — gene alias collection and gene-symbol support through [download_gene_aliases_from_mygene.py](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/scripts/download_gene_aliases_from_mygene.py), producing [raw_gene_alias_candidates.json](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/raw/raw_gene_alias_candidates.json) and [gene_aliases.json](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/gene_aliases.json).
2. **CIViC** — cancer-variant candidate collection through [download_variant_candidates_from_civic_graphql.py](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/scripts/download_variant_candidates_from_civic_graphql.py), producing [civic_variant_candidates.csv](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/raw/civic_variant_candidates.csv).
3. **Disease aliases** — [disease_aliases.json](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/disease_aliases.json), the manually curated MVP disease-normalization knowledge base.
4. **Disease-gene catalog** — [disease_gene_catalog.csv](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/disease_gene_catalog.csv), a curated/static source of disease-gene context.
5. **Gene-variant catalog** — built through [create_gene_variant_catalog.py](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/scripts/create_gene_variant_catalog.py), [create_expanded_gene_variant_catalog.py](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/scripts/create_expanded_gene_variant_catalog.py), or [create_curated_catalog_from_review.py](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/scripts/create_curated_catalog_from_review.py), producing [gene_variant_catalog.csv](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/gene_variant_catalog.csv).
6. **Benchmark generation** — [generate_benchmark_cases_from_catalogs.py](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/scripts/generate_benchmark_cases_from_catalogs.py) produces [benchmark_cases.csv](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/benchmark_cases.csv). The newer [benchmark_v2.csv](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/data/benchmark_v2.csv) is the current benchmark and contains 500 cases.

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

The data-source roadmap includes NCIt, OncoTree, COSMIC, OncoKB, SEER, TCGA, AACR GENIE, GA4GH VRS, GA4GH Cat-VRS, GA4GH VA-Spec, FHIR Genomics, and OMOP Oncology. These are future expansion targets, not claims of current clinical validation or complete standards compliance.

This governed data pipeline demonstrates that OncoReconcile AI is building a reusable biomedical knowledge asset and data quality infrastructure, not just a one-off reconciliation demo.

---

## Reviewer Governance Workflow

OncoReconcile AI is designed around three explicit outcomes:

| Outcome | Meaning | Next Step |
|---|---|---|
| `AUTO_RECONCILE` | Evidence and confidence support an automatic canonical mapping | Result remains auditable and exportable |
| `REVIEW_REQUIRED` | A plausible mapping exists but ambiguity or evidence gaps remain | Route to a human reviewer |
| `CANNOT_RECONCILE` | Available evidence does not support a reliable candidate | Preserve uncertainty and request additional information |

The governance workflow supports:

1. Stable review-queue cases and duplicate prevention
2. Reviewer approval, rejection, or canonical-value editing
3. Reviewer notes and chronological decision history
4. Reopening cases when new evidence becomes available
5. Multi-reviewer agreement measurement
6. Cohen's kappa reporting
7. Disagreement detection and senior-reviewer adjudication
8. Auditable provenance for the final governed result

The governing principle is:

> **AI assists. Humans decide.**

<div align="center">

![](screenshots/04-review-queue.png){width=5.8in}

**Figure 2. Human Review Queue**

</div>

---

## Validation & Quality

Current competition submission status:

| Metric | Result |
|---|---:|
| Backend Tests | 102 Passed |
| Benchmark | 500 Cases |
| Frontend Build | Passing |
| Evaluation Dashboard | Operational |
| Review Queue | Operational |
| Evidence Package | Operational |
| FHIR Export Prototype | Operational |
| OMOP Export Prototype | Operational |
| Knowledge Graph Export Prototype | Operational |

### Benchmark Evaluation Results

The benchmark framework supports alias normalization testing, ambiguous terminology testing, review-required scenarios, negative-control safety testing, and regression testing.

| Evaluation Metric | Result |
|---|---:|
| Disease Accuracy | 68.6% |
| Gene Accuracy | 96.6% |
| Variant Accuracy | 94.6% |
| Safety-Aware Status Accuracy | 89.8% |
| False Auto-Accept Rate | 0% |
| Negative Control Safety Rate | 100% |

The 500-case benchmark intentionally includes difficult ambiguity scenarios. Disease accuracy remains the clearest improvement opportunity, while the 0% false auto-accept rate demonstrates the value of routing uncertainty into governed review instead of forcing unsafe mappings.

The benchmark intentionally includes ambiguous and negative-control cases to evaluate safety-aware reconciliation behavior, not only exact-match accuracy.

---

<div style="page-break-before: always;"></div>

## Evaluation Dashboard Evidence

The submission dashboard evidence below summarizes the current `benchmark_v2.csv` evaluation context and the validated Checkpoint 2 metrics.

<div align="center">

![](screenshots/05-evaluation-dashboard.png){width=5.8in}

**Figure 3. Evaluation Dashboard**

</div>

---

## FHIR Interoperability

The platform provides an operational FHIR R4 export prototype for downstream healthcare integration.

FHIR output can represent:

* Patient context using a non-identifying placeholder where required
* Oncology disease as a `Condition`
* Gene and variant findings as `Observation` resources
* Sequence context as `MolecularSequence`
* Consolidated output as a `DiagnosticReport`
* Reconciliation activity and lineage as `Provenance`
* Confidence and review status through transparent extensions

The export layer preserves source terminology and reconciliation metadata so an enterprise system can trace the standardized result back to the original input. It is intended as an interoperability bridge for genomics pipelines, EHR integration, analytics, and governed data exchange—not as clinical interpretation.

---

## OMOP Interoperability

The platform provides an operational OMOP CDM v5.4-oriented export prototype for research and real-world evidence workflows.

OMOP output maps:

* Disease concepts to `condition_occurrence`
* Gene findings to `measurement`
* Variant findings to `observation`
* Known SNOMED and LOINC source codes to available OMOP standard concept identifiers
* Unresolved concepts to preserved source values for later vocabulary resolution

This structure supports cohort preparation, analytics, and integration with OMOP-based research environments while making vocabulary gaps explicit. A production deployment can connect the exporter to a complete OMOP vocabulary service for broader concept resolution.

---

## Enterprise Platform Vision

OncoReconcile AI is designed to grow from a focused reconciliation application into an enterprise precision-oncology data quality platform.

### Enterprise Data Quality Layer

The platform can sit between source systems and downstream applications:

```text
EHR + Laboratory + Registry + Research Data
                    |
                    v
        OncoReconcile Quality Layer
                    |
       +------------+-------------+
       |            |             |
       v            v             v
   FHIR/OMOP     Analytics    AI Applications
```

Enterprise capabilities can include:

* Batch and API-based reconciliation
* Organization-specific terminology catalogs
* Role-based reviewer workspaces
* Data-quality and governance dashboards
* Evidence and provenance APIs
* Auditable catalog-promotion workflows
* Multi-tenant or private enterprise deployment
* Integration with clinical, research, and analytics environments

### Commercial Paths

Potential future offerings include:

#### Professional Services

* Oncology data harmonization
* FHIR implementation
* OMOP implementation
* Clinical genomics consulting

#### SaaS Platform

* Individual subscriptions
* Team subscriptions
* Enterprise deployments

#### Enterprise APIs

* Reconciliation API
* Evidence API
* Governance API
* FHIR Quality API
* Interoperability API

---

## Patient Journey Analytics Vision

The same normalized disease, gene, variant, evidence, and governance data can support a future longitudinal patient-journey analytics layer.

```text
Diagnosis
    |
    v
Biomarker Testing
    |
    v
Treatment
    |
    v
Response
    |
    v
Progression
    |
    v
Next Therapy
```

Planned patient-journey capabilities include:

* Diagnosis timelines
* Biomarker-testing timelines
* Treatment history
* Disease-progression tracking
* Outcome reporting
* Cohort-level pathway analysis
* Data-completeness and quality monitoring across the journey

This is an enterprise analytics vision, not a claim that the current platform provides treatment recommendations or autonomous clinical decision support.

---

## Innovation

### Human-Governed AI

Rather than forcing automatic decisions, uncertain cases are escalated to human reviewers.

### Explainable Reconciliation

Every recommendation includes:

* Evidence
* Confidence score
* Audit trail
* Provenance

### Governance-First Design

The platform prioritizes transparency, reproducibility, and trust.

### Biomedical Specialization

Unlike general-purpose entity-resolution systems, OncoReconcile AI is purpose-built for precision-oncology workflows.

---

## User Experience & Product Quality

The Checkpoint 2 GUI is designed to make the system understandable in a short live demo:

* The Single Record tab includes curated example pathways for `AUTO_RECONCILE`, `REVIEW_REQUIRED`, and `CANNOT_RECONCILE`.
* The result view separates canonical output, confidence, evidence, decision rationale, audit trail, alternatives, and standards/export actions.
* The CSV Upload tab demonstrates a repeatable batch workflow using the same reconciliation engine.
* The Review Queue tab shows how uncertain records become human-governed decisions instead of silent automated guesses.
* The Benchmark and Evaluation tabs make quality, safety, and remaining gaps visible through metrics and charts.

---

## Team Differentiation

Team Variant Vanguard combines experience in precision oncology, clinical genomics, biomedical data engineering, healthcare interoperability, OMOP/FHIR-oriented data modeling, and AI-assisted data quality workflows. This domain background shaped the project's focus on governed reconciliation, explainability, evidence, and auditability rather than black-box automation.

---

## Expert Feedback & Customer Discovery

Early feedback from precision oncology and standards-oriented discussions highlighted several needs: reducing interpretation bottlenecks, preserving provenance, supporting human review, and aligning reconciliation outputs with emerging interoperability standards. This feedback informed the platform's emphasis on human governance, evidence packages, benchmark evaluation, and standards-aligned exports.

This feedback is formative and does not represent formal clinical validation.

---

## Target Users

| User Type | Example Use Cases |
|---|---|
| Cancer Centers | Data harmonization |
| Molecular Laboratories | Variant normalization |
| Pharmaceutical Companies | Biomarker analytics |
| Clinical Researchers | Cohort generation |
| Healthcare AI Teams | AI-ready datasets |
| Healthcare Data Platforms | Interoperability |

---

## Business Opportunity

Precision oncology generates growing volumes of clinical and genomic information, while healthcare organizations face pressure to improve data quality, reduce manual curation, support AI initiatives, and exchange data through standards-based interfaces.

OncoReconcile AI addresses this market as a biomedical data quality layer rather than a standalone terminology lookup tool. Its combination of reconciliation, evidence, governance, interoperability, and benchmark-driven validation creates a path toward enterprise services, SaaS deployment, and API licensing.

---

## Demonstration Assets

The Checkpoint 2 demonstration includes:

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

## Social Impact

Higher-quality oncology data can support:

* Better clinical research
* Safer healthcare AI
* Improved biomarker analytics
* Faster cohort discovery
* Greater interoperability

The platform promotes trustworthy AI by ensuring uncertain recommendations receive human review.

---

## Long-Term Vision

OncoReconcile AI aims to become the biomedical data quality and interoperability layer for precision oncology.

Future directions include:

* Multi-cancer support
* Enterprise APIs
* Biomedical knowledge graphs
* AI-assisted curation
* Clinical trial harmonization
* Patient journey analytics
* Precision oncology intelligence platforms

---

## Repository & Resources

All links in this PDF-export version are absolute and point to the `startup-platform` submission branch.

| Resource | URL |
|---|---|
| Repository | https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform |
| README | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/README.md |
| Primary Submission | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/DFWIT_Checkpoint2_Primary_Submission.md |
| Startup Platform Overview | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/startup_platform_overview.md |
| Architecture | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/architecture.md |
| Architecture Diagrams | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/architecture_diagrams.md |
| Commercial Strategy | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/commercial_strategy.md |
| Roadmap | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/roadmap.md |
| Curation Methodology | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/curation_methodology.md |
| Expert Feedback Summary | https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/expert_feedback_summary.md |

---

## Repository and Branch Information

**Organization:** oncoreconcile-ai  
**Repository:** oncoreconcile-ai  
**Submission branch:** `startup-platform`  
**Branch URL:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

---

## Disclaimer

OncoReconcile AI is a biomedical data harmonization and governance platform.

It is not a clinical decision support system and does not provide diagnosis, treatment recommendations, or medical advice.
