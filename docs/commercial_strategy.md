# OncoReconcile AI — Commercial Product Strategy

**Author:** Leadership Team
**Date:** June 20, 2026
**Status:** Board-level strategy document

---

## Executive Summary

OncoReconcile AI is a **human-governed biomedical AI platform** that transforms inconsistent oncology terminology — disease names, gene symbols, and variant descriptions — into canonical, standards-ready representations with auditable confidence, evidence provenance, and explicit human-in-the-loop governance.

The product sits at the intersection of three converging market forces:

| Force | Signal |
|---|---|
| **Precision oncology scale** | 10M+ next-gen sequencing results/year globally; every one requires normalization |
| **Regulatory pressure** | FDA checks on AI/ML in medical devices; EU AI Act governance requirements |
| **Interoperability mandates** | US ONC Cures Act, HL7 FHIR Genomics, OHDSI OMOP, GA4GH standards adoption |

OncoReconcile's competitive moat is its **governance-first architecture** — it does not hide uncertainty behind a black box. It surfaces ambiguity, preserves categorical uncertainty, routes hard cases to humans, measures reviewer agreement, and exports everything in standards-compatible formats.

---

## 1. Product Positioning

### Positioning Statement

> OncoReconcile AI is the first human-governed oncology terminology engine that normalizes disease, gene, and variant data with deterministic confidence scoring, evidence provenance, and GA4GH/FHIR/OMOP-ready exports — designed for regulated clinical genomics environments where black-box AI is unacceptable.

### Why This Matters Now

Existing approaches fail in regulated environments:

| Approach | Problem |
|---|---|
| Manual curation (spreadsheets) | Doesn't scale; no audit trail; institutional knowledge walks out the door |
| Black-box ML normalization | No explainability; cannot be validated for regulatory use; hallucinations |
| In-house lookup tables | One-off; brittle; never updated; no cross-institution alignment |
| Public knowledge bases (CIViC, ClinVar) | No governance workflow; no SLA; no commercial support |

OncoReconcile is **the only product** that provides:

- **Deterministic normalization** (no hallucinations — every output traceable to a rule or evidence source)
- **Explicit ambiguity preservation** (Cat-VRS-inspired categorical fusion handling)
- **Human governance workflow** with agreement metrics and adjudication
- **Standards-ready exports** (VRS, Cat-VRS, VA-Spec, PROV-O, FHIR-ready)
- **Benchmark-validated accuracy** (191 curated cases, 43 passing tests)

### Product Principles

1. **Deterministic before probabilistic** — rules first, AI suggestions are advisory only
2. **Preserve ambiguity** — never guess when uncertain; route to human review
3. **Every decision is auditable** — full provenance chain from input through evidence to canonical output
4. **Human governance is a feature, not a bug** — reviewer agreement metrics, adjudication, catalog promotion controls
5. **Interoperable by default** — exports map to GA4GH VRS, Cat-VRS, VA-Spec, FHIR, OMOP concepts

---

## 2. Customer Segments

### Tier 1: Early Adopters (0–12 months)

| Segment | Pain Point | Use Case | Willingness to Pay |
|---|---|---|---|
| **Molecular Pathology Labs** (200–500 bed hospitals) | Inconsistent reporting across pathologists; manual normalization for tumor boards | Normalize somatic variant reports to canonical terms before tumor board review | $15K–$50K/yr |
| **Clinical Genomics CROs** | Ingesting lab data from 20+ sites; each uses different notation | Batch normalization pipeline for clinical trial cohort assembly | $50K–$200K/yr |
| **Academic Medical Center Informatics Teams** | Data harmonization for tissue-agnostic trial matching | Real-time normalization of sequenced patient records against trial eligibility criteria | $20K–$80K/yr |
| **RWE Data Aggregators** | Ingesting EMR and lab data from heterogeneous sources | Normalize to OMOP oncology CDM for real-world evidence studies | $100K–$500K/yr |

