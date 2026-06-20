# OncoReconcile AI

OncoReconcile AI is a human-governed AI platform for harmonizing inconsistent oncology disease, gene, and variant terminology. It produces canonical candidates with confidence scores, explanations, evidence, provenance, and explicit review recommendations.

Built for the **DFWIT AI & Startup Competition 2026** by **Team Variant Vanguard**.

## Implemented Features

- Disease, gene, and variant reconciliation
- Exact, alias, and fuzzy matching
- Ambiguity preservation with `AUTO_RECONCILE`, `REVIEW_REQUIRED`, and `CANNOT_RECONCILE` outcomes
- MyVariant.info, ClinVar, CIViC, and ClinGen Allele Registry integrations
- Persistent human review queue
- Reviewer agreement metrics and Cohen's kappa
- Senior-curator adjudication workflow
- Provenance and JSON-LD knowledge graph exports
- Standards-inspired VRS-ready, Cat-VRS-ready, and VA-Spec-ready stubs

External evidence is advisory and cannot independently create a high-confidence automatic reconciliation.

## Validation Metrics

| Metric | Result |
|---|---|
| Backend tests | 43 passed |
| Benchmark cases | 191 |
| Frontend production build | Passed |

Verified June 20, 2026.

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/oncoreconcile-ai/oncoreconcile-ai.git
cd oncoreconcile-ai
git checkout feature/vanguard-justin-checkpoint2
```

### 2. Set Up and Start Backend

From the repository root:

```bash
cd backend

python3.10 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

> Recommended Python version: 3.10–3.12. Python 3.14 is not currently validated for this project.

The backend API will be available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 3. Set Up and Start Frontend

Open a second terminal and run:

```bash
cd oncoreconcile-ai
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite in the terminal, typically `http://localhost:5173`.

### 4. Validate the Project

Open another terminal at the repository root and run the backend tests:

```bash
source backend/.venv/bin/activate
python -m pytest -q
```

Then verify the frontend production build:

```bash
cd frontend
npm run build
```

## Environment

- Python 3.10–3.12
- Node.js 18+
- npm
- FastAPI
- React

## Documentation

- [MVP Product Definition](docs/mvp.md)
- [Checkpoint 2 Technical Evidence Package](docs/checkpoint2_submission.md)
- [Architecture](docs/architecture.md)
- [Curation Methodology](docs/curation_methodology.md)
- [Project Repository](https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/feature/vanguard-justin-checkpoint2)

OncoReconcile AI is a data-harmonization prototype. It does not provide clinical interpretation, treatment recommendations, or autonomous clinical decision support.
