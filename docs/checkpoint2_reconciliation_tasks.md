# Checkpoint 2 Reconciliation Workflow Tasks

## Current Baseline

Input data is fixed for Checkpoint 2.

Active data files:

- `data/disease_aliases.json`
- `data/gene_aliases.json`
- `data/gene_variant_catalog.csv`
- `data/disease_gene_catalog.csv`
- `data/benchmark_cases.csv`

Current backend status:

- `/reconcile` works for single records.
- `/reconcile/batch` works for basic batch requests.
- Backend tests validate the 156-case benchmark.
- Generic `TRK` routes to `REVIEW_REQUIRED`.

Checkpoint 2 focus:

Move from a single-record reconciliation demo to a practical reconciliation workflow with batch processing, review queue, explainability, auditability, and validation reporting.

## Workstream 1: Backend Reconciliation Contract

Owner: Backend

Goal: Make each reconciliation result clear, traceable, and easy for the frontend to render.

Tasks:

- [ ] Add a `decision` object to reconciliation responses.
- [ ] Include `matched_by` values such as `disease_alias`, `gene_alias`, `variant_catalog`, `review_required_rule`, and `cannot_reconcile_rule`.
- [ ] Include `decision_reason` as a short deterministic reason for the final status.
- [ ] Include `requires_review_reason` when `review_status` is `REVIEW_REQUIRED`.
- [ ] Include `catalog_source` or `catalog_row` metadata when a variant catalog row is used.
- [ ] Make sure all response fields are present for `AUTO_RECONCILE`, `REVIEW_REQUIRED`, and `CANNOT_RECONCILE`.
- [ ] Update `backend/app/models.py` to define the new response fields.
- [ ] Update `backend/tests/test_reconcile.py` to validate the new fields.

Acceptance criteria:

- [ ] Single-record API still passes all existing benchmark tests.
- [ ] Every response explains why the final status was chosen.
- [ ] Frontend can render result status without reverse-engineering backend logic.

## Workstream 2: Batch Reconciliation API

Owner: Backend

Goal: Make `/reconcile/batch` production-like enough for CSV workflows.

Tasks:

- [ ] Add row-level `row_id` or preserve input `case_id` in all batch results.
- [ ] Add row-level error handling for invalid records.
- [ ] Do not fail the entire batch when one row is invalid.
- [ ] Add batch summary fields:
  - `total_records`
  - `auto_reconcile`
  - `review_required`
  - `cannot_reconcile`
  - `invalid_records`
- [ ] Add tests for mixed valid and invalid batch input.
- [ ] Add tests for empty batch input.
- [ ] Add tests for duplicate input rows.

Acceptance criteria:

- [ ] `/reconcile/batch` returns a result or error object for every input row.
- [ ] Batch summary counts always equal total submitted rows.
- [ ] Invalid rows are visible to the frontend and do not crash the request.

## Workstream 3: Benchmark Evaluation Script

Owner: Backend / QA

Goal: Produce a clear validation report from fixed benchmark data.

Tasks:

- [ ] Create `scripts/evaluate_benchmark.py`.
- [ ] Load `data/benchmark_cases.csv`.
- [ ] Run every benchmark row through `reconcile_record()`.
- [ ] Report:
  - total cases
  - disease accuracy
  - gene accuracy
  - variant accuracy
  - status accuracy
  - exact full-row accuracy
- [ ] Print failed cases with expected vs actual outputs.
- [ ] Optionally write `data/benchmark_results.csv`.
- [ ] Add a short README command for running evaluation.

Acceptance criteria:

- [ ] One command generates a benchmark report.
- [ ] Failed cases are easy to inspect.
- [ ] Report can be used in final submission evidence.

## Workstream 4: Frontend Batch Upload

Owner: Frontend

Goal: Let users upload multiple records and see reconciliation results.

Tasks:

- [ ] Add CSV upload control.
- [ ] Support required columns:
  - `case_id`
  - `cancer_type`
  - `gene`
  - `variant`
- [ ] Parse CSV rows in the frontend.
- [ ] Send parsed rows to `/reconcile/batch`.
- [ ] Show upload validation errors before submitting.
- [ ] Show batch summary after reconciliation.
- [ ] Render a results table with one row per input.

Acceptance criteria:

- [ ] User can upload a CSV and reconcile all rows.
- [ ] User can see summary counts.
- [ ] User can identify which rows need review.

