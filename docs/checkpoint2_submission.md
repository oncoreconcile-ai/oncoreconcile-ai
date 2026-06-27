# OncoReconcile AI

## DFWIT AI & Startup Competition 2026 – Checkpoint 2 Technical Evidence Package

### Team Variant Vanguard

**Repository:** [Checkpoint 2 competition branch](https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform)

**Primary submission:** [DFWIT_Checkpoint2_Primary_Submission.md](DFWIT_Checkpoint2_Primary_Submission.md)

**Demo Video:** [Google Drive demo video](https://drive.google.com/file/d/12k0wm4KthaTWYMj6u33mElQiiQ2KhR7p/view)

## Team Information

| Field | Information |
|---|---|
| Team Name | Variant Vanguard |
| Project | OncoReconcile AI |
| Competition | DFWIT AI & Startup Competition 2026 |
| Checkpoint | Checkpoint 2 |
| Submission Branch | `startup-platform` |

## Verification Summary

Verified June 27, 2026:

| Verification | Result |
|---|---|
| Backend test suite | 102 passed |
| Curated benchmark | 500 cases |
| Frontend production build | Passed |
| External integration tests | Passed |
| Review governance tests | Passed |
| Export tests | Passed |

Commands:

```bash
cd backend
python -m pytest -q
```

```bash
python -c "import csv; print(sum(1 for _ in csv.DictReader(open('data/benchmark_v2.csv'))))"
```

```bash
cd frontend
npm run build
```

The benchmark and test suite are internal technical validation, not independent clinical validation.

## Official Rubric Alignment

| DFWIT Judging Dimension | Evidence in This Package |
|---|---|
| Innovation, Business Value & Social Impact | Human-governed AI for precision-oncology data harmonization, with safety-first handling of ambiguity and safe failures. |
| Tech Solution, Quality & User Experience | Working backend, frontend GUI, reconciliation workflow, review queue, benchmark/evaluation dashboards, evidence display, and export prototypes. |
| Business Development | Reusable biomedical data quality layer with paths to professional services, SaaS workflow tools, and enterprise APIs. |
| Presentation | GUI supports a clear demo path across single record, CSV upload, review queue, benchmark, and evaluation tabs. |

## GUI Evidence

The current React frontend exposes five demo tabs:

- **Single Record** - manual input, featured demo, curated example cards, evidence-supported decision summary, confidence scoring, alternatives, audit trail, and standards/export actions.
- **CSV Upload** - sample CSV, downloadable demo CSV, batch upload, status summary, and expandable row-level results.
- **Review Queue** - seeded ambiguous cases, pending/reviewed filters, curator decisions, canonical edits, reopen flow, review history, and adjudication support.
- **Benchmark** - accuracy, coverage, review rate, status counts, evidence counts, review-decision counts, and benchmark-source explanation.
- **Evaluation** - visual KPI cards, charts, false auto-accept rate, reviewer agreement, and failure breakdown.

## Technical Evidence

### Reconciliation Engine

The backend implements:

- Disease, gene, and variant reconciliation
- Exact, alias, and fuzzy matching
- Ambiguity preservation
- Confidence scoring and explanations
- `AUTO_RECONCILE`, `REVIEW_REQUIRED`, and `CANNOT_RECONCILE` outcomes

Primary evidence:

- `backend/app/reconcile.py`
- `data/disease_aliases.json`
- `data/gene_aliases.json`
- `data/gene_variant_catalog.csv`
- `data/benchmark_v2.csv`
- `backend/tests/test_reconcile.py`

### External Integrations

`backend/app/external_lookup.py` implements:

| Source | Function | Behavior |
|---|---|---|
| MyVariant.info | `lookup_myvariant()` | Retrieves advisory variant evidence |
| ClinVar | `lookup_clinvar()` | Searches and summarizes ClinVar records |
| CIViC | `lookup_civic()` | Retrieves oncology variant candidates |
| ClinGen Allele Registry | `lookup_clingen_allele_registry()` | Retrieves candidate allele identifiers |

`lookup_all_external_sources()` aggregates all four connectors. `backend/app/reconcile.py` integrates the aggregator so external evidence can support review-required records.

Tests verify successful responses and graceful API failure records for every connector. External API errors preserve the local result instead of failing the complete reconciliation request.

### Governance Features

Implemented in `backend/app/main.py`, `backend/app/review_store.py`, and `backend/app/models.py`:

- File-backed persistent review queue
- Stable generated review keys
- Duplicate prevention
- Approve, reject, edit, and reopen decisions
- Curator notes and timestamps
- Chronological multi-reviewer history
- Agreement percentage
- Cohen's kappa
- Disagreement detection
- Senior-curator adjudication

Conflicting reviewer decisions mark a case as requiring adjudication. An adjudicator can record the final decision and canonical override.

Catalog promotion is represented by an explicit endpoint that returns `not_implemented`. The MVP does not automatically modify its curated catalog.

### Export and Curation Evidence

Verified endpoints:

| Endpoint | Evidence produced |
|---|---|
| `POST /export/provenance` | PROV-O-inspired provenance |
| `POST /export/knowledge-graph` | JSON-LD knowledge graph prototype |
| `POST /export/vrs-ready` | VRS-ready stub |
| `POST /export/cat-vrs-ready` | Cat-VRS-ready stub |
| `POST /export/va-spec-ready` | VA-Spec-ready stub |
| `POST /curation/report` | Reconciliation, provenance, graph, and governance summary |
| `GET /review-queue-metrics` | Agreement and adjudication metrics |
| `POST /review-queue/{case_id}/adjudicate` | Final adjudication record |

The knowledge graph export contains reconciliation activity, canonical concept, evidence, and relationship nodes. It is a JSON-LD prototype, not an official RDF, GA4GH, FHIR, or OMOP implementation.

## Validation Coverage

The 102-test backend suite covers:

- Benchmark reconciliation across 500 cases
- Alias and fuzzy normalization
- Ambiguity and cannot-reconcile behavior
- MyVariant.info integration
- ClinVar integration
- CIViC integration
- ClinGen Allele Registry integration
- External evidence routing
- Graceful API failure handling
- Persistent review queue behavior
- Stable keys and duplicate prevention
- Review reopening
- Reviewer agreement metrics
- Cohen's kappa and disagreement detection
- Adjudication
- Provenance and knowledge graph exports
- Curation metadata

## Screenshots

Current screenshot assets are stored under `docs/screenshots/`.

### Single Record Reconciliation

`docs/screenshots/02-single-record-reconciliation.png`

### Review Queue

`docs/screenshots/04-review-queue.png`

### Evaluation Dashboard

`docs/screenshots/05-evaluation-dashboard.png`

### Knowledge Graph Export

`docs/screenshots/06-knowledge-graph-export.png`

### Interactive API Documentation

`docs/screenshots/07-api-docs.png`

## Claims Boundary

Confirmed capabilities are limited to data reconciliation, advisory evidence discovery, human-governed curation, internal validation, and prototype exports.

The project does not claim:

- Clinical interpretation
- Treatment recommendations
- Autonomous clinical decision support
- Official GA4GH, FHIR, OMOP, RDF, or other standards compliance

## Related Documentation

- [MVP Product Definition](mvp.md)
- [Architecture](architecture.md)
- [Curation Methodology](curation_methodology.md)
- [Screenshot Instructions](images/README.md)
