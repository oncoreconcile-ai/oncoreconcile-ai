# OncoReconcile AI

## DFWIT 2026 Final Demo Video Production Guide

### Team Variant Vanguard

---

# Purpose

This document is the production checklist for recording the final OncoReconcile AI demo video.

Use [`final_demo_script.md`](final_demo_script.md) as the narration source of truth. This guide describes what to prepare, what to show on screen, and how to verify the recording before delivery.

The demo should communicate:

- the real-world oncology data quality problem;
- AI-assisted reconciliation with transparent evidence;
- human-governed review for uncertain cases;
- enterprise patient journey analytics;
- coding-system alignment and semantic harmonization;
- interoperability through FHIR, OMOP, knowledge graph, and API prototypes;
- validation through internal engineering benchmarks.

Target audience:

- DFWIT judges;
- startup reviewers;
- healthcare innovation stakeholders;
- potential investors;
- future collaborators.

Target length:

```text
5 minutes
```

---

# Recording Setup

## Recommended Tools

Use any tool that records screen plus microphone and can export MP4:

- QuickTime Player;
- Loom;
- Zoom recording;
- OBS.

Recommended settings:

- record at 1080p if possible;
- keep browser zoom around 90-100%;
- hide bookmarks, notifications, terminals, API keys, and unrelated tabs;
- use a quiet room and test the microphone first.

---

# Repository Setup

Follow the Quick Start section in [`README.md`](../README.md).

Branch:

```bash
enterprise-patient-journey-demo
```

Backend should be available at:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

Frontend should be available at:

```text
http://127.0.0.1:5173
```

Before recording, open these tabs:

1. Homepage: `http://127.0.0.1:5173`
2. Review Queue: `http://127.0.0.1:5173/review`
3. Enterprise Patient Journey: `http://127.0.0.1:5173/enterprise/journeys`
4. Executive Dashboard: `http://127.0.0.1:5173/enterprise/executive`
5. Coding System Alignment: `http://127.0.0.1:5173/enterprise/coding-alignment`
6. Evaluation Dashboard: `http://127.0.0.1:5173/evaluation`
7. API Docs: `http://127.0.0.1:8000/docs`

If FHIR, OMOP, or knowledge graph outputs are shown, prepare them before recording so the video does not spend time waiting on API calls.

---

# Demo Flow Overview

```text
Homepage and problem
    ->
Single-record reconciliation
    ->
Review-required example
    ->
Review queue
    ->
Enterprise patient journey
    ->
Executive analytics dashboard
    ->
Semantic harmonization and coding systems
    ->
FHIR / OMOP / Knowledge Graph exports
    ->
API documentation
    ->
Validation
    ->
Closing business pitch
```

This order matches [`final_demo_script.md`](final_demo_script.md) and the final submission context in [`DFWIT_Final_Submission_PDF.md`](DFWIT_Final_Submission_PDF.md).

---

# Scene 1 - Homepage and Problem

## Duration

25 seconds

## Screen

Homepage.

## Demonstrate

- product name and main interface;
- data quality positioning;
- overall workflow.

## Key Message

Precision oncology data is fragmented across EHRs, labs, research systems, and clinical trials. OncoReconcile AI turns inconsistent oncology terminology into governed, reusable, analytics-ready data.

---

# Scene 2 - Single-Record Reconciliation

## Duration

40 seconds

## Screen

Single reconciliation form.

## Suggested Input

Use the prepared high-confidence example from [`final_demo_script.md`](final_demo_script.md):

```text
Disease: NSCLC
Gene: HER1
Variant: EGFR L858R
```

If the local demo data has a more reliable preloaded example, use that instead, but keep the narration focused on disease normalization, gene aliasing, variant reconciliation, evidence, confidence, and audit trail.

## Demonstrate

- original input;
- canonical disease, gene, and variant;
- evidence package;
- confidence score;
- explanation;
- alternatives and audit trail.

## Key Message

This is explainable reconciliation, not a black-box terminology lookup.

---

# Scene 3 - Review-Required Case

## Duration

30 seconds

## Screen

Prepared ambiguous TRK fusion example.

## Demonstrate

- `REVIEW_REQUIRED`;
- candidate genes;
- ambiguity explanation;
- confidence breakdown;
- no unsafe automatic acceptance.

## Key Message

Safe automation means knowing when not to automate. The platform preserves uncertainty and routes ambiguous records to human review.

---

# Scene 4 - Review Queue

## Duration

25 seconds

## Screen

Review Queue.

## Demonstrate

