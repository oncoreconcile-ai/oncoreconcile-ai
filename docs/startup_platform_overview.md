# OncoReconcile AI

# Startup Platform Overview

## AI-Powered Precision Oncology Data Quality, Governance & Interoperability Platform

---

# Vision

OncoReconcile AI is building the data quality and interoperability layer for precision oncology.

Our mission is to transform fragmented clinical and genomic data into trustworthy, explainable, and AI-ready information that can power the next generation of healthcare analytics, clinical research, and precision medicine applications.

We believe that healthcare AI can only be as reliable as the data it consumes.

Before organizations can successfully deploy advanced analytics, machine learning, large language models, or clinical decision support systems, they must first solve a fundamental challenge:

**Data quality.**

---

# The Problem

Modern oncology ecosystems generate large amounts of clinical and genomic information.

These data originate from:

* Electronic Health Records (EHR)
* Molecular Diagnostic Laboratories
* Clinical Trial Systems
* Cancer Registries
* Research Databases
* Real-World Evidence Platforms
* Claims Systems

Unfortunately, the same biological concept often appears under different names.

Examples include:

| Input    | Canonical Concept                |
| -------- | -------------------------------- |
| HER2     | ERBB2                            |
| HER1     | EGFR                             |
| p53      | TP53                             |
| NSCLC    | Lung Non-Small Cell Carcinoma    |
| Ex19del  | EGFR Exon 19 Deletion            |
| FLT3 ITD | FLT3 Internal Tandem Duplication |

As organizations scale precision oncology initiatives, inconsistent terminology becomes a major bottleneck.

This affects:

* Cohort generation
* Biomarker analytics
* Clinical trial matching
* AI model training
* Data integration
* Healthcare interoperability

Many organizations still rely on expensive manual curation workflows.

---

# Our Solution

OncoReconcile AI combines artificial intelligence with human governance to create trustworthy oncology data.

The platform automatically:

* Harmonizes diseases
* Harmonizes genes
* Harmonizes variants
* Retrieves supporting evidence
* Generates confidence scores
* Produces explainable recommendations
* Escalates uncertain cases for review

Rather than replacing experts, the platform augments expert decision-making.

---

# Platform Overview

```text
Raw Oncology Data
        |
        v

Entity Resolution

        |
        v

Evidence Intelligence

        |
        v

Confidence Scoring

        |
        v

Human Governance

        |
        v

FHIR / OMOP Export

        |
        v

Analytics & AI Applications
```

---

# Core Platform Modules

## 1. Clinical Data Harmonization

Transforms inconsistent oncology terminology into canonical representations.

Capabilities:

* Disease reconciliation
* Gene reconciliation
* Variant reconciliation
* Alias normalization
* Fuzzy matching
* Context-aware resolution

---

## 2. Evidence Intelligence

Supports reviewer decisions through evidence retrieval.

Sources include:

* Local oncology catalogs
* MyVariant.info
* ClinVar
* CIViC
* ClinGen resources

Capabilities:

* Evidence aggregation
* Evidence packages
* Provenance capture
* Explainable recommendations

---

## 3. Human-Governed AI

The platform is designed around governance.

Governance outcomes:

### AUTO_RECONCILE

High-confidence mappings.

### REVIEW_REQUIRED

Ambiguous mappings requiring expert review.

### CANNOT_RECONCILE

Insufficient evidence.

This approach prioritizes trust and safety.

---

## 4. Precision Oncology Analytics

Future enterprise capabilities include:

* Cohort analytics
* Biomarker analytics
* Disease analytics
* Data quality analytics
* Governance analytics

These capabilities allow organizations to measure and improve data quality at scale.

---

## 5. Interoperability Layer

The platform is designed to support industry standards.

Current and future capabilities include:

* FHIR export
* OMOP export
* Knowledge graph export
* Standards-aligned provenance

This enables downstream integration with healthcare ecosystems.

---

## Data Collection & Curation Pipeline

```text
Public Biomedical Sources
          ↓
Automated Collection Scripts
          ↓
Candidate Data
          ↓
Human Review / Curation
          ↓
Curated Knowledge Catalogs
          ↓
Benchmark Generation
          ↓
Reconciliation Engine
          ↓
Evaluation & Governance
```

The current pipeline combines public sources, automated collection, and controlled human promotion:

