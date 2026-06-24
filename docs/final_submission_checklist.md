# DFWIT 2026 Final Submission Checklist

**Project:** OncoReconcile AI  
**Team:** Variant Vanguard  
**Final deadline:** July 11, 2026  
**Final branch:** `enterprise-patient-journey-demo`

## Official Portal Requirements

- [ ] Team captain is the person uploading the submission.
- [ ] Upload uses the official portal: https://ai.dfwit.org/Submission
- [ ] Submission is marked **Demo Day Submission: Yes**.
- [ ] Team name, project name, all team members, and contact email are complete.
- [ ] Preview image is attached and is no larger than 10 MB.
- [ ] Preview image uses JPG/JPEG, PNG, WEBP, or GIF.
- [ ] At least one submission file is attached.
- [ ] No more than five submission files are attached.
- [ ] Every submission file is no larger than 25 MB.
- [ ] Submission files use an accepted format: PDF, ZIP, PPT/PPTX, DOC/DOCX, XLS/XLSX, CSV, JSON, TXT, or MP4.
- [ ] Notes field includes the repository, branch, demo video, and any judge access instructions.

## Required Repository Files

- [x] `docs/DFWIT_Final_Submission.md`
- [x] `docs/DFWIT_Final_Submission_PDF.md`
- [x] `docs/final_demo_script.md`
- [x] `docs/final_submission_checklist.md`
- [x] `docs/final_pitch_summary.md`
- [x] `docs/images/oncoreconcile_logo.png`
- [x] Core product screenshots in `docs/screenshots/`
- [ ] Enterprise patient journey screenshot
- [ ] Executive dashboard screenshot
- [ ] Semantic harmonization / coding-system screenshot
- [ ] FHIR export screenshot
- [ ] OMOP export screenshot

## GitHub Branch

- [x] Working branch is `enterprise-patient-journey-demo`.
- [x] Remote branch exists.
- [ ] Final documents are committed.
- [ ] Final screenshots are committed.
- [ ] Demo video link has replaced every placeholder.
- [ ] Local branch is pushed and matches `origin/enterprise-patient-journey-demo`.
- [ ] Repository and branch are accessible to judges without requesting permission.
- [ ] Absolute GitHub links were opened in a signed-out/private browser session.

## PDF

- [ ] Export `docs/DFWIT_Final_Submission_PDF.md` to `OncoReconcile_AI_DFWIT_2026_Final_Submission.pdf`.
- [ ] Verify the logo renders.
- [ ] Verify all screenshots render at readable resolution.
- [ ] Check page breaks, table wrapping, margins, and link formatting.
- [ ] Confirm no internal working notes or unresolved comments appear.
- [ ] Confirm the PDF is below 25 MB.
- [ ] Open the final PDF on a second device.

## Demo Video

- [ ] Follow `docs/final_demo_script.md`.
- [ ] Target approximately five minutes.
- [ ] Show homepage.
- [ ] Show high-confidence single-record reconciliation.
- [ ] Show a review-required case.
- [ ] Show review queue governance.
- [ ] Show enterprise patient journey.
- [ ] Show executive analytics.
- [ ] Show semantic harmonization and coding-system mapping.
- [ ] Show FHIR export.
- [ ] Show OMOP export.
- [ ] Show interactive API documentation.
- [ ] State that patient journey data is synthetic.
- [ ] State that validation is engineering validation, not clinical validation.
- [ ] End with customers, business model, and value proposition.
- [ ] Upload to a judge-accessible location and test the link without team credentials.
- [ ] Replace all `Demo video link will be added before final portal submission.` placeholders.

## Screenshots

- [x] Homepage
- [x] Single-record reconciliation
- [x] Review-required case
- [x] Review queue
- [x] Evaluation dashboard
- [x] Knowledge graph export
- [x] API documentation
- [ ] Enterprise patient journey
- [ ] Executive dashboard
- [ ] Semantic terminology mapping
- [ ] FHIR export
- [ ] OMOP export
- [ ] Preview image selected for portal upload

Recommended preview image: a clean 16:9 composite or executive-dashboard screenshot with the product logo and one-line value proposition.

## Validation Commands

Run from the repository root:

```bash
git status --short --branch
git branch --show-current
git diff --check
```

Run backend tests:

```bash
cd backend
PYTHONPATH=. pytest -q
```

Current repository state reviewed on June 24, 2026:

```text
149 tests collected
11 targeted HGVS/evidence tests passed
```

Do not mark the full suite as passing until `PYTHONPATH=. pytest -q` completes. The new federation path currently performs live, rate-limited ClinVar/CIViC calls during reconciliation, including benchmark-oriented paths.

Run the frontend build:

```bash
cd frontend
npm run build
```

Expected result:

```text
✓ built
```

Verify the current benchmark assets:

```bash
wc -l data/benchmark_cases.csv data/benchmark_v2.csv
```

Expected result: 192 lines for the current 191-case API/test benchmark and 501 lines for the expanded 500-case dataset.

Check placeholders and prohibited overclaims:

```bash
rg -n "TO BE ADDED|ADD PUBLIC|production-ready|149 passed|127 passed|50\\+ variants|clinical validation|treatment recommendation|medical advice" README.md docs/DFWIT_Final_Submission.md docs/DFWIT_Final_Submission_PDF.md docs/final_demo_script.md docs/final_pitch_summary.md
```

## Suggested Final Upload Package

The official portal permits up to five files. Recommended package:

1. `OncoReconcile_AI_DFWIT_2026_Final_Submission.pdf`
2. `OncoReconcile_AI_One_Page_Pitch.pdf`
3. `OncoReconcile_AI_Demo_Video_Link.pdf` or a short text/PDF link sheet if the video is hosted externally
4. `OncoReconcile_AI_Technical_Evidence.pdf` if a separate appendix is needed
5. `OncoReconcile_AI_Screenshots.pdf` only if key screenshots are not already legible in the primary PDF

Prefer a focused package over using all five slots automatically. The primary PDF and accessible video should carry the story.

## Final Upload Checklist

- [ ] Final PDF filename is clear and professional.
- [ ] One-page pitch PDF is included.
- [ ] Demo video link works.
- [ ] GitHub link opens to the final branch.
- [ ] Preview image is under 10 MB.
- [ ] Each file is under 25 MB.
- [ ] Submission contains no real patient data.
- [ ] Submission contains no secrets, credentials, tokens, or private URLs.
- [ ] Metrics match the final validation run.
- [ ] Claims distinguish implemented features, prototypes, and roadmap.
- [ ] No claim of clinical validation, treatment recommendation, or production clinical decision support appears.
- [ ] Team captain selects **Demo Day Submission: Yes**.
- [ ] Submission confirmation ID is saved.
- [ ] Uploaded files are downloaded once and opened to verify integrity.
