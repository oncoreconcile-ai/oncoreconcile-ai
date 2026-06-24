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
Demo video link will be added before final portal submission.

**Submission date:** July 11, 2026

</div>

<div style="page-break-after: always;"></div>

# The Opportunity

Precision oncology depends on data from electronic health records, molecular laboratories, research systems, clinical trials, and external partners. The same disease, gene, variant, treatment, or laboratory concept is frequently represented with different names and codes.

That inconsistency creates expensive manual work and weakens:

- cohort generation;
- biomarker analytics;
- longitudinal patient journeys;
- interoperability;
- real-world-data programs;
- AI training and evaluation.

**Trustworthy AI requires trustworthy data.**

OncoReconcile AI is a governed data-quality layer that converts fragmented oncology data into standardized, explainable, reviewable, and reusable information.

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

- 15 synthetic oncology patients;
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

- **FHIR R4 Bundle export:** Patient, Condition, Observation, MedicationStatement, Procedure, and Provenance resources;
- **OMOP CDM v5.4-oriented export:** condition occurrence, measurement, observation, drug exposure, and procedure occurrence records;
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

## 6. Enterprise Patient Journey

<p align="center">
  <img src="screenshots/08-patient-journey.png" alt="Enterprise Patient Journey dashboard" width="700" />
</p>
*Longitudinal oncology patient journey with diagnosis, biomarkers, treatment timeline, and semantic harmonization.*

## 7. Executive Dashboard

<p align="center">
  <img src="screenshots/09-executive-dashboard.png" alt="Executive Dashboard" width="700" />
</p>
*Executive summary with patients managed, data quality, governance score, AI readiness, and coverage scorecard.*

## 8. Coding System Alignment

<p align="center">
  <img src="screenshots/10-coding-alignment.png" alt="Coding System Alignment dashboard" width="700" />
</p>
*Semantic harmonization mappings across SNOMED CT, NCIt, HGNC, RxNorm, LOINC, ClinVar, ClinGen, and more.*

## 9. FHIR Export

<p align="center">
  <img src="screenshots/11-fhir-export.png" alt="FHIR R4 Bundle export" width="700" />
</p>
*FHIR R4 Bundle with Patient, Condition, Observation, Provenance, and DiagnosticReport resources.*

## 10. OMOP Export

<p align="center">
  <img src="screenshots/12-omop-export.png" alt="OMOP CDM v5.4 records export" width="700" />
</p>
*OMOP CDM v5.4-oriented condition_occurrence, measurement, and observation records.*

## 11. Knowledge Graph Export

<p align="center">
  <img src="screenshots/06-knowledge-graph-export.png" alt="Knowledge Graph export" width="700" />
</p>
*JSON-LD knowledge graph with disease-gene-variant-treatment-evidence relationships.*

## 12. API Documentation

<p align="center">
  <img src="screenshots/07-api-docs.png" alt="Interactive API documentation" width="700" />
</p>
*FastAPI interactive OpenAPI documentation exposing reconciliation, review, analytics, and export endpoints.*


# Validation

Validated on June 22, 2026:

| Metric | Result |
|---|---:|
| Backend tests | 127 passed |
| Frontend production build | Passing |
| Benchmark | 500 cases |
| Gene accuracy | 96.6% |
| Variant accuracy | 94.6% |
| Safety-aware status accuracy | 89.8% |
| False auto-accept rate | 0% |
| Negative-control safety rate | 100% |

The benchmark is an internal engineering evaluation, not a clinical validation study.

![Benchmark and safety evaluation dashboard](screenshots/05-evaluation-dashboard.png)

# Business Value

OncoReconcile AI targets the costly layer between raw oncology data and useful enterprise data products.

Potential customer value includes:

- less repetitive terminology cleanup;
- faster review of ambiguous records;
- reusable governed mappings;
- stronger traceability and quality reporting;
- easier preparation of analytics- and AI-ready datasets;
- reduced duplication across FHIR, OMOP, research, and warehouse projects.

# Target Customers

- cancer centers and health systems;
- molecular diagnostic laboratories;
- pharmaceutical and biotechnology companies;
- clinical research organizations;
- oncology registries and research networks;
- healthcare data and AI platforms.

# Commercial Strategy

1. **Paid services and pilots:** data-quality assessment, harmonization, governance design, FHIR/OMOP support.
2. **Team SaaS:** batch workflows, shared review queues, audit dashboards, governed catalogs.
3. **Enterprise APIs:** reconciliation, evidence, governance, exports, and customer-controlled deployment.

The services-first strategy creates early revenue and customer learning before scaling recurring software.

<div style="page-break-after: always;"></div>

# Competitive Differentiation

OncoReconcile AI does not attempt to replace authoritative biomedical terminology sources. It operationalizes them through an oncology-specific workflow that combines:

- semantic reconciliation;
- evidence and provenance;
- explicit uncertainty states;
- human governance and adjudication;
- safety-focused benchmarking;
- interoperability exports;
- enterprise patient and executive analytics;
- API-first integration.

# Social Impact

Improved oncology data quality can support more reliable research, safer healthcare AI development, more consistent biomarker analysis, and greater reuse of data across organizations.

The product’s current impact is data quality and governance. Any downstream clinical benefit requires further validation, clinical oversight, and regulatory assessment.

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
- FHIR Export Prototype
- OMOP Export Prototype
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