### Tier 2: Expansion (12–24 months)

| Segment | Pain Point | Use Case |
|---|---|---|
| **Biopharma Translational Research** | Internal biomarker data across 50+ trials uses different terminologies | Harmonize for cross-trial biomarker analysis |
| **Cancer Registry Teams** (SEER, state registries) | Manual coding of ICD-O-3; huge backlogs | Semi-automated coding with human review |
| **Precision Oncology Startups** | Building on top of inconsistent public data | Normalization pipeline as a service |
| **National Health Systems** (NHS, Kaiser) | System-wide data harmonization for population oncology | Enterprise-scale normalization |

### Tier 3: Strategic (24+ months)

| Segment | Use Case |
|---|---|
| **Diagnostic Vendors** (FoundationOne, Guardant, Tempus) | Normalize their own variant output for interoperability with hospital systems |
| **EHR Vendors** (Epic, Cerner, Meditech) | Built-in FHIR Genomics normalization pipeline |
| **Regulatory Bodies** (FDA, EMA) | Standardized submission format for tumor genomic data |

---

## 3. Service Offerings

### 3.1 Managed Reconciliation Service

For customers who want results without running infrastructure.

**Scope:**
- Customer uploads CSV/JSON records via portal or SFTP
- OncoReconcile processes, applies governance workflow, returns canonical output
- Weekly/biweekly batch cycle or real-time API

**Includes:**
- Dedicated reviewer pool for REVIEW_REQUIRED cases
- Monthly catalog refresh with customer-specific aliases
- Curation report and provenance export
- 99.5% SLA on processing time

**Pricing:** $0.15–$0.50 per record with volume tiers

### 3.2 Custom Catalog Curation

**Scope:**
- Build and maintain a customer-specific gene-variant-disease catalog
- Seed from public knowledge bases (CIViC, ClinVar, OncoKB where licensed)
- Add customer's historical data and institutional aliases
- Quarterly review cycle with customer subject matter experts

**Pricing:** $25K–$100K initial setup + $5K–$20K/mo maintenance

### 3.3 Standards Alignment Consulting

**Scope:**
- Audit existing data pipelines for FHIR Genomics, OMOP Oncology, or GA4GH VRS compliance
- Implement transformation layer
- Validate against published standards test suites
- Document for regulatory submission

**Pricing:** $15K–$50K per engagement (1–3 months)

### 3.4 Reviewer Governance Program

**Scope:**
- Deploy the governance dashboard (review queue, agreement metrics, adjudication)
- Train customer staff on dual-reviewer workflow
- Configure reviewer roles, adjudication rules, and escalation paths
- Monthly governance report with kappa trends

**Pricing:** $10K setup + $2K/mo per reviewer seat

---

## 4. SaaS Offerings

### 4.1 Core Platform — Reconcile Engine

| Feature | Free | Professional | Enterprise |
|---|---|---|---|
| Records/month | 5,000 | 100,000 | Unlimited |
| Reconcile API (REST) | ✓ | ✓ | ✓ |
| Batch upload (CSV) | ✓ | ✓ | ✓ |
| FHIR Genomics export | — | ✓ | ✓ |
| OMOP Oncology export | — | ✓ | ✓ |
| Custom alias catalog | — | 1 catalog | Unlimited |
| Review queue dashboard | ✓ | ✓ | ✓ |
| Reviewer agreement metrics | — | ✓ | ✓ |
| Adjudication workflow | — | Up to 3 reviewers | Unlimited |
| Knowledge graph export | — | ✓ | ✓ |
| Standards-ready exports | VRS-ready | All stubs | Full compliance |
| SLA | Best effort | 99.5% | 99.9% |
| SSO / SAML | — | — | ✓ |
| Audit log retention | 30 days | 1 year | 7 years |
| HIPAA BAA | — | ✓ | ✓ |
| Self-hosted option | — | — | ✓ |

