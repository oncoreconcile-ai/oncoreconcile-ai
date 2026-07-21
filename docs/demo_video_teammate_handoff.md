# Demo Video Teammate Handoff

This note is for the teammate recording the final OncoReconcile AI demo video. It should be sufficient to start without a separate meeting.

## Goal

Create a polished approximately 5-minute demo video for the DFWIT final submission. The video should show the working product workflow, not just slides. Please record screen plus voice narration.

## Repository and Branch

Repository:

https://github.com/oncoreconcile-ai/oncoreconcile-ai

Branch:

```bash
enterprise-patient-journey-demo
```

Please pull the latest branch before recording.

## Main Files to Follow

1. Demo production checklist: [`docs/demo_video_production_guide.md`](demo_video_production_guide.md)
2. Narration script: [`docs/final_demo_script.md`](final_demo_script.md)
3. Final submission context: [`docs/DFWIT_Final_Submission_PDF.md`](DFWIT_Final_Submission_PDF.md)
4. Setup commands: [`README.md`](../README.md)

## Local Setup

Clone and check out the final branch:

```bash
git clone https://github.com/oncoreconcile-ai/oncoreconcile-ai.git
cd oncoreconcile-ai
git checkout enterprise-patient-journey-demo
```

Start the backend in one terminal:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend in a second terminal:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open the app:

http://127.0.0.1:5173

API docs, if needed:

http://127.0.0.1:8000/docs

## Suggested Demo Flow

Follow [`final_demo_script.md`](final_demo_script.md) as the narration source of truth. The rough flow should be:

1. Open with the problem: precision oncology data uses inconsistent disease names, gene aliases, and variant descriptions. This makes analytics, AI, interoperability, and patient journey work harder to trust.
2. Show single-record reconciliation. Demonstrate a high-confidence example where the app normalizes disease, gene, and variant data and shows evidence, confidence, canonical output, and audit trail.
3. Show review-required behavior. Use an ambiguous case such as TRK fusion or uncertain mapping. Emphasize that the system does not force unsafe automation and routes ambiguity to human review.
4. Show the review queue. Demonstrate governance: reviewer decisions, alternatives, evidence, notes, and audit history.
5. Show the evaluation dashboard. Mention the final validation framing carefully: `149 backend tests collected; 146 passing; 3 skipped`, plus `0% false auto-accept rate` in the benchmark framing.
6. Show Enterprise -> Patient Journey. Show synthetic longitudinal patient data, biomarkers, treatment timeline, and data quality indicators.
7. Show Enterprise -> Executive Dashboard. Show patients managed, data quality, governance score, AI readiness, reconciliation coverage, coding coverage, and evidence coverage.
8. Show Enterprise -> Coding Alignment. Show semantic harmonization and coding mappings across systems.
9. Show Knowledge Graph export and/or FastAPI docs briefly if time permits.
10. Close with business value: OncoReconcile AI is a governed oncology data-quality and semantic harmonization layer for cancer centers, labs, CROs, pharma, real-world evidence teams, and healthcare AI teams.

## Important Talking Points

- This is not clinical decision support.
- It does not provide diagnosis or treatment recommendations.
- Patient journey data is synthetic.
- FHIR, OMOP, terminology, and knowledge graph features are prototypes.
- The value is governed reconciliation, evidence traceability, uncertainty handling, review workflow, analytics, and AI-ready data.

## Recording Requirements

- Target length: about 5 minutes.
- Use screen plus microphone.
- Use Loom, Zoom recording, QuickTime, or any tool that exports MP4.
- Record at 1080p if possible.
- Keep browser zoom around 90-100%.
- Do one clean take if possible; light pauses are fine.
- Suggested filename: `OncoReconcile_AI_Final_Demo.mp4`

## Before Sending the Video Back

Please verify:

- Backend is running on port 8000.
- Frontend is running on port 5173.
- The app loads correctly.
- Enterprise pages load correctly.
- No local error pages or terminal errors are visible.
- The final video file or hosted link is accessible to judges.

After recording, send the video file or public/judge-accessible link back in Discord so it can be added to the final submission checklist and portal notes.
