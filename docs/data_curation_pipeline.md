# OncoReconcile AI Data Collection & Curation Pipeline

## Overview

OncoReconcile AI uses a human-governed biomedical data curation pipeline to build trusted oncology knowledge assets for entity resolution, benchmark evaluation, interoperability workflows, and future AI applications.

Rather than relying solely on AI-generated mappings, the platform combines public biomedical knowledge sources, automated collection, human review, curated catalogs, benchmark generation, and governance workflows.

The objective is to create explainable, reproducible, and AI-ready oncology data assets.

```text
Public Biomedical Sources
          ↓
Automated Collection
          ↓
Candidate Data
          ↓
Human Review & Curation
          ↓
Curated Knowledge Catalogs
          ↓
Benchmark Generation
          ↓
Reconciliation Engine
          ↓
Evaluation & Governance
```

---

## Data Sources

### Gene Alias Collection

**Source:** MyGene.info

**Purpose:** Gene alias collection and canonical gene symbol normalization.

Examples:

| Input | Canonical |
| ----- | --------- |
| HER2  | ERBB2     |
| HER-2 | ERBB2     |
| HER1  | EGFR      |
| p53   | TP53      |

Outputs:

```text
data/gene_aliases.json
data/raw/raw_gene_alias_candidates.json
```

---

### Variant Candidate Collection

**Source:** CIViC (Clinical Interpretation of Variants in Cancer)

**Purpose:** Collection of candidate oncology variants and variant aliases.

Examples:

| Input   | Canonical             |
| ------- | --------------------- |
| Ex19del | EGFR Exon 19 Deletion |
| L858R   | EGFR L858R            |
| T790M   | EGFR T790M            |
| ITD     | FLT3 ITD              |

Outputs:

```text
data/raw/civic_variant_candidates.csv
```

---

### Disease Alias Curation

Examples:

| Input | Canonical                     |
| ----- | ----------------------------- |
| NSCLC | Lung Non-Small Cell Carcinoma |
| AML   | Acute Myeloid Leukemia        |
| CRC   | Colorectal Carcinoma          |

Catalog:

```text
data/disease_aliases.json
```

---

### Disease-Gene Context Catalog

Examples:

| Disease                       | Gene  |
| ----------------------------- | ----- |
| Lung Non-Small Cell Carcinoma | EGFR  |
| Breast Carcinoma              | ERBB2 |
| Acute Myeloid Leukemia        | FLT3  |

Catalog:

```text
data/disease_gene_catalog.csv
```

---

### Gene-Variant Catalog

Examples:

| Gene | Variant               |
| ---- | --------------------- |
| EGFR | EGFR Exon 19 Deletion |
| EGFR | EGFR L858R            |
| KRAS | KRAS G12C             |
| FLT3 | FLT3 ITD              |

Catalog:

```text
data/gene_variant_catalog.csv
```

---

## Human-Governed Curation

A core principle of OncoReconcile AI is that downloaded biomedical data is not automatically promoted into production catalogs.

```text
Downloaded Candidate Data
          ↓
Human Review
          ↓
Curated Catalog
          ↓
Production Reconciliation
```

Governance principles:

* Ambiguous concepts route to REVIEW_REQUIRED
* Unknown concepts route to CANNOT_RECONCILE
* Evidence is preserved for reviewer inspection
* Human experts remain responsible for final decisions

Examples:

```text
TRK
NTRK
Fusion candidate
```

↓

```text
REVIEW_REQUIRED
```

---

## Benchmark Generation

Benchmark datasets are generated from curated catalogs and reviewed mappings.

Purpose:

* Regression testing
* Evaluation dashboard metrics
* Accuracy tracking
* Governance validation
* False auto-accept monitoring

Current benchmark assets:

```text
data/benchmark_cases.csv
data/benchmark_v2.csv
```

### Current Benchmark Status

| Metric                       | Value |
| ---------------------------- | ----- |
| Benchmark Cases              | 500   |
| Disease Accuracy             | 68.6% |
| Gene Accuracy                | 96.6% |
| Variant Accuracy             | 94.6% |
| Safety-Aware Status Accuracy | 89.8% |
| False Auto-Accept Rate       | 0%    |

---

## External Evidence Sources

Current evidence integrations include:

| Source                  | Purpose                       |
| ----------------------- | ----------------------------- |
| MyGene.info             | Gene aliases                  |
| CIViC                   | Variant candidates            |
| ClinVar                 | Variant reference support     |
| MyVariant.info          | External evidence retrieval   |
| HGNC                    | Gene nomenclature             |
| ClinGen Allele Registry | Variant reference identifiers |

These sources support evidence gathering but do not replace human review when uncertainty exists.

---

## Future Data Sources

Planned future integrations include:

* NCIt
* OncoTree
* COSMIC
* OncoKB
* SEER
* TCGA
* AACR Project GENIE
* GA4GH VRS
* GA4GH Cat-VRS
* GA4GH VA-Spec
* FHIR Genomics
* OMOP Oncology

---

## Strategic Importance

OncoReconcile AI is building a governed biomedical knowledge asset and data quality infrastructure rather than relying solely on AI-generated mappings.

This supports:

* Precision Oncology
* Clinical Research
* Healthcare Interoperability
* Data Governance
* AI Readiness
* Enterprise Data Quality Programs

The long-term vision is to create trusted oncology data infrastructure that improves the quality and explainability of data used by healthcare analytics and future AI systems.

---

## Technical Implementation (Appendix)

```bash
python scripts/download_gene_aliases_from_mygene.py
python scripts/download_variant_candidates_from_civic_graphql.py
python scripts/create_gene_variant_catalog.py
python scripts/create_expanded_gene_variant_catalog.py
python scripts/create_curated_catalog_from_review.py
python scripts/generate_benchmark_cases_from_catalogs.py
```