### 4.2 Governance Dashboard

A web-based application that provides:

- **Real-time review queue** — filter by status, priority, reviewer assignment
- **Side-by-side comparison** — original input vs. canonical proposal with evidence
- **One-click decisions** — approve, reject, edit, or escalate
- **Agreement analytics** — per-reviewer kappa scores, disagreement trends
- **Adjudication console** — senior curator resolves disputes between reviewers
- **Catalog promotion controls** — governed, versioned promotion of reviewed records to the curated catalog

### 4.3 Benchmark & Validation Suite

- Online benchmark runner (191 cases and growing)
- Precision/recall/F1 per entity type (disease, gene, variant)
- Detailed failure analysis with suggested catalog updates
- Custom benchmark creation for customer-specific validation

### 4.4 Export Connectors

| Connector | Status | Description |
|---|---|---|
| VRS-ready | MVP stub | GA4GH VRS-inspired variant representation |
| Cat-VRS-ready | MVP stub | GA4GH Categorical VRS-inspired ambiguity preservation |
| VA-Spec-ready | MVP stub | VA-Spec-inspired evidence statement |
| PROV-O-inspired | MVP | W3C PROV-O provenance chain |
| JSON-LD Knowledge Graph | MVP | Full graph with entities, evidence, and provenance |
| **FHIR Genomics** | Roadmap (30-day) | FHIR DiagnosticReport, MolecularSequence, Variant |
| **OMOP Oncology** | Roadmap (90-day) | OMOP zero-observation table integration |

---

## 5. API Offerings

### 5.1 Reconcile API

```
POST /reconcile
POST /reconcile/batch
POST /reconcile/upload
```

Core normalization endpoint. Input: gene + variant (disease optional). Output: canonical concepts, evidence, confidence score, review status, explanation, alternatives, audit trail.

### 5.2 Governance API

```
GET  /review-queue
GET  /review-queue/{case_id}
POST /review-queue/{case_id}/decision
POST /review-queue/{case_id}/adjudicate
GET  /review-queue-metrics
```

Programmatic access to the governance workflow. Enables integration with existing LIMS, EHR, or workflow systems.

### 5.3 Export API

```
POST /export/provenance
POST /export/knowledge-graph
POST /export/vrs-ready
POST /export/cat-vrs-ready
POST /export/va-spec-ready
POST /curation/report
```

Retrieve reconciliation results in multiple standards-compatible formats.

### 5.4 Benchmark API

```
GET  /benchmark
```

Run the benchmark suite and return accuracy, coverage, and failure analysis.

### 5.5 API Rate Limits & Tiers

| Tier | Rate Limit | Max Batch Size | SLA |
|---|---|---|---|
| Free | 10 req/s, 5K/mo | 100 records | Best effort |
| Professional | 50 req/s, 100K/mo | 10K records | 99.5% |
| Enterprise | 200 req/s | 100K records | 99.9% |
| Self-hosted | Unlimited | Unlimited | N/A |

---

## 6. Pricing Strategy

### Philosophy

**Value-based pricing** tied to the cost of doing nothing:
- A single mis-normalized gene in a clinical trial cohort can cost $50K+ in rework or missed enrollment
- Manual normalization costs $2–$10 per record at scale (curator time)
- Our automated + governed workflow targets **$0.05–$0.50 per record**

### SaaS Pricing Tiers

| Tier | Price | Annual (2mo free) | Target Customer |
|---|---|---|---|
| **Free** | $0/mo | $0/yr | Evaluation, academic, individual researchers |
| **Startup** | $499/mo | $5,490/yr | Early-stage precision oncology companies |
| **Professional** | $2,499/mo | $27,490/yr | Mid-sized labs, CROs, academic medical centers |
| **Enterprise** | Custom quote | Custom | Health systems, biopharma, RWE aggregators |

### Add-On Pricing

