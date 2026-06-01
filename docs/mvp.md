# MVP Definition

## Project Name

OncoReconcile AI

## MVP Name

Human-Governed Oncology Reconciliation Workbench

---

## MVP Goal

Transform messy oncology entities into trusted canonical oncology concepts.

The MVP focuses on:

- Cancer type
- Gene
- Variant

The system does not make treatment recommendations or clinical decisions.

---

## User Problem

Oncology data teams receive data from many systems and vendors. The same disease, gene, or variant may appear in different forms.

Examples:

- NSCLC vs Non-Small Cell Lung Cancer
- LUAD vs Lung Adenocarcinoma
- HER2 vs HER-2 vs ERBB2
- p53 vs TP53
- EGFR Ex19del vs EGFR Exon 19 Deletion

This creates friction in:

- Data harmonization
- Evidence aggregation
- Cohort creation
- Research analytics
- Multi-vendor integration

---

## Target Users

Initial MVP users:

- Oncology data engineers
- Clinical genomics data analysts
- Molecular pathology informatics teams
- Translational research teams

Future users may include:

- Molecular pathologists
- Clinical laboratory teams
- Precision oncology platform teams

---

## Inputs

Required:

- `gene`
- `variant`

Optional:

- `cancer_type`
- `case_id`
- `patient_id`

Example:

```json
{
  "case_id": "case_001",
  "cancer_type": "NSCLC",
  "gene": "HER2",
  "variant": "Amplification"
}
```

---

## Outputs

Each input record returns:

- Original input
- Canonical cancer type
- Canonical gene
- Canonical variant
- Evidence context
- AI explanation
- Confidence
- Review status

Example:

```json
{
  "case_id": "case_001",
  "input": {
    "cancer_type": "NSCLC",
    "gene": "HER2",
    "variant": "Amplification"
  },
  "canonical": {
    "cancer_type": "Non-Small Cell Lung Cancer",
    "gene": "ERBB2",
    "variant": "ERBB2 Amplification"
  },
  "evidence": [
    {
      "source": "HGNC",
      "type": "gene_alias",
      "description": "HER2 is a recognized alias of ERBB2."
    }
  ],
  "explanation": "HER2 was reconciled to ERBB2 because HER2 is a recognized alias. Amplification was interpreted in the context of ERBB2.",
  "confidence": "HIGH",
  "review_status": "AUTO_RECONCILE"
}
```

---

## Confidence Rules for MVP

| Condition | Confidence |
|---|---|
| Exact dictionary or alias match | HIGH |
| Partial/fuzzy match or missing context | MEDIUM |
| LLM-only suggestion or weak evidence | LOW |
| No match | LOW |

---

## Review Recommendation Rules for MVP

| Confidence | Review Status |
|---|---|
| HIGH | AUTO_RECONCILE |
| MEDIUM | REVIEW_REQUIRED |
| LOW with candidate | REVIEW_REQUIRED |
| LOW without candidate | CANNOT_RECONCILE |

---

## Standards Alignment

The MVP uses a simplified Canonical Oncology Concept Object.

Future versions may align with:

- HGNC
- HGVS
- ClinVar
- CIViC
- GA4GH VRS
- CAT-VRS
- FHIR Genomics
- OMOP Oncology extensions

CAT-VRS is important for future standards alignment, but it is not required for the first working MVP implementation.

---

## MVP Success Criteria

By the end of the MVP phase, the team should demonstrate:

1. Upload or submit oncology records.
2. Reconcile cancer type, gene, and variant.
3. Show canonical concepts.
4. Show evidence and explanation.
5. Show confidence and review status.
6. Download or display final results.
7. Demonstrate at least 20 NSCLC benchmark cases.
