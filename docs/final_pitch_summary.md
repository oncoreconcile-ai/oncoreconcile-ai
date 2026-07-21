# OncoReconcile AI

## One-Page Judge Pitch — Team Variant Vanguard

**OncoReconcile AI makes precision oncology data trustworthy before analytics and AI depend on it.**

> *The same HER2 variant can arrive as HER2, HER-2, ERBB2, or V-erb-b2 — from four different data partners on the same project. Every time, someone must manually reconcile them. OncoReconcile AI automates this so experts can focus on science, not data plumbing.*

---

### The Problem

Cancer centers, molecular laboratories, pharmaceutical teams, CROs, and healthcare data platforms receive oncology data with inconsistent disease names, gene aliases, variant formats, and coding systems.

| If you receive... | ...it should map to | But without OncoReconcile, you must: |
|---|---|---|
| `HER2`, `HER-2`, `ERBB2`, `V-erb-b2` | ERBB2 | Look up each alias, check HGNC, choose a standard |
| `NSCLC`, `LUAD`, `non-small cell` | Lung Non-Small Cell Carcinoma | Check disease ontology, normalize manually |
| `Ex19del`, `del19`, `E746_A750del` | EGFR Exon 19 Deletion | Match variant patterns, verify with literature |

At enterprise scale, these small inconsistencies create fragmented cohorts, manual curation, unreliable analytics, difficult interoperability, and lower-confidence AI. **Organizations spend expert time on data plumbing instead of science — and every project starts from scratch.**

### The Solution

OncoReconcile AI is an AI-powered data quality, governance, and analytics platform for precision oncology. It combines:

| Capability | What it does |
|---|---|
| **Reconciliation** | Normalizes disease, gene, and variant terminology with deterministic rules, curated catalogs, and fuzzy matching |
| **Evidence** | Retrieves guarded evidence from MyVariant.info, ClinVar, CIViC, and an experimental ClinGen lookup |
| **Confidence** | 6-signal numeric score — transparent, not a black box |
| **Governance** | Review queue, approve/reject/edit/reopen, Cohen's kappa, adjudication |
| **Interoperability** | FHIR R4, OMOP CDM v5.4, and knowledge graph export prototypes |
| **Analytics** | Patient journey, executive dashboard, quality and governance metrics |

### Why It Is Different

| | Manual Curation | Mapping Tools | Generic LLMs | **OncoReconcile AI** |
|---|---|---|---|---|
| Variant normalization | Manual | Partial | Inconsistent | **✓** |
| Evidence retrieval | Manual | ✗ | Hallucinates | **✓** (guarded external connectors) |
| Confidence scoring | Subjective | ✗ | ✗ | **✓** (numeric) |
| Human governance | ✗ | ✗ | ✗ | **✓** (queue + kappa) |
| Audit trail | ✗ | ✗ | Unreliable | **✓** (full history) |
| FHIR/OMOP export | Manual | ✗ | ✗ | **✓** (prototypes) |
| Safety testing (0% false auto-accept) | ✗ | ✗ | ✗ | **✓** (benchmark) |

### Working Validation

| Metric | Result |
|---|---|
| Backend tests | **149 collected; 146 passing; 3 skipped** |
| Benchmark cases | **191 curated + 500 expanded** |
| Gene accuracy | **96.6%** |
| False auto-accept rate | **0%** |
| Frontend build | **Passing** |

### Business Model

1. **Professional services** — immediate revenue through harmonization and FHIR/OMOP projects
2. **SaaS subscriptions** — team ($999/mo) and enterprise (custom)
3. **Enterprise APIs** — reconciliation, evidence, governance, and export APIs

### Target Customers

Cancer centers · Molecular diagnostics labs · CROs · Pharmaceutical companies · Genomic knowledgebases · Healthcare AI platforms

### The Ask

We are seeking pilot partners and advisors who can help validate measurable workflow value.

**Repository:** https://github.com/oncoreconcile-ai/oncoreconcile-ai/tree/enterprise-patient-journey-demo

*OncoReconcile AI is a prototype data harmonization and governance platform. Not clinically validated. Not a medical device.*