| Add-On | Price |
|---|---|
| Additional reviewer seat (Professional) | $499/mo/seat |
| Custom alias catalog (per catalog) | $2,499 setup + $499/mo |
| FHIR Genomics export connector | Included in Professional+ |
| OMOP Oncology export connector | Included in Enterprise |
| Managed reconciliation service | $0.15–$0.50 per record |
| Professional services (consulting) | $350–$500/hr |

### Self-Hosted Enterprise Pricing

| Component | Price |
|---|---|
| Annual license (unlimited records) | $75K–$250K/yr depending on deployment scale |
| Annual maintenance (updates, support) | 20% of license |
| Implementation (on-site or remote) | $25K–$75K |
| Custom integration (EHR, LIMS, etc.) | $15K–$50K per connector |

### Discount Structure

- **Academic / non-profit:** 40% discount on SaaS tiers
- **Annual prepayment:** 2 months free (16.7% discount)
- **Volume records:** $0.25/record over 100K/mo (Professional), negotiable at Enterprise
- **Early adopter (2026):** 30% discount for first-year commitment

---

## 7. Competitive Analysis

### Competitive Landscape

| Competitor | Category | Strength | Weakness vs. OncoReconcile |
|---|---|---|---|
| **OncoKB** (MSKCC) | Curated knowledge base | Authoritative, NCCN-referenced | Not a normalization engine; restricted access; no governance workflow; no interoperability exports |
| **CIViC** (Open Source) | Community knowledge base | Open, community-driven, cancer-specific | Not normalization; no API governance; no commercial support; no SLAs |
| **ClinGen / ClinVar** (NCBI) | Public variant database | Curated clinical significance | Allele-level only (no disease/gene normalization); no workflow |
| **VICC** (Consortium) | Standards consortium | Driving GA4GH VRS/Cat-VRS | Not a product — standards and tools only |
| **VarSome** (Commercial) | Variant interpretation | Large user base, clinical interpretation | Not focused on normalization; no oncology-specific governance |
| **MolecularMatch** | Clinical trial matching | Strong trial database | Not a normalization engine; different use case |
| **QIAGEN IPA** | Pathway analysis | Enterprise integration | Expensive ($50K+/yr); not normalization-focused; no governance exports |
| **Seven Bridges** | Genomics platform | Full pipeline infrastructure | Platform, not normalization engine; different layer |
| **Google DeepVariant** | Variant calling | Google-scale ML | Variant *calling*, not *normalization*; no governance |

### OncoReconcile Differentiators

| Dimension | Competitors | OncoReconcile |
|---|---|---|
| **Normalization scope** | Single entity type (usually variants only) | Disease + gene + variant (+ categorical fusions) |
| **Governance workflow** | None | Full review queue, agreement metrics, adjudication |
| **Ambiguity handling** | Silent failure or forced guess | Cat-VRS-inspired ambiguity preservation |
| **Explainability** | None or opaque ML | Deterministic text + evidence chain + scores |
| **Standards alignment** | None | VRS, Cat-VRS, VA-Spec, PROV-O, FHIR-ready, OMOP-ready |
| **External evidence** | None or single source | Multi-source concurrent lookup (MyVariant, ClinVar, CIViC, ClinGen) with graceful degradation |
| **Human-in-the-loop** | None | First-class; reviewer roles, kappa, adjudication |
| **Self-hosted option** | Rarely available | Enterprise self-hosted |
| **Regulatory readiness** | None | Designed for audit trails, HIPAA BAA, governed promotion |

### Market Positioning Matrix

```
                      HIGH governance
                           │
                           │
        VarSome ───────────┤─────────── OncoReconcile AI
                           │
      ─────────────────────┼─────────────────────── HIGH automation
                           │
        OncoKB ────────────┤─────────── CIViC
                           │
                      LOW governance
```

OncoReconcile occupies the unique **high-governance, high-automation** quadrant — the product an FDA-regulated clinical genomics team would choose.

---

## 8. Revenue Model

