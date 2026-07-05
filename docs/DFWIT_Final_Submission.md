# DFWIT 2026 AI & Startup Competition

# Final Submission — OncoReconcile AI

**Team:** Variant Vanguard  
**Submission branch:** `enterprise-patient-journey-demo`  
**Repository:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo  
**Demo video:** Pending final recording upload; add the public or judge-accessible URL before portal submission.

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
| Tech Solution, Quality & User Experience | 20% | Working web product, API-first architecture, 149 collected backend tests with 146 passing and 3 skipped, passing frontend build, governed export prototypes |
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


## Evidence Retrieval Architecture

The current prototype adds curated HGVS resolution, structured ClinVar retrieval, CIViC variant-record search, a unified evidence model, and a separately reported evidence-weight calculation. This section distinguishes active code paths from future extension points.

### Architecture Flow

```text
Input (Disease, Gene, Variant)
        │
        ▼
Disease Reconciliation  →  Disease Aliases + Fuzzy Matching
        │
        ▼
Gene Reconciliation  →  Gene Aliases + HGNC-inspired lookup
        │
        ▼
Variant Reconciliation  →  Variant Aliases + Gene-Variant Catalog
        │
        ▼
Canonical HGVS Generation  [IMPLEMENTED]
  ├── Protein HGVS  (p.Cys797Ser)
  ├── Coding HGVS   (c.2390G>C)
  ├── Genomic HGVS  (chr7:g.55249192G>C)
  └── VRS future fields  (vrs_id, vrs_ready — design stubs)
        │
        ▼
Evidence Retrieval Layer  [IMPLEMENTED]
  ├── ClinVar        (NCBI E-utilities, rate-limited, HGVS-first)
  ├── CIViC          (GraphQL variant search)
  ├── Local Catalog  (curated alias/harmonization evidence)
  └── MyVariant.info (live variant annotation)
        │
        ▼
Unified Evidence Model  [IMPLEMENTED]
  Common schema across all sources with deduplication, ranking,
  and source-grouped display.
        │
        ▼
Evidence Summary & Weighting  [IMPLEMENTED]
  ├── ClinVar significance / review status → evidence weight
  └── Source-specific configuration → separate breakdown
        │
        ▼
Reconciliation Response
  ├── Existing 6-signal confidence score and routing
  └── Separate evidence_score_breakdown
        │
        ▼
Frontend Evidence Tab displays HGVS, grouped evidence,
and evidence-weight details
```

### 1. Canonical HGVS Layer

The canonical HGVS resolver returns protein, coding, and genomic fields when they are available in the curated map:

- **Protein HGVS** (e.g., `p.Cys797Ser`)
- **Coding HGVS** (e.g., `c.2390G>C`)
- **Genomic HGVS** (e.g., `chr7:g.55249192G>C`)

Resolution strategy:
1. **Reference map lookup** — `hgvs_reference_map.json` contains 30 entries across 10 genes (EGFR, KRAS, BRAF, PIK3CA, TP53, ERBB2, ALK, MET, BRCA1, BRCA2)
2. **Best-effort pattern fallback** — simple protein substitutions such as `V600E` can be converted to `p.Val600Glu`; this is not a full HGVS validator
3. **VRS future fields** — each result includes `vrs_id` (null) and `vrs_ready` (false) as design stubs for future GA4GH VRS integration

The canonical HGVS is stored in reconciliation results under the `canonical_hgvs` field and is exposed via the `POST /hgvs/resolve` API endpoint.

### 2. ClinVar Integration

The `evidence_clinvar` service queries NCBI ClinVar through the E-utilities API:

- **HGVS-first strategy:** queries by protein HGVS, falls back to coding HGVS, then genomic HGVS, then gene+variant text
- **Rate-limited:** respects NCBI's 3-requests/second limit
- **Retrieves:** clinical significance description, review status, variation ID, accession (VCV), supporting submissions count
- **Confidence mapping:** practice guideline (0.95), expert panel (0.90), criteria provided (0.75–0.80), conflicting (0.50), no assertion (0.30)

