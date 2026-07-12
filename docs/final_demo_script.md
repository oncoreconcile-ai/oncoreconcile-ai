# OncoReconcile AI — Five-Minute Final Demo Script

**Updated:** June 23, 2026

**Team:** Variant Vanguard  
**Target length:** 5:00  
**Primary message:** OncoReconcile AI turns fragmented oncology data into governed, interoperable, analytics-ready information without hiding uncertainty.

## Before Recording

- Start the backend and frontend.
- Open the homepage, review queue, enterprise journey, executive dashboard, API docs, and one prepared export in separate tabs.
- Seed or confirm the review-required example.
- Use the `enterprise-patient-journey-demo` branch.
- Keep the browser zoom and font size readable.
- Do not show terminals, API keys, patient identifiers, or internal notes.

## 0:00–0:25 — Homepage and Problem

**On screen:** Homepage.

**Narration:**

“Precision oncology data arrives from EHRs, molecular labs, research systems, and clinical trials with inconsistent disease names, gene aliases, variant formats, and coding systems. Before that data can support analytics or AI, organizations spend significant expert time cleaning and reconciling it.

OncoReconcile AI is a governed data-quality and semantic-harmonization platform built to make that information trustworthy, explainable, and reusable.”

## 0:25–1:05 — Single Record Reconciliation

**On screen:** Single reconciliation form. Use a prepared high-confidence example such as NSCLC, HER1, and EGFR L858R.

**Action:** Submit the record and open the result details.

**Narration:**

“Here is a common messy record. The platform normalizes NSCLC, recognizes HER1 as EGFR, reconciles the variant, retrieves evidence, and calculates a transparent confidence score.

The output includes the original input, canonical concepts, evidence package, score breakdown, explanation, alternatives, and audit trail. This is more than a terminology lookup—it is a governed data-quality decision that can be inspected and reused.”

## 1:05–1:35 — Review-Required Case

**On screen:** Submit or open the prepared ambiguous TRK fusion example.

**Narration:**

“The important behavior is what happens when the answer is uncertain. TRK can refer to multiple NTRK genes, so the platform does not force a canonical match. It assigns REVIEW_REQUIRED and preserves the candidate evidence and ambiguity.

Optional AI assistance is restricted to suggesting candidates for human review. It cannot silently convert an uncertain case into automatic acceptance.”

## 1:35–2:00 — Review Queue

**On screen:** Review queue and expanded case.

**Action:** Show evidence, audit trail, and decision controls. If safe for the recording, demonstrate a prepared approve, edit, or reopen action.

**Narration:**

“The case enters a review queue where a curator can inspect evidence, record a decision, add notes, override a mapping, reopen a case, or send it for adjudication. Reviewer identity, timestamps, decision history, and provenance remain attached to the record.

This is how organizations can scale automation without removing accountable human governance.”

## 2:00–2:35 — Enterprise Patient Journey

**On screen:** `/enterprise/journeys`

**Action:** Select one synthetic patient and scan the timeline and quality indicators.

**Narration:**

“Reconciliation becomes more valuable when it connects an entire patient journey. This demonstration uses 18 fully synthetic oncology patients across five cancer types.

The journey combines diagnosis, histology, stage, biomarker tests, genes, variants, fusions, copy-number alterations, treatments, response, progression, trial flags, evidence coverage, and data-quality status. No real patient data is used.”

## 2:35–3:05 — Executive Analytics Dashboard

**On screen:** `/enterprise/executive`, then briefly `/enterprise/analytics`.

**Narration:**

“Enterprise leaders can see cohort composition, coding coverage, evidence coverage, reconciliation quality, governance workload, and outcome summaries. Data stewards can drill into terminology and missing-data metrics, while executives receive a concise operational view.

The goal is to make data quality visible and manageable—not leave it buried inside one-off cleanup scripts.”

## 3:05–3:35 — Semantic Harmonization and Coding Systems

**On screen:** `/enterprise/coding-alignment` — the Coding System Alignment dashboard.

**Narration:**

“The semantic layer maps related concepts across SNOMED CT, NCIt, OncoTree, ICD-10, HGNC, RxNorm, ATC, ClinVar, ClinGen-inspired identifiers, and LOINC.

Each mapping carries a source, confidence, and review status. These mappings are a standards-oriented prototype, not a claim of complete terminology coverage or clinical certification.”

## 3:35–4:05 — FHIR and OMOP Exports

**On screen:** Prepared FHIR output, then prepared OMOP output.

**Narration:**

“Governed data can be exported as a FHIR R4 Bundle containing patient, condition, observation, medication, and provenance resources.

The same journey can be represented as OMOP CDM v5.4-oriented condition, measurement, observation, and drug-exposure records. A knowledge-graph export is also available for relationship-based analytics.

These are working interoperability prototypes designed for further implementation-specific validation.”

## 4:05–4:25 — API Docs

**On screen:** FastAPI `/docs`.

**Narration:**

“The platform is API-first. Interactive documentation exposes reconciliation, review, evaluation, enterprise analytics, and export endpoints, allowing the quality layer to integrate into existing healthcare data platforms rather than requiring a standalone workflow.”

## 4:25–4:45 — Validation

**On screen:** Evaluation dashboard.

**Narration:**

“The current branch has 149 backend tests collected, with 146 passing and 3 intentionally skipped live-evidence tests, plus a passing frontend production build. The repository includes a 191-case curated API benchmark and a 500-case expanded benchmark asset. The latest recorded internal benchmark results show 96.6 percent gene accuracy, 94.6 percent variant accuracy, 89.8 percent safety-aware status accuracy, a zero percent false auto-accept rate, and 100 percent negative-control safety.

This is engineering validation, not clinical validation.”

## 4:45–5:00 — Closing Business Pitch

**On screen:** Executive dashboard or homepage with logo.

**Narration:**

“Our customers are cancer centers, molecular laboratories, pharmaceutical and research organizations, CROs, and healthcare data platforms.

We plan to begin with paid harmonization and interoperability pilots, expand into team governance software, and deliver enterprise APIs.

OncoReconcile AI makes precision oncology data trustworthy before analytics and AI depend on it.”

## Recording Notes

- If time runs long, shorten the coding-system list and API narration.
- Do not remove the review-required example; it is the clearest safety differentiator.
- Keep the synthetic-data disclaimer audible.
- End on the customer value proposition, not the technology stack.