### Revenue Streams

| Stream | Contribution (Year 1) | Contribution (Year 3) |
|---|---|---|
| SaaS subscriptions | 40% | 55% |
| Per-record API consumption | 20% | 15% |
| Self-hosted enterprise licenses | 15% | 20% |
| Professional services | 20% | 5% |
| Marketplace / catalog licensing | 5% | 5% |

### Unit Economics

| Metric | Free | Startup | Professional | Enterprise |
|---|---|---|---|---|
| ACV (Annual Contract Value) | $0 | $5,490 | $27,490 | $75K–$250K |
| Gross margin (cloud) | — | 75% | 80% | 85% |
| Gross margin (self-hosted) | — | — | — | 90%+ |
| Customer acquisition cost | $0 | $1,500 | $8,000 | $25K |
| Sales cycle | Self-serve | 2–4 weeks | 4–8 weeks | 8–16 weeks |

### Revenue Projections

| Year | SaaS Revenue | Enterprise Licenses | Services | Total |
|---|---|---|---|---|
| **Year 1** (2027) | $120K | $75K | $150K | **$345K** |
| **Year 2** (2028) | $480K | $375K | $200K | **$1.055M** |
| **Year 3** (2029) | $1.8M | $1.0M | $250K | **$3.05M** |

**Assumptions:**
- Year 1: 2 Free → 15 Startup × $499, 3 Professional × $2,499, 1 Enterprise at $75K
- Year 2: 5× growth in Startup (75), 5× growth in Professional (15), 3× Enterprise (3)
- Year 3: 2× growth in all segments + first self-hosted deals
- Services revenue declines as % of total as product maturity increases

### Go-to-Market Motion

| Segment | Channel | Sales Motion |
|---|---|---|
| Individual / academic | Self-serve / product-led | Free tier → upgrade via usage limits |
| Startup | Inbound + Developer Relations | API-first; PLG with technical demo |
| Professional (labs, CROs) | Inside sales + Clinical informatics conferences | Demo + free trial + pilot |
| Enterprise | Direct enterprise sales + Channel partners | POC → pilot → enterprise license |

---

## 9. 30-Day Roadmap (July 2026)

**Theme: Productize the MVP for commercial use**

### Week 1-2: FHIR Genomics Export Connector

| Task | Owner | Priority |
|---|---|---|
| Implement FHIR DiagnosticReport exporter from canonical result | Engineering | P0 |
| Implement FHIR MolecularSequence exporter | Engineering | P0 |
| Implement FHIR Variant exporter (VRS mapping optional) | Engineering | P0 |
| Add `POST /export/fhir-genomics` endpoint | Engineering | P0 |
| Write validation tests against published FHIR Genomics examples | Engineering | P1 |
| Document FHIR export format for customers | Technical Writer | P1 |

### Week 2-3: Commercial Readiness

| Task | Owner | Priority |
|---|---|---|
| Implement tenant isolation for SaaS multi-tenancy | Engineering | P0 |
| Add API key authentication and usage tracking | Engineering | P0 |
| Implement rate limiting per tier | Engineering | P0 |
| Build Stripe billing integration | Engineering | P1 |
| Add tier-based feature gating | Engineering | P1 |
| Implement usage dashboard for customers | Frontend | P1 |
| Add 30-day free trial flow (Professional tier) | Product | P1 |

### Week 3-4: Governance Dashboard v1

| Task | Owner | Priority |
|---|---|---|
| Build dedicated reviewer assignment UI | Frontend | P0 |
| Add notification system (email/Slack) for review assignments | Engineering | P0 |
| Build agreement trend visualization (kappa over time) | Frontend | P1 |
| Add catalog promotion controls (governed, versioned) | Engineering | P1 |
| Build adjudication console with side-by-side comparison | Frontend | P1 |
| Add reviewer role management (admin, senior, reviewer) | Engineering | P0 |

### Week 4: Customer Onboarding Materials

