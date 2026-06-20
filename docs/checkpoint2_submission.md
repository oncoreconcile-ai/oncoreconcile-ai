# OncoReconcile AI

## DFWIT AI & Startup Competition 2026 – Checkpoint 2 Technical Evidence Package

### Team Variant Vanguard

**Team Members**

- Justin (Lead)
- [NAME]
- [NAME]

**Repository:** [github.com/justin-mbca/oncoreconcile-ai](https://github.com/justin-mbca/oncoreconcile-ai)

**Demo:** [INSERT DEMO URL]

## Verification Summary

Verified June 20, 2026:

| Verification | Result |
|---|---|
| Backend test suite | 43 passed |
| Curated benchmark | 191 cases |
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
python -c "import csv; print(sum(1 for _ in csv.DictReader(open('data/benchmark_cases.csv'))))"
```

```bash
cd frontend
npm run build
```

The benchmark and test suite are internal technical validation, not independent clinical validation.

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
- `data/benchmark_cases.csv`
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

The 43-test backend suite covers:

- Benchmark reconciliation across 191 cases
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

Final screenshots should use the reserved paths below. Text placeholders remain until the competition assets are captured.

### Single Record Reconciliation

`docs/images/single_reconciliation.png`

[INSERT SCREENSHOT]

### Review Queue

`docs/images/review_queue.png`

[INSERT SCREENSHOT]

### Reviewer Agreement Metrics

`docs/images/reviewer_agreement.png`

[INSERT SCREENSHOT]

### Knowledge Graph Export

`docs/images/knowledge_graph_export.png`

[INSERT SCREENSHOT]

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
