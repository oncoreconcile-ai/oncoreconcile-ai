import csv
import hashlib
import io
import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    ReconcileRequest, BatchRequest, BatchResponse,
    ReviewDecision, ReviewQueueItem, ReviewQueueResponse,
)
from .reconcile import reconcile_record
from .provenance_export import build_prov_o_inspired_record
from .knowledge_graph_export import build_knowledge_graph
from .standards_alignment import get_ga4gh_aiws_alignment
from .standards_export import (
    build_cat_vrs_ready_stub,
    build_va_spec_ready_stub,
    build_vrs_ready_stub,
)
from .fhir_export import build_fhir_bundle, build_fhir_bundle_batch
from .omop_export import build_omop_records, build_omop_records_batch
from .canonical_hgvs import get_canonical_hgvs
from .evidence_unified import fetch_federated_evidence, compute_evidence_boost, group_by_source
from . import review_store

ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = ROOT / "data" / "benchmark_cases.csv"


def get_allowed_origins() -> list[str]:
    configured = os.getenv("ALLOWED_ORIGINS", "")
    origins = [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:5175", "http://127.0.0.1:5175",
        *origins,
    ]

app = FastAPI(
    title="OncoReconcile AI API",
    description="Human-governed oncology entity reconciliation API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+)(:\d+)?|https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    alignment = get_ga4gh_aiws_alignment()
    return {
        "project": "OncoReconcile AI",
        "version": "2.0.0",
        "status": "ok",
        "docs": "/docs",
        "product_positioning": alignment["product_positioning"],
        "mvp": {
            "workflow": [
                "normalize",
                "reconcile",
                "detect_ambiguity",
                "explain",
                "review",
                "audit",
            ],
            "standards_alignment": {
                "implemented": ["HGNC-inspired", "HGVS-inspired", "ClinVar-inspired", "ClinGen-inspired", "FHIR Genomics R4 Bundle", "OMOP CDM v5.4 Export"],
                "partially_implemented": ["GA4GH Cat-VRS-inspired", "GA4GH VA-Spec-inspired"],
                "future": ["GA4GH VRS"],
            },
        },
    }


def resolve_reconciliation_payload(payload: dict, persist_review: bool = False) -> dict:
    if {"input", "canonical", "review_status", "evidence"}.issubset(payload):
        return payload

    try:
        request = ReconcileRequest.model_validate(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail="Provide a reconciliation result or original input with gene and variant.",
        ) from exc

    result = reconcile_record(request)
    if persist_review:
        queue_review_required(result)
    return result.model_dump(mode="json")


def queue_review_required(result) -> None:
    if result.review_status != "REVIEW_REQUIRED":
        return

    if result.case_id:
        case_id = result.case_id
    else:
        stable_key = "|".join(
            str(result.input.get(field) or "").strip().lower()
            for field in ("cancer_type", "gene", "variant")
        )
        digest = hashlib.sha1(stable_key.encode("utf-8")).hexdigest()[:12]
        case_id = f"review-{digest}" if stable_key != "||" else str(uuid.uuid4())
    review_store.add_to_queue(ReviewQueueItem(
        case_id=case_id,
        input=result.input,
        canonical=result.canonical,
        confidence=result.confidence,
        confidence_score=result.confidence_score,
        score_breakdown=result.score_breakdown,
        review_status=result.review_status,
        explanation=result.explanation,
        evidence=result.evidence,
        alternatives=result.alternatives,
        notes=result.notes,
        audit_trail=result.audit_trail,
        curation_metadata=result.curation_metadata,
    ))


def benchmark_metrics() -> dict:
    if not BENCHMARK_PATH.exists():
        raise HTTPException(status_code=404, detail="Benchmark file not found.")

    with BENCHMARK_PATH.open(newline="", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))

    if not cases:
        raise HTTPException(status_code=400, detail="Benchmark file is empty.")

    total = len(cases)
    full_correct = 0
    status_correct = 0
    resolved = 0
    review_required = 0
    cannot_reconcile = 0
    candidate_evidence_cases = 0
    live_external_lookup_attempted = 0
    live_external_evidence_found = 0
    failures = []

    for row in cases:
        result = reconcile_record(ReconcileRequest(
            case_id=row.get("case_id") or None,
            cancer_type=row.get("input_disease") or None,
            gene=row["input_gene"],
            variant=row["input_variant"],
        ), allow_live_lookup=False)

        expected_gene = None if row["expected_gene"] in {"REVIEW_REQUIRED", "CANNOT_RECONCILE"} else row["expected_gene"]
        expected_variant = None if row["expected_variant"] == "CANNOT_RECONCILE" else row["expected_variant"]
        expected_disease = None if row["expected_disease"] == "CANNOT_RECONCILE" else row["expected_disease"]
        expected_status = row["expected_status"]

        disease_ok = result.canonical.cancer_type == expected_disease
        gene_ok = result.canonical.gene == expected_gene or row["expected_gene"] == "REVIEW_REQUIRED"
        variant_ok = result.canonical.variant == expected_variant
        status_ok = result.review_status == expected_status

        if status_ok:
            status_correct += 1
        if disease_ok and gene_ok and variant_ok and status_ok:
            full_correct += 1
        if result.review_status != "CANNOT_RECONCILE":
            resolved += 1
        if result.review_status == "REVIEW_REQUIRED":
            review_required += 1
        if result.review_status == "CANNOT_RECONCILE":
            cannot_reconcile += 1
        if any(
            item.type in {"variant_external_candidate", "gene_catalog_candidate", "gene_external_candidate"}
            or item.retrieval_mode in {
                "external_api_or_syntax_candidate",
                "local_gene_variant_catalog_candidate",
                "external_mygene_api_candidate",
            }
            for item in result.evidence
        ):
            candidate_evidence_cases += 1
        if any("Live external evidence lookup started" in entry for entry in result.audit_trail):
            live_external_lookup_attempted += 1
        if any(
            item.retrieval_mode.startswith("live_")
            and not item.retrieval_mode.endswith("_error")
            for item in result.evidence
        ):
            live_external_evidence_found += 1
        if not (disease_ok and gene_ok and variant_ok and status_ok):
            failures.append({
                "case_id": row["case_id"],
                "expected_status": expected_status,
                "actual_status": result.review_status,
                "expected_gene": expected_gene,
                "actual_gene": result.canonical.gene,
                "expected_variant": expected_variant,
                "actual_variant": result.canonical.variant,
            })

    def rate(value: int) -> float:
        return round(value / total, 4)

    reviewed_items = review_store.get_queue("reviewed")
    review_decisions = {
        "approved": sum(item.decision == "approve" for item in reviewed_items),
        "rejected": sum(item.decision == "reject" for item in reviewed_items),
        "edited": sum(item.decision in {"edit", "override"} for item in reviewed_items),
    }

    return {
        "benchmark_file": str(BENCHMARK_PATH.relative_to(ROOT)),
        "total_cases": total,
        "accuracy": rate(full_correct),
        "status_accuracy": rate(status_correct),
        "coverage": rate(resolved),
        "review_rate": rate(review_required),
        "cannot_reconcile_rate": rate(cannot_reconcile),
        "targets": {
            "accuracy": 0.90,
            "coverage": 0.95,
        },
        "target_status": {
            "accuracy": rate(full_correct) >= 0.90,
            "coverage": rate(resolved) >= 0.95,
        },
        "counts": {
            "total_records": total,
            "full_correct": full_correct,
            "status_correct": status_correct,
            "auto_reconcile": total - review_required - cannot_reconcile,
            "resolved": resolved,
            "review_required": review_required,
            "cannot_reconcile": cannot_reconcile,
            "candidate_evidence_cases": candidate_evidence_cases,
            "live_external_lookup_attempted": live_external_lookup_attempted,
            "live_external_evidence_found": live_external_evidence_found,
            "approved_review_cases": review_decisions["approved"],
            "rejected_review_cases": review_decisions["rejected"],
            "edited_review_cases": review_decisions["edited"],
        },
        "failures": failures[:20],
    }


