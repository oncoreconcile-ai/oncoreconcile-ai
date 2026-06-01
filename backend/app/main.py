from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ReconcileRequest, BatchRequest, BatchResponse
from .reconcile import reconcile_record

app = FastAPI(
    title="OncoReconcile AI API",
    description="Human-governed oncology entity reconciliation API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "project": "OncoReconcile AI",
        "status": "ok",
        "docs": "/docs",
    }


@app.post("/reconcile")
def reconcile(req: ReconcileRequest):
    return reconcile_record(req)


@app.post("/reconcile/batch")
def reconcile_batch(req: BatchRequest):
    results = [reconcile_record(record) for record in req.records]
    summary = {
        "total_records": len(results),
        "auto_reconcile": sum(r.review_status == "AUTO_RECONCILE" for r in results),
        "review_required": sum(r.review_status == "REVIEW_REQUIRED" for r in results),
        "cannot_reconcile": sum(r.review_status == "CANNOT_RECONCILE" for r in results),
    }
    return BatchResponse(results=results, summary=summary)