The service is exposed through the `POST /evidence/federated` endpoint as part of the unified evidence pipeline.

### 3. CIViC Integration

The `evidence_civic` service queries CIViC (Clinical Interpretation of Variants in Cancer) via GraphQL:

- **Variant search:** queries CIViC's GraphQL API by gene + variant text
- **Retrieves:** variant name, CIViC variant ID, direct URL to variant record
- **Current scope:** returns variant name, CIViC variant ID, and a direct record URL with a fixed variant-match confidence
- **Not yet active:** evidence-statement details, levels, directions, therapies, diseases, and PubMed citations

The service gracefully handles API errors by returning structured error evidence items rather than failing the entire reconciliation.

### 4. Unified Evidence Model

All evidence sources share a common schema:

```json
{
  "source": "ClinVar | CIViC | Local Catalog | MyVariant.info",
  "source_label": "Human-readable display name",
  "source_badge": "Badge key for frontend",
  "variant": "Variant identifier",
  "evidence_type": "clinical_significance | predictive | variant_match",
  "summary": "Human-readable summary",
  "confidence": 0.0–1.0,
  "url": "Link to source record",
  "metadata": { "variation_id": "...", "review_status": "..." },
  "retrieval_mode": "live_clinvar_api | live_civic_api | ...",
  "timestamp": "ISO 8601"
}
```

Key capabilities:
- **Deduplication** by source + variation ID / evidence ID across all sources
- **Ranking helper** by confidence descending
- **Grouping** by source for frontend display (ClinVar, CIViC, Local Catalog, MyVariant.info)
- **Evidence weighting** computes a separate capped value and per-source breakdown

### 5. Evidence Weight Breakdown

The federation computes an `evidence_score_breakdown` alongside the existing six-signal reconciliation score:

- **ClinVar:** Pathogenic designation applies a 1.2× multiplier. Review status adds 0.08–0.15 bonus. Benign designation halves the weight.
- **CIViC configuration:** supports evidence-level, predictive, and direction weights if those metadata fields are supplied, but the current CIViC search path does not retrieve them.
- **Local Catalog configuration:** contains an AUTO_RECONCILE bonus, but normalized local evidence does not currently populate `mvp_status`.

The value is exposed for transparency. It is not currently added to `confidence_score` and does not change `AUTO_RECONCILE`, `REVIEW_REQUIRED`, or `CANNOT_RECONCILE` routing.

### 6. Frontend Evidence Tab

A new `EvidenceTab` component in `frontend/src/EvidenceTab.jsx` provides:
- **HGVS panel** displaying protein, coding, and genomic HGVS
- **Evidence boost panel** with per-source bar chart and calculation details
- **Source summary cards** with confidence mini-bars for each evidence source
- **Expandable evidence cards** grouped by source, showing metadata when a source supplies it
- **Error reporting** for any evidence source failures

The component is integrated into the reconciliation result view and batch upload results.

### 7. New API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/evidence/federated` | POST | Fetch evidence from all sources for a gene+variant |
| `/hgvs/resolve` | POST | Resolve canonical HGVS (protein/coding/genomic) |
| `/evidence/boost` | POST | Compute confidence score boost from unified evidence items |

### 8. Future Architecture (Design Only)

The following extension points are fields or commented design stubs, not working integrations in the new federation layer:

| Standard | Location | Fields / Stubs |
|---|---|---|
| GA4GH VRS | `canonical_hgvs.py` | `vrs_id` field, `vrs_ready` boolean |
| ClinGen Allele Registry | `canonical_hgvs.py` | commented `lookup_clingen_allele()` design stub |
| OncoKB | `canonical_hgvs.py`, `evidence_civic.py` | commented lookup design stubs |
| gnomAD | `canonical_hgvs.py` | commented lookup design stub |
| GA4GH Beacon | `evidence_clinvar.py` | commented query design stub |
| GA4GH Phenopackets | `evidence_clinvar.py`, `evidence_civic.py` | commented conversion design stubs |

### Local Oncology Catalogs