- evidence review;
- decision controls;
- reviewer notes;
- decision history;
- provenance.

## Key Message

Manual curation becomes a measurable governance workflow with review history and accountability.

---

# Scene 5 - Enterprise Patient Journey

## Duration

35 seconds

## Screen

```text
/enterprise/journeys
```

## Demonstrate

- synthetic patient list;
- selected patient summary;
- biomarkers and genomic findings;
- treatment timeline;
- quality or review indicators.

## Key Message

Reconciliation becomes more valuable when it connects the full longitudinal oncology journey.

Important disclaimer:

```text
All patient journey data is synthetic.
```

---

# Scene 6 - Executive Analytics Dashboard

## Duration

30 seconds

## Screen

```text
/enterprise/executive
```

Optionally show `/enterprise/analytics` briefly if time allows.

## Demonstrate

- patients managed;
- data quality;
- governance score;
- AI readiness;
- reconciliation coverage;
- coding coverage;
- evidence coverage.

## Key Message

Data quality becomes visible and manageable at enterprise level.

---

# Scene 7 - Semantic Harmonization and Coding Systems

## Duration

30 seconds

## Screen

```text
/enterprise/coding-alignment
```

## Demonstrate

- coding-system coverage;
- total mappings;
- examples of canonical mappings;
- mapping confidence;
- terminology coverage table.

## Key Message

The semantic layer maps related oncology concepts across demonstrated coding systems. It is a prototype semantic-harmonization layer, not a complete certified terminology service.

---

# Scene 8 - FHIR, OMOP, and Knowledge Graph Exports

## Duration

30 seconds

## Screen

Prepared export output or API docs.

## Demonstrate

- FHIR R4 Bundle prototype;
- OMOP CDM v5.4-oriented records;
- JSON-LD knowledge graph export;
- provenance and original source values.

## Key Message

Governed reconciliation outputs can feed interoperability, research, and relationship-based analytics workflows.

Important disclaimer:

```text
FHIR, OMOP, terminology, and knowledge graph capabilities are prototypes requiring implementation-specific validation before production use.
```

---

# Scene 9 - API Documentation

## Duration

20 seconds

## Screen

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

## Demonstrate

- reconciliation endpoints;
- review queue endpoints;
- enterprise analytics endpoints;
- export endpoints.

## Key Message

The platform is API-first and can integrate into existing healthcare data platforms.

---

# Scene 10 - Validation

## Duration

20 seconds

## Screen

Evaluation dashboard.

## Demonstrate

Use this final validation framing:

```text
149 backend tests collected
146 passing
3 skipped live-evidence tests
191 curated API/test benchmark cases
500 expanded benchmark asset cases
96.6% gene accuracy
94.6% variant accuracy
89.8% safety-aware status accuracy
0% false auto-accept rate
100% negative-control safety
```

## Key Message

These are internal engineering benchmark results, not clinical validation.

---

# Scene 11 - Closing Business Pitch

## Duration

15 seconds

## Screen

Executive dashboard or homepage with logo.

## Key Message

OncoReconcile AI is a governed oncology data-quality and semantic-harmonization platform for cancer centers, molecular laboratories, pharma, CROs, research organizations, and healthcare data platforms.

---

# Safety and Scope Language

Keep these limitations clear in the recording:

- This is not clinical decision support.
- It does not provide diagnosis or treatment recommendations.
- It is not a medical device.
- Patient journey data is synthetic.
- FHIR, OMOP, terminology, and knowledge graph capabilities are prototypes.
- Current metrics are internal engineering validation, not clinical validation.

---

# Production Checklist

Before recording:

- Homepage loads correctly.
- Review Queue contains at least one `REVIEW_REQUIRED` example.
- Enterprise Patient Journey loads correctly.
- Executive Dashboard loads correctly.
- Coding System Alignment loads correctly.
- Evaluation Dashboard loads correctly.
- Prepared FHIR, OMOP, or knowledge graph output is ready if shown.
- Swagger documentation is accessible.
- Browser zoom is readable.
- Microphone is tested.
- Notifications are disabled.

After recording:

- Video is approximately 5 minutes.
- Audio is clear.
- No terminals, API keys, patient identifiers, or internal notes are visible.
- Synthetic-data and prototype disclaimers are audible.
- Video file or hosted link is accessible to judges.

---

# Final Deliverable

Suggested filename:

```text
OncoReconcile_AI_Final_Demo.mp4
```

Submission assets:

- final submission PDF;
- demo video;
- GitHub repository;
- screenshots;
- architecture documentation.
