# OncoReconcile AI

## Human-Governed Biomedical Entity Resolution Platform for Precision Oncology

OncoReconcile AI is a human-governed AI platform for harmonizing inconsistent oncology disease, gene, and variant terminology. It produces canonical candidates with confidence scores, explanations, evidence, provenance, and explicit review recommendations.

Built for the **DFWIT AI & Startup Competition 2026** by **Team Variant Vanguard**.

Official submission branch:

https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform

This project is a biomedical data harmonization and governance prototype. It does not provide clinical interpretation or treatment recommendations.

---

# Problem

Precision oncology data is fragmented across:

* Electronic Health Records (EHR)
* Molecular diagnostic reports
* Clinical trial systems
* Research databases
* Laboratory information systems
* Real-world evidence platforms

The same disease, gene, or variant may appear in multiple forms:

| Input    | Canonical Form                       |
| -------- | ------------------------------------ |
| NSCLC    | Non-Small Cell Lung Carcinoma        |
| HER2     | ERBB2                                |
| Ex19del  | EGFR c.2235_2249del15                |
| FLT3 ITD | Standardized FLT3 ITD representation |

---

# Solution

OncoReconcile AI provides:

* Disease reconciliation
* Gene reconciliation
* Variant reconciliation
* Confidence scoring
* Human review governance
* Provenance tracking
* Benchmark evaluation
* External evidence retrieval

---

# Implemented Features

## Reconciliation Engine

* Exact matching
* Alias matching
* Fuzzy matching
* Compound disease-gene-variant matching
* Review-required routing

## Governance

* AUTO_RECONCILE
* REVIEW_REQUIRED
* CANNOT_RECONCILE

## Evidence Sources

* Local curated catalog
* MyVariant.info
* ClinVar
* CIViC
* ClinGen Allele Registry

## Human Review Workflow

* Persistent review queue
* Curator review
* Senior curator adjudication
* Reviewer agreement metrics
* Cohen's kappa reporting

## Standards Alignment

* VRS-inspired structures
* Cat-VRS-inspired structures
* VA-Spec-inspired provenance
* Knowledge graph export foundations

---

# Validation

| Metric                    | Result     |
| ------------------------- | ---------- |
| Backend Tests             | 102 Passed |
| Benchmark Cases           | 191        |
| Frontend Production Build | Passed     |

Verified June 2026.

---

# Platform Architecture

```text
User Input
     |
     v
Normalization Engine
     |
     +--> Alias Matching
     +--> Fuzzy Matching
     +--> Catalog Matching
     |
     v
Evidence Retrieval Layer
     |
     +--> Local Catalog
     +--> MyVariant
     +--> ClinVar
     +--> CIViC
     |
     v
Confidence Scoring
     |
     v
Governance Decision
     |
     +--> AUTO_RECONCILE
     +--> REVIEW_REQUIRED
     +--> CANNOT_RECONCILE
     |
     v
Review Queue
     |
     v
Export / Benchmark / Analytics
```

Additional architecture documentation:

* docs/architecture.md
* docs/architecture_diagrams.md

---

# Evaluation Dashboard

Frontend route:

```text
/evaluation

The startup-platform branch includes:

* Benchmark evaluation API
* Accuracy reporting
* Review-rate reporting
* False auto-accept tracking
* Evaluation Dashboard UI

---

# Startup Vision

The long-term vision of OncoReconcile AI is to become the biomedical entity resolution and interoperability layer for precision oncology.

Future directions include:

* FHIR interoperability
* OMOP interoperability
* Biomedical knowledge graphs
* Enterprise APIs
* Multi-cancer support
* AI-assisted curation workflows
* Clinical trial harmonization

---

# Repository Structure

```text
backend/
frontend/
data/
contracts/
demo/
docs/
scripts/
archive/
```

---

# Documentation

See:

* docs/README.md
* docs/mvp.md
* docs/commercial_strategy.md
* docs/architecture.md
* docs/architecture_diagrams.md
* docs/curation_methodology.md
* docs/final_submission_draft.md

---

# Quick Start

## Clone Repository

```bash
git clone https://github.com/oncoreconcile-ai/oncoreconcile-ai.git
cd oncoreconcile-ai
git checkout startup-platform
```

## Backend

```bash
cd backend

python3.10 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Frontend

```bash
cd frontend

npm install
npm run dev
```

---

# Validation

```bash
cd backend
python -m pytest -q
```

Expected:

```text
102 passed
```

---

# Disclaimer

OncoReconcile AI is a data harmonization and governance platform.

It is not a clinical decision support system and does not provide diagnosis, treatment recommendations, or medical advice.
