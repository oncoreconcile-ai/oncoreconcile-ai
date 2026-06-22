# OncoReconcile AI

## DFWIT 2026 Checkpoint 2 Demo Video Production Guide

### Team Variant Vanguard

---

# Purpose

This document describes the official demonstration workflow for OncoReconcile AI.

The objective of the demo is to communicate:

* The real-world oncology data quality problem
* The AI-assisted reconciliation solution
* Human-governed review workflows
* Validation through benchmark evaluation
* Interoperability through FHIR and OMOP exports
* Enterprise platform potential

Target audience:

* DFWIT judges
* Startup reviewers
* Healthcare innovation stakeholders
* Potential investors
* Future collaborators

Target length:

**4 minutes**

---

# Recording Setup

## Recommended Tools

### macOS

QuickTime Player

```text
File
→ New Screen Recording
```

### Alternative

Loom

Benefits:

* Screen + microphone recording
* Easy sharing
* Automatic hosting
* Professional presentation

---

# Demo Flow Overview

```text
Homepage
    ↓
Single Record Reconciliation
    ↓
Review Required Example
    ↓
Review Queue
    ↓
Evaluation Dashboard
    ↓
Knowledge Graph Export
    ↓
FHIR Export
    ↓
OMOP Export
    ↓
API Documentation
    ↓
Closing Vision
```

---

# Scene 1 — Homepage

## Duration

15 seconds

## Screen

Homepage

## Demonstrate

* Product branding
* Workflow diagram

```text
Normalize
→ Retrieve Evidence
→ Score Confidence
→ Govern Review
→ Export Provenance
```

## Narration

Precision oncology generates valuable data, but inconsistent disease names, gene aliases, and variant descriptions make that data difficult to trust and reuse.

OncoReconcile AI transforms fragmented oncology inputs into governed, evidence-supported, interoperable data.

## Key Message

Data Quality Foundation

---

# Scene 2 — Single Record Reconciliation

## Duration

30 seconds

## Input

Disease:

```text
NSCLC
```

Gene:

```text
HER2
```

Variant:

```text
Amplification
```

## Action

Click:

```text
Reconcile Record
```

## Demonstrate

* Canonical disease
* ERBB2 mapping
* Variant normalization
* Evidence package
* Confidence score
* Audit trail

## Narration

Here we receive NSCLC, HER2, and Amplification.

The platform normalizes disease terminology, maps HER2 to its canonical symbol ERBB2, identifies the standardized alteration, and returns an evidence-supported recommendation.

Every decision includes confidence, provenance, alternatives considered, and an audit trail.

This is explainable AI rather than a black-box answer.

## Key Message

Explainable Reconciliation

---

# Scene 3 — Review Required Example

## Duration

30 seconds

## Input

Disease:

```text
NSCLC
```

Gene:

```text
TRK
```

Variant:

```text
pan-trk fusion
```

## Demonstrate

* REVIEW_REQUIRED
* Candidate genes
* Ambiguity explanation
* Confidence breakdown

## Narration

Safe automation also means knowing when not to automate.

TRK may refer to multiple NTRK-family genes.

Instead of guessing, the platform preserves the categorical fusion, identifies candidate genes, and routes the case for expert review.

AI assists.

Humans decide.

## Key Message

Governance First

---

# Scene 4 — Review Queue

## Duration

30 seconds

## Screen

Review Queue

## Demonstrate

* Evidence review
* Approve
* Reject
* Reopen
* Reviewer notes
* Decision history

## Narration

The ambiguous case enters a structured review workflow.

Experts can inspect evidence, modify recommendations, approve or reject decisions, and preserve a complete audit trail.

This transforms manual curation into a measurable governance process.

## Key Message

Human Governance

---

# Scene 5 — Evaluation Dashboard

## Duration

35 seconds

## Screen

Evaluation Dashboard

## Demonstrate

Current benchmark metrics:

```text
500 Cases
102 Tests
96.6% Gene Accuracy
94.6% Variant Accuracy
89.8% Safety-Aware Accuracy
0% False Auto-Accepts
100% Negative-Control Safety
```

## Narration

We validate the platform using a 500-case benchmark containing aliases, ambiguities, and negative controls.

Gene accuracy is 96.6 percent.

Variant accuracy is 94.6 percent.

Safety-aware status accuracy is 89.8 percent.

Most importantly, the false auto-accept rate is zero percent.

For healthcare data quality, knowing when to escalate uncertainty is just as important as matching correctly.

## Key Message

Evidence-Based Validation

---

# Scene 6 — Knowledge Graph Export

## Duration

25 seconds

## Screen

Knowledge Graph Export

## Demonstrate

JSON-LD output

Highlight:

* Original input
* Canonical entities
* Evidence
* Provenance
* Alternatives

## Narration

Every governed result can become a lightweight biomedical knowledge graph.

This preserves relationships among original inputs, canonical concepts, evidence, and reviewer actions.

The result is a reusable knowledge asset rather than a one-time mapping.

## Key Message

Reusable Knowledge Assets

---

# Scene 7 — FHIR Export

## Duration

20 seconds

## Screen

FHIR Export

## Demonstrate

FHIR Bundle

Highlight:

* Condition
* Observation
* DiagnosticReport
* Provenance

## Narration

For interoperability, OncoReconcile includes a FHIR export prototype.

Original terminology, governance decisions, and provenance remain traceable for downstream healthcare workflows.

## Key Message

Healthcare Interoperability

---

# Scene 8 — OMOP Export

## Duration

20 seconds

## Screen

OMOP Export

## Demonstrate

OMOP records

Highlight:

* condition_occurrence
* measurement
* observation

## Narration

For real-world evidence and research environments, the same governed result can be exported to OMOP-compatible structures.

Source values remain visible when uncertainty exists.

## Key Message

Research & Analytics Enablement

---

# Scene 9 — API Documentation

## Duration

20 seconds

## Screen

Swagger UI

## Demonstrate

Endpoints:

* Reconciliation
* Batch processing
* Review queue
* Benchmark evaluation
* Export APIs

## Narration

The platform is API-first.

Organizations can integrate reconciliation, governance, benchmarking, and interoperability workflows directly into existing healthcare systems.

## Key Message

Enterprise Platform

---

# Scene 10 — Closing Vision

## Duration

15 seconds

## Screen

Homepage or Branded Cover Page

## Narration

OncoReconcile AI transforms fragmented oncology terminology into evidence-supported, human-governed, interoperable data.

Team Variant Vanguard is building the trusted data-quality foundation that precision medicine and healthcare AI need to scale safely.

Thank you.

## Key Message

Future Precision Oncology Infrastructure

---

# Production Checklist

Before Recording

✓ Homepage loads correctly

✓ Review Queue contains at least one REVIEW_REQUIRED example

✓ Evaluation Dashboard shows 500 benchmark cases

✓ Knowledge Graph export functions

✓ FHIR export functions

✓ OMOP export functions

✓ Swagger documentation accessible

✓ Browser zoom set to 110–125%

✓ Microphone tested

✓ Notifications disabled

---

# Final Deliverables

Video:

```text
OncoReconcile_AI_Checkpoint2_Demo.mp4
```

Length:

```text
4:00 ± 30 seconds
```

Submission Assets:

* Checkpoint 2 PDF
* Demo Video
* GitHub Repository
* Screenshots
* Architecture Documentation

---

# Core Message

OncoReconcile AI is not simply a terminology lookup tool.

It is a human-governed biomedical data quality, interoperability, and AI-readiness platform for precision oncology.
