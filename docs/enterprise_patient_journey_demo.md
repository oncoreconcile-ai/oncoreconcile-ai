# Enterprise Patient Journey Demo

The enterprise patient journey extension transforms OncoReconcile AI from a biomedical entity resolution demo into a **Precision Oncology Data Quality, Semantic Harmonization & Interoperability Platform**.

## Architecture

```
Raw Data
↓
Semantic Harmonization
↓
Coding System Mapping
↓
Evidence Retrieval
↓
Confidence Scoring
↓
Governance
↓
Patient Journey
↓
FHIR / OMOP
↓
Analytics
↓
AI-Ready Dataset
```

## Data

### Synthetic Longitudinal Dataset
- **File:** `data/patient_journey_demo.json`
- **Patients:** 18 synthetic oncology patients
- **Cancer Types:** NSCLC (6), Breast Cancer (4), Colorectal Cancer (3), Melanoma (3), AML (2)
- **Fields per patient:** patient_id, sex, age_group, diagnosis, histology, stage, diagnosis_date, biomarker_tests, genes, variants, fusions, copy_number_alterations, treatments, line_of_therapy, response, progression_events, clinical_trial_flags, review_required_count, data_quality_score, reconciliation_status, evidence_coverage

### Semantic Harmonization Layer
- **File:** `data/semantic_harmonization.json`
- Diseases mapped to SNOMED CT, NCIt, OncoTree, ICD-10
- Histologies mapped to SNOMED CT, NCIt
- Genes mapped to HGNC
- Drugs mapped to RxNorm, ATC
- Biomarkers mapped to ClinVar, ClinGen
- Lab tests mapped to LOINC

## APIs

| Endpoint | Description |
|---|---|
| GET /enterprise/patient-journey | List all patient journeys |
| GET /enterprise/patient-journey/{id} | Full patient journey detail |
| GET /enterprise/analytics/summary | Comprehensive cohort analytics |
| GET /enterprise/analytics/biomarkers | Biomarker analytics |
| GET /enterprise/analytics/treatments | Treatment analytics |
| GET /enterprise/analytics/outcomes | Outcome analytics |
| GET /enterprise/analytics/data-quality | Data quality metrics |
| GET /enterprise/analytics/governance | Governance metrics |
| GET /enterprise/analytics/terminology | Terminology mapping metrics |
| GET /enterprise/executive-dashboard | Executive summary view |
| POST /enterprise/export/fhir/{id} | Expanded FHIR R4 Bundle |
| POST /enterprise/export/omop/{id} | Expanded OMOP v5.4 records |
| POST /enterprise/export/knowledge-graph/{id} | Expanded knowledge graph |

## FHIR Expansion

The expanded FHIR export supports:
- Patient
- Condition (disease, histology)
- Observation (biomarker tests, genes, variants, fusions, CNA)
- MedicationStatement (treatments)
- Provenance

## OMOP Expansion

The expanded OMOP export maps to:
- condition_occurrence
- measurement
- observation
- drug_exposure

## Frontend Routes

| Route | Page |
|---|---|
| /enterprise/journeys | Patient Journey Dashboard |
| /enterprise/analytics | Cohort Analytics Dashboard |
| /enterprise/executive | Executive Dashboard |
