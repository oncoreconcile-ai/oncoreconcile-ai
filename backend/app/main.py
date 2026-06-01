from fastapi import FastAPI
from .models import ReconcileRequest, BatchRequest, BatchResponse
from .reconcile import reconcile_record

app = FastAPI(
    title="OncoReconcile AI API",
    description="Human-governed oncology entity reconciliation API",
    version="0.1.0",
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