# ── Single record ─────────────────────────────────────────────────────────────

@app.post("/reconcile")
def reconcile(req: ReconcileRequest):
    result = reconcile_record(req)
    queue_review_required(result)
    return result


# ── AI-assisted curation and standards-ready exports ─────────────────────────

@app.get("/standards/alignment")
def standards_alignment():
    return get_ga4gh_aiws_alignment()


@app.post("/export/provenance")
def export_provenance(payload: dict):
    result = resolve_reconciliation_payload(payload)
    return build_prov_o_inspired_record(result)


@app.post("/export/knowledge-graph")
def export_knowledge_graph(payload: dict):
    result = resolve_reconciliation_payload(payload)
    return build_knowledge_graph(result)


@app.post("/export/vrs-ready")
def export_vrs_ready(payload: dict):
    result = resolve_reconciliation_payload(payload)
    return build_vrs_ready_stub(result)


@app.post("/export/cat-vrs-ready")
def export_cat_vrs_ready(payload: dict):
    result = resolve_reconciliation_payload(payload)
    return build_cat_vrs_ready_stub(result)


@app.post("/export/va-spec-ready")
def export_va_spec_ready(payload: dict):
    result = resolve_reconciliation_payload(payload)
    return build_va_spec_ready_stub(result)


@app.post("/curation/report")
def curation_report(payload: dict):
    result = resolve_reconciliation_payload(payload, persist_review=True)
    metadata = result.get("curation_metadata") or {}
    requires_review = result.get("review_status") == "REVIEW_REQUIRED"
    promotion_candidate = bool(metadata.get("catalog_promotion_candidate"))
    if requires_review and promotion_candidate:
        reason = "Candidate evidence requires human review before catalog promotion."
    elif requires_review:
        reason = "The reconciliation result requires human governance."
    else:
        reason = "No human review is required by the current MVP status rules."

    return {
        "reconciliation_result": result,
        "curation_metadata": metadata,
        "provenance_export": build_prov_o_inspired_record(result),
        "knowledge_graph_export": build_knowledge_graph(result),
        "standards_ready_exports": {
            "vrs_ready": build_vrs_ready_stub(result),
            "cat_vrs_ready": build_cat_vrs_ready_stub(result),
            "va_spec_ready": build_va_spec_ready_stub(result),
        },
        "governance_summary": {
            "requires_human_review": requires_review,
            "reason": reason,
            "candidate_for_catalog_promotion": promotion_candidate,
        },
    }