| Task | Owner | Priority |
|---|---|---|
| Write customer onboarding guide | Technical Writer | P1 |
| Record product walkthrough video | Product | P1 |
| Create sample integration in Python and JavaScript | Developer Relations | P1 |
| Build public API documentation (OpenAPI) | Engineering | P1 |
| Publish benchmark results page | Frontend | P2 |

**30-Day Deliverable:** A multi-tenant SaaS product with FHIR export, billing, governance dashboard, and self-serve onboarding. Ready for paid Professional tier.

---

## 10. 90-Day Roadmap (July–September 2026)

**Theme: Enterprise-grade governance, OMOP, and first customer pilots**

### Month 2: OMOP Oncology Connector & Catalog Expansion

| Task | Priority |
|---|---|
| Map OncoReconcile canonical concepts to OMOP Oncology CDM | P0 |
| Implement OMOP observation table and fact relationship export | P0 |
| Add `POST /export/omop-oncology` endpoint | P0 |
| Expand benchmark to 500 curated cases | P0 |
| Add disease-gene-variant triplet validation against oncology guidelines (NCCN, ESMO) | P1 |
| Add support for HGVS expressions as variant input | P1 |
| Add LOINC and SNOMED CT code mapping for diseases | P1 |

### Month 2: Reviewer Copilot (AI-Assisted Governance)

| Task | Priority |
|---|---|
| Train a lightweight classifier on existing review decisions | P0 |
| Add "suggested decision" banner on review queue items | P0 |
| Show historical similar-case precedent to reviewer | P0 |
| Add conflict-of-interest flagging (same reviewer on similar case) | P1 |
| Implement reviewer performance scoring (accuracy vs. adjudication outcome) | P1 |
| Add reviewer calibration alerts (kappa trending down) | P1 |

### Month 3: First Customer Pilots

| Task | Priority |
|---|---|
| Identify and onboard 3 pilot customers (1 lab, 1 CRO, 1 academic) | CEO |
| 3-week pilot with onboarding + weekly check-ins | Customer Success |
| Collect structured feedback on workflow, accuracy, governance | Product |
| Implement top 5 customer-requested features from pilot feedback | Engineering |
| Publish case studies from pilot customers (with permission) | Marketing |
| Establish HIPAA BAA process for paid customers | Operations |

### Month 3: Advanced Governance & Audit

| Task | Priority |
|---|---|
| Full audit log with immutable event store (append-only) | P0 |
| Add reviewer blinding (hide other decisions during review) | P0 |
| Implement governance policy engine (configurable kappa thresholds) | P0 |
| Add bulk review actions (approve/reject batch of similar cases) | P1 |
| Add automated quality checks (inconsistent decisions alert) | P1 |
| Build compliance export (FDA 21 CFR Part 11 audit trail) | P1 |

**90-Day Deliverable:** Enterprise-ready governance platform with OMOP connectivity, AI-assisted review copilot, first paid customers onboarded, and a validated path to regulatory compliance.

---

## 11. 12-Month Roadmap (July 2026–June 2027)

**Theme: Scale to a platform, expand markets, build ecosystem**

### Q3 2026 (Months 1-3) — described above

### Q4 2026 (Months 4-6): Platform Expansion

| Initiative | Description | Success Metric |
|---|---|---|
| **GA4GH VRS compliance** | Full VRS 2.0 allele, haplotype, copy number representation | Pass GA4GH test suite |
| **Real-time FHIR subscription** | Subscribe to FHIR server for auto-normalization of incoming records | 3 FHIR-connected health systems |
| **Batch pipeline SDK** | Python SDK for embedding reconciliation in existing pipelines | 500 GitHub stars |
| **Multi-language variant input** | HGVS, VCF, COSMIC, protein notation for variant input | Support 5 input formats |
| **Customer catalog self-service** | UI for adding customer-specific aliases and variants | 100% pilot customers use it |
| **Advanced fuzzy matching** | Soundex, Levenshtein, token-based matching for non-standard input | 95% precision on fuzzy variants |

