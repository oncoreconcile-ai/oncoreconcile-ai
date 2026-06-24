# OncoReconcile AI

## One-Page Judge Pitch — Team Variant Vanguard

**OncoReconcile AI makes precision oncology data trustworthy before analytics and AI depend on it.**

### The Problem

Cancer centers, molecular laboratories, pharmaceutical teams, CROs, and healthcare data platforms receive oncology data with inconsistent disease names, gene aliases, variant formats, and coding systems.

Examples such as `HER2` versus `ERBB2`, `HER1` versus `EGFR`, or `NSCLC` versus a formal disease concept look simple one at a time. At enterprise scale, they create fragmented cohorts, manual curation, unreliable analytics, difficult interoperability, and lower-confidence AI.

### The Solution

OncoReconcile AI is an AI-powered data quality, semantic harmonization, governance, interoperability, and analytics platform for precision oncology.

It:

- normalizes disease, gene, and variant terminology;
- resolves curated protein, coding, and genomic HGVS values when available and provides a best-effort protein-substitution fallback;
- retrieves structured evidence from ClinVar (via E-utilities) and CIViC (via GraphQL);
- unifies evidence into a common schema with deduplication and source grouping;
- reports a separate evidence-weight breakdown without changing reconciliation routing;
- routes uncertainty to `REVIEW_REQUIRED` or `CANNOT_RECONCILE`;
- gives curators a governed review queue and audit history;
- maps concepts across SNOMED CT, NCIt, OncoTree, ICD-10, HGNC, RxNorm, ATC, ClinVar, ClinGen-inspired identifiers, and LOINC;
- exports FHIR, OMOP, and knowledge-graph prototypes;
- connects harmonized data to synthetic patient journeys and enterprise analytics;
- exposes an API-first architecture for integration;
- includes GA4GH VRS placeholder fields and commented extension points for future standards alignment.

### Why It Is Different

Most tools address only one part of the problem: terminology lookup, a knowledgebase, a generic AI assistant, or a manual curation workflow.

OncoReconcile AI combines the full governed data-quality loop:

**reconcile → explain → review → map → export → measure**

The platform does not hide uncertainty. Optional AI suggestions remain inside human review and cannot automatically approve an ambiguous result.

### Working Validation

| Metric | Current result |
|---|---:|
| Backend tests | 149 collected; 11 targeted HGVS/evidence tests passed |
| Frontend build | Passing |
| Current API/test benchmark | 191 curated cases |
| Expanded benchmark dataset | 500 cases |
| Full benchmark rerun | Required before submission |

These are repository and engineering validation results, not clinical validation. The full benchmark is currently network-dependent because the new federation path invokes live external evidence services.

### Business Model

1. **Paid pilots and services:** oncology harmonization, data-quality assessment, governance design, and FHIR/OMOP implementation.
2. **Team SaaS:** batch workflows, shared review queues, governed catalogs, and quality dashboards.
3. **Enterprise APIs:** reconciliation, evidence, governance, and interoperability services in customer-controlled environments.

Initial buyers include cancer centers, molecular laboratories, pharmaceutical and biotechnology companies, CROs, registries, and healthcare data platforms.

### Impact

OncoReconcile AI can reduce repetitive data cleanup, make expert review more efficient, improve dataset traceability, and create stronger foundations for research, analytics, interoperability, and safer healthcare AI development.

### The Ask

We are seeking pilot partners, oncology data collaborators, and advisors who can help validate measurable workflow value using appropriately governed, de-identified data.

**Repository:**  
https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

**Demo video:**  
Demo video link will be added before final portal submission.

*OncoReconcile AI is a prototype data harmonization and governance platform. It is not clinically validated and does not provide diagnosis, treatment recommendations, clinical decision support, or medical advice. The patient journey demonstration uses synthetic data only.*
