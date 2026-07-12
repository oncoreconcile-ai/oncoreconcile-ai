<div align="center">

<p align="center">
  <img src="images/oncoreconcile_logo.png" alt="OncoReconcile AI / Variant Vanguard logo" width="520" />
</p>

# OncoReconcile AI

## AI-Powered Precision Oncology Data Quality, Semantic Harmonization, Governance, Interoperability & Analytics

### DFWIT 2026 AI & Startup Competition — Final Submission

**Team Variant Vanguard**

**Final branch:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

**Demo video:**  
https://drive.google.com/file/d/1YKf1d22VhIZ5ue-pHQKTllWpvWo5zt9S/view

**Submission date:** July 12, 2026

</div>

<div style="page-break-after: always;"></div>

# The Problem: Fragmented Oncology Data

Precision oncology depends on data from electronic health records, molecular laboratories, research systems, clinical trials, and external partners. The same disease, gene, variant, treatment, or laboratory concept is frequently represented with different names and codes.

**A real example:** one laboratory reports `HER2`, another reports `HER-2`, a third reports `ERBB2`, and a claims system records `V-erb-b2`. A researcher trying to identify all ERBB2-altered patients must manually reconcile these representations — every time, for every project.

This fragmentation creates expensive, repetitive work:

| Impact | Real-world consequence |
|---|---|
| Manual curation | Experts spend weeks cleaning and mapping data instead of analyzing it |
| Fragmented cohorts | Patient populations are split across terminologies, hiding signal |
| Inconsistent analytics | Biomarker trends, outcome analyses, and AI inputs depend on how terminology was mapped |
| Interoperability gaps | FHIR, OMOP, and research exports use different coding systems that are not aligned |
| Safety risk | Forced automatic mappings disguise uncertainty — bad data becomes harder to detect downstream |

**Trustworthy AI requires trustworthy data.** Poorly harmonized data produces unreliable analytics, reduces confidence in AI outputs, and slows precision medicine adoption.

OncoReconcile AI is a governed data-quality layer that converts fragmented oncology data into standardized, explainable, reviewable, and reusable information — before it reaches analytics, AI, or interoperability pipelines.

# The Product

```text
Raw oncology data
      ↓
Semantic normalization
      ↓
Disease / gene / variant reconciliation
      ↓
Evidence + confidence scoring
      ↓
AUTO_RECONCILE | REVIEW_REQUIRED | CANNOT_RECONCILE
      ↓
Human governance and audit history
      ↓
Coding-system mapping
      ↓
FHIR | OMOP | Knowledge Graph
      ↓
Enterprise analytics and AI-ready datasets
```

The product combines:

- disease, gene, and variant normalization;
- evidence packages and transparent score breakdowns;
- a governed review queue and adjudication history;
- optional LLM suggestions restricted to review-required cases;
- semantic mappings across oncology coding systems;
- synthetic longitudinal patient journeys;
- enterprise, governance, and executive analytics;
- FHIR R4, OMOP CDM v5.4, and knowledge-graph export prototypes;
- interactive APIs and benchmark evaluation.

![Platform homepage](screenshots/01-homepage.png)

<div style="page-break-after: always;"></div>

# Working Reconciliation & Evidence

A user submits a disease, gene, and variant record. The platform:

1. normalizes the raw text;
2. checks governed aliases and catalogs;
3. retrieves supporting context and evidence;
4. calculates a confidence score;
5. assigns a safety-aware status;
6. presents evidence, alternatives, notes, and an audit trail;
7. exports the governed result through standards-oriented formats.

![High-confidence reconciliation with evidence](screenshots/02-single-record-reconciliation.png)

# Human-Governed AI

The platform does not force an answer when evidence is incomplete.

| Status | Meaning |
|---|---|
| `AUTO_RECONCILE` | Evidence supports a high-confidence canonical mapping |
| `REVIEW_REQUIRED` | A plausible mapping exists, but a person must decide |
| `CANNOT_RECONCILE` | No sufficiently trustworthy mapping is available |

Optional LLM assistance is model-agnostic and restricted to review suggestions. It cannot silently promote an uncertain case to automatic acceptance.

![Ambiguous case routed to human review](screenshots/03-review-required.png)

![Review queue and curator workflow](screenshots/04-review-queue.png)

<div style="page-break-after: always;"></div>

