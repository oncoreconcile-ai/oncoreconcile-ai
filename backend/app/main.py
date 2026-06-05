from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ReconcileRequest, BatchRequest, BatchResponse
from .reconcile import reconcile_record
from .vicc import lookup_gene_vicc, lookup_variant_vicc, lookup_disease_vicc
from .llm_extract import extract_entities_llm
from .embedding import find_similar_variant, find_similar_gene, find_similar_cancer_type

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


# ---------------------------------------------------------------------------
# Stub routes — not yet implemented; return 501 with a clear message.
# These exist to define the API surface for frontend and future implementors.
# ---------------------------------------------------------------------------

@app.post("/normalize/gene", status_code=501)
def normalize_gene_vicc(payload: dict):
    """VICC gene normalization. Stub — Checkpoint 2."""
    return {"status": "not_implemented", "detail": "VICC gene normalization is a Checkpoint 2 feature."}


@app.post("/normalize/variant", status_code=501)
def normalize_variant_vicc(payload: dict):
    """VICC variant normalization. Stub — Checkpoint 2."""
    return {"status": "not_implemented", "detail": "VICC variant normalization is a Checkpoint 2 feature."}


@app.post("/normalize/disease", status_code=501)
def normalize_disease_vicc(payload: dict):
    """VICC disease normalization. Stub — Checkpoint 2."""
    return {"status": "not_implemented", "detail": "VICC disease normalization is a Checkpoint 2 feature."}


@app.post("/extract/entities", status_code=501)
def extract_entities(payload: dict):
    """LLM-based structured entity extraction. Stub — Checkpoint 2 / Hao Jun 30+."""
    return {"status": "not_implemented", "detail": "LLM entity extraction is deferred to Jun 30, 2026."}


@app.post("/embedding/similarity", status_code=501)
def embedding_similarity(payload: dict):
    """Embedding-based semantic similarity search. Stub — requires sentence-transformers."""
    return {"status": "not_implemented", "detail": "Embedding similarity is not yet implemented."}
