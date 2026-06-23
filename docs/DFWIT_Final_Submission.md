# DFWIT 2026 AI & Startup Competition

# Final Submission — OncoReconcile AI

**Team:** Variant Vanguard  
**Submission branch:** `enterprise-patient-journey-demo`  
**Repository:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo  
**Demo video:** [FINAL DEMO VIDEO LINK — TO BE ADDED]

## Executive Summary

OncoReconcile AI is an AI-powered precision oncology data quality, semantic harmonization, governance, interoperability, and analytics platform.

Healthcare organizations receive oncology data from electronic health records, molecular laboratories, research systems, clinical trials, and external data partners. The same disease, gene, or genomic variant can be represented in many incompatible ways. Those inconsistencies increase manual curation, weaken analytics, complicate interoperability, and make downstream AI less trustworthy.

OncoReconcile AI turns fragmented inputs into explainable, governed, reusable data. It combines deterministic normalization, evidence retrieval, confidence scoring, narrowly controlled AI assistance, human review, coding-system mapping, standards-oriented exports, benchmark evaluation, and enterprise analytics.

The platform does not make treatment recommendations. Its purpose is to improve the quality and traceability of the data used by researchers, analysts, data stewards, interoperability teams, and future AI applications.

## Judging-Criteria Alignment

The final package follows the official DFWIT 2026 rubric:

| Judging dimension | Weight | OncoReconcile AI evidence |
|---|---:|---|
| Innovation, Business Value & Social Impact | 35% | Human-governed AI, oncology-specific semantic harmonization, safer data for analytics and AI |
| Tech Solution, Quality & User Experience | 20% | Working web product, API-first architecture, 127 passing backend tests, passing frontend build, governed exports |
| Business Development | 35% | Defined enterprise customers, services-to-SaaS commercialization path, API and integration opportunities |
| Presentation | 10% | Five-minute workflow, executive dashboard, evidence-backed metrics, clear limitations and safety boundaries |

Official rules: https://ai.dfwit.org/Rules  
Official submission portal: https://ai.dfwit.org/Submission

## Problem Statement

Precision oncology data is fragmented across:

- electronic health records and cancer registries;
- molecular diagnostic and next-generation sequencing reports;
- clinical-trial and research datasets;
- pharmaceutical and real-world-evidence platforms;
- claims, data warehouses, and interoperability feeds.

Common concepts arrive as aliases, abbreviations, legacy labels, free text, and inconsistent codes:

| Raw input | Harmonized representation |
|---|---|
| `HER2` | `ERBB2` |
| `HER1` | `EGFR` |
| `p53` | `TP53` |
| `NSCLC` | Lung Non-Small Cell Carcinoma |
| `Ex19del` | EGFR Exon 19 Deletion |

Organizations often resolve these inconsistencies through spreadsheets, one-off scripts, manual lookup, or disconnected terminology tools. Those methods are difficult to scale, audit, and govern.

## Why This Matters

Trustworthy AI requires trustworthy data.

If semantically equivalent records are not aligned, cohort counts can be incomplete, biomarker trends can be distorted, patient journeys can fragment across systems, and AI models can learn from inconsistent labels. If uncertain mappings are accepted automatically, bad data can become more difficult to detect after it reaches downstream systems.

OncoReconcile AI addresses the data-quality layer before clinical analytics, research, interoperability, or AI consumption. Its governance model treats uncertainty as information: a record can be automatically reconciled, routed for human review, or explicitly marked as not safely reconcilable.

## Solution Overview

```text
Raw oncology and genomics data
              ↓
Entity and text normalization
              ↓
Disease / gene / variant reconciliation
              ↓
Evidence retrieval and confidence scoring
              ↓
Governance decision
   AUTO_RECONCILE | REVIEW_REQUIRED | CANNOT_RECONCILE
              ↓
Human review, adjudication, and audit trail
              ↓
Semantic and coding-system mappings
              ↓
FHIR / OMOP / knowledge graph exports
              ↓
Enterprise analytics and AI-ready datasets
```

The product is designed as a quality-control and semantic-governance layer that can sit between source systems and downstream analytics, research, interoperability, or AI workflows.