# Enterprise Patient Journey

The enterprise demonstration expands the reconciliation workflow into longitudinal analytics:

- 18 synthetic oncology patients;
- NSCLC, breast cancer, colorectal cancer, melanoma, and AML;
- diagnosis, histology, stage, biomarkers, genomic alterations, treatment lines, response, progression, trial flags, and governance signals;
- patient, cohort, terminology, quality, governance, and executive views;
- expanded FHIR, OMOP, and knowledge-graph exports.

All patient journey data is synthetic and used only for product demonstration.

# Semantic Harmonization

| Domain | Demonstrated coding systems |
|---|---|
| Disease | SNOMED CT, NCIt, OncoTree, ICD-10 |
| Histology | SNOMED CT, NCIt |
| Gene | HGNC |
| Drug | RxNorm, ATC |
| Variant / biomarker | ClinVar, ClinGen-inspired identifiers |
| Laboratory test | LOINC |

Mappings retain source, confidence, and review status. These are prototype mappings, not a complete certified terminology service.

# Interoperability

The platform demonstrates:

- **FHIR R4 Bundle export:** Patient, Condition, Observation, MedicationStatement, and Provenance resources;
- **OMOP CDM v5.4-oriented export:** condition occurrence, measurement, observation, and drug exposure records;
- **knowledge graph export:** disease-gene-variant-treatment-evidence relationships;
- **API-first integration:** FastAPI endpoints and interactive OpenAPI documentation.

![Knowledge graph export](screenshots/06-knowledge-graph-export.png)

![Interactive API documentation](screenshots/07-api-docs.png)

<div style="page-break-after: always;"></div>


<div style="page-break-before: always;"></div>

# Final Demo Screenshots

The following screenshots demonstrate the complete OncoReconcile AI enterprise platform workflow.

## 1. Homepage

<p align="center">
  <img src="screenshots/01-homepage.png" alt="Platform homepage with reconciliation entry" width="700" />
</p>
*Homepage showing the Single Record Reconciliation interface, featured demo, and manual input form.*

## 2. Single Record Reconciliation

<p align="center">
  <img src="screenshots/02-single-record-reconciliation.png" alt="High-confidence reconciliation with evidence" width="700" />
</p>
*Evidence-supported reconciliation result showing canonical values, confidence score, evidence sources, and audit trail.*

## 3. Review Required Case

<p align="center">
  <img src="screenshots/03-review-required.png" alt="Ambiguous case routed to human review" width="700" />
</p>
*Cat-VRS-style ambiguity (TRK fusion) preserved for accountable human review.*

## 4. Review Queue

<p align="center">
  <img src="screenshots/04-review-queue.png" alt="Review queue and curator workflow" width="700" />
</p>
*Governed review queue with decision controls, alternatives, evidence, and audit history.*

## 5. Evaluation Dashboard

<p align="center">
  <img src="screenshots/05-evaluation-dashboard.png" alt="Benchmark and safety evaluation dashboard" width="700" />
</p>
*Benchmark validation metrics, accuracy and coverage gauges, failure analysis, and reviewer agreement.*

## 6. Knowledge Graph Export

<p align="center">
  <img src="screenshots/06-knowledge-graph-export.png" alt="Knowledge Graph export" width="700" />
</p>
*JSON-LD knowledge graph with disease-gene-variant-treatment-evidence relationships.*

## 7. API Documentation

<p align="center">
  <img src="screenshots/07-api-docs.png" alt="Interactive API documentation" width="700" />
</p>
*FastAPI interactive OpenAPI documentation exposing reconciliation, review, analytics, and export endpoints.*

## 8. Enterprise Patient Journey

![Enterprise patient journey timeline with biomarker and treatment history](screenshots/08-enterprise-patient-journey.png){ width=700px }
*Longitudinal patient journey view showing diagnosis, biomarkers, copy-number alterations, treatment timeline, review status, and quality indicators.*

## 9. Executive Dashboard

![Executive dashboard with platform coverage and readiness metrics](screenshots/09-executive-dashboard.png){ width=700px }
*Enterprise dashboard summarizing patients managed, data quality, governance, AI readiness, reconciliation coverage, evidence coverage, and semantic harmonization.*

## 10. Coding System Alignment

