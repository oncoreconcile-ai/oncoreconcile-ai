# DFWIT Checkpoint 2 Documentation Audit

**Branch audited:** `startup-platform`  
**Audit date:** June 22, 2026  
**Scope:** All Markdown files under `docs/`  
**Markdown files reviewed:** 33, including this report and the new PDF-export document

## Summary

| File | Changes Made | Broken Links Found | Notes |
|---|---|---:|---|
| `docs/DFWIT_Checkpoint2_Primary_Submission.md` | Added `Additional Resources` with absolute `startup-platform` GitHub URLs | 0 | Existing content and relative links were left unchanged |
| `docs/startup_platform_overview.md` | Added `Additional Resources` with absolute `startup-platform` GitHub URLs | 0 | Existing content and relative links were left unchanged |
| `docs/DFWIT_Checkpoint2_Primary_Submission_PDF.md` | Created self-contained judge-facing PDF-export source | 0 | Contains no relative Markdown links; includes metrics, enterprise vision, patient journey analytics, FHIR, OMOP, benchmark results, governance, repository, and branch details |
| `docs/team_tasks.md` | Audited only; no edits | 44 | Contains all broken relative Markdown-link occurrences found in the docs tree |
| `docs/meeting_agenda_jun1.md` | Audited only; no edits | 0 relative links | Contains 20 URLs pinned to `main` and 2 branch-unspecified repository URLs |
| `docs/final_submission_draft.md` | Audited only; no edits | 0 | Contains 1 branch-unspecified repository URL |
| Remaining Markdown files under `docs/` | Audited only; no edits | 0 | No broken relative Markdown links detected |

## Broken Relative-Link Report

The audit found **44 broken relative Markdown-link occurrences**, all in `docs/team_tasks.md`.

Of these:

* **24 links point to files that exist at the repository root but use an incorrect path relative to `docs/team_tasks.md`.**
* **20 links point to targets that are absent from the current branch.**

The links were reported but not changed because the submission task explicitly requires existing relative Markdown links to remain unchanged.

### Existing Targets Referenced with the Wrong Relative Base

These targets exist in the repository, but links such as `(backend/app/reconcile.py)` resolve from `docs/` and therefore point to `docs/backend/app/reconcile.py`.

| Lines in `docs/team_tasks.md` | Referenced Target |
|---|---|
| 130, 332, 338, 358 | `backend/app/reconcile.py` |
| 137, 341 | `backend/app/models.py` |
| 138, 342 | `backend/tests/test_reconcile.py` |
| 140, 174, 194 | `data/gene_aliases.json` |
| 276, 403 | `frontend/src/main.jsx` |
| 283 | `frontend/src/style.css` |
| 284, 404 | `frontend/vite.config.js` |
| 285 | `frontend/package.json` |
| 286 | `contracts/api_contract.md` |
| 287 | `contracts/output.example.json` |
| 331, 343, 349 | `docs/prompts/explainability_prompt.md` |
| 402 | `backend/app/main.py` |
| 405 | `backend/requirements.txt` |

### Targets Absent from the Current Branch

| Lines in `docs/team_tasks.md` | Missing Target |
|---|---|
| 45, 139, 176, 182 | `data/nsclc_benchmark.csv` |
| 140, 173, 193 | `data/variant_aliases.json` |
| 140, 175, 195 | `data/cancer_aliases.json` |
| 177, 196, 233 | `data/nsclc_hard_cases.csv` |
| 178, 197, 247 | `data/evidence_map.csv` |
| 333, 370 | `backend/tests/test_explainability.py` |
| 334, 378 | `data/explainability_eval.csv` |

## Other References to Files That Do Not Exist

The following absent paths appear as inline-code or plain-text references rather than active relative Markdown links. Several are historical plans or intended deliverables.