**Q4 Revenue Target:** $120K ARR

### Q1 2027 (Months 7-9): Scale & Ecosystem

| Initiative | Description | Success Metric |
|---|---|---|
| **Marketplace for curated catalogs** | Oncology-specific: NSCLC catalog, CLL catalog, pediatric catalog | 10 catalogs available |
| **Cross-institution de-identification** | HIPAA-compliant de-identification for multi-site harmonization | 2 multi-site deployments |
| **Regulatory pathway assessment** | Determine 510(k) vs. CLIA vs. CE-IVDR path | Published regulatory white paper |
| **Clinical trial matching pilot** | Normalize patient records against trial eligibility criteria (e.g., ClinicalTrials.gov) | 1 pilot with CRO partner |
| **Multi-language support** | Chinese, Japanese, Korean oncology term normalization | 3 new languages |
| **Community edition launch** | Open-source core engine (Apache 2.0) for community contributions | 200 GitHub stars, 10 contributors |

**Q1 Revenue Target:** $350K ARR

### Q2 2027 (Months 10-12): Market Leadership

| Initiative | Description | Success Metric |
|---|---|---|
| **Enterprise GA (General Availability)** | Full enterprise feature set, HIPAA BAA, SOC 2 Type I | 5 enterprise customers |
| **EHR-native integration** | Epic App Orchard and Cerner integration | 2 health system deployments |
| **Diagnostic vendor partnerships** | Integrate with FoundationOne, Tempus, Guardant output | 1 partnership signed |
| **International expansion** | EU data residency, GDPR compliance, UK NHS data standards | 1 EU customer |
| **Oncology NLP pipeline** | Extract disease/gene/variant from unstructured pathology reports | 90% F1 on extraction |
| **First patent filings** | Ambiguity preservation model, multi-source evidence governance | 3 provisional patents |
| **Series A fundraise** | $5M–$8M based on $1M ARR, validated governance model, enterprise pipeline | $5M+ raised |

**Q2 Revenue Target:** $700K–$1M ARR (run rate approaching $4M)

### 12-Month Milestone Map

```
July 2026                        Jan 2027                          June 2027
│                                 │                                  │
├─ FHIR Genomics export           ├─ Curated catalog marketplace    ├─ Enterprise GA
├─ Omop export                    ├─ Multi-institution de-ident      ├─ Epic integration
├─ Multi-tenant SaaS              ├─ Regulatory assessment          ├─ Series A
├─ Billing / auth                 ├─ Community edition              ├─ Patent filings
├─ Governance dashboard           ├─ Multi-language                 ├─ $1M ARR
├─ AI reviewer copilot            ├─ Clinical trial matching        ├─ International
├─ First pilots (3)               ├─ $350K ARR                      ├─ NLP pipeline
└─ $75K ARR                       └─                                 └─ $4M ARR run rate
```

---

## Appendix A: Standards Alignment Map

| Standard | Current Status | 30-Day | 90-Day | 12-Month |
|---|---|---|---|---|
| **GA4GH VRS** | Stub export | Partial (allele only) | Partial + haplotype | Full VRS 2.0 |
| **GA4GH Cat-VRS** | Stub export | Stable stub | Full categorical preservation | GA4GH test suite |
| **GA4GH VA-Spec** | Stub export | Stable stub | Evidence provenance model | GA4GH test suite |
| **W3C PROV-O** | Inspired proto | Full W3C PROV-O JSON-LD | Stable | Embedded in all exports |
| **FHIR Genomics** | None | DiagnosticReport, MolecularSequence, Variant | Observation, patient bundle | EHR subscription |
| **OMOP Oncology CDM** | None | None | Observation table, fact relationships | Full zero-observation mapping |
| **HL7 v2 / IHE** | None | None | None | Lab result integration |
| **SNOMED CT** | None | Disease code mapping | Gene → SNOMED mapping | Full integrated |
| **LOINC** | None | LOINC for lab observations | Variant → LOINC mapping | Full integrated |