![Coding system alignment dashboard with semantic harmonization mappings](screenshots/10-coding-alignment.png){ width=700px }
*Semantic interoperability dashboard showing coding-system coverage, canonical mappings, terminology examples, and complete mapping coverage.*


# Evidence Retrieval Architecture

The current prototype adds curated HGVS resolution, structured ClinVar retrieval, CIViC variant-record search, a unified evidence model, and a separately reported evidence-weight calculation.

## Architecture

```text
Input (Disease, Gene, Variant)
        │
        ▼
Disease Reconciliation
        │
        ▼
Gene Reconciliation
        │
        ▼
Variant Reconciliation
        │
        ▼
Canonical HGVS Generation  [IMPLEMENTED]
  ├── Protein HGVS (p.Cys797Ser)
  ├── Coding HGVS  (c.2390G>C)
  ├── Genomic HGVS (chr7:g.55249192G>C)
  └── VRS future fields (vrs_id, vrs_ready — design stubs)
        │
        ▼
Evidence Retrieval Layer  [IMPLEMENTED]
  ├── ClinVar        (NCBI E-utilities, HGVS-first)
  ├── CIViC          (GraphQL variant search)
  ├── Local Catalog  (curated alias evidence)
  └── MyVariant.info (live variant annotation)
        │
        ▼
Unified Evidence Model  [IMPLEMENTED]
  Deduplication, ranking, source-grouped display
        │
        ▼
Evidence Summary & Weighting  [IMPLEMENTED]
  ClinVar metadata and source configuration → separate breakdown
        │
        ▼
Existing Confidence Score + Separate Evidence Breakdown
```

## Canonical HGVS

The resolver returns protein, coding, and genomic HGVS fields when present in a curated map of 30 entries across 10 genes. A best-effort pattern fallback handles simple protein substitutions but is not a full HGVS validator. Each result includes `vrs_id` and `vrs_ready` fields as GA4GH VRS placeholders.

## ClinVar Integration

The `evidence_clinvar` service queries NCBI ClinVar via E-utilities using HGVS-first strategy with rate-limiting (3 req/s). Retrieves clinical significance, review status, variation ID, accession, and submission count. Confidence is mapped from review status (practice guideline → 0.95, expert panel → 0.90, etc.).

## CIViC Integration

The `evidence_civic` service queries CIViC via GraphQL variant search and returns variant name, CIViC variant ID, and a direct record URL. Evidence statements, levels, therapies, diseases, and citations are not yet retrieved by the active path.

## Unified Evidence Model

Evidence sources share a common schema with deduplication and source grouping for frontend display. A capped evidence-weight value and breakdown are returned separately; they do not currently change the core confidence score or reconciliation routing.

## New API Endpoints

| Endpoint | Description |
|---|---|
| `POST /evidence/federated` | Fetch all-source evidence for a gene+variant |
| `POST /hgvs/resolve` | Resolve canonical HGVS |
| `POST /evidence/boost` | Compute confidence score boost |

## Future Architecture (Design Only)

Interface stubs exist for: GA4GH VRS (`vrs_id`, `vrs_ready`), ClinGen Allele Registry, OncoKB, gnomAD, GA4GH Beacon, GA4GH Phenopackets. No implementation has been started.

## Testing

The evidence upgrade is covered by the reconciliation test module. On June 24, 2026, pytest collected 149 backend tests; 146 pass deterministically and 3 live-evidence tests are intentionally skipped when external network services are unavailable.

# Validation

Reviewed on June 24, 2026:

| Metric | Result |
|---|---:|
| Backend tests | 149 collected; 146 passing; 3 skipped |
| Frontend production build | Passing |
| Current API/test benchmark | 191 curated cases |
| Expanded benchmark dataset | 500 cases |
| Latest recorded benchmark metrics | 96.6% gene accuracy; 94.6% variant accuracy; 89.8% safety-aware status accuracy; 0% false auto-accept rate |

The benchmark assets are internal engineering evaluation materials, not clinical validation studies.

![Benchmark and safety evaluation dashboard](screenshots/05-evaluation-dashboard.png)

# Customer Pain Points

Before OncoReconcile AI, each oncology organization independently solves the same terminology fragmentation problem — often multiple times across different projects and teams.