## AI Components

OncoReconcile AI uses a layered approach so that AI does not silently override governed data rules.

1. **AI-assisted entity reconciliation:** candidate matching and contextual interpretation help identify potential disease, gene, and variant mappings.
2. **Evidence-aware confidence scoring:** local catalog support, disease-gene context, gene-variant context, external evidence, ambiguity, and missing information contribute to a transparent score.
3. **Controlled LLM review suggestion:** an optional model-agnostic module can suggest a candidate only for a review-required workflow. It does not convert an uncertain case into automatic acceptance.
4. **Human governance:** ambiguous outputs are presented with evidence, alternatives, notes, and an audit trail for curator review.
5. **Benchmark-driven safety evaluation:** negative controls and status-aware evaluation measure whether the system avoids unsafe automatic reconciliation.

The default LLM provider is a safe stub unless explicitly configured. Deterministic local matches remain the primary path, and AI suggestions are review aids rather than clinical outputs.

## Product Demo Workflow

The final demonstration follows one coherent data story:

1. Open the platform homepage and explain the data-quality problem.
2. Reconcile a high-confidence disease-gene-variant record.
3. Inspect the canonical output, confidence score, evidence package, and audit trail.
4. Submit an ambiguous case and show `REVIEW_REQUIRED`.
5. Open the review queue and demonstrate the curator workflow.
6. Move from one record to the synthetic longitudinal patient journey.
7. Show enterprise cohort, quality, governance, and executive analytics.
8. Inspect semantic mappings across clinical coding systems.
9. Export the governed data as FHIR, OMOP, and a knowledge graph.
10. Open the interactive API documentation to show integration readiness.

## Enterprise Patient Journey Demo

The enterprise extension demonstrates how reconciliation can support a broader longitudinal oncology data platform.

- **Dataset:** 15 synthetic oncology patient journeys
- **Cancer types:** NSCLC, breast cancer, colorectal cancer, melanoma, and AML
- **Journey content:** diagnosis, histology, stage, biomarker testing, genes, variants, fusions, copy-number alterations, treatments, responses, progression events, trial flags, reconciliation status, evidence coverage, and data-quality scores
- **Dashboards:** patient journey, cohort analytics, terminology coverage, governance metrics, and executive summary
- **Exports:** expanded FHIR R4 Bundle, OMOP CDM v5.4-oriented records, and knowledge graph

All patient journey data is synthetic and is used only to demonstrate product workflow, interoperability, governance, and analytics.

## Semantic Harmonization & Coding Systems

The demonstration includes a curated semantic layer that maps oncology concepts across:

| Domain | Demonstrated coding systems |
|---|---|
| Disease | SNOMED CT, NCIt, OncoTree, ICD-10 |
| Histology | SNOMED CT, NCIt |
| Gene | HGNC |
| Drug | RxNorm, ATC |
| Variant / biomarker | ClinVar, ClinGen-inspired identifiers |
| Laboratory test | LOINC |

Mappings include source, confidence, and review status. This is a prototype semantic layer, not a complete terminology service or an assertion of official certification by any standards organization.

## Human Governance Workflow

OncoReconcile AI separates three outcomes:

- **AUTO_RECONCILE:** evidence and context support a high-confidence canonical mapping.
- **REVIEW_REQUIRED:** a plausible mapping exists, but ambiguity or incomplete evidence requires human judgment.
- **CANNOT_RECONCILE:** no sufficiently trustworthy mapping is available.

Review-queue records retain:

- original and canonical values;
- confidence and score breakdown;
- evidence and alternatives;
- reviewer identity and notes;
- decision history and timestamps;
- adjudication state;
- audit and provenance details.

This design helps organizations scale automation while preserving accountable human control.

## Technical Architecture

| Layer | Current implementation |
|---|---|
| Frontend | React and Vite web application |
| API | FastAPI endpoints with interactive OpenAPI documentation |
| Reconciliation | Disease, gene, and variant normalization with curated aliases and catalogs |
| Evidence | Local evidence packages plus guarded external retrieval integrations |
| Governance | Review queue, decisions, reopening, adjudication, and metrics |
| Analytics | Benchmark dashboard and enterprise patient/cohort/executive views |
| Interoperability | FHIR R4 prototype, OMOP CDM v5.4 prototype, JSON-LD knowledge graph |
| Validation | Pytest backend suite, frontend production build, 500-case benchmark |