The primary evidence layer consists of curated local catalogs:
- **Disease-Gene Catalog:** curated disease-to-gene associations from NCCN guidelines and oncology knowledgebases
- **Gene-Variant Catalog:** structured variant aliases and synonym mappings
- **Alias Catalogs:** gene aliases and variant representations normalized from multiple sources

### Governance Integration

Evidence retrieval supports reconciliation decisions but does not independently determine outcomes:
- Local catalog matches can produce AUTO_RECONCILE results
- External evidence may identify candidate mappings routed for human review
- Review decisions incorporate evidence from all available sources
- Audit trails and provenance tracking capture which sources informed each decision

### Platform Positioning

OncoReconcile AI uses structured evidence retrieval — not a fully autonomous RAG platform. Evidence supports governance decisions; human oversight remains the final authority for uncertain cases. The platform does not make autonomous clinical decisions or treatment recommendations.

### Testing

The evidence upgrade has 22 test cases in the reconciliation test module, covering:
- Canonical HGVS resolution for EGFR C797S, BRAF V600E, KRAS G12C
- Reconcile integration ensures HGVS and unified evidence are present in response
- ClinVar service returns structured evidence with clinical significance and review status
- CIViC service returns variant matches via GraphQL
- Federated evidence endpoint returns full federation result
- Evidence deduplication across sources
- Weight configuration validation

On June 24, 2026, pytest collected 149 backend tests. The current branch passes 146 deterministic tests, with 3 live-evidence tests intentionally skipped when external network services are unavailable. The frontend production build also passes.

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

Repository validation reviewed on the `enterprise-patient-journey-demo` branch on June 24, 2026:

| Validation item | Current result |
|---|---:|
| Backend automated tests | 149 collected; 146 passing; 3 skipped |
| Frontend production build | Passing |
| Current API/test benchmark | 191 curated cases |
| Expanded benchmark dataset | 500 cases |
| Latest recorded benchmark metrics | 96.6% gene accuracy; 94.6% variant accuracy; 89.8% safety-aware status accuracy; 0% false auto-accept rate |

The benchmarks are internal engineering assets, not clinical validation studies.

## Customer Pain Points

Before OncoReconcile AI, each oncology organization independently solves the same terminology fragmentation problem, often multiple times across different projects and teams.

| Stage | Current approach | Hidden cost |
|---|---|---|
| Data ingestion | Spreadsheets, one-off scripts, manual lookup | Hours per dataset, errors from copy-paste |
| Terminology mapping | Each analyst rebuilds mappings for each project | Duplicate work, inconsistent results across teams |
| Ambiguity handling | Guesses or escalates through email | Lost context, no audit trail, delays |
| Quality validation | Manual spot-checking | Inconsistent coverage, hard to reproduce |
| Interoperability | Ad hoc FHIR/OMOP field mapping | Fragile, project-specific, hard to maintain |
| Governance | Email chains, meeting decisions, post-hoc documentation | No traceability, hard to prove compliance |

**The result:** organizations spend expert time on data plumbing instead of science, and every project starts from scratch.

## Customer Personas

| Customer | Primary pain | Value OncoReconcile provides |
|---|---|---|
| Cancer centers | Biomarker data is fragmented across EHR, laboratory, and registry systems, making cohort identification slow and unreliable | Harmonized patient data, governed review workflows, and AI-ready datasets for precision oncology programs |
| Molecular diagnostic laboratories | Variant naming inconsistencies between reporting systems, clinical databases, and research partners increase manual review | Standardized gene/variant representation, automated evidence lookup, and quality dashboards |
| CROs | Multi-site clinical trial data arrives with different terminology standards, requiring weeks of harmonization before analysis | Cross-site data standardization, governed mappings, and FHIR/OMOP-ready outputs |
| Pharmaceutical companies | Real-world evidence and biomarker programs depend on consistent terminology across data partners | Cohort analytics, RWE pipelines, clinical trial matching, and reproducible governance |
| Genomic knowledgebases | Curating public and internal variant evidence requires reconciling gene and variant names from heterogeneous sources | Normalized inputs, evidence retrieval, governed review, and audit-ready curation |
| Healthcare AI platforms | AI model training and evaluation are only as reliable as the underlying terminology mappings | Governed, provenance-tracked data with explicit uncertainty |