| Stage | Current approach | Hidden cost |
|---|---|---|
| Data ingestion | Spreadsheets, one-off scripts, manual lookup | Hours per dataset, errors from copy-paste |
| Terminology mapping | Each analyst rebuilds mappings for each project | Duplicate work, inconsistent results across teams |
| Ambiguity handling | Guesses or escalates through email | Lost context, no audit trail, delays |
| Quality validation | Manual spot-checking | Inconsistent coverage, hard to reproduce |
| Interoperability | Ad hoc FHIR/OMOP field mapping | Fragile, project-specific, hard to maintain |
| Governance | Email chains, meeting decisions, post-hoc documentation | No traceability, hard to prove compliance |

**The result:** organizations spend expert time on data plumbing instead of science, and every project starts from scratch.

# Customer Personas

| Customer | Primary Pain | Value OncoReconcile Provides |
|---|---|---|
| **Cancer Centers** | Biomarker data is fragmented across EHR, laboratory, and registry systems, making cohort identification slow and unreliable | Harmonized patient data, governed review workflows, and AI-ready datasets for precision oncology programs |
| **Molecular Diagnostic Laboratories** | Variant naming inconsistencies between reporting systems, clinical databases, and research partners increase manual review | Standardized gene/variant representation, automated evidence lookup, and quality dashboards |
| **CROs** | Multi-site clinical trial data arrives with different terminology standards, requiring weeks of harmonization before analysis | Cross-site data standardization, governed mappings, and FHIR/OMOP-ready outputs |
| **Pharmaceutical Companies** | Real-world evidence and biomarker programs depend on consistent terminology across data partners that may use different coding systems | Cohort analytics, RWE pipelines, clinical trial matching, and reproducible governance |
| **Genomic Knowledgebases** | Curating public and internal variant evidence requires reconciling gene and variant names from heterogeneous sources | Normalized inputs, evidence retrieval, governed review, and audit-ready curation |
| **Healthcare AI Platforms** | AI model training and evaluation are only as reliable as the underlying terminology mappings | Governed, provenance-tracked data with explicit uncertainty — trustworthy AI starts with trustworthy data |

# Business Model

| Revenue stream | Description | Maturity |
|---|---|---|
| **Professional Services** | Oncology data harmonization, terminology assessment, governance workflow design, FHIR/OMOP implementation support | Immediate — project-based engagements |
| **SaaS — Team** | Shared review queues, batch reconciliation, governed catalogs, audit dashboards, quality reporting | Near-term — subscription pricing |
| **SaaS — Enterprise** | Multi-user governance, role-based access, persistent storage, enterprise analytics, API access | Medium-term — custom pricing |
| **Enterprise APIs** | Reconciliation, evidence, governance, and export APIs for integration into customer platforms | Medium-term — usage-based or contract |
| **Licensing & Deployment** | Private-cloud or customer-controlled deployment for regulated environments | Long-term — enterprise agreements |

## Go-to-Market Strategy

1. **Validate with services** — data-quality assessments and harmonization projects generate revenue while building domain understanding and customer relationships.
2. **Convert to SaaS** — pilot customers transition to team subscriptions as governed workflows demonstrate measurable value.
3. **Scale through APIs** — enterprise customers integrate OncoReconcile capabilities into their own platforms, creating recurring API revenue.

## ROI Framework

OncoReconcile AI does not make unsupported numerical claims. Instead, it delivers measurable operational improvements:

| Benefit | How it creates value |
|---|---|
| **Reduced manual normalization** | Curated alias catalogs and automated reconciliation replace spreadsheet-based lookups |
| **Standardized review workflows** | Structured governance replaces email chains and undocumented decisions |
| **Improved traceability** | Every mapping has evidence, provenance, and audit history — reproducible and defensible |
| **Governed AI-ready datasets** | Data quality is measured and uncertainty is explicit before data reaches analytics or AI |
| **Reusable mappings** | Once reconciled, a concept is mapped across all coding systems — not rebuilt for each project |
| **Scalable enterprise curation** | Human reviewers focus on ambiguous cases while routine mappings are automated |

<div style="page-break-after: always;"></div>

# Competitive Differentiation

## How OncoReconcile AI compares

