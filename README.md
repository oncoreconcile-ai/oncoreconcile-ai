# OncoReconcile AI

OncoReconcile AI is a human-governed platform for harmonizing inconsistent oncology disease, gene, and variant terminology. It produces canonical candidates with confidence scores, explanations, evidence, provenance, and explicit review recommendations.

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

Start the backend:

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Run validation:

```bash
python -m pytest -q
cd frontend && npm run build
```

## Documentation

- [MVP Product Definition](docs/mvp.md)
- [Checkpoint 2 Technical Evidence Package](docs/checkpoint2_submission.md)
- [Architecture](docs/architecture.md)
- [Curation Methodology](docs/curation_methodology.md)
- [Project Repository](https://github.com/justin-mbca/oncoreconcile-ai)

OncoReconcile AI is a data-harmonization prototype. It does not provide clinical interpretation, treatment recommendations, or autonomous clinical decision support.