# ── JSON batch ────────────────────────────────────────────────────────────────

@app.post("/reconcile/batch")
def reconcile_batch(req: BatchRequest):
    results = [reconcile_record(record) for record in req.records]
    for result in results:
        queue_review_required(result)
    summary = {
        "total_records": len(results),
        "auto_reconcile": sum(r.review_status == "AUTO_RECONCILE" for r in results),
        "review_required": sum(r.review_status == "REVIEW_REQUIRED" for r in results),
        "cannot_reconcile": sum(r.review_status == "CANNOT_RECONCILE" for r in results),
    }
    return BatchResponse(results=results, summary=summary)


# ── CSV file upload ───────────────────────────────────────────────────────────

@app.post("/reconcile/upload")
async def reconcile_upload(file: UploadFile = File(...)):
    """
    Upload a CSV file with columns: case_id (opt), cancer_type (opt), gene, variant.
    Returns batch reconciliation results + summary.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    text = content.decode("utf-8-sig")  # handle BOM
    reader = csv.DictReader(io.StringIO(text))

    required = {"gene", "variant"}
    if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
        raise HTTPException(
            status_code=422,
            detail=f"CSV must contain columns: {required}. Found: {reader.fieldnames}"
        )

    records = []
    for row in reader:
        records.append(ReconcileRequest(
            case_id=row.get("case_id") or None,
            cancer_type=row.get("cancer_type") or None,
            gene=row["gene"].strip(),
            variant=row["variant"].strip(),
        ))

    if not records:
        raise HTTPException(status_code=400, detail="CSV file is empty.")

    results = [reconcile_record(r) for r in records]
    for result in results:
        queue_review_required(result)

    summary = {
        "total_records": len(results),
        "auto_reconcile": sum(r.review_status == "AUTO_RECONCILE" for r in results),
        "review_required": sum(r.review_status == "REVIEW_REQUIRED" for r in results),
        "cannot_reconcile": sum(r.review_status == "CANNOT_RECONCILE" for r in results),
        "filename": file.filename,
    }
    return BatchResponse(results=results, summary=summary)


# ── Review queue ──────────────────────────────────────────────────────────────

@app.get("/benchmark")
def get_benchmark_metrics():
    """Evaluate benchmark accuracy, coverage, and review rate for demo validation."""
    return benchmark_metrics()


@app.get("/review-queue")
def get_review_queue(status: str = Query(default="pending", enum=["pending", "reviewed", "all"])):
    """Return items in the review queue. Filter by status: pending | reviewed | all."""
    filter_status = None if status == "all" else status
    items = review_store.get_queue(filter_status)
    return ReviewQueueResponse(
        items=items,
        total=len(review_store.get_queue()),
        pending=len(review_store.get_queue("pending")),
        reviewed=len(review_store.get_queue("reviewed")),
    )


@app.get("/review-queue/{case_id}")
def get_review_item(case_id: str):
    """Retrieve a single review queue item by case_id."""
    item = review_store.get_item(case_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found in review queue.")
    return item


@app.get("/review-queue-metrics")
def get_review_queue_metrics():
    """Return reviewer agreement and adjudication metrics."""
    return review_store.agreement_metrics()


@app.post("/review-queue/{case_id}/decision")
def submit_review_decision(case_id: str, decision: ReviewDecision):
    """Submit a curator decision (approve | reject | edit | override) for a case."""
    decision.case_id = case_id
    updated = review_store.apply_decision(decision)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found in review queue.")
    return {"status": "ok", "case_id": case_id, "decision": decision.decision, "item": updated}


@app.post("/review-queue/{case_id}/adjudicate")
def adjudicate_review_decision(case_id: str, decision: ReviewDecision):
    """Resolve a disagreement between two or more curator decisions."""
    decision.case_id = case_id
    updated = review_store.apply_adjudication(decision)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found in review queue.")
    if updated.adjudication_status == "REQUIRED":
        raise HTTPException(status_code=409, detail="Adjudication was not resolved.")
    return {"status": "ok", "case_id": case_id, "item": updated}


@app.delete("/review-queue")
def clear_review_queue():
    """Clear the entire review queue (admin/testing use)."""
    review_store.clear_queue()
    return {"status": "ok", "message": "Review queue cleared."}


from fastapi.responses import Response


# ── FHIR R4 export ──────────────────────────────────────────────────────────


@app.post("/export/fhir")
def export_fhir(payload: dict):
    """
    Export reconciliation result as a FHIR R4 Bundle.

    Maps:
      - Disease (cancer_type) → Condition (SNOMED CT coded)
      - Gene → Observation (LOINC 48018-6, HGNC coded)
      - Variant → Observation (LOINC 69548-6) or MolecularSequence
      - Full result → DiagnosticReport (LOINC 81247-9)
      - Reconciliation activity → Provenance

    Includes a placeholder Patient resource. All resources are wrapped in a
    Bundle of type 'collection'.

    Suitable for integration with FHIR Genomics pipelines, EHR systems, and
    health information exchanges.
    """
    result = resolve_reconciliation_payload(payload)
    canonical = result.get("canonical") or {}
    bundle = build_fhir_bundle(
        canonical=canonical,
        evidence=result.get("evidence"),
        confidence=result.get("confidence"),
        case_id=result.get("case_id"),
        review_status=result.get("review_status"),
        score_breakdown=result.get("score_breakdown"),
        alternatives=result.get("alternatives"),
    )
    return bundle


@app.post("/export/fhir/download")
def export_fhir_download(payload: dict):
    """
    Download reconciliation result as a FHIR R4 Bundle JSON file.

    Same as POST /export/fhir but returns the bundle as a downloadable
    `.json` file with Content-Disposition attachment headers.
    """
    result = resolve_reconciliation_payload(payload)
    canonical = result.get("canonical") or {}
    bundle = build_fhir_bundle(
        canonical=canonical,
        evidence=result.get("evidence"),
        confidence=result.get("confidence"),
        case_id=result.get("case_id"),
        review_status=result.get("review_status"),
        score_breakdown=result.get("score_breakdown"),
        alternatives=result.get("alternatives"),
    )
    import json
    case_id = result.get("case_id") or "unknown"
    content = json.dumps(bundle, indent=2, default=str)
    return Response(
        content=content,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="oncoreconcile-fhir-{case_id}.json"',
        },
    )


@app.post("/export/fhir/batch")
def export_fhir_batch(payload: dict):
    """
    Export multiple reconciliation results as a single FHIR R4 Bundle.

    Accepts either a list of results or a BatchRequest-style payload.
    Each result produces Patient + Condition + Observation + MolecularSequence
    + Provenance + DiagnosticReport resources, all merged into one Bundle.
    """
    results = payload.get("results") if isinstance(payload, dict) and "results" in payload else [payload]
    bundle = build_fhir_bundle_batch(results)
    return bundle


# ── OMOP CDM v5.4 export ────────────────────────────────────────────────────


@app.post("/export/omop")
def export_omop(payload: dict):
    """
    Export reconciliation result as OMOP CDM v5.4 records.

    Maps:
      - Disease (cancer_type) → condition_occurrence (SNOMED→OMOP concept_id)
      - Gene → measurement (LOINC 48018-6 concept_id)
      - Variant → observation (LOINC 69548-6 concept_id)

    Records use placeholder person_id=0. Where OMOP vocabulary concept_ids
    cannot be resolved (unmapped SNOMED/HGNC codes), concept_id is set to 0
    and the source_value preserves the original code for later backfill.
    """
    result = resolve_reconciliation_payload(payload)
    canonical = result.get("canonical") or {}
    omop = build_omop_records(
        canonical=canonical,
        confidence=result.get("confidence"),
        case_id=result.get("case_id"),
        review_status=result.get("review_status"),
        evidence=result.get("evidence"),
        score_breakdown=result.get("score_breakdown"),
        alternatives=result.get("alternatives"),
    )
    return omop


@app.post("/export/omop/download")
def export_omop_download(payload: dict):
    """
    Download OMOP CDM v5.4 records as a JSON file.

    Returns the OMOP records with Content-Disposition attachment headers
    for direct file download.
    """
    result = resolve_reconciliation_payload(payload)
    canonical = result.get("canonical") or {}
    omop = build_omop_records(
        canonical=canonical,
        confidence=result.get("confidence"),
        case_id=result.get("case_id"),
        review_status=result.get("review_status"),
        evidence=result.get("evidence"),
        score_breakdown=result.get("score_breakdown"),
        alternatives=result.get("alternatives"),
    )
    import json
    case_id = result.get("case_id") or "unknown"
    content = json.dumps(omop, indent=2, default=str)
    return Response(
        content=content,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="oncoreconcile-omop-{case_id}.json"',
        },
    )


@app.post("/export/omop/batch")
def export_omop_batch(payload: dict):
    """
    Export multiple reconciliation results as OMOP CDM v5.4 records.

    Accepts either a list of results or a single result. Each result
    produces condition_occurrence + measurement + observation records.
    """
    results = payload.get("results") if isinstance(payload, dict) and "results" in payload else [payload]
    omop = build_omop_records_batch(results)
    return {"omop_records": omop, "total_records": len(omop)}


@app.post("/review-queue/{case_id}/promote")
def promote_review_candidate(case_id: str):
    """Roadmap stub. Catalog promotion remains disabled for the MVP."""
    if not review_store.get_item(case_id):
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found in review queue.")
    return review_store.promote_candidate_to_catalog(case_id)


# ── Evidence & HGVS APIs ──────────────────────────────────────────────────


@app.post("/evidence/federated")
def get_federated_evidence(payload: dict):
    """
    Fetch federated evidence for a gene + variant from all configured sources
    (ClinVar, CIViC, Local Catalog, MyVariant.info).

    Accepts raw input or a reconciliation result. When provided with canonical
    gene/variant, also resolves canonical HGVS.

    Request formats:
      {"gene": "EGFR", "variant": "C797S"}
      {"gene": "EGFR", "variant": "C797S", "cancer_type": "NSCLC"}
      (full reconciliation result)
    """
    # Extract gene/variant from payload
    if "input" in payload and isinstance(payload.get("input"), dict):
        gene = payload["input"].get("gene", "")
        variant = payload["input"].get("variant", "")
        canonical_gene = payload.get("canonical", {}).get("gene")
        canonical_variant = payload.get("canonical", {}).get("variant")
    else:
        gene = payload.get("gene", "")
        variant = payload.get("variant", "")
        canonical_gene = payload.get("canonical_gene") or gene
        canonical_variant = payload.get("canonical_variant") or variant

    # Resolve via reconcile if needed
    if not gene or not variant:
        raise HTTPException(status_code=422, detail="gene and variant are required.")

    result = fetch_federated_evidence(
        gene=gene,
        variant=variant,
        canonical_gene=canonical_gene or gene,
        canonical_variant=canonical_variant or variant,
        local_evidence=payload.get("evidence"),
    )
    return result


@app.post("/hgvs/resolve")
def resolve_hgvs(payload: dict):
    """
    Resolve canonical HGVS (protein, coding, genomic) for a gene + variant.

    Request:
      {"gene": "EGFR", "variant": "C797S"}

    Returns:
      {"canonical_variant": "...", "protein_hgvs": "...", ...}
    """
    gene = payload.get("gene") or payload.get("canonical_gene")
    variant = payload.get("variant") or payload.get("canonical_variant")

    # Fallback to reconciliation result fields
    if not gene or not variant:
        canonical = payload.get("canonical", {})
        gene = gene or canonical.get("gene")
        variant = variant or canonical.get("variant")

    if not gene or not variant:
        raise HTTPException(status_code=422, detail="gene and variant are required.")

    result = get_canonical_hgvs(gene, variant)
    return result


@app.post("/evidence/boost")
def compute_evidence_boost_endpoint(payload: dict):
    """
    Compute confidence score boost from evidence items.

    Accepts a list of unified evidence items (with source, confidence, metadata fields).
    Returns boost breakdown per source.

    Request:
      {"unified_evidence": [...]}
    """
    evidence = payload.get("unified_evidence", [])
    if not evidence:
        return {"evidence_boost": 0.0, "breakdown": {}, "details": ["No evidence provided."]}
    result = compute_evidence_boost(evidence)
    return result


# ── Enterprise Patient Journey APIs ──────────────────────────────────────────


from .enterprise import (
    get_patient_journey_list,
    get_patient_journey_detail,
    compute_analytics_summary,
    compute_analytics_biomarkers,
    compute_analytics_treatments,
    compute_analytics_outcomes,
    compute_data_quality,
    compute_governance_metrics,
    compute_terminology_metrics,
    compute_executive_dashboard,
    build_expanded_fhir_bundle,
    build_expanded_omop_records,
    build_expanded_knowledge_graph,
    build_ai_ready_dataset,
)


@app.get("/enterprise/patient-journey")
def enterprise_patient_journey_list():
    """Return a summary list of all enterprise patient journeys."""
    return {
        "patients": get_patient_journey_list(),
        "total": len(get_patient_journey_list()),
    }


@app.get("/enterprise/patient-journey/{patient_id}")
def enterprise_patient_journey_detail(patient_id: str):
    """Return the full patient journey with timeline and harmonization for a specific patient."""
    detail = get_patient_journey_detail(patient_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")
    return detail


@app.get("/enterprise/analytics/summary")
def enterprise_analytics_summary():
    """Return comprehensive cohort analytics summary."""
    return compute_analytics_summary()


@app.get("/enterprise/analytics/biomarkers")
def enterprise_analytics_biomarkers():
    """Return biomarker-specific analytics across the cohort."""
    return compute_analytics_biomarkers()


@app.get("/enterprise/analytics/treatments")
def enterprise_analytics_treatments():
    """Return treatment-specific analytics across the cohort."""
    return compute_analytics_treatments()


@app.get("/enterprise/analytics/outcomes")
def enterprise_analytics_outcomes():
    """Return outcome-related analytics across the cohort."""
    return compute_analytics_outcomes()


@app.get("/enterprise/analytics/data-quality")
def enterprise_analytics_data_quality():
    """Return data quality metrics with green/yellow/red indicators."""
    return compute_data_quality()


@app.get("/enterprise/analytics/governance")
def enterprise_analytics_governance():
    """Return governance workflow metrics."""
    return compute_governance_metrics()


@app.get("/enterprise/analytics/terminology")
def enterprise_analytics_terminology():
    """Return terminology mapping coverage metrics."""
    return compute_terminology_metrics()


@app.get("/enterprise/executive-dashboard")
def enterprise_executive_dashboard():
    """Return executive summary view with key performance indicators."""
    return compute_executive_dashboard()


@app.get("/enterprise/semantic-harmonization")
def enterprise_semantic_harmonization():
    """Return the full semantic harmonization data with coding system mappings."""
    from .enterprise import load_semantic_harmonization
    return load_semantic_harmonization()


@app.get("/enterprise/coding-system-mappings")
def enterprise_coding_system_mappings():
    """Return a flat list of all coding system mappings for display in CodingCoverageDashboard."""
    from .enterprise import load_semantic_harmonization
    harm = load_semantic_harmonization()
    all_mappings = []
    
    for cat in ["diseases", "histologies", "drugs", "biomarkers", "lab_tests"]:
        cat_data = harm.get(cat, {})
        for entity_key, entity_data in cat_data.items():
            canonical = entity_data.get("canonical_value", entity_key)
            for m in entity_data.get("mappings", []):
                all_mappings.append({
                    "category": cat,
                    "original": entity_key,
                    "canonical": canonical,
                    "coding_system": m.get("coding_system"),
                    "code": m.get("code"),
                    "display_name": m.get("display_name"),
                    "confidence": m.get("confidence", entity_data.get("confidence", 0.85)),
                })
    
    # Add variant aliases
    for alias_key, alias_data in harm.get("variant_aliases", {}).items():
        canonical = alias_data.get("canonical_value", alias_key)
        for m in alias_data.get("mappings", []):
            all_mappings.append({
                "category": "variant_aliases",
                "original": alias_key,
                "canonical": canonical,
                "coding_system": m.get("coding_system"),
                "code": m.get("code"),
                "display_name": m.get("display_name"),
                "confidence": m.get("confidence", alias_data.get("confidence", 0.85)),
            })
    
    return {
        "total_mappings": len(all_mappings),
        "mappings": all_mappings,
        "coding_system_descriptions": harm.get("coding_system_descriptions", {}),
        "variant_canonical_mappings": harm.get("variant_canonical_mappings", []),
    }


@app.get("/enterprise/ai-ready-dataset")
def enterprise_ai_ready_dataset():
    """Return AI-ready standardized dataset from all patient journeys."""
    return build_ai_ready_dataset()


@app.post("/enterprise/export/fhir/{patient_id}")
def enterprise_export_fhir(patient_id: str):
    """Export a patient journey as an expanded FHIR R4 Bundle."""
    detail = get_patient_journey_detail(patient_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")
    return build_expanded_fhir_bundle(detail["patient"])


@app.post("/enterprise/export/omop/{patient_id}")
def enterprise_export_omop(patient_id: str):
    """Export a patient journey as expanded OMOP CDM v5.4 records."""
    detail = get_patient_journey_detail(patient_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")
    return build_expanded_omop_records(detail["patient"])


@app.post("/enterprise/export/knowledge-graph/{patient_id}")
def enterprise_export_knowledge_graph(patient_id: str):
    """Export a patient journey as an expanded enterprise knowledge graph."""
    detail = get_patient_journey_detail(patient_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found.")
    return build_expanded_knowledge_graph(detail["patient"])