## Business Model

| Revenue stream | Description | Maturity |
|---|---|---|
| Professional services | Oncology data harmonization, terminology assessment, governance workflow design, FHIR/OMOP implementation support | Immediate project-based engagements |
| SaaS team workspace | Shared review queues, batch reconciliation, governed catalogs, audit dashboards, quality reporting | Near-term subscription |
| Enterprise platform | Multi-user governance, role-based access, persistent storage, enterprise analytics, API access | Medium-term custom pricing |
| Enterprise APIs | Reconciliation, evidence, governance, and export APIs for integration into customer platforms | Medium-term usage-based or contract pricing |
| Licensing and deployment | Private-cloud or customer-controlled deployment for regulated environments | Long-term enterprise agreements |

## Go-to-Market Strategy

1. **Validate with services:** data-quality assessments and harmonization projects generate revenue while building domain understanding and customer relationships.
2. **Convert to SaaS:** pilot customers transition to team subscriptions as governed workflows demonstrate measurable value.
3. **Scale through APIs:** enterprise customers integrate OncoReconcile capabilities into their own platforms, creating recurring API revenue.

## ROI Framework

OncoReconcile AI does not make unsupported numerical claims. Instead, it delivers measurable operational improvements:

| Benefit | How it creates value |
|---|---|
| Reduced manual normalization | Curated alias catalogs and automated reconciliation replace spreadsheet-based lookups |
| Standardized review workflows | Structured governance replaces email chains and undocumented decisions |
| Improved traceability | Every mapping has evidence, provenance, and audit history |
| Governed AI-ready datasets | Data quality is measured and uncertainty is explicit before data reaches analytics or AI |
| Reusable mappings | Once reconciled, a concept can be reused across downstream mappings and exports |
| Scalable enterprise curation | Human reviewers focus on ambiguous cases while routine mappings are automated |

## Competitive Differentiation

| Capability | Manual curation | Terminology mapping tools | Generic LLM assistants | OncoReconcile AI |
|---|---|---|---|---|
| Disease normalization | Manual | Yes | Inconsistent | Yes |
| Gene normalization | Manual | Partial | Inconsistent | Yes |
| Variant normalization | Manual | Partial | Inconsistent | Yes |
| Canonical HGVS | Manual lookup | No | No | Yes, curated reference map |
| Evidence retrieval | Manual search | No | Hallucination risk | Guarded MyVariant, ClinVar, CIViC, and experimental ClinGen lookup |
| Confidence scoring | Subjective | No | No | Six-signal numeric score |
| Human governance | No | No | No | Review queue, approve, reject, edit, reopen |
| Audit trail | No | No | Unreliable | Chronological, reviewer-identified history |
| Review agreement metrics | No | No | No | Agreement and Cohen's kappa metrics |
| FHIR/OMOP export | Manual mapping | No | No | Prototype exports |
| Negative-control safety testing | No | No | No | Benchmark with zero false auto-accept in latest recorded run |
| Enterprise analytics | No | No | No | Patient journey, executive, and governance views |

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

**Final video:** Pending final recording upload; add the public or judge-accessible URL before portal submission.

## GitHub Repository Link

**Final branch:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

**Final submission document:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/enterprise-patient-journey-demo/docs/DFWIT_Final_Submission.md

## Disclaimer

OncoReconcile AI is a prototype biomedical data harmonization, governance, interoperability, and analytics platform.

It has not been clinically validated. It is not a medical device, clinical decision support system, diagnostic system, or treatment-recommendation system. It does not provide medical advice. FHIR, OMOP, terminology, and knowledge-graph capabilities are prototype demonstrations and require implementation-specific validation before production use.

The enterprise patient journey uses entirely synthetic demonstration data. No real patient data is included.