1. **MyGene.info** — gene alias collection and symbol support through [`download_gene_aliases_from_mygene.py`](../scripts/download_gene_aliases_from_mygene.py). Outputs: [`raw_gene_alias_candidates.json`](../data/raw/raw_gene_alias_candidates.json) and [`gene_aliases.json`](../data/gene_aliases.json).
2. **CIViC** — cancer-variant candidate collection through [`download_variant_candidates_from_civic_graphql.py`](../scripts/download_variant_candidates_from_civic_graphql.py). Output: [`civic_variant_candidates.csv`](../data/raw/civic_variant_candidates.csv).
3. **Disease aliases** — [`disease_aliases.json`](../data/disease_aliases.json), the manually curated MVP disease terminology knowledge base.
4. **Disease-gene catalog** — [`disease_gene_catalog.csv`](../data/disease_gene_catalog.csv), a curated/static contextual support file.
5. **Gene-variant catalog** — produced through [`create_gene_variant_catalog.py`](../scripts/create_gene_variant_catalog.py), [`create_expanded_gene_variant_catalog.py`](../scripts/create_expanded_gene_variant_catalog.py), or [`create_curated_catalog_from_review.py`](../scripts/create_curated_catalog_from_review.py). Output: [`gene_variant_catalog.csv`](../data/gene_variant_catalog.csv).
6. **Benchmark generation** — [`generate_benchmark_cases_from_catalogs.py`](../scripts/generate_benchmark_cases_from_catalogs.py) produces [`benchmark_cases.csv`](../data/benchmark_cases.csv); [`benchmark_v2.csv`](../data/benchmark_v2.csv) is the current evaluation benchmark and contains 500 cases.

| Data Source | Purpose | Current Status |
|---|---|---|
| MyGene.info | Gene aliases | Integrated |
| CIViC | Variant candidates | Integrated |
| ClinVar | Evidence support | Integrated |
| MyVariant.info | Evidence retrieval | Integrated |
| HGNC | Gene nomenclature support | Curated / integrated |
| ClinGen Allele Registry | Variant reference support | Integrated |
| Internal Curated Catalogs | Production mappings | Active |

Downloaded candidate data is not blindly promoted into production. Candidate aliases and variants are reviewed before becoming curated catalog entries. Ambiguous terms such as `TRK` should route to `REVIEW_REQUIRED`; unknown terms should route to `CANNOT_RECONCILE`.

Future expansion may include NCIt, OncoTree, COSMIC, OncoKB, SEER, TCGA, AACR GENIE, GA4GH VRS, GA4GH Cat-VRS, GA4GH VA-Spec, FHIR Genomics, and OMOP Oncology. These are roadmap targets rather than claims of current clinical validation.

This governed data pipeline demonstrates that OncoReconcile AI is building a reusable biomedical knowledge asset and data quality infrastructure, not just a one-off reconciliation demo.

---

# Why Human Governance Matters

Many AI systems focus exclusively on automation.

Healthcare requires a different approach.

OncoReconcile AI intentionally routes uncertain cases to human reviewers.

Benefits include:

* Increased trust
* Better transparency
* Reduced automation risk
* Improved reproducibility
* Regulatory readiness

Our philosophy is:

**"AI assists. Humans decide."**

---

# Target Customers

## Cancer Centers

Need:

* Biomarker harmonization
* Cohort generation
* Oncology analytics

---

## Molecular Diagnostic Laboratories

Need:

* Variant standardization
* Quality control
* Reporting consistency

---

## Pharmaceutical Companies

Need:

* Biomarker analytics
* Clinical development support
* Precision oncology datasets

---

## Clinical Research Organizations

Need:

* Trial data harmonization
* Data quality improvement

---

## Healthcare Data Platforms

Need:

* Standardized oncology data
* Interoperability services
* AI-ready datasets

---

# Market Opportunity

Precision oncology continues to generate increasing volumes of genomic and clinical data.

Organizations face growing pressure to:

* Improve data quality
* Reduce manual effort
* Support AI initiatives
* Improve interoperability

OncoReconcile AI addresses these needs by providing a scalable governance and harmonization platform.

---

# Business Model

Future commercial offerings may include:

## Professional Services

* Data harmonization
* FHIR implementation
* OMOP implementation
* Oncology data consulting

## SaaS Platform

* Individual subscriptions
* Team subscriptions
* Enterprise deployments

## Enterprise APIs

* Reconciliation API
* Evidence API
* Governance API
* Interoperability API

---

# Competitive Differentiation

Many existing solutions focus on:

* Variant databases
* Knowledgebases
* Generic AI assistants
* Terminology lookups

OncoReconcile AI combines:

* Biomedical entity resolution
* Evidence-supported recommendations
* Explainable AI
* Human governance
* Interoperability
* Benchmark-driven validation

This positions the platform as a biomedical data quality layer rather than simply a terminology lookup tool.

---

# Long-Term Vision

Our long-term vision is to become the trusted data quality and interoperability layer for precision oncology.

Future directions include:

* Multi-cancer support
* Biomedical knowledge graphs
* Enterprise APIs
* AI-assisted curation
* Clinical trial harmonization
* Precision oncology intelligence platforms

As healthcare organizations increasingly adopt AI, the demand for trustworthy and explainable data infrastructure will continue to grow.

OncoReconcile AI aims to become a foundational component of that future ecosystem.

---

## Additional Resources

* **Repository:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/startup-platform
* **README:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/README.md
* **Architecture:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/architecture.md
* **Architecture Diagrams:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/architecture_diagrams.md
* **Commercial Strategy:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/commercial_strategy.md
* **Roadmap:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/blob/startup-platform/docs/roadmap.md
