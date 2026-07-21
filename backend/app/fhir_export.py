"""
FHIR R4 export module — production-grade oncology FHIR Genomics resources.

Maps OncoReconcile reconciliation results to FHIR R4 resources:
  - Disease (cancer_type) → Condition
  - Gene → Observation (LOINC 48018-6 "Gene studied ID")
  - Variant → Observation (LOINC 69548-6 "Genetic variant assessment")
  - Variant (detailed) → MolecularSequence

All resources are wrapped in a Bundle (type=collection) with a placeholder Patient.

SNOMED CT mappings are provided for common cancer types; unrecognised diseases
use text-only coding. HGNC gene identifiers are resolved from the local alias
catalog when available.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── SNOMED CT disease mappings (curated subset) ──────────────────────────────
SNOMED_DISEASE_MAP: dict[str, tuple[str, str]] = {
    "Lung Non-Small Cell Carcinoma":         ("254637007", "Non-small cell lung cancer"),
    "Non-Small Cell Lung Cancer":             ("254637007", "Non-small cell lung cancer"),
    "Lung Adenocarcinoma":                    ("359332006", "Lung adenocarcinoma"),
    "Breast Invasive Carcinoma":              ("705544002", "Invasive carcinoma of breast"),
    "Breast Cancer":                          ("254837009", "Malignant neoplasm of breast"),
    "Melanoma":                               ("372130007", "Malignant melanoma of skin"),
    "Cutaneous Melanoma":                     ("372130007", "Malignant melanoma of skin"),
    "Colorectal Adenocarcinoma":              ("438817007", "Colorectal adenocarcinoma"),
    "Colorectal Cancer":                      ("363406005", "Malignant neoplasm of colon"),
    "Pancreatic Adenocarcinoma":              ("399487003", "Pancreatic adenocarcinoma"),
    "Pancreatic Cancer":                      ("372142000", "Malignant neoplasm of pancreas"),
    "Prostate Adenocarcinoma":                ("399547004", "Adenocarcinoma of prostate"),
    "Prostate Cancer":                        ("399547004", "Adenocarcinoma of prostate"),
    "Ovarian Serous Carcinoma":              ("394574004", "Serous cystadenocarcinoma of ovary"),
    "Ovarian Cancer":                         ("363443007", "Malignant neoplasm of ovary"),
    "Gastric Adenocarcinoma":                 ("363358000", "Malignant neoplasm of stomach"),
    "Gastric Cancer":                         ("363358000", "Malignant neoplasm of stomach"),
    "Hepatocellular Carcinoma":              ("109841003", "Hepatocellular carcinoma"),
    "Renal Cell Carcinoma":                   ("701000124108", "Renal cell carcinoma"),
    "Bladder Urothelial Carcinoma":          ("385425000", "Urothelial carcinoma of bladder"),
    "Endometrial Carcinoma":                  ("448084005", "Endometrial carcinoma"),
    "Acute Myeloid Leukemia":                 ("91861009", "Acute myeloid leukemia"),
    "AML":                                    ("91861009", "Acute myeloid leukemia"),
    "Chronic Lymphocytic Leukemia":           ("92814006", "Chronic lymphocytic leukemia"),
    "CLL":                                    ("92814006", "Chronic lymphocytic leukemia"),
    "Diffuse Large B-Cell Lymphoma":          ("109979007", "Diffuse large B-cell lymphoma"),
    "Multiple Myeloma":                       ("109989006", "Multiple myeloma"),
    "Glioblastoma":                           ("636531009", "Glioblastoma multiforme"),
}

# ── HGNC gene ID mappings ────────────────────────────────────────────────────
HGNC_GENE_MAP: dict[str, str] = {
    "EGFR":   "HGNC:3236",
    "ERBB2":  "HGNC:3430",
    "HER2":   "HGNC:3430",
    "BRAF":   "HGNC:1097",
    "KRAS":   "HGNC:6407",
    "NRAS":   "HGNC:7989",
    "HRAS":   "HGNC:5173",
    "PIK3CA": "HGNC:8975",
    "ALK":    "HGNC:427",
    "ROS1":   "HGNC:10261",
    "RET":    "HGNC:9967",
    "MET":    "HGNC:7029",
    "NTRK1":  "HGNC:8031",
    "NTRK2":  "HGNC:8032",
    "NTRK3":  "HGNC:8033",
    "IDH1":   "HGNC:5382",
    "IDH2":   "HGNC:5383",
    "TP53":   "HGNC:11998",
    "PTEN":   "HGNC:9588",
    "AR":     "HGNC:644",
    "ESR1":   "HGNC:3467",
    "BRCA1":  "HGNC:1100",
    "BRCA2":  "HGNC:1101",
    "CDK4":   "HGNC:1773",
    "CDK6":   "HGNC:1777",
    "CCND1":  "HGNC:1582",
    "MYC":    "HGNC:7553",
    "FGFR1":  "HGNC:3688",
    "FGFR2":  "HGNC:3690",
    "FGFR3":  "HGNC:3691",
    "KIT":    "HGNC:6342",
    "PDGFRA": "HGNC:8803",
    "PDGFRB": "HGNC:8804",
    "FLT3":   "HGNC:3765",
    "JAK2":   "HGNC:6192",
    "JAK3":   "HGNC:6193",
    "STAT3":  "HGNC:11364",
    "CTNNB1": "HGNC:2514",
    "APC":    "HGNC:583",
    "SMAD4":  "HGNC:6770",
    "MLH1":   "HGNC:7127",
    "MSH2":   "HGNC:7325",
    "MSH6":   "HGNC:7329",
    "PMS2":   "HGNC:9122",
}

# ── HGNC gene name map ────────────────────────────────────────────────────────
HGNC_GENE_NAME: dict[str, str] = {
    "EGFR":   "Epidermal growth factor receptor",
    "ERBB2":  "Erb-b2 receptor tyrosine kinase 2",
    "BRAF":   "B-Raf proto-oncogene, serine/threonine kinase",
    "KRAS":   "KRAS proto-oncogene, GTPase",
    "NRAS":   "NRAS proto-oncogene, GTPase",
    "HRAS":   "HRas proto-oncogene, GTPase",
    "PIK3CA": "Phosphatidylinositol-4,5-bisphosphate 3-kinase catalytic subunit alpha",
    "ALK":    "ALK receptor tyrosine kinase",
    "ROS1":   "ROS proto-oncogene 1, receptor tyrosine kinase",
    "RET":    "Ret proto-oncogene",
    "MET":    "MET proto-oncogene, receptor tyrosine kinase",
    "NTRK1":  "Neurotrophic receptor tyrosine kinase 1",
    "NTRK2":  "Neurotrophic receptor tyrosine kinase 2",
    "NTRK3":  "Neurotrophic receptor tyrosine kinase 3",
    "IDH1":   "Isocitrate dehydrogenase (NADP(+)) 1",
    "IDH2":   "Isocitrate dehydrogenase (NADP(+)) 2",
    "TP53":   "Tumor protein p53",
    "PTEN":   "Phosphatase and tensin homolog",
    "BRCA1":  "BRCA1 DNA repair associated",
    "BRCA2":  "BRCA2 DNA repair associated",
    "FLT3":   "Fms related receptor tyrosine kinase 3",
    "JAK2":   "Janus kinase 2",
    "JAK3":   "Janus kinase 3",
    "KIT":    "KIT proto-oncogene, receptor tyrosine kinase",
    "PDGFRA": "Platelet derived growth factor receptor alpha",
}


def _uuid() -> str:
    return str(uuid.uuid4())


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _hgnc_id(gene: str) -> Optional[str]:
    """Return HGNC ID for a gene symbol, or None."""
    return HGNC_GENE_MAP.get(gene.upper().strip())


def _snomed_disease(disease: str) -> tuple[Optional[str], Optional[str], str]:
    """Return (snomed_code, snomed_display, text) for a disease string."""
    code, display = SNOMED_DISEASE_MAP.get(disease.strip(), (None, None))
    return code, display, disease


def _build_patient() -> tuple[dict, str]:
    """Build a placeholder Patient resource."""
    patient_id = _uuid()
    return {
        "fullUrl": f"urn:uuid:{patient_id}",
        "resource": {
            "resourceType": "Patient",
            "id": patient_id,
            "meta": {
                "profile": ["http://hl7.org/fhir/StructureDefinition/Patient"]
            },
            "identifier": [{
                "system": "https://oncoreconcile.ai/fhir/placeholder",
                "value": "placeholder-patient-001",
            }],
            "gender": "unknown",
        },
    }, patient_id


def build_condition_resource(
    disease: Optional[str],
    patient_id: str,
    case_id: Optional[str] = None,
    confidence: Optional[str] = None,
) -> Optional[dict]:
    """Build a FHIR Condition resource from a disease/cancer_type string."""
    if not disease:
        return None

    resource_id = _uuid()
    snomed_code, snomed_display, text = _snomed_disease(disease)

    coding = []
    if snomed_code:
        coding.append({
            "system": "http://snomed.info/sct",
            "code": snomed_code,
            "display": snomed_display,
        })

    condition = {
        "resourceType": "Condition",
        "id": resource_id,
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/Condition"],
            "tag": [{
                "system": "https://oncoreconcile.ai/fhir/tags",
                "code": "oncology-disease",
                "display": "Oncology Disease Condition",
            }],
        },
        "subject": {"reference": f"urn:uuid:{patient_id}"},
        "code": {
            "coding": coding if coding else None,
            "text": text,
        },
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                "code": "problem-list-item",
                "display": "Problem List Item",
            }],
        }],
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active",
                "display": "Active",
            }],
        },
    }

    if confidence:
        condition["extension"] = [{
            "url": "https://oncoreconcile.ai/fhir/StructureDefinition/reconciliation-confidence",
            "valueString": confidence,
        }]

    if case_id:
        condition["identifier"] = [{
            "system": "https://oncoreconcile.ai/fhir/case-identifier",
            "value": case_id,
        }]

    return {
        "fullUrl": f"urn:uuid:{resource_id}",
        "resource": condition,
    }


def build_gene_observation(
    gene: Optional[str],
    patient_id: str,
    case_id: Optional[str] = None,
    confidence: Optional[str] = None,
) -> Optional[dict]:
    """Build a FHIR Observation resource for a gene (LOINC 48018-6)."""
    if not gene:
        return None

    resource_id = _uuid()
    hgnc_id = _hgnc_id(gene)
    gene_name = HGNC_GENE_NAME.get(gene.upper().strip())

    value_coding = [{
        "system": "http://www.genenames.org/geneId",
        "code": hgnc_id or gene,
        "display": gene_name or gene,
    }]

    obs = {
        "resourceType": "Observation",
        "id": resource_id,
        "meta": {
            "profile": [
                "http://hl7.org/fhir/StructureDefinition/Observation",
                "http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/gene",
            ],
            "tag": [{
                "system": "https://oncoreconcile.ai/fhir/tags",
                "code": "oncology-gene",
                "display": "Oncology Gene Observation",
            }],
        },
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "48018-6",
                "display": "Gene studied ID",
            }],
            "text": "Gene studied",
        },
        "subject": {"reference": f"urn:uuid:{patient_id}"},
        "valueCodeableConcept": {
            "coding": value_coding,
            "text": gene,
        },
    }

    if confidence:
        obs["extension"] = [{
            "url": "https://oncoreconcile.ai/fhir/StructureDefinition/reconciliation-confidence",
            "valueString": confidence,
        }]

    if case_id:
        obs["identifier"] = [{
            "system": "https://oncoreconcile.ai/fhir/case-identifier",
            "value": case_id,
        }]

    return {
        "fullUrl": f"urn:uuid:{resource_id}",
        "resource": obs,
    }


def build_variant_observation(
    variant: Optional[str],
    patient_id: str,
    gene: Optional[str] = None,
    case_id: Optional[str] = None,
    confidence: Optional[str] = None,
) -> Optional[dict]:
    """
    Build a FHIR Observation resource for a variant (LOINC 69548-6).

    If the variant is a categorical fusion (e.g., "Categorical NTRK Fusion..."),
    the Observation uses component-level coding to preserve the ambiguity.
    """
    if not variant:
        return None

    resource_id = _uuid()
    is_categorical = "categorical" in variant.lower() or "fusion" in variant.lower()

    obs = {
        "resourceType": "Observation",
        "id": resource_id,
        "meta": {
            "profile": [
                "http://hl7.org/fhir/StructureDefinition/Observation",
                "http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant",
            ],
            "tag": [{
                "system": "https://oncoreconcile.ai/fhir/tags",
                "code": "oncology-variant",
                "display": "Oncology Variant Observation",
            }],
        },
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "69548-6",
                "display": "Genetic variant assessment",
            }],
            "text": "Genetic variant assessment",
        },
        "subject": {"reference": f"urn:uuid:{patient_id}"},
    }

    if is_categorical:
        obs["valueCodeableConcept"] = {
            "text": variant,
        }
        obs["component"] = [{
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "48018-6",
                    "display": "Gene studied ID",
                }],
                "text": "Gene studied",
            },
            "valueCodeableConcept": {
                "text": gene or "Multiple",
            },
        }, {
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "81258-6",
                    "display": "Variant category",
                }],
                "text": "Variant category",
            },
            "valueCodeableConcept": {
                "text": variant,
            },
        }]
    else:
        obs["valueCodeableConcept"] = {
            "text": variant,
        }
        if gene:
            obs["component"] = [{
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "48018-6",
                        "display": "Gene studied ID",
                    }],
                    "text": "Gene studied",
                },
                "valueCodeableConcept": {
                    "coding": [{
                        "system": "http://www.genenames.org/geneId",
                        "code": _hgnc_id(gene) or gene,
                        "display": HGNC_GENE_NAME.get(gene.upper().strip()) or gene,
                    }],
                    "text": gene,
                },
            }]

    if confidence:
        if "extension" not in obs:
            obs["extension"] = []
        obs["extension"].append({
            "url": "https://oncoreconcile.ai/fhir/StructureDefinition/reconciliation-confidence",
            "valueString": confidence,
        })

    if case_id:
        obs["identifier"] = [{
            "system": "https://oncoreconcile.ai/fhir/case-identifier",
            "value": case_id,
        }]

    return {
        "fullUrl": f"urn:uuid:{resource_id}",
        "resource": obs,
    }


def build_molecular_sequence(
    variant: Optional[str],
    gene: Optional[str],
    patient_id: str,
    case_id: Optional[str] = None,
) -> Optional[dict]:
    """
    Build a FHIR MolecularSequence resource for a variant.

    This is a structured representation suitable for genomics pipelines.
    For non-standardized variant descriptions, we use text representation
    rather than allele-specific coordinates.
    """
    if not variant or not gene:
        return None

    resource_id = _uuid()
    is_protein = any(c.isdigit() for c in variant.split()[-1]) if variant else False

    sequence = {
        "resourceType": "MolecularSequence",
        "id": resource_id,
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/MolecularSequence"],
            "tag": [{
                "system": "https://oncoreconcile.ai/fhir/tags",
                "code": "oncology-variant",
                "display": "Oncology Variant MolecularSequence",
            }],
        },
        "type": "aa" if is_protein else "dna",
        "coordinateSystem": 1,
        "patient": {"reference": f"urn:uuid:{patient_id}"},
        "referenceSeq": {
            "referenceSeqType": "gene",
            "referenceSeqId": {
                "coding": [{
                    "system": "http://www.genenames.org/geneId",
                    "code": _hgnc_id(gene) or gene,
                    "display": HGNC_GENE_NAME.get(gene.upper().strip()) or gene,
                }],
            },
        },
        "variant": [{
            "type": "indel",
            "display": variant,
        }],
    }

    if case_id:
        sequence["identifier"] = [{
            "system": "https://oncoreconcile.ai/fhir/case-identifier",
            "value": case_id,
        }]

    return {
        "fullUrl": f"urn:uuid:{resource_id}",
        "resource": sequence,
    }


# ── Main export functions ───────────────────────────────────────────────────

def build_fhir_bundle(
    canonical: dict,
    evidence: Optional[list] = None,
    confidence: Optional[str] = None,
    case_id: Optional[str] = None,
    review_status: Optional[str] = None,
    score_breakdown: Optional[dict] = None,
    alternatives: Optional[list] = None,
) -> dict:
    """
    Build a FHIR R4 Bundle (type=collection) from reconciliation results.

    Args:
        canonical: dict with keys 'cancer_type', 'gene', 'variant'
        evidence: list of EvidenceItem dicts
        confidence: "HIGH" | "MEDIUM" | "LOW"
        case_id: optional case identifier
        review_status: "AUTO_RECONCILE" | "REVIEW_REQUIRED" | "CANNOT_RECONCILE"
        score_breakdown: optional confidence score components
        alternatives: optional list of alternative candidates

    Returns:
        FHIR Bundle JSON as a dict, suitable for HTTP response or file download.
    """
    bundle_id = _uuid()
    entry: list[dict] = []

    # 1. Placeholder Patient
    patient_entry, patient_id = _build_patient()
    entry.append(patient_entry)

    # 2. Condition (disease)
    disease = canonical.get("cancer_type") if canonical else None
    condition_entry = build_condition_resource(
        disease=disease,
        patient_id=patient_id,
        case_id=case_id,
        confidence=confidence,
    )
    if condition_entry:
        entry.append(condition_entry)

    # 3. Observation (gene)
    gene = canonical.get("gene") if canonical else None
    gene_obs = build_gene_observation(
        gene=gene,
        patient_id=patient_id,
        case_id=case_id,
        confidence=confidence,
    )
    if gene_obs:
        entry.append(gene_obs)

    # 4. Observation (variant)
    variant = canonical.get("variant") if canonical else None
    variant_obs = build_variant_observation(
        variant=variant,
        patient_id=patient_id,
        gene=gene,
        case_id=case_id,
        confidence=confidence,
    )
    if variant_obs:
        entry.append(variant_obs)

    # 5. MolecularSequence (variant)
    mol_seq = build_molecular_sequence(
        variant=variant,
        gene=gene,
        patient_id=patient_id,
        case_id=case_id,
    )
    if mol_seq:
        entry.append(mol_seq)

    # 6. Provenance
    provenance_id = _uuid()
    provenance_target_ids = []
    for e in entry:
        resource = e.get("resource", {})
        rt = resource.get("resourceType")
        if rt in {"Condition", "Observation", "MolecularSequence"}:
            provenance_target_ids.append({"reference": e["fullUrl"]})

    provenance_entry = {
        "fullUrl": f"urn:uuid:{provenance_id}",
        "resource": {
            "resourceType": "Provenance",
            "id": provenance_id,
            "meta": {
                "profile": ["http://hl7.org/fhir/StructureDefinition/Provenance"],
            },
            "target": provenance_target_ids,
            "recorded": _now_iso(),
            "activity": {
                "coding": [{
                    "system": "https://oncoreconcile.ai/fhir/CodeSystem/reconciliation-activity",
                    "code": "oncology-entity-reconciliation",
                    "display": "Oncology entity reconciliation",
                }],
            },
            "agent": [{
                "type": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                        "code": "device",
                        "display": "Device",
                    }],
                },
                "who": {
                    "identifier": {
                        "system": "https://oncoreconcile.ai/fhir/device-identifier",
                        "value": "OncoReconcile-AI",
                    },
                },
            }],
            "entity": [{
                "role": "source",
                "what": {
                    "identifier": {
                        "system": "https://oncoreconcile.ai/fhir/case-identifier",
                        "value": case_id or "unknown",
                    },
                },
            }],
        },
    }
    entry.append(provenance_entry)

    # 7. DiagnosticReport
    report_id = _uuid()
    result_references = []
    for e in entry:
        resource = e.get("resource", {})
        rt = resource.get("resourceType")
        if rt in {"Observation", "MolecularSequence"}:
            result_references.append({"reference": e["fullUrl"]})

    report_entry = {
        "fullUrl": f"urn:uuid:{report_id}",
        "resource": {
            "resourceType": "DiagnosticReport",
            "id": report_id,
            "meta": {
                "profile": [
                    "http://hl7.org/fhir/StructureDefinition/DiagnosticReport",
                    "http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/genomics-report",
                ],
                "tag": [{
                    "system": "https://oncoreconcile.ai/fhir/tags",
                    "code": "oncology-reconciliation",
                    "display": "Oncology Reconciliation Report",
                }],
            },
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "81247-9",
                    "display": "Master genomic report",
                }],
                "text": "Oncology genomic reconciliation report",
            },
            "subject": {"reference": f"urn:uuid:{patient_id}"},
            "result": result_references if result_references else None,
        },
    }

    extensions = []
    if review_status:
        extensions.append({
            "url": "https://oncoreconcile.ai/fhir/StructureDefinition/review-status",
            "valueString": review_status,
        })
    if confidence:
        extensions.append({
            "url": "https://oncoreconcile.ai/fhir/StructureDefinition/confidence",
            "valueString": confidence,
        })
    if score_breakdown:
        extensions.append({
            "url": "https://oncoreconcile.ai/fhir/StructureDefinition/confidence-score-breakdown",
            "valueQuantity": {
                "value": score_breakdown.get("score", 0.0),
                "unit": "%",
            },
        })
    if extensions:
        report_entry["resource"]["extension"] = extensions

    for e in entry:
        resource = e.get("resource", {})
        if resource.get("resourceType") == "Condition":
            report_entry["resource"]["encounter"] = None
            report_entry["resource"]["conclusionCode"] = [resource["code"]]
            break

    entry.append(report_entry)

    bundle = {
        "resourceType": "Bundle",
        "id": bundle_id,
        "meta": {
            "lastUpdated": _now_iso(),
            "tag": [{
                "system": "https://oncoreconcile.ai/fhir/tags",
                "code": "oncoreconcile-export",
                "display": "OncoReconcile AI FHIR Export",
            }],
        },
        "type": "collection",
        "timestamp": _now_iso(),
        "entry": entry,
    }

    return bundle


def build_fhir_bundle_batch(
    results: list[dict],
) -> dict:
    """
    Build a FHIR Bundle from multiple reconciliation results.
    Each result produces its own sub-Bundle; all are wrapped in a single
    top-level collection Bundle.

    Args:
        results: list of reconciliation result dicts

    Returns:
        FHIR Bundle JSON as dict.
    """
    bundle_id = _uuid()
    entries: list[dict] = []

    for result in results:
        canonical = result.get("canonical") or {}
        evidence = result.get("evidence")
        confidence = result.get("confidence")
        case_id = result.get("case_id")
        review_status = result.get("review_status")
        score_breakdown = result.get("score_breakdown")
        alternatives = result.get("alternatives")

        sub_bundle = build_fhir_bundle(
            canonical=canonical,
            evidence=evidence,
            confidence=confidence,
            case_id=case_id,
            review_status=review_status,
            score_breakdown=score_breakdown,
            alternatives=alternatives,
        )

        for sub_entry in sub_bundle.get("entry", []):
            entries.append(sub_entry)

    return {
        "resourceType": "Bundle",
        "id": bundle_id,
        "meta": {
            "lastUpdated": _now_iso(),
            "tag": [{
                "system": "https://oncoreconcile.ai/fhir/tags",
                "code": "oncoreconcile-export-batch",
                "display": "OncoReconcile AI FHIR Batch Export",
            }],
        },
        "type": "collection",
        "timestamp": _now_iso(),
        "entry": entries,
    }
