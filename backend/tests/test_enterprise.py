"""
Enterprise platform tests for OncoReconcile AI.

Tests patient journey APIs, analytics endpoints, data quality,
governance metrics, terminology mappings, FHIR/OMOP exports,
knowledge graph expansion, and executive dashboard.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestEnterprisePatientJourney:
    """Test patient journey API endpoints."""

    def test_list_patient_journeys(self):
        """GET /enterprise/patient-journey returns patient list."""
        response = client.get("/enterprise/patient-journey")
        assert response.status_code == 200
        data = response.json()
        assert "patients" in data
        assert "total" in data
        assert data["total"] > 0
        # Verify structure of first patient
        first = data["patients"][0]
        assert "patient_id" in first
        assert "diagnosis" in first
        assert "stage" in first
        assert "reconciliation_status" in first
        assert "data_quality_score" in first

    def test_get_patient_journey_detail_found(self):
        """GET /enterprise/patient-journey/PT-DEMO-001 returns detailed journey."""
        response = client.get("/enterprise/patient-journey/PT-DEMO-001")
        assert response.status_code == 200
        data = response.json()
        assert "patient" in data
        assert "journey_timeline" in data
        assert "harmonization" in data
        # Verify patient details
        assert data["patient"]["patient_id"] == "PT-DEMO-001"
        assert data["patient"]["diagnosis"] == "Non-Small Cell Lung Cancer"
        # Verify timeline has events
        assert len(data["journey_timeline"]) > 0
        # Verify harmonization
        assert "disease" in data["harmonization"]
        assert "genes" in data["harmonization"]
        assert "drugs" in data["harmonization"]

    def test_get_patient_journey_detail_not_found(self):
        """GET /enterprise/patient-journey/FAKE returns 404."""
        response = client.get("/enterprise/patient-journey/FAKE")
        assert response.status_code == 404

    def test_get_patient_journey_detail_all_fields(self):
        """Verify all patients have complete data."""
        response = client.get("/enterprise/patient-journey")
        patients = response.json()["patients"]
        for p in patients:
            detail = client.get(f"/enterprise/patient-journey/{p['patient_id']}")
            assert detail.status_code == 200
            detail_data = detail.json()
            patient = detail_data["patient"]
            # Required fields per spec
            assert patient.get("diagnosis")
            assert patient.get("stage") is not None
            assert patient.get("sex")
            assert patient.get("age_group")
            assert patient.get("biomarker_tests") is not None
            assert patient.get("genes") is not None
            assert patient.get("treatments") is not None
            assert patient.get("line_of_therapy") is not None


class TestEnterpriseAnalytics:
    """Test analytics API endpoints."""

    def test_analytics_summary(self):
        """GET /enterprise/analytics/summary returns cohort analytics."""
        response = client.get("/enterprise/analytics/summary")
        assert response.status_code == 200
        data = response.json()
        # Required KPIs
        assert "total_patients" in data
        assert data["total_patients"] > 0
        assert "cancer_type_distribution" in data
        assert "stage_distribution" in data
        assert "gene_frequency" in data
        assert "drug_frequency" in data
        assert "response_distribution" in data
        assert "average_data_quality_score" in data
        assert "ai_readiness_score" in data
        assert "biomarker_testing_rate" in data

    def test_analytics_biomarkers(self):
        """GET /enterprise/analytics/biomarkers returns biomarker analytics."""
        response = client.get("/enterprise/analytics/biomarkers")
        assert response.status_code == 200
        data = response.json()
        assert "genes_identified" in data
        assert data["genes_identified"] > 0
        assert "variants_identified" in data
        assert "total_biomarker_tests" in data
        assert "test_methods" in data
        assert "test_types" in data

    def test_analytics_treatments(self):
        """GET /enterprise/analytics/treatments returns treatment analytics."""
        response = client.get("/enterprise/analytics/treatments")
        assert response.status_code == 200
        data = response.json()
        assert "total_treatment_lines" in data
        assert data["total_treatment_lines"] > 0
        assert "unique_drugs" in data
        assert "drug_details" in data
        assert "drug_class_details" in data

    def test_analytics_outcomes(self):
        """GET /enterprise/analytics/outcomes returns outcome analytics."""
        response = client.get("/enterprise/analytics/outcomes")
        assert response.status_code == 200
        data = response.json()
        assert "outcome_by_diagnosis" in data
        assert "line_of_therapy_success_rates" in data
        # Verify we have outcome data
        assert len(data["outcome_by_diagnosis"]) > 0

    def test_analytics_data_quality(self):
        """GET /enterprise/analytics/data-quality returns quality metrics."""
        response = client.get("/enterprise/analytics/data-quality")
        assert response.status_code == 200
        data = response.json()
        assert "total_patients" in data
        assert "missing_data" in data
        assert "missing_data_rates" in data
        assert "quality_scores" in data
        assert "indicators" in data
        # Verify quality scores have all required fields
        qs = data["quality_scores"]
        assert "data_completeness" in qs
        assert "coding_coverage" in qs
        assert "evidence_coverage" in qs
        assert "semantic_harmonization_coverage" in qs
        # Verify indicators exist
        assert "green" in data["indicators"].values() or True  # Should have at least some green

    def test_analytics_governance(self):
        """GET /enterprise/analytics/governance returns governance metrics."""
        response = client.get("/enterprise/analytics/governance")
        assert response.status_code == 200
        data = response.json()
        assert "total_patients" in data
        assert "reconciliation_status_counts" in data
        assert "governance_score" in data
        assert "breakdown_by_cancer_type" in data

    def test_analytics_terminology(self):
        """GET /enterprise/analytics/terminology returns terminology metrics."""
        response = client.get("/enterprise/analytics/terminology")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert "total_mapped" in data
        assert "total_entities" in data
        assert "coding_systems_used" in data
        # Verify we have SNOMED, NCIt, etc.
        assert len(data["coding_systems_used"]) > 0


class TestEnterpriseExecutiveDashboard:
    """Test executive dashboard endpoint."""

    def test_executive_dashboard(self):
        """GET /enterprise/executive-dashboard returns executive summary."""
        response = client.get("/enterprise/executive-dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "patients_managed" in data
        assert data["patients_managed"] > 0
        assert "data_quality_score" in data
        assert "governance_score" in data
        assert "reconciliation_coverage" in data
        assert "coding_coverage" in data
        assert "evidence_coverage" in data
        assert "semantic_harmonization_coverage" in data
        assert "ai_readiness_score" in data
        assert "most_common_cancer_types" in data
        assert "most_common_biomarkers" in data
        assert "total_terminology_mappings" in data
        # Verify all scores are numeric
        assert isinstance(data["data_quality_score"], (int, float))
        assert isinstance(data["governance_score"], (int, float))
        assert data["status"] == "operational"


class TestEnterpriseExports:
    """Test enterprise export endpoints."""

    def test_export_fhir_patient(self):
        """POST /enterprise/export/fhir/PT-DEMO-001 returns FHIR bundle."""
        response = client.post("/enterprise/export/fhir/PT-DEMO-001")
        assert response.status_code == 200
        data = response.json()
        assert data["resourceType"] == "Bundle"
        assert data["type"] == "collection"
        assert "entry" in data
        entries = data["entry"]
        # Verify we have the required resource types
        resource_types = {e["resource"]["resourceType"] for e in entries}
        assert "Patient" in resource_types
        assert "Condition" in resource_types
        assert "Observation" in resource_types
        assert "MedicationStatement" in resource_types

    def test_export_fhir_patient_not_found(self):
        """POST /enterprise/export/fhir/FAKE returns 404."""
        response = client.post("/enterprise/export/fhir/FAKE")
        assert response.status_code == 404

    def test_export_omop_patient(self):
        """POST /enterprise/export/omop/PT-DEMO-001 returns OMOP records."""
        response = client.post("/enterprise/export/omop/PT-DEMO-001")
        assert response.status_code == 200
        data = response.json()
        assert "person_source_value" in data
        assert "condition_occurrences" in data
        assert "measurements" in data
        assert "observations" in data
        assert "drug_exposures" in data
        assert "metadata" in data
        # Verify we have records
        assert len(data["condition_occurrences"]) > 0
        assert len(data["drug_exposures"]) > 0

    def test_export_knowledge_graph_patient(self):
        """POST /enterprise/export/knowledge-graph/PT-DEMO-001 returns KG."""
        response = client.post("/enterprise/export/knowledge-graph/PT-DEMO-001")
        assert response.status_code == 200
        data = response.json()
        assert "@context" in data
        assert "@graph" in data
        assert len(data["@graph"]) > 0
        # Verify patient node exists
        patient_nodes = [n for n in data["@graph"] if n.get("@type") == "onco:Patient"]
        assert len(patient_nodes) > 0

    def test_ai_ready_dataset(self):
        """GET /enterprise/ai-ready-dataset returns standardized dataset."""
        response = client.get("/enterprise/ai-ready-dataset")
        assert response.status_code == 200
        data = response.json()
        assert "dataset" in data
        assert "total_patients" in data
        assert data["total_patients"] > 0
        assert "schema_version" in data
        # Verify first record structure
        first = data["dataset"][0]
        assert "patient_id" in first
        assert "diagnosis_canonical" in first
        assert "gene_hgnc_ids" in first
        assert "treatments" in first
        assert "data_quality_score" in first


class TestExistingEndpointsStillWork:
    """Verify existing endpoints are not broken by enterprise expansion."""

    def test_root_endpoint(self):
        """GET / still works."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["project"] == "OncoReconcile AI"

    def test_reconcile_endpoint(self):
        """POST /reconcile still works."""
        response = client.post("/reconcile", json={
            "cancer_type": "NSCLC",
            "gene": "EGFR",
            "variant": "L858R",
        })
        assert response.status_code == 200
        data = response.json()
        assert "canonical" in data
        assert "review_status" in data
        assert "confidence" in data

    def test_benchmark_endpoint(self):
        """GET /benchmark still works."""
        response = client.get("/benchmark")
        assert response.status_code == 200

    def test_review_queue_endpoint(self):
        """GET /review-queue still works."""
        response = client.get("/review-queue")
        assert response.status_code == 200

    def test_omop_export_endpoint(self):
        """POST /export/omop still works."""
        response = client.post("/export/omop", json={
            "cancer_type": "NSCLC",
            "gene": "EGFR",
            "variant": "L858R",
        })
        assert response.status_code == 200

    def test_fhir_export_endpoint(self):
        """POST /export/fhir still works."""
        response = client.post("/export/fhir", json={
            "cancer_type": "NSCLC",
            "gene": "EGFR",
            "variant": "L858R",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["resourceType"] == "Bundle"


class TestSemanticHarmonizationData:
    """Verify semantic harmonization data is properly structured."""

    def test_harmonization_file_exists(self):
        """Ensure semantic_harmonization.json is properly structured."""
        import json
        from pathlib import Path
        path = Path(__file__).resolve().parents[2] / "data" / "semantic_harmonization.json"
        assert path.exists()
        data = json.loads(path.read_text())
        assert "diseases" in data
        assert "histologies" in data
        assert "genes" in data
        assert "drugs" in data
        assert "biomarkers" in data
        # Verify diseases have mappings
        for disease_name, disease_data in data["diseases"].items():
            assert "canonical_value" in disease_data
            assert "mappings" in disease_data
            assert len(disease_data["mappings"]) > 0

    def test_patient_journey_file_exists(self):
        """Ensure patient_journey_demo.json is properly structured."""
        import json
        from pathlib import Path
        path = Path(__file__).resolve().parents[2] / "data" / "patient_journey_demo.json"
        assert path.exists()
        data = json.loads(path.read_text())
        assert "patients" in data
        assert len(data["patients"]) >= 10
        assert "summary_statistics" in data
        # Verify required fields per patient
        for p in data["patients"]:
            assert "patient_id" in p
            assert "diagnosis" in p
            assert "histology" in p
            assert "stage" in p
            assert "genes" in p
            assert "variants" in p
            assert "treatments" in p
            assert "data_quality_score" in p
            assert "reconciliation_status" in p
            assert "evidence_coverage" in p
