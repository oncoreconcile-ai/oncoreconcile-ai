"""
Enterprise Patient Journey & Analytics Module for OncoReconcile AI.

This module provides:
  - Patient journey data management
  - Cohort analytics and dashboards
  - Data quality and governance metrics
  - Terminology harmonization services
  - Expanded FHIR and OMOP exports
  - Executive dashboards
  - Knowledge graph expansion

All data used is synthetic. No patient data is real.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"


# ── Data Loaders ──────────────────────────────────────────────────────────────

def load_patient_journeys() -> dict:
    """Load the synthetic longitudinal patient journey dataset."""
    path = DATA_DIR / "patient_journey_demo.json"
    if not path.exists():
        return {"patients": [], "summary_statistics": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def load_semantic_harmonization() -> dict:
    """Load the semantic harmonization and coding system mappings."""
    path = DATA_DIR / "semantic_harmonization.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Patient Journey APIs ─────────────────────────────────────────────────────

def get_patient_journey_list() -> list[dict]:
    """Return a summary list of all patient journeys."""
    data = load_patient_journeys()
    patients = data.get("patients", [])
    result = []
    for p in patients:
        result.append({
            "patient_id": p["patient_id"],
            "sex": p["sex"],
            "age_group": p["age_group"],
            "diagnosis": p["diagnosis"],
            "histology": p["histology"],
            "stage": p["stage"],
            "diagnosis_date": p["diagnosis_date"],
            "line_of_therapy": p["line_of_therapy"],
            "genes": p["genes"],
            "drugs": [t["drug"] for t in p.get("treatments", [])],
            "data_quality_score": p["data_quality_score"],
            "reconciliation_status": p["reconciliation_status"],
            "evidence_coverage": p["evidence_coverage"],
            "clinical_trial_count": len(p.get("clinical_trial_flags", [])),
            "progression_count": len(p.get("progression_events", [])),
        })
    return result


def get_patient_journey_detail(patient_id: str) -> Optional[dict]:
    """Return the full patient journey for a specific patient."""
    data = load_patient_journeys()
    patients = data.get("patients", [])
    for p in patients:
        if p["patient_id"] == patient_id:
            journey = build_journey_timeline(p)
            harmonization = harmonize_patient_entities(p)
            return {
                "patient": p,
                "journey_timeline": journey,
                "harmonization": harmonization,
                "summary_statistics": data.get("summary_statistics"),
            }
    return None


def build_journey_timeline(patient: dict) -> list[dict]:
    """Build a chronological timeline of events for a patient journey."""
    events = []

    # Diagnosis
    events.append({
        "event_type": "diagnosis",
        "title": f"Diagnosis: {patient['diagnosis']}",
        "date": patient["diagnosis_date"],
        "description": f"{patient['histology']} - Stage {patient['stage']}",
        "details": {"histology": patient["histology"], "stage": patient["stage"]},
    })

    # Biomarker tests
    for test in patient.get("biomarker_tests", []):
        events.append({
            "event_type": "biomarker_test",
            "title": f"Test: {test['test']}",
            "date": test["date"],
            "description": f"Method: {test['method']}, Sample: {test['sample_type']}",
            "details": test,
        })

    # Treatments and responses
    for tx in patient.get("treatments", []):
        events.append({
            "event_type": "treatment",
            "title": f"Line {tx['line_of_therapy']}: {tx['drug']}",
            "date": tx["start_date"],
            "description": tx["regimen"],
            "details": tx,
        })

    # Responses
    for resp in patient.get("response", []):
        if resp.get("date"):
            events.append({
                "event_type": "response",
                "title": f"Response Assessment: {resp['assessment']}",
                "date": resp["date"],
                "description": f"Line {resp['line_of_therapy']}: {resp.get('recist', 'N/A')}",
                "details": resp,
            })

    # Progression events
    for prog in patient.get("progression_events", []):
        events.append({
            "event_type": "progression",
            "title": f"Progression: {prog['event']}",
            "date": prog["date"],
            "description": prog.get("notes", ""),
            "details": prog,
        })

    # Sort by date
    events.sort(key=lambda e: (e.get("date") or "", e["event_type"]))
    return events


def harmonize_patient_entities(patient: dict) -> dict:
    """Harmonize patient entities using the semantic harmonization layer."""
    harm = load_semantic_harmonization()
    disease_harm = harm.get("diseases", {}).get(patient["diagnosis"], {})
    histology_harm = harm.get("histologies", {}).get(patient["histology"], {})

    gene_harmonizations = []
    for gene in patient.get("genes", []):
        g = harm.get("genes", {}).get(gene, {})
        gene_harmonizations.append({
            "original": gene,
            "canonical_value": g.get("canonical_value", gene),
            "hgnc_id": g.get("hgnc_id"),
            "hgnc_name": g.get("hgnc_name"),
            "confidence": g.get("confidence"),
            "review_status": g.get("review_status", "UNKNOWN"),
        })

    drug_harmonizations = []
    for tx in patient.get("treatments", []):
        drug_name = tx["drug"]
        d = harm.get("drugs", {}).get(drug_name, {})
        drug_harmonizations.append({
            "original": drug_name,
            "canonical_value": d.get("canonical_value", drug_name),
            "mappings": d.get("mappings", []),
            "confidence": d.get("confidence"),
            "review_status": d.get("review_status", "UNKNOWN"),
        })

    return {
        "disease": {
            "original": patient["diagnosis"],
            "canonical_value": disease_harm.get("canonical_value", patient["diagnosis"]),
            "mappings": disease_harm.get("mappings", []),
            "provenance": disease_harm.get("provenance"),
            "confidence": disease_harm.get("confidence"),
        },
        "histology": {
            "original": patient["histology"],
            "canonical_value": histology_harm.get("canonical_value", patient["histology"]),
            "mappings": histology_harm.get("mappings", []),
            "confidence": histology_harm.get("confidence"),
        },
        "genes": gene_harmonizations,
        "drugs": drug_harmonizations,
    }


# ── Analytics ─────────────────────────────────────────────────────────────────

def compute_analytics_summary() -> dict:
    """Compute comprehensive analytics across all patients."""
    data = load_patient_journeys()
    patients = data.get("patients", [])
    stats = data.get("summary_statistics", {})

    if not patients:
        return {"error": "No patient data available"}

    total = len(patients)

    # Cancer type distribution
    cancer_types = {}
    for p in patients:
        diag = p["diagnosis"]
        cancer_types[diag] = cancer_types.get(diag, 0) + 1

    # Stage distribution
    stages = {}
    for p in patients:
        s = p["stage"]
        stages[s] = stages.get(s, 0) + 1

    # Sex distribution
    sex_dist = {}
    for p in patients:
        s = p["sex"]
        sex_dist[s] = sex_dist.get(s, 0) + 1

    # Age groups
    age_groups = {}
    for p in patients:
        a = p["age_group"]
        age_groups[a] = age_groups.get(a, 0) + 1

    # Gene frequency
    gene_freq = {}
    for p in patients:
        for g in p.get("genes", []):
            gene_freq[g] = gene_freq.get(g, 0) + 1

    # Variant frequency
    variant_freq = {}
    for p in patients:
        for v in p.get("variants", []):
            key = f"{v['gene']} {v['variant']}"
            variant_freq[key] = variant_freq.get(key, 0) + 1

    # Drug frequency
    drug_freq = {}
    for p in patients:
        drugs = list(set(t["drug"] for t in p.get("treatments", [])))
        for d in drugs:
            drug_freq[d] = drug_freq.get(d, 0) + 1

    # Regimen frequency
    regimen_freq = {}
    for p in patients:
        for t in p.get("treatments", []):
            regimen_freq[t["regimen"]] = regimen_freq.get(t["regimen"], 0) + 1

    # Response distribution
    resp_dist = {}
    for p in patients:
        for r in p.get("response", []):
            resp_dist[r["assessment"]] = resp_dist.get(r["assessment"], 0) + 1

    # Lines of therapy
    lot_counts = {i: 0 for i in range(1, 6)}
    for p in patients:
        lot = p["line_of_therapy"]
        lot_counts[lot] = lot_counts.get(lot, 0) + 1

    # Progression rate
    progressed = sum(1 for p in patients if len(p.get("progression_events", [])) > 0)
    progression_rate = progressed / total if total > 0 else 0

    # Clinical trial eligible
    trial_eligible = sum(1 for p in patients if len(p.get("clinical_trial_flags", [])) > 0)
    trial_rate = trial_eligible / total if total > 0 else 0

    # Review required
    review_required = sum(1 for p in patients if p.get("reconciliation_status") == "REVIEW_REQUIRED")
    review_rate = review_required / total if total > 0 else 0

    # Biomarker testing rate (patients with at least one test)
    tested = sum(1 for p in patients if len(p.get("biomarker_tests", [])) > 0)
    biomarker_rate = tested / total if total > 0 else 0

    # Average scores
    avg_dq = sum(p.get("data_quality_score", 0) for p in patients) / total if total > 0 else 0
    avg_ev = sum(p.get("evidence_coverage", 0) for p in patients) / total if total > 0 else 0

    # Reconciliation coverage
    auto = sum(1 for p in patients if p.get("reconciliation_status") == "AUTO_RECONCILE")
    cannot = sum(1 for p in patients if p.get("reconciliation_status") == "CANNOT_RECONCILE")

    # Top 5 of each
    top_genes = sorted(gene_freq.items(), key=lambda x: -x[1])[:10]
    top_variants = sorted(variant_freq.items(), key=lambda x: -x[1])[:10]
    top_drugs = sorted(drug_freq.items(), key=lambda x: -x[1])[:10]

    # AI Readiness Score: composite of data quality, evidence coverage,
    # biomarker testing rate, and reconciliation coverage
    ai_readiness = round(
        (avg_dq * 0.3) +
        (avg_ev * 0.25) +
        (biomarker_rate * 0.25) +
        (auto / total if total > 0 else 0) * 0.2,
        4
    )

    return {
        "total_patients": total,
        "cancer_type_distribution": cancer_types,
        "stage_distribution": stages,
        "sex_distribution": sex_dist,
        "age_group_distribution": age_groups,
        "gene_frequency": dict(top_genes),
        "variant_frequency": dict(top_variants),
        "drug_frequency": dict(top_drugs),
        "regimen_frequency": regimen_freq,
        "response_distribution": resp_dist,
        "line_of_therapy_distribution": lot_counts,
        "progression_rate": round(progression_rate, 4),
        "clinical_trial_eligibility_rate": round(trial_rate, 4),
        "review_required_rate": round(review_rate, 4),
        "biomarker_testing_rate": round(biomarker_rate, 4),
        "average_data_quality_score": round(avg_dq, 4),
        "average_evidence_coverage": round(avg_ev, 4),
        "reconciliation_coverage": {
            "auto_reconcile": auto,
            "review_required": review_required,
            "cannot_reconcile": cannot,
            "total": total,
        },
        "ai_readiness_score": ai_readiness,
    }


def compute_analytics_biomarkers() -> dict:
    """Compute biomarker-specific analytics."""
    data = load_patient_journeys()
    patients = data.get("patients", [])

    all_genes = {}
    all_variants = {}
    biomarker_methods = {}
    biomarker_types = {}

    for p in patients:
        for v in p.get("variants", []):
            gene = v["gene"]
            if gene not in all_genes:
                all_genes[gene] = {"count": 0, "patients": []}
            all_genes[gene]["count"] += 1
            all_genes[gene]["patients"].append(p["patient_id"])

            var_key = f"{gene}:{v['variant']}"
            if var_key not in all_variants:
                all_variants[var_key] = {"count": 0, "patients": [], "classification": v["classification"]}
            all_variants[var_key]["count"] += 1
            all_variants[var_key]["patients"].append(p["patient_id"])

        for test in p.get("biomarker_tests", []):
            method = test["method"]
            biomarker_methods[method] = biomarker_methods.get(method, 0) + 1
            test_type = test["test"]
            biomarker_types[test_type] = biomarker_types.get(test_type, 0) + 1

    # Fusions
    fusions = []
    for p in patients:
        for f in p.get("fusions", []):
            fusions.append({
                "fusion": f["fusion"],
                "type": f["type"],
                "patient_id": p["patient_id"],
            })

    # Copy number alterations
    cnas = {}
    for p in patients:
        for cna in p.get("copy_number_alterations", []):
            gene = cna["gene"]
            if gene not in cnas:
                cnas[gene] = {"amplifications": 0, "deletions": 0, "patients": []}
            if "Amplification" in cna.get("alteration", ""):
                cnas[gene]["amplifications"] += 1
            else:
                cnas[gene]["deletions"] += 1
            cnas[gene]["patients"].append(p["patient_id"])

    return {
        "genes_identified": len(all_genes),
        "variants_identified": len(all_variants),
        "total_biomarker_tests": sum(len(p.get("biomarker_tests", [])) for p in patients),
        "gene_details": all_genes,
        "variant_details": all_variants,
        "test_methods": biomarker_methods,
        "test_types": biomarker_types,
        "fusions": fusions,
        "copy_number_alterations": cnas,
        "patients_with_fusions": len([p for p in patients if p.get("fusions")]),
        "patients_with_cna": len([p for p in patients if p.get("copy_number_alterations")]),
    }


def compute_analytics_treatments() -> dict:
    """Compute treatment-specific analytics."""
    data = load_patient_journeys()
    patients = data.get("patients", [])

    drug_details = {}
    regimen_details = {}
    class_details = {}
    lot_details = {}

    for p in patients:
        for tx in p.get("treatments", []):
            drug = tx["drug"]
            if drug not in drug_details:
                drug_details[drug] = {"count": 0, "patients": [], "lines_of_therapy": []}
            drug_details[drug]["count"] += 1
            drug_details[drug]["patients"].append(p["patient_id"])
            drug_details[drug]["lines_of_therapy"].append(tx["line_of_therapy"])

            regimen = tx["regimen"]
            if regimen not in regimen_details:
                regimen_details[regimen] = {"count": 0, "patients": [], "drug": drug}
            regimen_details[regimen]["count"] += 1
            regimen_details[regimen]["patients"].append(p["patient_id"])

            drug_class = tx["class"]
            if drug_class not in class_details:
                class_details[drug_class] = {"count": 0, "patients": [], "drugs": []}
            class_details[drug_class]["count"] += 1
            class_details[drug_class]["patients"].append(p["patient_id"])
            if drug not in class_details[drug_class]["drugs"]:
                class_details[drug_class]["drugs"].append(drug)

            lot = tx["line_of_therapy"]
            if lot not in lot_details:
                lot_details[lot] = {"count": 0}
            lot_details[lot]["count"] += 1

    return {
        "total_treatment_lines": sum(len(p.get("treatments", [])) for p in patients),
        "unique_drugs": len(drug_details),
        "drug_details": drug_details,
        "regimen_details": regimen_details,
        "drug_class_details": class_details,
        "line_of_therapy_details": lot_details,
    }


def compute_analytics_outcomes() -> dict:
    """Compute outcome-related analytics."""
    data = load_patient_journeys()
    patients = data.get("patients", [])

    outcome_by_diagnosis = {}
    progression_by_diagnosis = {}
    lot_success_rates = {}

    for p in patients:
        diag = p["diagnosis"]

        if diag not in outcome_by_diagnosis:
            outcome_by_diagnosis[diag] = {"CR": 0, "PR": 0, "SD": 0, "PD": 0, "other": 0}
        if diag not in progression_by_diagnosis:
            progression_by_diagnosis[diag] = {"progressed": 0, "total": 0}
        progression_by_diagnosis[diag]["total"] += 1

        has_progressed = len(p.get("progression_events", [])) > 0
        if has_progressed:
            progression_by_diagnosis[diag]["progressed"] += 1

        for resp in p.get("response", []):
            assessment = resp["assessment"]
            if "Complete" in assessment:
                outcome_by_diagnosis[diag]["CR"] += 1
            elif "Partial" in assessment:
                outcome_by_diagnosis[diag]["PR"] += 1
            elif "Stable" in assessment:
                outcome_by_diagnosis[diag]["SD"] += 1
            elif "Progressive" in assessment:
                outcome_by_diagnosis[diag]["PD"] += 1
            else:
                outcome_by_diagnosis[diag]["other"] += 1

        lot = p["line_of_therapy"]
        if lot not in lot_success_rates:
            lot_success_rates[lot] = {"patients": 0, "with_response": 0}
        lot_success_rates[lot]["patients"] += 1
        best_responses = [r["assessment"] for r in p.get("response", []) if r["line_of_therapy"] == lot]
        if any("Complete" in r or "Partial" in r for r in best_responses):
            lot_success_rates[lot]["with_response"] += 1

    # Progression-free survival proxy (months between diagnosis and first progression)
    pfs_data = []
    for p in patients:
        from datetime import datetime
        diag_date = p.get("diagnosis_date")
        progs = p.get("progression_events", [])
        if diag_date and progs:
            try:
                diag_dt = datetime.strptime(diag_date, "%Y-%m-%d")
                first_prog = min(progs, key=lambda x: x.get("date", ""))
                prog_dt = datetime.strptime(first_prog["date"], "%Y-%m-%d")
                months = (prog_dt.year - diag_dt.year) * 12 + (prog_dt.month - diag_dt.month)
                pfs_data.append({
                    "patient_id": p["patient_id"],
                    "diagnosis": p["diagnosis"],
                    "pfs_months": months,
                })
            except (ValueError, KeyError):
                pass

    return {
        "outcome_by_diagnosis": outcome_by_diagnosis,
        "progression_by_diagnosis": progression_by_diagnosis,
        "line_of_therapy_success_rates": lot_success_rates,
        "progression_free_survival_proxy": pfs_data,
        "total_progression_events": sum(len(p.get("progression_events", [])) for p in patients),
    }


# ── Data Quality and Governance ───────────────────────────────────────────────

def compute_data_quality() -> dict:
    """Compute data quality metrics across the patient cohort."""
    data = load_patient_journeys()
    patients = data.get("patients", [])
    total = len(patients)

    if total == 0:
        return {"error": "No patient data available"}

    # Missing data tracking
    missing_stage = sum(1 for p in patients if not p.get("stage"))
    missing_biomarker = sum(1 for p in patients if not p.get("biomarker_tests"))
    missing_treatment = sum(1 for p in patients if not p.get("treatments"))
    missing_genes = sum(1 for p in patients if not p.get("genes"))
    missing_variants = sum(1 for p in patients if not p.get("variants"))
    missing_response = sum(1 for p in patients if not p.get("response"))
    missing_histology = sum(1 for p in patients if not p.get("histology"))

    review_required = sum(1 for p in patients if p.get("review_required_count", 0) > 0)
    total_review_needed = sum(p.get("review_required_count", 0) for p in patients)

    # Average data quality score
    avg_dq = sum(p.get("data_quality_score", 0) for p in patients) / total if total else 0

    # Evidence coverage rate
    avg_ev = sum(p.get("evidence_coverage", 0) for p in patients) / total if total else 0

    # Data completeness score (composite)
    completeness_fields = {
        "stage": (total - missing_stage) / total,
        "biomarker": (total - missing_biomarker) / total,
        "treatment": (total - missing_treatment) / total,
        "genes": (total - missing_genes) / total,
        "response": (total - missing_response) / total,
        "histology": (total - missing_histology) / total,
    }
    data_completeness = round(sum(completeness_fields.values()) / len(completeness_fields), 4) if completeness_fields else 0

    # Coding coverage (from semantic harmonization)
    harm = load_semantic_harmonization()
    disease_count = len(harm.get("diseases", {}))
    histology_count = len(harm.get("histologies", {}))
    gene_count = len(harm.get("genes", {}))
    drug_count = len(harm.get("drugs", {}))

    total_coded_entities = disease_count + histology_count + gene_count + drug_count
    total_mappings = sum(
        len(d.get("mappings", []))
        for cat in ["diseases", "histologies", "drugs"]
        for d in harm.get(cat, {}).values()
    )
    coding_coverage = round(total_mappings / max(total_coded_entities, 1), 4)

    # Semantic harmonization coverage
    total_patient_entities = 0
    harmonized_entities = 0
    for p in patients:
        if p.get("diagnosis") in harm.get("diseases", {}):
            harmonized_entities += 1
        total_patient_entities += 1
        for g in p.get("genes", []):
            total_patient_entities += 1
            if g in harm.get("genes", {}):
                harmonized_entities += 1
        drugs_in_patient = list(set(t["drug"] for t in p.get("treatments", []) if t.get("drug")))
        total_patient_entities += len(drugs_in_patient)
        harmonized_entities += sum(1 for d in drugs_in_patient if d in harm.get("drugs", {}))

    sem_harm_coverage = round(harmonized_entities / max(total_patient_entities, 1), 4) if total_patient_entities else 0

    # Threshold-based indicators
    def indicator(value, green=0.9, yellow=0.7):
        if value >= green:
            return "green"
        elif value >= yellow:
            return "yellow"
        return "red"

    return {
        "total_patients": total,
        "missing_data": {
            "missing_stage": missing_stage,
            "missing_biomarker": missing_biomarker,
            "missing_treatment": missing_treatment,
            "missing_genes": missing_genes,
            "missing_variants": missing_variants,
            "missing_response": missing_response,
            "missing_histology": missing_histology,
        },
        "missing_data_rates": {
            "stage_missing_rate": round(missing_stage / total, 4) if total else 0,
            "biomarker_missing_rate": round(missing_biomarker / total, 4) if total else 0,
            "treatment_missing_rate": round(missing_treatment / total, 4) if total else 0,
            "genes_missing_rate": round(missing_genes / total, 4) if total else 0,
            "variants_missing_rate": round(missing_variants / total, 4) if total else 0,
            "response_missing_rate": round(missing_response / total, 4) if total else 0,
            "histology_missing_rate": round(missing_histology / total, 4) if total else 0,
        },
        "review_metrics": {
            "review_required_cases": review_required,
            "total_review_items": total_review_needed,
            "review_required_rate": round(review_required / total, 4) if total else 0,
        },
        "quality_scores": {
            "average_data_quality_score": round(avg_dq, 4),
            "average_evidence_coverage": round(avg_ev, 4),
            "data_completeness": data_completeness,
            "coding_coverage": coding_coverage,
            "evidence_coverage": round(avg_ev, 4),
            "semantic_harmonization_coverage": sem_harm_coverage,
        },
        "indicators": {
            "data_completeness": indicator(data_completeness),
            "coding_coverage": indicator(coding_coverage),
            "evidence_coverage": indicator(avg_ev),
            "semantic_harmonization_coverage": indicator(sem_harm_coverage),
            "missing_stage": "red" if missing_stage > 0 else "green",
            "missing_biomarker": indicator(1 - (missing_biomarker / total) if total else 1),
            "missing_treatment": indicator(1 - (missing_treatment / total) if total else 1),
        },
        "harmonization": {
            "diseases_mapped": disease_count,
            "histologies_mapped": histology_count,
            "genes_mapped": gene_count,
            "drugs_mapped": drug_count,
            "total_mappings": total_mappings,
        },
    }


def compute_governance_metrics() -> dict:
    """Compute governance workflow metrics."""
    data = load_patient_journeys()
    patients = data.get("patients", [])
    total = len(patients)

    review_by_status = {}
    review_by_cancer_type = {}

    for p in patients:
        status = p.get("reconciliation_status", "UNKNOWN")
        review_by_status[status] = review_by_status.get(status, 0) + 1

        diag = p.get("diagnosis", "UNKNOWN")
        if diag not in review_by_cancer_type:
            review_by_cancer_type[diag] = {"total": 0, "AUTO_RECONCILE": 0, "REVIEW_REQUIRED": 0, "CANNOT_RECONCILE": 0}
        review_by_cancer_type[diag]["total"] += 1
        review_by_cancer_type[diag][status] = review_by_cancer_type[diag].get(status, 0) + 1

    auto = review_by_status.get("AUTO_RECONCILE", 0)
    review_req = review_by_status.get("REVIEW_REQUIRED", 0)
    cannot = review_by_status.get("CANNOT_RECONCILE", 0)

    governance_score = round(
        (auto * 1.0 + review_req * 0.5 + cannot * 0.0) / max(total, 1),
        4
    )

    return {
        "total_patients": total,
        "reconciliation_status_counts": review_by_status,
        "auto_reconcile_rate": round(auto / total, 4) if total else 0,
        "review_required_rate": round(review_req / total, 4) if total else 0,
        "cannot_reconcile_rate": round(cannot / total, 4) if total else 0,
        "governance_score": governance_score,
        "breakdown_by_cancer_type": review_by_cancer_type,
    }


def compute_terminology_metrics() -> dict:
    """Compute terminology mapping coverage metrics."""
    harm = load_semantic_harmonization()

    categories = {
        "diseases": {"mapped": 0, "total": 0},
        "histologies": {"mapped": 0, "total": 0},
        "genes": {"mapped": 0, "total": 0},
        "drugs": {"mapped": 0, "total": 0},
        "biomarkers": {"mapped": 0, "total": 0},
        "lab_tests": {"mapped": 0, "total": 0},
    }

    coding_system_counts = {}

    for cat_key, cat_label in [("diseases", "diseases"), ("histologies", "histologies"),
                                 ("drugs", "drugs"), ("biomarkers", "biomarkers"),
                                 ("lab_tests", "lab_tests")]:
        cat_data = harm.get(cat_label, {})
        categories[cat_key]["total"] = len(cat_data)
        for entity_key, entity_data in cat_data.items():
            mappings = entity_data.get("mappings", [])
            if mappings:
                categories[cat_key]["mapped"] += 1
            for m in mappings:
                sys = m.get("coding_system", "UNKNOWN")
                if sys not in coding_system_counts:
                    coding_system_counts[sys] = {"codes": 0, "entities": set()}
                coding_system_counts[sys]["codes"] += 1
                coding_system_counts[sys]["entities"].add(entity_key)

    # Genes always have HGNC
    for g in harm.get("genes", {}):
        categories["genes"]["mapped"] += 1

    # Convert entity sets to counts
    for sys in coding_system_counts:
        coding_system_counts[sys]["entity_count"] = len(coding_system_counts[sys]["entities"])
        del coding_system_counts[sys]["entities"]

    return {
        "categories": categories,
        "total_mapped": sum(c["mapped"] for c in categories.values()),
        "total_entities": sum(c["total"] for c in categories.values()),
        "coding_systems_used": list(coding_system_counts.keys()),
        "coding_system_details": coding_system_counts,
        "terminology_coverage_rate": round(
            sum(c["mapped"] for c in categories.values()) / max(sum(c["total"] for c in categories.values()), 1),
            4
        ),
    }


# ── Executive Dashboard ───────────────────────────────────────────────────────

def compute_executive_dashboard() -> dict:
    """Compute the executive summary view."""
    analytics = compute_analytics_summary()
    dq = compute_data_quality()
    gov = compute_governance_metrics()
    term = compute_terminology_metrics()

    ai_readiness = analytics.get("ai_readiness_score", 0)
    governance_score = gov.get("governance_score", 0)
    reconciliation_coverage = analytics.get("reconciliation_coverage", {})
    auto_rate = reconciliation_coverage.get("auto_reconcile", 0) / max(reconciliation_coverage.get("total", 1), 1)

    return {
        "patients_managed": analytics.get("total_patients", 0),
        "data_quality_score": dq.get("quality_scores", {}).get("average_data_quality_score", 0),
        "governance_score": governance_score,
        "reconciliation_coverage": round(auto_rate, 4),
        "coding_coverage": dq.get("quality_scores", {}).get("coding_coverage", 0),
        "evidence_coverage": dq.get("quality_scores", {}).get("evidence_coverage", 0),
        "semantic_harmonization_coverage": dq.get("quality_scores", {}).get("semantic_harmonization_coverage", 0),
        "ai_readiness_score": ai_readiness,
        "most_common_cancer_types": list(analytics.get("cancer_type_distribution", {}).keys())[:5],
        "most_common_biomarkers": [v.split(" ")[0] for v in list(analytics.get("variant_frequency", {}).keys())[:5]],
        "total_terminology_mappings": term.get("total_mapped", 0),
        "status": "operational",
    }


# ── Expanded FHIR Export ──────────────────────────────────────────────────────

def build_expanded_fhir_bundle(patient: dict) -> dict:
    """
    Build an expanded FHIR R4 Bundle from a patient journey, supporting:
      - Patient
      - Condition (disease, histology)
      - Observation (biomarker tests, gene, variant)
      - DiagnosticReport (comprehensive NGS report)
      - MedicationStatement (treatments)
      - Procedure (biopsies, infusions, transplant)
      - Provenance
    """
    from .fhir_export import _uuid, _now_iso, SNOMED_DISEASE_MAP, HGNC_GENE_MAP, HGNC_GENE_NAME

    bundle_id = _uuid()
    entries = []

    # Patient
    patient_id = _uuid()
    gender = "female" if patient.get("sex") == "F" else "male"
    entries.append({
        "fullUrl": f"urn:uuid:{patient_id}",
        "resource": {
            "resourceType": "Patient",
            "id": patient_id,
            "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Patient"]},
            "identifier": [{
                "system": "https://oncoreconcile.ai/fhir/patient",
                "value": patient["patient_id"],
            }],
            "gender": gender,
        },
    })

    # Condition - disease
    disease = patient.get("diagnosis", "")
    snomed = SNOMED_DISEASE_MAP.get(disease)
    disease_id = _uuid()
    disease_entry = {
        "fullUrl": f"urn:uuid:{disease_id}",
        "resource": {
            "resourceType": "Condition",
            "id": disease_id,
            "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Condition"]},
            "subject": {"reference": f"urn:uuid:{patient_id}"},
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": snomed[0], "display": snomed[1]}] if snomed else [],
                "text": disease,
            },
            "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
            "onsetPeriod": {"start": patient.get("diagnosis_date")},
        },
    }

    # Add stage as extension
    if patient.get("stage"):
        disease_entry["resource"]["stage"] = [{
            "summary": {"text": f"Stage {patient['stage']}"}
        }]
    entries.append(disease_entry)

    # Observations for biomarker tests
    for test in patient.get("biomarker_tests", []):
        obs_id = _uuid()
        entries.append({
            "fullUrl": f"urn:uuid:{obs_id}",
            "resource": {
                "resourceType": "Observation",
                "id": obs_id,
                "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Observation"]},
                "status": "final",
                "code": {"text": test["test"]},
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "effectiveDateTime": test.get("date", ""),
                "valueString": f"Method: {test['method']}, Sample: {test['sample_type']}",
            },
        })

    # Gene and variant observations
    for v in patient.get("variants", []):
        gene = v["gene"]
        variant = v["variant"]
        hgnc = HGNC_GENE_MAP.get(gene)
        gene_name = HGNC_GENE_NAME.get(gene)

        # Gene observation
        gene_obs_id = _uuid()
        entries.append({
            "fullUrl": f"urn:uuid:{gene_obs_id}",
            "resource": {
                "resourceType": "Observation",
                "id": gene_obs_id,
                "meta": {"profile": ["http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/gene"]},
                "status": "final",
                "code": {"coding": [{"system": "http://loinc.org", "code": "48018-6", "display": "Gene studied ID"}]},
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "valueCodeableConcept": {
                    "coding": [{"system": "http://www.genenames.org/geneId", "code": hgnc or gene, "display": gene_name or gene}],
                },
                "interpretation": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", "code": "CAR", "display": "Carrier"}]}],
            },
        })

        # Variant observation
        var_obs_id = _uuid()
        entries.append({
            "fullUrl": f"urn:uuid:{var_obs_id}",
            "resource": {
                "resourceType": "Observation",
                "id": var_obs_id,
                "meta": {"profile": ["http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant"]},
                "status": "final",
                "code": {"coding": [{"system": "http://loinc.org", "code": "69548-6", "display": "Genetic variant assessment"}]},
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "valueCodeableConcept": {"text": f"{gene} {variant}"},
                "component": [{
                    "code": {"coding": [{"system": "http://loinc.org", "code": "48018-6", "display": "Gene studied ID"}]},
                    "valueCodeableConcept": {
                        "coding": [{"system": "http://www.genenames.org/geneId", "code": hgnc or gene, "display": gene_name or gene}],
                    },
                }, {
                    "code": {"coding": [{"system": "http://loinc.org", "code": "81258-6", "display": "Variant category"}]},
                    "valueCodeableConcept": {"text": variant},
                }],
                "interpretation": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", "code": v.get("classification") == "Oncogenic" and "ABN" or "N"}]}],
            },
        })

    # Fusions
    for f in patient.get("fusions", []):
        fusion_obs_id = _uuid()
        entries.append({
            "fullUrl": f"urn:uuid:{fusion_obs_id}",
            "resource": {
                "resourceType": "Observation",
                "id": fusion_obs_id,
                "status": "final",
                "code": {"coding": [{"system": "http://loinc.org", "code": "82121-5", "display": "Gene fusion analysis"}]},
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "valueCodeableConcept": {"text": f["fusion"]},
            },
        })

    # Copy Number Alterations
    for cna in patient.get("copy_number_alterations", []):
        cna_obs_id = _uuid()
        entries.append({
            "fullUrl": f"urn:uuid:{cna_obs_id}",
            "resource": {
                "resourceType": "Observation",
                "id": cna_obs_id,
                "status": "final",
                "code": {"coding": [{"system": "http://loinc.org", "code": "82122-3", "display": "Gene copy number assessment"}]},
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "valueString": f"{cna['gene']} {cna['alteration']}: copy number {cna.get('copy_number', 'N/A')}",
            },
        })

    # MedicationStatement for each treatment
    for tx in patient.get("treatments", []):
        med_id = _uuid()
        med_entry = {
            "fullUrl": f"urn:uuid:{med_id}",
            "resource": {
                "resourceType": "MedicationStatement",
                "id": med_id,
                "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/MedicationStatement"]},
                "status": "completed" if tx.get("end_date") else "active",
                "medicationCodeableConcept": {"text": tx["drug"]},
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "effectivePeriod": {
                    "start": tx.get("start_date"),
                    "end": tx.get("end_date") if tx.get("end_date") else None,
                },
                "dosage": [{"text": tx.get("regimen", "")}],
                "reasonCode": [{"text": f"Line {tx['line_of_therapy']}: {disease}"}],
            },
        }
        entries.append(med_entry)

    # Procedure for key interventions (stem cell transplant as example)
    if patient.get("diagnosis") == "Acute Myeloid Leukemia":
        proc_id = _uuid()
        entries.append({
            "fullUrl": f"urn:uuid:{proc_id}",
            "resource": {
                "resourceType": "Procedure",
                "id": proc_id,
                "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/Procedure"]},
                "status": "completed",
                "code": {"coding": [{"system": "http://snomed.info/sct", "code": "106880006", "display": "Bone marrow transplant"}]},
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "performedPeriod": {"start": "2023-09-01", "end": "2023-09-20"},
            },
        })

    # Provenance
    prov_id = _uuid()
    target_refs = [{"reference": e["fullUrl"]} for e in entries if e["resource"]["resourceType"] != "Patient"]
    entries.append({
        "fullUrl": f"urn:uuid:{prov_id}",
        "resource": {
            "resourceType": "Provenance",
            "id": prov_id,
            "target": target_refs,
            "recorded": _now_iso(),
            "activity": {"coding": [{"system": "https://oncoreconcile.ai/fhir/CodeSystem/reconciliation-activity", "code": "patient-journey-harmonization", "display": "Patient journey semantic harmonization"}]},
            "agent": [{"type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type", "code": "device"}]}, "who": {"identifier": {"system": "https://oncoreconcile.ai/fhir/device-identifier", "value": "OncoReconcile-AI"}}}],
        },
    })

    return {
        "resourceType": "Bundle",
        "id": bundle_id,
        "meta": {"lastUpdated": _now_iso(), "tag": [{"system": "https://oncoreconcile.ai/fhir/tags", "code": "oncoreconcile-patient-journey", "display": "OncoReconcile AI Patient Journey FHIR Export"}]},
        "type": "collection",
        "timestamp": _now_iso(),
        "entry": entries,
    }


# ── Expanded OMOP Export ─────────────────────────────────────────────────────

def build_expanded_omop_records(patient: dict) -> dict:
    """
    Build expanded OMOP CDM records from a patient journey, supporting:
      - condition_occurrence (disease + histology)
      - measurement (biomarker tests)
      - observation (genes, variants, fusions, CNA)
      - drug_exposure (treatments)
      - procedure_occurrence (key procedures)
    """
    person_id = f"PERSON-{patient['patient_id']}"
    disease = patient.get("diagnosis", "")

    records = {
        "person_source_value": patient["patient_id"],
        "gender_source_value": "F" if patient.get("sex") == "F" else "M",
        "condition_occurrences": [],
        "measurements": [],
        "observations": [],
        "drug_exposures": [],
        "procedure_occurrences": [],
        "metadata": {
            "cdm_version": "5.4",
            "source": "OncoReconcile AI Patient Journey OMOP Export",
            "generated_at": _now_iso(),
            "note": "Concept IDs are 0 for unmapped entries. Connect an OMOP vocabulary database to resolve full concept_ids.",
        },
    }

    # Condition occurrence - disease
    records["condition_occurrences"].append({
        "condition_occurrence_id": str(uuid.uuid4()),
        "person_id": person_id,
        "condition_concept_id": 0,
        "condition_start_date": patient.get("diagnosis_date", ""),
        "condition_source_value": disease,
        "condition_type_concept_id": 0,
        "stop_reason": None,
        "_oncoreconcile_metadata": {"diagnosis": disease, "stage": patient.get("stage")},
    })

    # Measurements - biomarker tests
    for test in patient.get("biomarker_tests", []):
        records["measurements"].append({
            "measurement_id": str(uuid.uuid4()),
            "person_id": person_id,
            "measurement_concept_id": 0,
            "measurement_date": test.get("date", ""),
            "measurement_source_value": test["test"],
            "measurement_type_concept_id": 0,
            "value_source_value": f"Method: {test['method']}",
        })

    # Observations - genes, variants, fusions, CNA
    for v in patient.get("variants", []):
        records["observations"].append({
            "observation_id": str(uuid.uuid4()),
            "person_id": person_id,
            "observation_concept_id": 0,
            "observation_date": patient.get("diagnosis_date", ""),
            "observation_source_value": f"Gene: {v['gene']}",
            "value_as_string": v["variant"],
            "qualifier_source_value": v.get("classification", ""),
            "observation_type_concept_id": 0,
        })

    for f in patient.get("fusions", []):
        records["observations"].append({
            "observation_id": str(uuid.uuid4()),
            "person_id": person_id,
            "observation_concept_id": 0,
            "observation_date": patient.get("diagnosis_date", ""),
            "observation_source_value": "Fusion",
            "value_as_string": f["fusion"],
            "observation_type_concept_id": 0,
        })

    # Drug exposures
    for tx in patient.get("treatments", []):
        records["drug_exposures"].append({
            "drug_exposure_id": str(uuid.uuid4()),
            "person_id": person_id,
            "drug_concept_id": 0,
            "drug_exposure_start_date": tx.get("start_date", ""),
            "drug_exposure_end_date": tx.get("end_date"),
            "drug_source_value": tx["drug"],
            "drug_type_concept_id": 0,
            "route_source_value": "Oral" if "oral" in tx.get("regimen", "").lower() or "daily" in tx.get("regimen", "").lower() else "IV",
            "dose_unit_source_value": tx.get("regimen", ""),
            "_oncoreconcile_metadata": {
                "line_of_therapy": tx["line_of_therapy"],
                "drug_class": tx["class"],
            },
        })

    # Procedure occurrences (key interventions)
    if patient.get("diagnosis") == "Acute Myeloid Leukemia":
        records["procedure_occurrences"].append({
            "procedure_occurrence_id": str(uuid.uuid4()),
            "person_id": person_id,
            "procedure_concept_id": 0,
            "procedure_date": "2023-09-01",
            "procedure_source_value": "Allogeneic Stem Cell Transplant",
            "procedure_type_concept_id": 0,
        })

    records["metadata"]["record_count"] = {
        "condition_occurrences": len(records["condition_occurrences"]),
        "measurements": len(records["measurements"]),
        "observations": len(records["observations"]),
        "drug_exposures": len(records["drug_exposures"]),
        "procedure_occurrences": len(records["procedure_occurrences"]),
    }

    return records


# ── Expanded Knowledge Graph ──────────────────────────────────────────────────

def build_expanded_knowledge_graph(patient: dict) -> dict:
    """
    Build an expanded enterprise knowledge graph from a patient journey.
    Represents:
      - Patient
      - Disease
      - Gene
      - Variant
      - Drug
      - Treatment
      - Evidence
      - Coding Systems
      - Reviewer Decisions
      - FHIR Resources
      - OMOP Concepts
    """
    harm = load_semantic_harmonization()

    context = {
        "onco": "https://example.org/oncoreconcile/enterprise/",
        "schema": "https://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "fhir": "http://hl7.org/fhir/",
        "omop": "https://ohdsi.github.io/CommonDataModel/",
        "type": "@type",
        "label": "schema:name",
    }

    nodes = []
    patient_node_id = f"onco:patient/{patient['patient_id']}"

    # Patient node
    nodes.append({
        "@id": patient_node_id,
        "@type": "onco:Patient",
        "label": f"Patient {patient['patient_id']}",
        "onco:sex": patient.get("sex"),
        "onco:ageGroup": patient.get("age_group"),
        "onco:diagnosis": patient.get("diagnosis"),
        "onco:stage": patient.get("stage"),
        "onco:lineOfTherapy": patient.get("line_of_therapy"),
        "onco:dataQualityScore": patient.get("data_quality_score"),
        "onco:reconciliationStatus": patient.get("reconciliation_status"),
        "onco:evidenceCoverage": patient.get("evidence_coverage"),
    })

    # Disease node with harmonization
    disease_id = f"onco:disease/{patient['diagnosis'].replace(' ', '_')}"
    disease_harm = harm.get("diseases", {}).get(patient["diagnosis"], {})
    disease_node = {
        "@id": disease_id,
        "@type": "onco:OncologyDiagnosis",
        "label": patient["diagnosis"],
        "onco:canonicalValue": disease_harm.get("canonical_value", patient["diagnosis"]),
        "onco:confidence": disease_harm.get("confidence"),
        "onco:reviewStatus": disease_harm.get("review_status"),
        "onco:provenance": disease_harm.get("provenance"),
        "schema:citation": disease_harm.get("evidence"),
        "onco:hasCoding": [],
    }
    for mapping in disease_harm.get("mappings", []):
        mapping_id = f"onco:coding/{mapping['coding_system']}/{mapping['code']}"
        disease_node["onco:hasCoding"].append(mapping_id)
        nodes.append({
            "@id": mapping_id,
            "@type": "onco:TerminologyCode",
            "onco:codingSystem": mapping["coding_system"],
            "onco:code": mapping["code"],
            "onco:displayName": mapping["display_name"],
            "onco:source": mapping.get("source"),
            "onco:confidence": mapping.get("confidence"),
            "onco:reviewStatus": mapping.get("review_status"),
        })
    nodes.append(disease_node)
    nodes[0]["onco:hasDiagnosis"] = disease_id

    # Gene nodes with HGNC codes
    for gene in patient.get("genes", []):
        gene_harm = harm.get("genes", {}).get(gene, {})
        gene_id = f"onco:gene/{gene}"
        gene_node = {
            "@id": gene_id,
            "@type": "onco:Gene",
            "label": gene,
            "onco:canonicalValue": gene_harm.get("canonical_value", gene),
            "onco:hgncId": gene_harm.get("hgnc_id"),
            "onco:hgncName": gene_harm.get("hgnc_name"),
            "onco:confidence": gene_harm.get("confidence"),
            "onco:reviewStatus": gene_harm.get("review_status"),
        }
        # Add HGNC coding
        hgnc_id = gene_harm.get("hgnc_id")
        if hgnc_id:
            coding_id = f"onco:coding/HGNC/{hgnc_id}"
            gene_node["onco:hasCoding"] = [coding_id]
            nodes.append({
                "@id": coding_id,
                "@type": "onco:TerminologyCode",
                "onco:codingSystem": "HGNC",
                "onco:code": hgnc_id,
                "onco:displayName": gene_harm.get("hgnc_name", gene),
            })
        nodes.append(gene_node)
        nodes[0]["onco:hasGene"] = gene_id

    # Variant nodes
    for v in patient.get("variants", []):
        var_id = f"onco:variant/{v['gene']}_{v['variant'][:20]}"
        nodes.append({
            "@id": var_id,
            "@type": "onco:GenomicVariant",
            "label": f"{v['gene']} {v['variant']}",
            "onco:gene": v["gene"],
            "onco:variant": v["variant"],
            "onco:classification": v.get("classification"),
            "onco:alleleFrequency": v.get("allele_frequency"),
        })
        if "onco:hasVariant" not in nodes[0]:
            nodes[0]["onco:hasVariant"] = []
        nodes[0]["onco:hasVariant"].append(var_id)

    # Drug/Treatment nodes with RxNorm codes
    for tx in patient.get("treatments", []):
        drug = tx["drug"]
        drug_harm = harm.get("drugs", {}).get(drug, {})
        drug_id = f"onco:drug/{drug[:30].replace(' ', '_')}"
        drug_node = {
            "@id": drug_id,
            "@type": "onco:Therapy",
            "label": drug,
            "onco:canonicalValue": drug_harm.get("canonical_value", drug),
            "onco:lineOfTherapy": tx["line_of_therapy"],
            "onco:drugClass": tx["class"],
            "onco:regimen": tx["regimen"],
            "onco:startDate": tx.get("start_date"),
            "onco:endDate": tx.get("end_date"),
        }
        rxnorm_codes = [m for m in drug_harm.get("mappings", []) if m["coding_system"] == "RxNorm"]
        if rxnorm_codes:
            coding_id = f"onco:coding/RxNorm/{rxnorm_codes[0]['code']}"
            drug_node["onco:hasCoding"] = [coding_id]
            nodes.append({
                "@id": coding_id,
                "@type": "onco:TerminologyCode",
                "onco:codingSystem": "RxNorm",
                "onco:code": rxnorm_codes[0]["code"],
                "onco:displayName": rxnorm_codes[0]["display_name"],
            })
        nodes.append(drug_node)
        if "onco:hasTreatment" not in nodes[0]:
            nodes[0]["onco:hasTreatment"] = []
        nodes[0]["onco:hasTreatment"].append(drug_id)

    # Evidence and provenance
    evidence_id = f"onco:evidence/{patient['patient_id']}"
    nodes.append({
        "@id": evidence_id,
        "@type": "onco:EvidenceSummary",
        "label": f"Evidence for {patient['patient_id']}",
        "onco:dataQualityScore": patient.get("data_quality_score"),
        "onco:evidenceCoverage": patient.get("evidence_coverage"),
        "onco:reviewRequiredCount": patient.get("review_required_count"),
        "onco:reconciliationStatus": patient.get("reconciliation_status"),
        "onco:generatedAt": _now_iso(),
        "prov:wasGeneratedBy": "OncoReconcile AI Enterprise Platform",
    })
    nodes[0]["onco:hasEvidence"] = evidence_id

    return {
        "@context": context,
        "@graph": nodes,
        "export_type": "JSON-LD Enterprise Knowledge Graph",
        "note": "Synthetic data for enterprise platform demonstration. Not for clinical use.",
    }


# ── AI-Ready Dataset ──────────────────────────────────────────────────────────

def build_ai_ready_dataset() -> dict:
    """Build an AI-ready standardized dataset from all patient journeys."""
    data = load_patient_journeys()
    patients = data.get("patients", [])
    harm = load_semantic_harmonization()

    dataset = []
    for p in patients:
        record = {
            "patient_id": p["patient_id"],
            "sex": p.get("sex"),
            "age_group": p.get("age_group"),
            "diagnosis": p.get("diagnosis"),
            "diagnosis_canonical": harm.get("diseases", {}).get(p["diagnosis"], {}).get("canonical_value", p.get("diagnosis")),
            "histology": p.get("histology"),
            "stage": p.get("stage"),
            "diagnosis_date": p.get("diagnosis_date"),
            "genes": p.get("genes"),
            "gene_hgnc_ids": [harm.get("genes", {}).get(g, {}).get("hgnc_id") for g in p.get("genes", [])],
            "variants": [{"gene": v["gene"], "variant": v["variant"], "classification": v.get("classification")} for v in p.get("variants", [])],
            "fusions": p.get("fusions", []),
            "copy_number_alterations": p.get("copy_number_alterations", []),
            "treatments": [{
                "drug": t["drug"],
                "drug_canonical": harm.get("drugs", {}).get(t["drug"], {}).get("canonical_value", t["drug"]),
                "drug_class": t["class"],
                "line_of_therapy": t["line_of_therapy"],
                "start_date": t.get("start_date"),
                "end_date": t.get("end_date"),
            } for t in p.get("treatments", [])],
            "responses": [{"line": r["line_of_therapy"], "assessment": r["assessment"]} for r in p.get("response", [])],
            "progression_events": [{"event": e["event"], "type": e.get("type"), "date": e.get("date")} for e in p.get("progression_events", [])],
            "clinical_trial_flags": p.get("clinical_trial_flags", []),
            "data_quality_score": p.get("data_quality_score"),
            "reconciliation_status": p.get("reconciliation_status"),
            "evidence_coverage": p.get("evidence_coverage"),
        }
        dataset.append(record)

    return {
        "dataset": dataset,
        "total_patients": len(dataset),
        "schema_version": "1.0.0",
        "generated_at": _now_iso(),
        "intended_use": "AI model training, cohort analytics, and platform demonstration",
        "data_origin": "synthetically_generated",
        "contains_real_patient_data": False,
    }