## Workstream 5: Results Table And Filters

Owner: Frontend

Goal: Make reconciliation results easy to review.

Tasks:

- [ ] Add table columns:
  - input disease
  - input gene
  - input variant
  - canonical disease
  - canonical gene
  - canonical variant
  - confidence
  - review status
  - decision reason
- [ ] Add filters:
  - all
  - `AUTO_RECONCILE`
  - `REVIEW_REQUIRED`
  - `CANNOT_RECONCILE`
  - invalid rows
- [ ] Add search by case ID, gene, variant, or status.
- [ ] Add row expansion for evidence, notes, and audit trail.
- [ ] Add status badges with consistent colors.

Acceptance criteria:

- [ ] Reviewer can quickly find all `REVIEW_REQUIRED` rows.
- [ ] Reviewer can inspect evidence without leaving the table.
- [ ] Table remains readable for at least 100 rows.

## Workstream 6: Human Review Queue

Owner: Frontend + Backend

Goal: Support a realistic review workflow for uncertain records.

Tasks:

- [ ] Add a review-only view filtered to `REVIEW_REQUIRED`.
- [ ] Add reviewer action options:
  - approve suggested canonical values
  - modify canonical gene
  - modify canonical variant
  - mark cannot reconcile
  - add reviewer note
- [ ] Store review decisions locally first, either in frontend state or local storage.
- [ ] Add an export format that includes reviewer decisions.
- [ ] Add backend persistence later only if needed for final delivery.

Acceptance criteria:

- [ ] Reviewer can make a decision on each review-required row.
- [ ] Reviewer note is preserved in export.
- [ ] Original system recommendation is still visible after reviewer override.

## Workstream 7: Export

Owner: Frontend

Goal: Let users download reconciled results.

Tasks:

- [ ] Add export to CSV.
- [ ] Add export to JSON.
- [ ] Include original input values.
- [ ] Include canonical output values.
- [ ] Include confidence and review status.
- [ ] Include decision reason.
- [ ] Include reviewer decision fields when available.

Acceptance criteria:

- [ ] User can download results after batch reconciliation.
- [ ] Exported file can be opened in Excel or loaded as JSON.
- [ ] Export includes enough information for audit/review.

## Workstream 8: Explainability Improvements

Owner: Backend

Goal: Make explanation text more specific and useful.

Tasks:

- [ ] Update `backend/app/explain.py` to use evidence types more directly.
- [ ] Create separate explanation templates for:
  - disease alias match
  - gene alias match
  - variant catalog match
  - generic variant requiring review
  - ambiguous gene requiring review
  - cannot reconcile
- [ ] Avoid vague explanations like "one or more entities".
- [ ] Add tests for explanation text by review status.

Acceptance criteria:

- [ ] `AUTO_RECONCILE` explanation names what matched.
- [ ] `REVIEW_REQUIRED` explanation names why review is needed.
- [ ] `CANNOT_RECONCILE` explanation names what could not be resolved.

## Workstream 9: Documentation

Owner: Documentation / Product

Goal: Keep project materials aligned with the fixed data and new workflow.

Tasks:

- [ ] Create `docs/checkpoint2_plan.md`.
- [ ] Update API contract to reflect new response fields.
- [ ] Update architecture doc to use current data files.
- [ ] Update README run instructions.
- [ ] Add a demo script:
  - start backend
  - start frontend
  - upload benchmark sample
  - review rows
  - export results

Acceptance criteria:

- [ ] A new teammate can understand the Checkpoint 2 workflow from docs.
- [ ] Final demo steps are clear and repeatable.
- [ ] Docs no longer reference removed files as active inputs.

## Recommended Build Order

1. Backend response contract.
2. Batch API hardening.
3. Benchmark evaluation script.
4. Frontend CSV upload.
5. Results table and filters.
6. Review queue.
7. Export.
8. Explainability polish.
9. Documentation cleanup.

## Definition Of Done For Checkpoint 2

- [ ] Fixed data files are treated as frozen.
- [ ] Backend passes benchmark tests.
- [ ] Batch reconciliation handles valid and invalid rows.
- [ ] Frontend supports CSV upload.
- [ ] Frontend shows summary counts and filtered results.
- [ ] Review-required rows can be reviewed.
- [ ] Results can be exported.
- [ ] Benchmark evaluation report can be generated.
- [ ] Demo workflow is documented end to end.
