# Decision Log

## Decision 001: Human-Governed Workbench

Date: 2026-06-01

Decision:
The MVP will be positioned as a Human-Governed Oncology Reconciliation Workbench.

Reason:
Expert feedback and clinical genomics best practices indicate that human review remains essential for ambiguous records.

---

## Decision 002: Scope Reduction

Date: 2026-06-01

Decision:
PDF extraction, OCR, treatment recommendation, and clinical interpretation are excluded from the MVP.

Reason:
These features increase risk and are not required to demonstrate the core value.

---

## Decision 003: Simplified Canonical Object Before CAT-VRS

Date: 2026-06-01

Decision:
The MVP will use a simplified Canonical Oncology Concept Object.

Reason:
GA4GH VRS/CAT-VRS alignment is valuable, but full implementation is too complex for the short competition timeline.

---

## Decision 005: G12C Variant Alias is KRAS-Hardcoded

Date: 2026-06-05

Decision:
`G12C` in `data/variant_aliases.json` maps directly to `KRAS p.G12C` rather than using a `{gene}` template.

Reason:
All current benchmark cases with G12C are KRAS. The hardcoded value is intentional and correct for the current dataset.

Risk:
If a non-KRAS G12C case is added (e.g. NRAS p.G12C), the alias will silently return the wrong canonical output. Revisit this entry and convert to a `{gene}` template if non-KRAS G12C cases are introduced.

---

## Decision 006: `expected_review_status` Not Included in Benchmark CSV

Date: 2026-06-05

Decision:
`data/nsclc_benchmark.csv` does not have an `expected_review_status` column. The benchmark tests do not assert `review_status`.

Reason:
`review_status` is fully derived from `confidence`, which is derived from the canonical outputs. If all three canonical fields are correct, `review_status` is correct by construction. Asserting it would be redundant given the current derivation logic.

Risk:
If the derivation logic ever becomes more complex (e.g. source-dependent overrides), this implicit coverage will no longer be sufficient.

Recommendation:
Add `expected_review_status` as a column to the CSV and assert it explicitly in the tests. This is a low-effort change that closes the gap and makes the contract visible to non-engineers reading the benchmark file. Suggested owner: Rin (data) + Nikola (test wiring).

---

## Decision 004: NSCLC First

Date: 2026-06-01

Decision:
The initial benchmark dataset focuses on NSCLC.

Reason:
NSCLC includes common oncology reconciliation challenges: SNVs, indels, fusions, amplifications, and resistance mutations.