---

## Appendix B: Competitive Feature Matrix

| Feature | OncoReconcile | OncoKB | CIViC | VarSome | QIAGEN IPA |
|---|---|---|---|---|---|
| Disease normalization | ✓ | — | — | — | — |
| Gene normalization | ✓ | — | Only HGNC | ✓ | ✓ |
| Variant normalization | ✓ | ✓ | Partial | ✓ | ✓ |
| Confidence scoring | ✓ | — | — | — | — |
| Deterministic explanation | ✓ | — | — | — | — |
| Evidence provenance | ✓ | — | ✓ | ✓ | ✓ |
| Human review workflow | ✓ | — | — | — | — |
| Reviewer agreement (kappa) | ✓ | — | — | — | — |
| Adjudication workflow | ✓ | — | — | — | — |
| Multi-source evidence | ✓ | Single | Community | Single | Single |
| Ambiguity preservation | ✓ | — | — | — | — |
| Categorical fusion (Cat-VRS) | ✓ | — | — | — | — |
| FHIR export | 30-day | — | — | — | ✓ (limited) |
| OMOP export | 90-day | — | — | — | — |
| GA4GH VRS export | 12-month | — | — | — | — |
| Benchmark suite | ✓ | — | — | — | — |
| Audit trail | ✓ | — | — | Limited | — |
| Self-hosted | ✓ | On-prem license | Open source | — | On-prem |
| **Regulatory-ready** | ✓ | — | — | ✓ (CLIA) | — |

---

## Appendix C: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Slow enterprise sales cycles** (8–16 weeks) | High | High | Self-serve PLG for SMB; invest in developer advocacy |
| **Competitive response from OncoKB/VarSome** | Medium | Medium | Focus on governance workflow they cannot match quickly |
| **Market not ready for governance-first approach** | Low | High | Regulated clinical genomics IS ready; pharma FOMO on AI governance |
| **Open-source competitor emerges** | Medium | Medium | Community edition + proprietary governance layer make it hard to replicate |
| **FHIR/OMOP standards change** | Low | Medium | Abstraction layer decouples internal models from export formats |
| **LLM-based normalization improves** | Medium | Medium | Our moat is governance, not just normalization — LLMs will need governance too |
| **Customer data privacy concerns** | Low | High | Self-hosted option, HIPAA BAA, SOC 2 by Q2 2027 |
| **Funding timeline slips** | Medium | High | Bootstrap with services revenue in Year 1; keep burn low |
| **Key person dependency (Justin)** | High | High | Cross-train Nikolai, Michael, Nikola on all critical modules; document everything |

---

## Appendix D: Strategic Assumptions to Validate

| Assumption | Validation Method | Timeline |
|---|---|---|
| CROs will pay $0.25/record for normalization | 3 pilot customer conversations | Month 1-2 |
| Labs need governance workflow more than accuracy | A/B test; track demo-to-pilot conversion | Month 2-4 |
| Enterprise will self-host rather than use cloud | Track cloud vs. on-prem in pilot conversations | Month 3-6 |
| FHIR export is a purchase trigger for health systems | Track feature requests in pilot feedback | Month 1-3 |
| Reviewer copilot reduces review time by 40% | Measure pilot customer review time before/after | Month 3-6 |
| Academic segment converts at 30% from free tier | Track conversion rates after 90-day free trial | Month 3-6 |
| Series A requires $1M ARR | Investor conversations; track ARR milestone | Month 12 |
| Multi-language is a market differentiator | Customer validation with Japanese/Chinese oncology teams | Month 6-9 |

---

*This document is a living strategy guide. Update quarterly based on customer feedback, market conditions, and product development velocity.*

*Version 1.0 — June 20, 2026*