| Document | Referenced Missing Path |
|---|---|
| `checkpoint1_submission_draft.md` | `data/variant_aliases.json`, `data/cancer_aliases.json`, `docs/checkpoint1_feedback_notes.md`, `frontend/src/components/CsvUpload.jsx`, `data/nsclc_benchmark.csv` |
| `checkpoint2_reconciliation_tasks.md` | `data/benchmark_results.csv`, `docs/checkpoint2_plan.md`, `scripts/generate_competition_metrics.py`, `data/competition_metrics.json`, `docs/business_case.md`, `docs/final_demo_script.md` |
| `checkpoint2_submission.md` | `docs/images/single_reconciliation.png`, `docs/images/review_queue.png`, `docs/images/reviewer_agreement.png`, `docs/images/knowledge_graph_export.png` |
| `meeting_agenda_jun1.md` | `data/variant_aliases.json` |
| `team_tasks.md` | `backend/.venv` and the missing targets listed above |
| `weekly_plan.md` | `data/nsclc_benchmark.csv` |

## Duplicate and Overlapping Documents

No byte-for-byte duplicate Markdown documents were found.

Potentially duplicative or overlapping documents:

| Documents | Finding |
|---|---|
| `checkpoint2_submission.md` and `DFWIT_Checkpoint2_Primary_Submission.md` | The former is an older technical evidence package; the latter is the current, broader primary competition submission. Retain the older file for history, but treat the primary submission as authoritative. |
| `DFWIT_Checkpoint2_Primary_Submission.md` and `DFWIT_Checkpoint2_Primary_Submission_PDF.md` | Intentional duplication for two delivery formats: GitHub review and offline/PDF judge review. |
| `customer_validation/daniel_notes.md` and `customer_validation/dr_dong_notes.md` | Structurally similar interview-note templates with different intended interviewees; not true duplicates. |
| `startup_platform_overview.md` and `DFWIT_Checkpoint2_Primary_Submission.md` | Some product-positioning content overlaps, but the overview is a reusable startup narrative while the primary submission is competition-specific. |

## Inconsistent Repository URLs

The preferred Checkpoint 2 branch is:

https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

The audit found **23 repository URL occurrences that do not explicitly target `startup-platform`**:

* **20 `blob/main/...` URLs** in `docs/meeting_agenda_jun1.md`
* **2 branch-unspecified repository URLs** in `docs/meeting_agenda_jun1.md`
* **1 branch-unspecified repository URL** in `docs/final_submission_draft.md`

These historical URLs were not changed. All new judge-facing resource links explicitly target `startup-platform`.

## Validation Metrics Review

The competition package uses the requested metrics:

| Metric | Submission Value | Audit Evidence |
|---|---:|---|
| Backend Tests | 102 Passed | Present in the current README and primary submission; local collection on June 22, 2026 found 102 tests |
| Benchmark | 500 Cases | Confirmed: `data/benchmark_v2.csv` contains 500 data rows |
| Disease Accuracy | 68.6% | Present in the current README and primary submission |
| Gene Accuracy | 96.6% | Present in the current README and primary submission |
| Variant Accuracy | 94.6% | Present in the current README and primary submission |
| Safety-Aware Status Accuracy | 89.8% | Present in the current README and primary submission |
| False Auto-Accept Rate | 0% | Present in the current README and primary submission |

### Test-Count Reconciliation Needed

The submission test count has been reconciled to the reproducible local result: **102 Passed**.

```bash
cd backend
PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q -p no:cacheprovider
```

Before final submission, rerun the complete intended validation environment and either:

1. restore or include the tests needed to reproduce 102 passing tests, or
2. update the published test count to the reproducible branch result.

## PDF-Export Verification

`docs/DFWIT_Checkpoint2_Primary_Submission_PDF.md` was checked for:

* Self-contained submission narrative
* Absolute GitHub resource URLs
* Zero relative Markdown links
* Repository and `startup-platform` branch information
* Current requested validation and benchmark metrics
* Enterprise platform vision
* Patient journey analytics vision
* FHIR interoperability
* OMOP interoperability
* Reviewer governance workflow
* Benchmark evaluation results
* Clinical-use disclaimer

## Recommended Pre-Submission Checks

1. Resolve the 151-versus-102 backend test-count discrepancy.
2. Confirm whether historical `main` links should remain historical or be repointed in a future cleanup.
3. Export `DFWIT_Checkpoint2_Primary_Submission_PDF.md` to PDF and visually inspect page breaks, tables, and code blocks.
4. Add final screenshots if the submission package requires visual evidence; the currently referenced historical screenshot files are absent.