The API-first design supports future integration into data warehouses, research platforms, clinical data pipelines, laboratory systems, and enterprise governance workflows.

## Validation Metrics

Validated on the `enterprise-patient-journey-demo` branch on June 22, 2026:

| Validation item | Current result |
|---|---:|
| Backend automated tests | 127 passed |
| Frontend production build | Passing |
| Benchmark size | 500 cases |
| Gene accuracy | 96.6% |
| Variant accuracy | 94.6% |
| Safety-aware status accuracy | 89.8% |
| False auto-accept rate | 0% |
| Negative-control safety rate | 100% |

The benchmark is an internal evaluation framework, not a clinical validation study. Disease accuracy remains an improvement area and is not hidden by the stronger gene, variant, and safety results.

## Business Opportunity

Oncology organizations invest substantial expert time in cleaning, reconciling, reviewing, and remapping data before it can support analytics, interoperability, research, or AI. OncoReconcile AI can create value by:

- reducing repetitive terminology cleanup;
- making uncertain cases easier to prioritize and review;
- improving traceability for governed datasets;
- accelerating preparation of analytics- and AI-ready data;
- reducing duplicate mapping logic across projects;
- supporting standards-oriented delivery to downstream systems.

The initial commercial thesis is business-to-business data infrastructure and workflow software—not a consumer medical application.

## Target Customers

| Customer | Initial use case |
|---|---|
| Cancer centers and health systems | Oncology warehouse harmonization, registry quality, biomarker analytics |
| Molecular diagnostic laboratories | Consistent gene and variant representation, review workflows |
| Pharmaceutical and biotechnology companies | Multi-source biomarker and real-world-data harmonization |
| Clinical research organizations | Cross-site data standardization and trial-data readiness |
| Healthcare data and AI platforms | Governed oncology data-quality APIs and interoperability |
| Research networks and registries | Reusable mappings, provenance, and cohort consistency |

## Competitive Differentiation

OncoReconcile AI is differentiated by the combination of capabilities around the normalization task:

- oncology-specific disease, gene, and variant reconciliation;
- explicit uncertainty states instead of forced answers;
- evidence packages and score breakdowns;
- review queue, decision history, and adjudication;
- cross-terminology semantic mapping;
- FHIR, OMOP, and knowledge-graph export prototypes;
- benchmark and negative-control safety evaluation;
- patient-journey and executive analytics;
- API-first integration.

The platform is not positioned as a replacement for authoritative terminology sources or public biomedical knowledgebases. It is the governed workflow and data-quality layer that helps organizations apply, inspect, and operationalize those resources across messy real-world data.

## Social Impact

Higher-quality oncology data can contribute to:

- more reliable research datasets;
- safer and more transparent healthcare AI development;
- more consistent biomarker and cohort analytics;
- improved reuse of data across institutions and systems;
- less expert time spent on repetitive cleanup;
- stronger visibility into uncertain or missing data.

The near-term product impact is data quality and governance. Any downstream patient benefit would require further customer validation, clinical governance, and appropriate regulatory assessment.

## Commercial Strategy

### Phase 1 — Paid validation and services

- oncology data-quality assessments;
- harmonization and mapping projects;
- FHIR and OMOP implementation support;
- benchmark design and governance consulting;
- tightly scoped pilots with measurable workflow outcomes.

### Phase 2 — Team SaaS

- shared review queues;
- governed mapping catalogs;
- audit and quality dashboards;
- batch reconciliation;
- role-based enterprise workflows.

### Phase 3 — Enterprise platform and APIs

- reconciliation, evidence, governance, and export APIs;
- private-cloud or customer-controlled deployment;
- data-platform and laboratory integrations;
- usage-based and enterprise-contract revenue.

The services-first approach supports customer discovery and revenue before assuming product-market fit. Pilot success should be measured through review time, reconciliation coverage, error reduction, and integration effort.

