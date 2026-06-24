# Final Submission Repository Review

**Repository:** OncoReconcile AI  
**Branch reviewed:** `enterprise-patient-journey-demo`  
**Review date:** June 24, 2026

## Review Outcome

The final-submission documents now distinguish implemented prototype behavior from roadmap work. The canonical HGVS, ClinVar, CIViC, unified evidence, and frontend evidence features exist in code, but several draft claims were broader than the active implementation.

## Implemented and Verified in Code

- Curated HGVS resolution in `backend/app/canonical_hgvs.py`
  - 30 reference-map entries across 10 genes
  - protein, coding, and genomic fields when present in the map
  - best-effort protein-substitution fallback
  - `vrs_id` and `vrs_ready` placeholder fields
- ClinVar retrieval in `backend/app/evidence_clinvar.py`
  - NCBI E-utilities search and summary requests
  - HGVS-first fallback order
  - rate limiting and structured error results
  - clinical significance, review status, variation ID, accession, and submission-count metadata
- CIViC retrieval in `backend/app/evidence_civic.py`
  - GraphQL variant search
  - variant name, CIViC variant ID, and direct record URL
  - structured error results
- Unified evidence federation in `backend/app/evidence_unified.py`
  - common response schema
  - deduplication and grouping by source
  - separate capped evidence-weight calculation and breakdown
- API endpoints:
  - `POST /evidence/federated`
  - `POST /hgvs/resolve`
  - `POST /evidence/boost`
- Frontend evidence display in `frontend/src/EvidenceTab.jsx`, integrated into reconciliation results.
- Existing reconciliation, review queue, enterprise analytics, FHIR, OMOP, knowledge graph, provenance, and standards-stub endpoints remain present.

## Roadmap or Placeholder Functionality

- Full GA4GH VRS object generation, identifiers, validation, or compliance
- ClinGen Allele Registry integration in the new canonical-HGVS/federation layer
- OncoKB, gnomAD, GA4GH Beacon, and Phenopackets integrations
- Full HGVS validation for arbitrary substitutions, indels, fusions, copy-number changes, or transcript selection
- CIViC evidence-statement retrieval, including evidence levels, directions, therapies, diseases, and PubMed citations
- Applying the evidence-weight value to the core `confidence_score` or review-status routing

## Corrected Unsupported or Overstated Claims

| Previous claim | Repository evidence | Review action |
|---|---|---|
| “Production-ready evidence pipeline” | Working prototype with live API dependencies and incomplete extension points | Reworded as implemented prototype |
| “50+ variants across 10 genes” | `data/hgvs_reference_map.json` contains 30 entries across 10 genes | Corrected to 30 |
| CIViC retrieves evidence levels, therapies, disease, and citations | Active GraphQL path returns variant search records only | Narrowed to variant-record search |
| Evidence boost is incorporated into confidence scoring | `evidence_score_breakdown` is returned separately; `confidence_score` and routing are unchanged | Corrected throughout |
| Local catalog AUTO_RECONCILE bonus is active | Weight config exists, but normalized local evidence does not populate `mvp_status` | Described as configuration, not active behavior |
| 149 backend tests pass | 149 tests collect; 11 targeted HGVS/evidence tests passed in this review | Full-pass claim removed |
| Missing screenshots are complete | Only screenshots `01` through `07` exist | Missing references removed and checklist reset |

## Validation Performed

- `PYTHONPATH=. pytest --collect-only -q`
  - Result: 149 tests collected
- Targeted HGVS/evidence pytest selection
  - Result: 11 passed, 138 deselected
- `npm run build` from `frontend/`
  - Result: successful Vite production build
- Local asset/link check across the five synchronized documents
  - Before correction: five missing screenshot references
  - After correction: no missing local references
- Benchmark asset count
  - `data/benchmark_cases.csv`: 191 cases plus header
  - `data/benchmark_v2.csv`: 500 cases plus header

## Validation Blocker

The full backend suite and benchmark were not claimed as passing. `reconcile_record()` now always calls `fetch_federated_evidence()`, which performs live ClinVar and CIViC requests even when callers use `allow_live_lookup=False`. This makes local regression and benchmark execution slow, network-dependent, and rate-limited.

Before final submission, the implementation should provide a local/offline federation switch or mock the federation clients for regression tests. Then rerun:

```bash
cd backend
PYTHONPATH=. pytest -q
```

and the intended benchmark workflow.

## Screenshot Inventory

Verified present:

- `docs/screenshots/01-homepage.png`
- `docs/screenshots/02-single-record-reconciliation.png`
- `docs/screenshots/03-review-required.png`
- `docs/screenshots/04-review-queue.png`
- `docs/screenshots/05-evaluation-dashboard.png`
- `docs/screenshots/06-knowledge-graph-export.png`
- `docs/screenshots/07-api-docs.png`

Still required:

- Enterprise patient journey
- Executive dashboard
- Coding-system alignment
- FHIR export
- OMOP export

## Architecture Diagram Review

The architecture shown in the synchronized README and final-submission documents now matches the active evidence implementation.

`docs/architecture_diagrams.md` still needs a later dedicated update. Its “current system architecture”:

- omits the new canonical HGVS and unified federation modules;
- presents VRS, Cat-VRS, and VA-Spec alongside implemented standards exports without consistently labeling them as stubs;
- describes CIViC/ClinGen behavior more broadly than the active evidence federation;
- lists the older 191-case benchmark while other submission materials also reference the 500-case expanded dataset.

No architecture-diagram source was edited because it was outside the requested update-file list. These mismatches should be resolved before using that diagram in the final pitch deck.

## Files Synchronized

- `README.md`
- `docs/DFWIT_Final_Submission.md`
- `docs/DFWIT_Final_Submission_PDF.md`
- `docs/final_pitch_summary.md`
- `docs/final_submission_checklist.md`
- `FINAL_SUBMISSION_REVIEW.md`
