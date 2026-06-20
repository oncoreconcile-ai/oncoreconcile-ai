# OncoReconcile AI MVP

## Product Definition

OncoReconcile AI is a human-governed oncology data-quality product. It transforms inconsistent cancer-type, gene, and variant strings into canonical candidates suitable for analytics, cohort preparation, evidence aggregation, and downstream data workflows.

The product is designed for oncology data engineers, clinical-genomics analysts, molecular-pathology informatics teams, translational researchers, and other teams preparing governed oncology datasets.

### Product Principles

- Prefer deterministic reconciliation before probabilistic assistance.
- Preserve ambiguity instead of forcing a specific mapping.
- Treat external evidence as advisory context.
- Keep human reviewers accountable for uncertain decisions.
- Preserve evidence, provenance, and decision history.

### Inputs and Outputs

Inputs:

- Required: `gene`, `variant`
- Optional: `cancer_type`, `case_id`

Outputs include:

- Canonical disease, gene, and variant candidates
- Evidence records and alternatives
- Confidence score and score breakdown
- Deterministic explanation
- Review status
- Audit trail and curation metadata

Every record receives one status:

| Status | Product behavior |
|---|---|
| `AUTO_RECONCILE` | High-confidence local reconciliation |
| `REVIEW_REQUIRED` | Ambiguous or evidence-supported candidate requiring review |
| `CANNOT_RECONCILE` | No reliable candidate found |

## Workflow

```text
Oncology record
  ↓
Disease normalization
  ↓
Gene normalization
  ↓
Variant normalization
  ↓
Local catalog and ambiguity checks
  ↓
External evidence retrieval when needed
  ↓
Confidence scoring and explanation
  ↓
Review recommendation
  ↓
Human review, agreement measurement, and adjudication
  ↓
Governed output and exports
```

Automatic results rely on local reconciliation rules. External API evidence can support candidate discovery and route a record to review, but it does not independently produce `AUTO_RECONCILE`.

## Product Features

### Reconciliation and Explainability

- Disease, gene, and variant reconciliation
- Exact and alias matching
- Fuzzy matching with safeguards for precise variants
- Categorical ambiguity preservation
- Alternatives considered
- Confidence scoring
- Deterministic explanations
- Audit trails
- Batch and CSV workflows

### Evidence

- Local alias, disease-gene, and variant catalogs
- MyVariant.info integration
- ClinVar integration
- CIViC integration
- ClinGen Allele Registry integration
- Graceful source-specific error handling

### Human Governance

- Persistent review queue
- Stable review keys and duplicate prevention
- Approve, reject, edit, and reopen actions
- Curator notes and chronological review history
- Reviewer agreement metrics
- Cohen's kappa
- Disagreement detection
- Senior-curator adjudication workflow

Catalog promotion remains an explicit disabled MVP control; reviewed records do not automatically modify the curated catalog.

### Exports

- PROV-O-inspired provenance export
- JSON-LD knowledge graph export
- Curation report
- VRS-ready export stub
- Cat-VRS-ready export stub
- VA-Spec-ready export stub

## Validation

The current MVP has:

- **43 passing backend tests**
- **191 curated benchmark cases**
- A passing frontend production build

The benchmark covers automatic reconciliation, ambiguous terminology, review-required candidates, cannot-reconcile cases, external evidence behavior, governance workflows, and exports. It is an internal product benchmark rather than independent clinical validation.

Detailed test and endpoint evidence is maintained in the [Checkpoint 2 technical package](checkpoint2_submission.md).

## Standards Alignment

The MVP is influenced by:

- GA4GH VRS and Cat-VRS representation concepts
- VA-Spec evidence concepts
- PROV-O provenance concepts
- JSON-LD graph representation

Current exports are standards-inspired prototypes or stubs. The project does not claim official GA4GH, RDF, FHIR, or OMOP compliance.

The product addresses data harmonization and curation. It does not provide clinical interpretation, treatment recommendations, or autonomous clinical decision support.

## Roadmap

- Expand benchmark coverage and independent validation
- Rank evidence quality across sources
- Add coordinated multi-source evidence agents
- Develop a reviewer copilot
- Add governed, versioned catalog promotion
- Support FHIR Genomics interoperability
- Support OMOP Oncology interoperability
- Generate standards-compliant genomic representations