| Capability | Manual Curation | Terminology Mapping Tools | Generic LLM Assistants | **OncoReconcile AI** |
|---|---|---|---|---|
| Disease normalization | Manual | ✓ | Inconsistent | ✓ |
| Gene normalization | Manual | Partial | Inconsistent | ✓ |
| Variant normalization | Manual | Partial | Inconsistent | ✓ |
| Canonical HGVS | Manual lookup | ✗ | ✗ | ✓ (30 curated entries) |
| Evidence retrieval | Manual search | ✗ | Hallucination risk | ✓ (guarded MyVariant, ClinVar, CIViC, and experimental ClinGen lookup) |
| Confidence scoring | Subjective | ✗ | ✗ | ✓ (6-signal numeric score) |
| Human governance | ✗ | ✗ | ✗ | ✓ (review queue, approve/reject/edit/reopen) |
| Audit trail | ✗ | ✗ | Unreliable | ✓ (chronological, reviewer-identified) |
| Review agreement metrics | ✗ | ✗ | ✗ | ✓ (Cohen's kappa, adjudication) |
| Knowledge graph | ✗ | ✗ | Unreliable | ✓ (JSON-LD, disease-gene-variant-evidence) |
| FHIR export | Manual mapping | ✗ | ✗ | ✓ (R4 Bundle prototype) |
| OMOP export | Manual mapping | ✗ | ✗ | ✓ (CDM v5.4-oriented prototype) |
| Categorical ambiguity preservation | ✗ | ✗ | ✗ | ✓ (Cat-VRS-inspired) |
| Negative control safety testing | ✗ | ✗ | ✗ | ✓ (benchmark with 0% false auto-accept) |
| Enterprise analytics | ✗ | ✗ | ✗ | ✓ (patient journey, executive, governance) |

**The key difference:** OncoReconcile AI combines all of these capabilities in an oncology-specific, governance-first platform. It is not a terminology tool, not a knowledgebase, and not a generic AI — it is a governed data-quality layer for precision oncology.

## Why This Combination Matters

- **Manual curation** is slow, inconsistent, and does not scale.
- **Terminology mapping tools** resolve codes but do not handle variant normalization, evidence, or governance.
- **Generic LLM assistants** hallucinate, lack provenance, and cannot be trusted for regulated data.
- **OncoReconcile AI** provides deterministic reconciliation where possible, evidence-supported review where needed, and human governance everywhere.

<div style="page-break-after: always;"></div>

# Social Impact

| Impact | How OncoReconcile AI contributes |
|---|---|
| **Higher-quality oncology data** | Standardized terminology reduces errors, fragmentation, and ambiguity in datasets used for research and analytics |
| **Reproducible research** | Governed mappings with audit trails mean every data transformation can be traced, validated, and reproduced |
| **Trustworthy AI development** | AI models trained on governed, provenance-tracked data with explicit uncertainty markers are safer and more transparent |
| **Reduced repetitive work** | Automation of routine normalization frees expert curators to focus on ambiguous cases and higher-value analysis |
| **Human accountability** | The governance model ensures human experts remain in the loop for uncertain decisions — AI assists, humans decide |
| **Interoperability for better care** | Standardized data across institutions supports larger, more diverse research cohorts and more robust evidence generation |

OncoReconcile AI is a data-quality and governance platform. It does not make clinical decisions, provide treatment recommendations, or replace clinical judgment. Its impact is enabling better, more trustworthy data — which is a prerequisite for safer AI and more reliable research in precision oncology.

# Team

Variant Vanguard combines healthcare data-engineering insight, software development, product strategy, and a governance-first AI philosophy.

The team’s core insight is simple: oncology organizations do not only need a model that produces an answer. They need a data-quality platform that can explain the answer, preserve uncertainty, route difficult cases to experts, and integrate governed results across the enterprise.

# Roadmap

- improve disease normalization and governed catalog coverage;
- validate workflow value with de-identified pilot data;
- add authentication, persistent enterprise storage, and role-based access;
- measure curator time, review agreement, and correction rates;
- expand integration and standards-conformance testing;
- scale into a customer-controlled oncology data-quality platform.

# Standards Alignment & Reference Resources

OncoReconcile AI is designed to align with widely adopted healthcare interoperability, precision oncology, and biomedical knowledge standards. These resources inform the platform's semantic harmonization, governance, interoperability, and future expansion roadmap.

## Healthcare Interoperability

- HL7 FHIR (Fast Healthcare Interoperability Resources)
- OMOP Common Data Model (OHDSI)
- SNOMED CT
- LOINC
- RxNorm
- ICD-10-CM

## Precision Oncology & Genomics Standards

- HGNC Gene Nomenclature
- ClinVar
- ClinGen Allele Registry
- GA4GH Variant Representation Specification (VRS)
- GA4GH Categorical Variation Representation (Cat-VRS)
- GA4GH Variant Annotation Specification (VA-Spec)
- NCI Thesaurus (NCIt)
- OncoTree

## Biomedical Knowledge Sources

- CIViC (Clinical Interpretation of Variants in Cancer)
- MyGene.info
- MyVariant.info
- AACR Project GENIE
- ClinGen
- National Center for Biotechnology Information (NCBI)

## Platform Positioning

OncoReconcile AI does not replace these standards or knowledge resources. Instead, the platform provides a governance and semantic harmonization layer that helps organizations transform heterogeneous oncology data into explainable, interoperable, and AI-ready assets.

Current implementation includes selected interoperability and terminology concepts. Additional standards integration remains part of the future product roadmap.

# Repository Resources

## Primary Repository

https://github.com/oncoreconcile-ai/oncoreconcile-ai

## Submission Branch

https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

## Key Documentation

- [README](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/README.md)
- [Final Submission](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/DFWIT_Final_Submission.md)
- [Architecture](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/architecture.md)
- [Architecture Diagrams](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/architecture_diagrams.md)
- [Commercial Strategy](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/commercial_strategy.md)
- [Roadmap](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/roadmap.md)
- [Curation Methodology](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/curation_methodology.md)
- [Data Curation Pipeline](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/data_curation_pipeline.md)
- [Enterprise Patient Journey Demo](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/enterprise_patient_journey_demo.md)

## Supporting Assets

- Benchmark Evaluation Framework
- Review Queue Governance Workflow
- [Prepared FHIR Demo Export](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/demo_exports/oncoreconcile-fhir-PT-DEMO-001.json)
- [Prepared OMOP Demo Export](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/demo_exports/oncoreconcile-omop-PT-DEMO-001.json)
- [Demo Export Documentation](https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/demo_exports/README.md)
- Knowledge Graph Export Prototype
- Enterprise Analytics Dashboard

# Links

**Repository:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

**Final submission:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/DFWIT_Final_Submission.md

**Architecture:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/architecture.md

**Enterprise demo documentation:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/enterprise_patient_journey_demo.md

**Official DFWIT rules:**  
https://ai.dfwit.org/Rules

# Disclaimer

OncoReconcile AI is a prototype biomedical data harmonization, governance, interoperability, and analytics platform. It has not been clinically validated. It is not a medical device, clinical decision support system, diagnostic system, or treatment-recommendation system and does not provide medical advice.

FHIR, OMOP, terminology, and knowledge-graph capabilities are prototypes requiring implementation-specific validation before production use. The enterprise patient journey uses entirely synthetic data; no real patient data is included.

<div style="page-break-before: always;"></div>

# Appendix A – Standards & Reference Resources

OncoReconcile AI is designed to work alongside widely adopted healthcare interoperability, precision oncology, terminology, and biomedical knowledge resources.

## Healthcare Interoperability

- HL7 FHIR (Fast Healthcare Interoperability Resources)
- OMOP Common Data Model (OHDSI)
- SNOMED CT
- LOINC
- RxNorm
- ICD-10-CM

## Precision Oncology & Genomics Standards

- HGNC Gene Nomenclature
- ClinVar
- ClinGen Allele Registry
- GA4GH Variant Representation Specification (VRS)
- GA4GH Categorical Variation Representation (Cat-VRS)
- GA4GH Variant Annotation Specification (VA-Spec)
- NCI Thesaurus (NCIt)
- OncoTree

## Biomedical Knowledge Sources

- CIViC (Clinical Interpretation of Variants in Cancer)
- MyGene.info
- MyVariant.info
- AACR Project GENIE
- ClinGen
- National Center for Biotechnology Information (NCBI)

## Enterprise Positioning

OncoReconcile AI does not replace these standards or knowledge resources. It provides the governance, semantic harmonization, evidence, and workflow layer needed to apply them to heterogeneous oncology data and produce explainable, interoperable, and AI-ready assets.

Current implementation demonstrates selected terminology and interoperability concepts. Broader standards integration and conformance testing remain part of the product roadmap.