## Roadmap

| Horizon | Priority |
|---|---|
| Competition final | Polish the demo, capture enterprise screenshots, export the PDF, record video, freeze validated metrics |
| Near term | Improve disease normalization, expand governed catalogs, strengthen authentication and persistence, add deployment automation |
| Pilot stage | Validate with de-identified customer data, measure curator time and agreement, add customer-specific terminology controls |
| Product stage | Multi-tenant governance, role-based access, enterprise observability, scalable terminology services, integration connectors |
| Long term | Broader oncology coverage, standards conformance testing, knowledge-graph intelligence, customer-governed learning loops |

## Standards Alignment & Reference Resources

OncoReconcile AI is designed to align with widely adopted healthcare interoperability, precision oncology, and biomedical knowledge standards. These resources inform the platform's semantic harmonization, governance, interoperability, and future expansion roadmap.

### Healthcare Interoperability

- HL7 FHIR (Fast Healthcare Interoperability Resources)
- OMOP Common Data Model (OHDSI)
- SNOMED CT
- LOINC
- RxNorm
- ICD-10-CM

### Precision Oncology & Genomics Standards

- HGNC Gene Nomenclature
- ClinVar
- ClinGen Allele Registry
- GA4GH Variant Representation Specification (VRS)
- GA4GH Categorical Variation Representation (Cat-VRS)
- GA4GH Variant Annotation Specification (VA-Spec)
- NCI Thesaurus (NCIt)
- OncoTree

### Biomedical Knowledge Sources

- CIViC (Clinical Interpretation of Variants in Cancer)
- MyGene.info
- MyVariant.info
- AACR Project GENIE
- ClinGen
- National Center for Biotechnology Information (NCBI)

### Platform Positioning

OncoReconcile AI does not replace these standards or knowledge resources. Instead, the platform provides a governance and semantic harmonization layer that helps organizations transform heterogeneous oncology data into explainable, interoperable, and AI-ready assets.

Current implementation includes selected interoperability and terminology concepts. Additional standards integration remains part of the future product roadmap.

## Repository Resources

### Primary Repository

https://github.com/oncoreconcile-ai/oncoreconcile-ai

### Submission Branch

https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

### Key Documentation

- [README](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/README.md)
- [Final Submission](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/DFWIT_Final_Submission.md)
- [Architecture](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/architecture.md)
- [Architecture Diagrams](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/architecture_diagrams.md)
- [Commercial Strategy](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/commercial_strategy.md)
- [Roadmap](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/roadmap.md)
- [Curation Methodology](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/curation_methodology.md)
- [Data Curation Pipeline](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/data_curation_pipeline.md)
- [Enterprise Patient Journey Demo](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/enterprise_patient_journey_demo.md)

### Supporting Assets

- Benchmark Evaluation Framework
- Review Queue Governance Workflow
- FHIR Export Prototype
- OMOP Export Prototype
- Knowledge Graph Export Prototype
- Enterprise Analytics Dashboard

## Team Differentiation

Variant Vanguard combines healthcare data-engineering insight, software implementation, product thinking, and a governance-first view of AI.

The project began from a domain observation: precision oncology programs do not merely need another model that produces an answer. They need a trustworthy data layer that can explain mappings, preserve uncertainty, route difficult cases to experts, and deliver standardized outputs to the rest of the enterprise.

That combination of clinical-data domain framing and working full-stack implementation is the team’s central advantage.

## Demo Video Link

**Final video:** [ADD PUBLIC OR JUDGE-ACCESSIBLE VIDEO URL]

## GitHub Repository Link

**Final branch:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

**Final submission document:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/DFWIT_Final_Submission.md

## Disclaimer

OncoReconcile AI is a prototype biomedical data harmonization, governance, interoperability, and analytics platform.

It has not been clinically validated. It is not a medical device, clinical decision support system, diagnostic system, or treatment-recommendation system. It does not provide medical advice. FHIR, OMOP, terminology, and knowledge-graph capabilities are prototype demonstrations and require implementation-specific validation before production use.

The enterprise patient journey uses entirely synthetic demonstration data. No real patient data is included.
