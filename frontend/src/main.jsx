import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import "./style.css";

const configuredApi = import.meta.env.VITE_API_BASE_URL;
const currentHostApi = `${window.location.protocol}//${window.location.hostname || "127.0.0.1"}:8000`;
const API_CANDIDATES = Array.from(new Set([
  configuredApi,
  currentHostApi,
  "http://127.0.0.1:8000",
  "http://localhost:8000",
].filter(Boolean)));

async function apiFetch(path, options = {}) {
  let lastError;
  for (const baseUrl of API_CANDIDATES) {
    try {
      const response = await fetch(`${baseUrl}${path}`, options);
      window.__ONCORECONCILE_API_BASE__ = baseUrl;
      return response;
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError || new Error("Backend API is not reachable.");
}

// ── Colours ──────────────────────────────────────────────────────────────────
const STATUS_COLOR = { AUTO_RECONCILE:"#1a7f37", REVIEW_REQUIRED:"#9a6700", CANNOT_RECONCILE:"#cf222e" };
const CONF_COLOR   = { HIGH:"#1a7f37", MEDIUM:"#9a6700", LOW:"#cf222e" };

// ── Shared components ─────────────────────────────────────────────────────────
function Badge({ label, color }) {
  return <span style={{ background:color, color:"#fff", borderRadius:4, padding:"2px 10px", fontSize:13, fontWeight:"bold" }}>{label}</span>;
}

function ScoreBar({ label, value }) {
  const pct = Math.round(Number(value) * 100);
  const col = pct >= 75 ? "#1a7f37" : pct >= 45 ? "#9a6700" : "#cf222e";
  return (
    <div className="score-row">
      <div className="score-row-label">
        <span>{label}</span>
        <span style={{ fontWeight:"bold", color:col }}>{pct}%</span>
      </div>
      <div className="score-track">
        <div style={{ background:col, width:`${Math.max(0, Math.min(100, pct))}%` }} />
      </div>
    </div>
  );
}

const SCORE_LABELS = {
  match_type: "Match quality",
  source_authority: "Source authority",
  string_similarity: "String similarity",
  context_consistency: "Context consistency",
  alias_coverage: "Alias coverage",
  variant_catalog: "Variant catalog",
};

const EVIDENCE_SOURCE_LABELS = {
  live_myvariant_api: "MyVariant.info",
  live_clinvar_api: "ClinVar",
  live_civic_api: "CIViC",
  live_clingen_allele_registry_api: "ClinGen",
  local_exact_alias: "Local Catalog",
  local_disease_gene_catalog: "Disease-Gene Catalog",
  local_gene_variant_catalog: "Gene-Variant Catalog",
  local_variant_catalog: "Gene-Variant Catalog",
  local_civic_candidate_csv: "CIViC",
};

function evidenceSourceLabel(item) {
  const mode = item?.retrieval_mode || "";
  const matchedMode = Object.keys(EVIDENCE_SOURCE_LABELS).find(key => mode === key || mode.startsWith(`${key}_`));
  if (matchedMode) return EVIDENCE_SOURCE_LABELS[matchedMode];
  if (mode.startsWith("local_")) return "Local Catalog";
  const source = String(item?.source || "").toLowerCase();
  if (source.includes("myvariant")) return "MyVariant.info";
  if (source.includes("clinvar")) return "ClinVar";
  if (source.includes("civic")) return "CIViC";
  if (source.includes("clingen")) return "ClinGen";
  if (source.includes("seed")) return "Seed Knowledge Base";
  return item?.source || "Local Catalog";
}

function getEvidenceBadges(evidence = []) {
  return Array.from(new Set(evidence.map(evidenceSourceLabel).filter(Boolean)));
}

function isGovernanceEvidence(item) {
  const text = [
    item?.source,
    item?.type,
    item?.evidence_type,
    item?.retrieval_mode,
    item?.description,
    item?.governance_standard,
  ].filter(Boolean).join(" ").toLowerCase();
  return ["review", "governance", "adjudication", "catalog promotion", "human review"]
    .some(term => text.includes(term));
}

function EvidenceList({ evidence }) {
  if (!evidence?.length) return <p className="empty-evidence">No evidence returned in this category.</p>;
  return (
    <div className="evidence-list">
      {evidence.map((e,i) => (
        <article className="evidence-row" key={`${e.retrieval_mode || e.source}-${i}`}>
          <div className="evidence-row-header">
            <strong>{e.source || "Not available"}</strong>
            <span>{e.evidence_type || e.type || "Not available"}</span>
          </div>
          <p>{e.description || "Not available"}</p>
          <dl className="evidence-meta">
            <div><dt>Retrieval mode</dt><dd>{e.retrieval_mode || "Not available"}</dd></div>
            <div><dt>Confidence weight</dt><dd>{e.confidence_weight || "Not available"}</dd></div>
            <div><dt>Timestamp</dt><dd>{e.timestamp || "Not available"}</dd></div>
            <div><dt>External ID</dt><dd>{e.external_id || "Not available"}</dd></div>
          </dl>
          {(e.source_url || e.url) && (
            <a className="evidence-link" href={e.source_url || e.url} target="_blank" rel="noreferrer">
              View source ↗
            </a>
          )}
          {e.governance_standard && (
            <div className="governance-note">{e.governance_standard}</div>
          )}
        </article>
      ))}
    </div>
  );
}

function EvidenceGroup({ title, evidence, tone }) {
  return (
    <section className={`evidence-group evidence-group-${tone}`}>
      <div className="evidence-group-title">
        <h4>{title}</h4>
        <span>{evidence.length}</span>
      </div>
      <EvidenceList evidence={evidence}/>
    </section>
  );
}

function EvidenceGroups({ evidence = [] }) {
  const groups = {
    governance: [],
    errors: [],
    live: [],
    local: [],
  };
  evidence.forEach(item => {
    const mode = item?.retrieval_mode || "";
    if (mode.startsWith("live_") && mode.endsWith("_error")) groups.errors.push(item);
    else if (mode.startsWith("live_")) groups.live.push(item);
    else if (isGovernanceEvidence(item)) groups.governance.push(item);
    else groups.local.push(item);
  });
  return (
    <div className="evidence-groups">
      <EvidenceGroup title="Local Evidence" evidence={groups.local} tone="local"/>
      <EvidenceGroup title="Live External Evidence" evidence={groups.live} tone="live"/>
      <EvidenceGroup title="External API Errors" evidence={groups.errors} tone="error"/>
      <EvidenceGroup title="Governance Evidence" evidence={groups.governance} tone="governance"/>
    </div>
  );
}

function reviewRecommendation(status) {
  if (status === "AUTO_RECONCILE") return "Eligible for automated reconciliation";
  if (status === "REVIEW_REQUIRED") return "Human review required before curated use";
  if (status === "CANNOT_RECONCILE") return "Do not reconcile; curator investigation required";
  return "Not available";
}

function ResultCard({ result }) {
  const [expanded, setExpanded] = useState(false);
  const [standardsExport, setStandardsExport] = useState(null);
  const [standardsExportLabel, setStandardsExportLabel] = useState("");
  const [standardsLoading, setStandardsLoading] = useState("");
  if (!result) return null;
  const { canonical, confidence, confidence_score, score_breakdown, review_status, explanation, evidence = [], alternatives, notes, audit_trail, curation_metadata } = result;
  const evidenceBadges = getEvidenceBadges(evidence);
  const hasConfidenceScore = typeof confidence_score === "number" && Number.isFinite(confidence_score);
  const hasScoreBreakdown = score_breakdown && Object.keys(score_breakdown).length > 0;

  async function showStandardsExport(label, path) {
    setStandardsLoading(label);
    try {
      const response = await apiFetch(path, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(result),
      });
      if (!response.ok) throw new Error(`API error ${response.status}`);
      setStandardsExport(await response.json());
      setStandardsExportLabel(label);
    } catch (error) {
      setStandardsExport({ error:error.message });
      setStandardsExportLabel(label);
    } finally {
      setStandardsLoading("");
    }
  }

  return (
    <section className="result-shell" aria-live="polite">
      <div className="result-heading">
        <div>
          <span className="eyebrow">Reconciliation result</span>
          <h3>Evidence-supported decision summary</h3>
        </div>
        <div className="status-stack">
          <Badge label={review_status || "Not available"} color={STATUS_COLOR[review_status] || "#64748b"}/>
          {confidence && <Badge label={`${confidence} CONFIDENCE`} color={CONF_COLOR[confidence] || "#64748b"}/>}
        </div>
      </div>

      <div className="result-overview-grid">
        <div className="decision-panel">
          <div className="summary-label">Final Status</div>
          <div className="decision-status" style={{ color:STATUS_COLOR[review_status] || "#334155" }}>
            {review_status || "Not available"}
          </div>
          <div className="recommendation-box">
            <span>Review Recommendation</span>
            <strong>{reviewRecommendation(review_status)}</strong>
          </div>
        </div>

        <div className="canonical-panel">
          {[
            ["Canonical Disease", canonical?.cancer_type],
            ["Canonical Gene", canonical?.gene],
            ["Canonical Variant", canonical?.variant],
          ].map(([label,value]) => (
            <div className="canonical-value" key={label}>
              <span>{label}</span>
              <strong>{value || "Not available"}</strong>
            </div>
          ))}
        </div>

        <div className="confidence-panel">
          <div className="confidence-number">
            <span>Overall confidence</span>
            <strong>{hasConfidenceScore ? `${Math.round(confidence_score * 100)}%` : "Not available"}</strong>
          </div>
          {hasConfidenceScore && <ScoreBar label="Overall score" value={confidence_score}/>}
          {hasScoreBreakdown && (
            <div className="confidence-breakdown">
              {Object.entries(score_breakdown).map(([key,value]) => (
                <ScoreBar key={key} label={SCORE_LABELS[key] || key.replace(/_/g," ")} value={value}/>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="evidence-badge-row">
        <span>Evidence sources</span>
        <div>
          {evidenceBadges.length
            ? evidenceBadges.map(label => <span className="evidence-badge" key={label}>{label}</span>)
            : <span className="evidence-badge evidence-badge-muted">Not available</span>}
        </div>
      </div>

      <div className="explanation-box">
        <span>Decision rationale</span>
        <p>{explanation || "Not available"}</p>
      </div>

      {/* Alternatives */}
      {alternatives?.length > 0 && (
        <div className="alternatives-box">
          <p>Alternatives considered</p>
          <ul style={{ paddingLeft:16, margin:0 }}>
            {alternatives.map((a,i)=>(
              <li key={i} style={{ fontSize:12, color:"#555" }}>{a.name || a.id} {a.reason && `— ${a.reason}`}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Notes */}
      {notes?.length > 0 && <div className="result-notes">⚠ {notes.join(" ")}</div>}

      {curation_metadata && (
        <section className="standards-panel">
          <div className="standards-title">
            <div>
              <span className="eyebrow">Knowledge graph & standards readiness</span>
              <h4>Standards & Curation Alignment</h4>
            </div>
            <span className="prototype-pill">{curation_metadata.standards_status || "standards-inspired prototype"}</span>
          </div>
          <div className="standards-facts">
            <span>Stage: <strong>{curation_metadata.curation_stage}</strong></span>
            <span>Human governance: <strong>{curation_metadata.human_governance_required ? "Required" : "Not required"}</strong></span>
            <span>Catalog promotion candidate: <strong>{curation_metadata.catalog_promotion_candidate ? "Yes" : "No"}</strong></span>
          </div>
          <div className="alignment-copy">
            AIWS alignment: {(curation_metadata.aiws_use_case_alignment || []).join(" · ")}
          </div>
          <div className="standards-actions">
            {[
              ["Provenance Export","/export/provenance"],
              ["Knowledge Graph","/export/knowledge-graph"],
              ["VRS-ready Stub","/export/vrs-ready"],
              ["Cat-VRS-ready Stub","/export/cat-vrs-ready"],
              ["VA-Spec-ready Stub","/export/va-spec-ready"],
            ].map(([label,path])=>(
              <button
                key={label}
                type="button"
                onClick={()=>showStandardsExport(label,path)}
                disabled={Boolean(standardsLoading)}
                className="standards-button"
              >
                {standardsLoading === label ? "Loading..." : `Show ${label}`}
              </button>
            ))}
          </div>
          {standardsExport && (
            <div style={{ marginTop:8 }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", gap:8 }}>
                <strong style={{ fontSize:11, color:"#444" }}>{standardsExportLabel}</strong>
                <button type="button" onClick={()=>setStandardsExport(null)}
                  style={{ fontSize:11, border:"none", background:"none", color:"#666", cursor:"pointer" }}>
                  Close
                </button>
              </div>
              <pre style={{ margin:"5px 0 0", padding:8, background:"#f6f8fa", border:"1px solid #d0d7de", borderRadius:4, fontSize:10, overflowX:"auto", whiteSpace:"pre-wrap" }}>
                {JSON.stringify(standardsExport,null,2)}
              </pre>
            </div>
          )}
        </section>
      )}

      <button onClick={()=>setExpanded(!expanded)} className="evidence-toggle">
        {expanded ? "Hide detailed evidence" : "Explore evidence sources & audit trail"}
      </button>
      {expanded && (
        <div className="evidence-details">
          <h3>Evidence Sources</h3>
          <p>Provenance is grouped by retrieval behavior so judges can distinguish local evidence, live APIs, safe API failures, and governance signals.</p>
          <EvidenceGroups evidence={evidence}/>
          <section className="audit-panel">
            <h4>Audit trail</h4>
            {audit_trail?.length
              ? <ol>{audit_trail.map((s,i)=><li key={i}>{s}</li>)}</ol>
              : <p className="empty-evidence">Not available</p>}
          </section>
        </div>
      )}
    </section>
  );
}

// ── PAGE: Single record ───────────────────────────────────────────────────────
const EXAMPLES = [
  {
    id:"step_001",
    label:"Exact Alias / Catalog",
    type:"Exact Alias / Catalog",
    cancer_type:"NSCLC",
    gene:"HER2",
    variant:"amp",
    expected_status:"AUTO_RECONCILE",
    description:"Disease alias + gene alias + catalog variant + external evidence."
  },
  {
    id:"step_004",
    label:"Variant Alias",
    type:"Variant Alias",
    cancer_type:"NSCLC",
    gene:"EGFR",
    variant:"Ex19del",
    expected_status:"AUTO_RECONCILE",
    description:"Variant synonym/catalog normalization with evidence."
  },
  {
    id:"fuzzy_001",
    label:"Fuzzy Disease",
    type:"Fuzzy Disease",
    cancer_type:"non-small cell lung carcinom",
    gene:"EGFR",
    variant:"Ex19del",
    expected_status:"AUTO_RECONCILE",
    description:"Misspelled disease term resolved by RapidFuzz."
  },
  {
    id:"fuzzy_002",
    label:"Fuzzy Gene",
    type:"Fuzzy Gene",
    cancer_type:"NSCLC",
    gene:"ERBB-2",
    variant:"amp",
    expected_status:"AUTO_RECONCILE",
    description:"Gene punctuation/typo resolved to canonical gene."
  },
  {
    id:"fuzzy_003",
    label:"Fuzzy Variant",
    type:"Fuzzy Variant",
    cancer_type:"NSCLC",
    gene:"EGFR",
    variant:"Exon 19 deletin",
    expected_status:"AUTO_RECONCILE",
    description:"Variant typo resolved to catalog synonym."
  },
  {
    id:"step_005",
    label:"Cat-VRS-style Ambiguity",
    type:"Cat-VRS-style Ambiguity",
    cancer_type:"NSCLC",
    gene:"TRK",
    variant:"pan-trk fusion",
    expected_status:"REVIEW_REQUIRED",
    description:"Ambiguous TRK/NTRK-family fusion is preserved and routed to review."
  },
  {
    id:"step_006",
    label:"Catalog Review Required",
    type:"Catalog Review Required",
    cancer_type:"NSCLC",
    gene:"EGFR",
    variant:"Exon20ins",
    expected_status:"REVIEW_REQUIRED",
    description:"Known variant category that should not be auto-reconciled."
  },
  {
    id:"llm_004",
    label:"LLM-gated Review",
    type:"LLM-gated Review",
    cancer_type:"NSCLC",
    gene:"KRAS",
    variant:"mutation",
    expected_status:"REVIEW_REQUIRED",
    description:"Generic mutation triggers human review and optional LLM suggestion."
  },
  {
    id:"external_001",
    label:"External Candidate",
    type:"External Candidate",
    cancer_type:"NSCLC",
    gene:"PIK3CA",
    variant:"E545K",
    expected_status:"REVIEW_REQUIRED",
    description:"Known hotspot syntax outside the trusted local disease context becomes a review candidate."
  },
  {
    id:"step_007",
    label:"Unknown Gene",
    type:"Unknown Gene",
    cancer_type:"NSCLC",
    gene:"unknown_gene",
    variant:"G12C",
    expected_status:"CANNOT_RECONCILE",
    description:"Unknown gene safely fails instead of guessing."
  },
  {
    id:"step_010",
    label:"No Trusted Match",
    type:"No Trusted Match",
    cancer_type:"NSCLC",
    gene:"FAKE_GENE_XYZ",
    variant:"FAKE_VARIANT_XYZ",
    expected_status:"CANNOT_RECONCILE",
    description:"No trusted gene or variant evidence exists."
  },
];

const EXAMPLE_GROUPS = {
  "Auto-Reconcile Examples": {
    status: "AUTO_RECONCILE",
    description: "Deterministic normalization and high-confidence catalog pathways.",
  },
  "Human Review Examples": {
    status: "REVIEW_REQUIRED",
    description: "Ambiguous or advisory candidates preserved for accountable curator review.",
  },
  "Safe Failure Examples": {
    status: "CANNOT_RECONCILE",
    description: "Unknown inputs stop safely instead of being forced into an unsupported match.",
  },
};

const REVIEW_EXAMPLES = [
  { label:"TRK Fusion", cancer_type:"NSCLC", gene:"TRK", variant:"fusion" },
  { label:"BRAF V600", cancer_type:"Melanoma", gene:"BRAF", variant:"V600" },
  { label:"EGFR Exon20ins", cancer_type:"NSCLC", gene:"EGFR", variant:"Exon20ins" },
  { label:"KRAS Mutation + LLM", cancer_type:"NSCLC", gene:"KRAS", variant:"mutation" },
];

const SAMPLE_CSV_ROWS = [
  { case_id:"workflow_001", workflow_step:"Disease alias + variant alias", cancer_type:"NSCLC", gene:"EGFR", variant:"Ex19del", expected_status:"AUTO_RECONCILE" },
  { case_id:"workflow_002", workflow_step:"Gene alias normalization", cancer_type:"NSCLC", gene:"HER1", variant:"L858R", expected_status:"AUTO_RECONCILE" },
  { case_id:"workflow_003", workflow_step:"Gene + copy number synonym", cancer_type:"NSCLC", gene:"HER2", variant:"amp", expected_status:"AUTO_RECONCILE" },
  { case_id:"workflow_004", workflow_step:"Catalog match", cancer_type:"Melanoma", gene:"BRAF", variant:"V600E", expected_status:"AUTO_RECONCILE" },
  { case_id:"workflow_005", workflow_step:"Disease fuzzy matching", cancer_type:"melanomaa", gene:"BRAF", variant:"V600E", expected_status:"AUTO_RECONCILE" },
  { case_id:"workflow_006", workflow_step:"Gene fuzzy matching", cancer_type:"NSCLC", gene:"ERRB2", variant:"amp", expected_status:"AUTO_RECONCILE" },
  { case_id:"workflow_007", workflow_step:"Variant fuzzy matching", cancer_type:"NSCLC", gene:"EGFR", variant:"Ex19dele", expected_status:"AUTO_RECONCILE" },
  { case_id:"workflow_008", workflow_step:"Cat-VRS categorical ambiguity", cancer_type:"NSCLC", gene:"TRK", variant:"fusion", expected_status:"REVIEW_REQUIRED" },
  { case_id:"workflow_009", workflow_step:"Variant ambiguity candidates", cancer_type:"Melanoma", gene:"BRAF", variant:"V600", expected_status:"REVIEW_REQUIRED" },
  { case_id:"workflow_010", workflow_step:"Catalog review required", cancer_type:"NSCLC", gene:"EGFR", variant:"Exon20ins", expected_status:"REVIEW_REQUIRED" },
  { case_id:"workflow_011", workflow_step:"LLM-gated review suggestion", cancer_type:"NSCLC", gene:"KRAS", variant:"mutation", expected_status:"REVIEW_REQUIRED" },
  { case_id:"workflow_012", workflow_step:"External candidate review", cancer_type:"NSCLC", gene:"PIK3CA", variant:"E545K", expected_status:"REVIEW_REQUIRED" },
  { case_id:"workflow_013", workflow_step:"Cannot reconcile safe failure", cancer_type:"NSCLC", gene:"unknown_gene", variant:"G12C", expected_status:"CANNOT_RECONCILE" },
  { case_id:"workflow_014", workflow_step:"Cross-disease HER2 alias", cancer_type:"Breast Cancer", gene:"HER2", variant:"HER2+", expected_status:"AUTO_RECONCILE" },
];

const SAMPLE_CSV_HEADERS = ["case_id","workflow_step","cancer_type","gene","variant","expected_status"];

const SAMPLE_CSV_TEXT = [
  SAMPLE_CSV_HEADERS.join(","),
  ...SAMPLE_CSV_ROWS.map(row => SAMPLE_CSV_HEADERS.map(header => row[header]).join(",")),
].join("\n");

function statusBadgeColor(status) {
  return STATUS_COLOR[status] || "#555";
}

function ExampleCard({ example, onLoad, onRun, loading }) {
  return (
    <div className="example-card">
      <div className="example-card-header">
        <span className="example-type">{example.type}</span>
        <Badge label={example.expected_status} color={statusBadgeColor(example.expected_status)} />
      </div>
      <h4>{example.label}</h4>
      <p>{example.description}</p>
      <div className="example-values">
        <code>{example.cancer_type}</code>
        <code>{example.gene}</code>
        <code>{example.variant}</code>
      </div>
      <div className="example-actions">
        <button type="button" onClick={() => onLoad(example)} className="secondary-button">
          Load
        </button>
        <button type="button" onClick={() => onRun(example)} className="primary-mini-button" disabled={loading}>
          Run
        </button>
      </div>
    </div>
  );
}

function SinglePage() {
  const [form, setForm] = useState({ cancer_type:"NSCLC", gene:"HER2", variant:"Amplification" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState("All");

  async function submit(overrideForm = null) {
    const payload = overrideForm || form;
    setError(""); setResult(null); setLoading(true);
    try {
      const r = await apiFetch("/reconcile", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload) });
      if (!r.ok) throw new Error(`API error ${r.status}`);
      setResult(await r.json());
    } catch(e) { setError(e.message); }
    finally { setLoading(false); }
  }

  function loadExample(example) {
    setForm({
      case_id: example.id,
      cancer_type: example.cancer_type,
      gene: example.gene,
      variant: example.variant,
    });
    setError("");
    setResult(null);
  }

  function runExample(example) {
    const payload = {
      case_id: example.id,
      cancer_type: example.cancer_type,
      gene: example.gene,
      variant: example.variant,
    };
    setForm(payload);
    submit(payload);
  }

  const featuredDemo = {
    id:"featured_egfr_c797s",
    cancer_type:"NSCLC",
    gene:"EGFR",
    variant:"C797S",
  };
  const groupedExamples = Object.entries(EXAMPLE_GROUPS)
    .map(([group, metadata]) => ({
      group,
      ...metadata,
      examples: EXAMPLES.filter(example => example.expected_status === metadata.status),
    }))
    .filter(section => selectedGroup === "All" || section.group === selectedGroup);

  return (
    <div>
      <header className="single-hero">
        <span className="eyebrow">AI-assisted oncology data harmonization</span>
        <h1>Single Record Reconciliation</h1>
        <p>
          Use this tab to demonstrate how OncoReconcile AI transforms messy oncology inputs into canonical
          candidates with evidence, confidence scoring, and human-governed review recommendations.
        </p>
      </header>

      <div className="workflow-strip">
        {["Normalize", "Retrieve evidence", "Score confidence", "Govern review", "Export provenance"].map(step => (
          <span key={step}>{step}</span>
        ))}
      </div>

      <div className="demo-input-grid">
        <section className="featured-demo">
          <div>
            <span className="featured-kicker">Featured Demo</span>
            <h2>Evidence-Supported Human Review</h2>
            <p>
              This example demonstrates disease and gene normalization, external evidence retrieval,
              confidence scoring, and REVIEW_REQUIRED governance.
            </p>
          </div>
          <div className="featured-values">
            <div><span>Disease / Cancer Type</span><strong>NSCLC</strong></div>
            <div><span>Gene</span><strong>EGFR</strong></div>
            <div><span>Variant</span><strong>C797S</strong></div>
          </div>
          <button type="button" onClick={() => runExample(featuredDemo)} disabled={loading} className="featured-button">
            {loading ? "Running Demo…" : "Run Featured Demo"}
          </button>
        </section>

        <section className="single-form-card">
          <div className="form-card-heading">
            <div>
              <span className="eyebrow">Try your own record</span>
              <h3>Manual input</h3>
            </div>
            <span>Required: gene + variant</span>
          </div>
          <div className="manual-input-grid">
            {[["cancer_type","Disease / Cancer Type"],["gene","Gene"],["variant","Variant"]].map(([k,lbl])=>(
              <div key={k}>
                <label htmlFor={`single-${k}`}>{lbl}</label>
                <input id={`single-${k}`} value={form[k]||""} onChange={e=>setForm({...form,[k]:e.target.value})}/>
              </div>
            ))}
          </div>
          <button onClick={() => submit()} disabled={loading} className="reconcile-button">
            {loading ? "Reconciling…" : "Reconcile Record"}
          </button>
        </section>
      </div>

      {error && <p style={{ color:"#cf222e", marginTop:8 }}>{error}</p>}
      <ResultCard result={result}/>

      <section className="example-library">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Demo pathway library</span>
            <h2>Explore reconciliation outcomes</h2>
          </div>
          <p>All existing examples are preserved and organized around the decision a judge will see.</p>
        </div>
        <div className="example-filter-row">
          {["All", ...Object.keys(EXAMPLE_GROUPS)].map(group => (
            <button
              key={group}
              type="button"
              onClick={() => setSelectedGroup(group)}
              className={selectedGroup === group ? "filter-chip active" : "filter-chip"}
            >
              {group}
            </button>
          ))}
        </div>
        {groupedExamples.map(section => (
          <section className="example-section" key={section.group}>
            <div className="example-section-heading">
              <div>
                <h3>{section.group}</h3>
                <p>{section.description}</p>
              </div>
              <Badge label={section.status} color={statusBadgeColor(section.status)}/>
            </div>
            <div className="example-grid-wide">
              {section.examples.map(ex => (
                <ExampleCard
                  key={ex.id}
                  example={ex}
                  onLoad={loadExample}
                  onRun={runExample}
                  loading={loading}
                />
              ))}
            </div>
          </section>
        ))}
      </section>

      <p className="safety-note">
        Prototype for oncology data harmonization and curation. Not intended for clinical interpretation,
        treatment recommendation, or autonomous clinical decision support.
      </p>
    </div>
  );
}

// ── PAGE: CSV Upload ──────────────────────────────────────────────────────────
function UploadPage() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [expandedIdx, setExpandedIdx] = useState(null);

  function useSampleCsv() {
    const sampleFile = new File([SAMPLE_CSV_TEXT], "oncoreconcile_demo_cases.csv", {
      type:"text/csv",
    });
    setFile(sampleFile);
    setError("");
  }

  function downloadSampleCsv() {
    const blob = new Blob([SAMPLE_CSV_TEXT], { type:"text/csv" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "oncoreconcile_demo_cases.csv";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  async function upload() {
    if (!file) return;
    setError(""); setResults(null); setSummary(null); setLoading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const r = await apiFetch("/reconcile/upload", { method:"POST", body:fd });
      if (!r.ok) { const e = await r.json(); throw new Error(e.detail || `Error ${r.status}`); }
      const data = await r.json();
      setResults(data.results);
      setSummary(data.summary);
    } catch(e) { setError(e.message); }
    finally { setLoading(false); }
  }

  return (
    <div>
      <h2 style={{ color:"#028090", marginBottom:4 }}>CSV Batch Upload</h2>
      <p style={{ color:"#666", fontSize:13 }}>Upload a CSV with columns: <code>case_id</code> (optional), <code>cancer_type</code> (optional), <code>gene</code>, <code>variant</code>. Extra demo columns are ignored by the API.</p>

      <div style={{ border:"1px solid #d0d7de", borderRadius:8, background:"#fff", padding:12, margin:"12px 0 16px" }}>
        <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", gap:10, flexWrap:"wrap", marginBottom:8 }}>
          <strong style={{ color:"#444", fontSize:13 }}>Sample CSV</strong>
          <div style={{ display:"flex", gap:8, flexWrap:"wrap" }}>
            <button onClick={useSampleCsv}
              style={{ marginTop:0, fontSize:12, padding:"5px 12px", borderRadius:4, border:"1px solid #028090", background:"#e8f4f6", color:"#028090", cursor:"pointer" }}>
              Use Sample
            </button>
            <button onClick={downloadSampleCsv}
              style={{ marginTop:0, fontSize:12, padding:"5px 12px", borderRadius:4, border:"1px solid #ccc", background:"#fff", color:"#333", cursor:"pointer" }}>
              Download CSV
            </button>
          </div>
        </div>
        <div style={{ overflowX:"auto" }}>
          <table style={{ fontSize:12, minWidth:760 }}>
            <thead>
              <tr>
                {SAMPLE_CSV_HEADERS.map(header=>(
                  <th key={header} style={{ color:"#555", background:"#f6f8fa" }}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {SAMPLE_CSV_ROWS.map(row=>(
                <tr key={row.case_id}>
                  {SAMPLE_CSV_HEADERS.map(header=>(
                    <td key={header}>{row[header]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={{ display:"flex", gap:10, alignItems:"center", marginBottom:12 }}>
        <input type="file" accept=".csv" onChange={e=>setFile(e.target.files[0])}
          style={{ fontSize:13 }}/>
        {file && <span style={{ fontSize:12, color:"#666" }}>{file.name}</span>}
        <button onClick={upload} disabled={!file||loading}
          style={{ padding:"7px 20px", background:"#028090", color:"#fff", border:"none", borderRadius:6, fontSize:13, cursor:"pointer", opacity:(!file||loading)?0.6:1 }}>
          {loading ? "Processing…" : "Upload & Reconcile"}
        </button>
      </div>

      {error && <p style={{ color:"#cf222e" }}>{error}</p>}

      {summary && (
        <div style={{ display:"flex", gap:12, marginBottom:16, flexWrap:"wrap" }}>
          {[["Total",summary.total_records,"#555"],["Auto",summary.auto_reconcile,STATUS_COLOR.AUTO_RECONCILE],
            ["Review",summary.review_required,STATUS_COLOR.REVIEW_REQUIRED],["Cannot",summary.cannot_reconcile,STATUS_COLOR.CANNOT_RECONCILE]].map(([l,n,c])=>(
            <div key={l} style={{ background:"#f5f5f5", borderRadius:8, padding:"10px 18px", textAlign:"center", border:`2px solid ${c}` }}>
              <div style={{ fontSize:22, fontWeight:"bold", color:c }}>{n}</div>
              <div style={{ fontSize:11, color:"#666" }}>{l}</div>
            </div>
          ))}
        </div>
      )}

      {results && results.map((r,i)=>(
        <div key={i} style={{ border:"1px solid #e0e0e0", borderRadius:6, marginBottom:8, overflow:"hidden" }}>
          <div style={{ display:"flex", alignItems:"center", gap:10, padding:"8px 12px", background:"#f9f9f9", cursor:"pointer" }}
            onClick={()=>setExpandedIdx(expandedIdx===i?null:i)}>
            <Badge label={r.review_status} color={STATUS_COLOR[r.review_status]}/>
            <span style={{ fontSize:13, fontWeight:"bold" }}>{r.input?.gene} / {r.input?.variant}</span>
            <span style={{ fontSize:12, color:"#888" }}>{r.input?.cancer_type}</span>
            <span style={{ marginLeft:"auto", fontSize:12, color:"#028090" }}>{expandedIdx===i?"▲":"▼"}</span>
          </div>
          {expandedIdx===i && <div style={{ padding:"0 12px 12px" }}><ResultCard result={r}/></div>}
        </div>
      ))}
    </div>
  );
}

// ── PAGE: Review Queue ────────────────────────────────────────────────────────
function ReviewQueuePage() {
  const [items, setItems] = useState([]);
  const [summary, setSummary] = useState({total:0,pending:0,reviewed:0});
  const [agreement, setAgreement] = useState(null);
  const [filter, setFilter] = useState("pending");
  const [loading, setLoading] = useState(false);
  const [seeding, setSeeding] = useState("");
  const [seedError, setSeedError] = useState("");
  const [deciding, setDeciding] = useState({});
  const [curatorId, setCuratorId] = useState("curator-1");
  const [selectedCandidateByCase, setSelectedCandidateByCase] = useState({});
  const [reviewerNotesByCase, setReviewerNotesByCase] = useState({});
  const [canonicalEditsByCase, setCanonicalEditsByCase] = useState({});
  const [expandedAuditByCase, setExpandedAuditByCase] = useState({});

  async function load() {
    setLoading(true);
    try {
      const r = await apiFetch(`/review-queue?status=${filter}`);
      const data = await r.json();
      setItems(data.items);
      setSummary({ total:data.total, pending:data.pending, reviewed:data.reviewed });
      const metricsResponse = await apiFetch("/review-queue-metrics");
      if (metricsResponse.ok) setAgreement(await metricsResponse.json());
    } catch(e) { console.error(e); }
    finally { setLoading(false); }
  }

  useEffect(()=>{ load(); }, [filter]);

  async function seedReviewExample(example) {
    setSeedError("");
    setSeeding(example.label);
    try {
      const r = await apiFetch("/reconcile", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
          case_id:`review-demo-${example.label.toLowerCase().replace(/[^a-z0-9]+/g,"-")}-${Date.now()}`,
          cancer_type:example.cancer_type,
          gene:example.gene,
          variant:example.variant,
        }),
      });
      if (!r.ok) throw new Error(`API error ${r.status}`);
      const result = await r.json();
      if (result.review_status !== "REVIEW_REQUIRED") {
        setSeedError(`${example.label} returned ${result.review_status}, so it was not added to the queue.`);
      }
      if (filter !== "pending") {
        setFilter("pending");
      } else {
        load();
      }
    } catch(e) {
      setSeedError(e.message);
    } finally {
      setSeeding("");
    }
  }

  async function decide(caseId, decision) {
    setDeciding(d=>({...d,[caseId]:true}));
    try {
      await apiFetch(`/review-queue/${caseId}/decision`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
          case_id:caseId,
          decision,
          curator_id:curatorId,
          notes:reviewerNotesByCase[caseId] || null,
        })
      });
      load();
    } catch(e) { console.error(e); }
    finally { setDeciding(d=>({...d,[caseId]:false})); }
  }

  async function editToCandidate(item, candidate) {
    if (!candidate) return;
    const name = candidate.name || candidate.id || "";
    const gene = candidate.gene || name.split(" ")[0] || item.canonical?.gene;
    setDeciding(d=>({...d,[item.case_id]:true}));
    try {
      await apiFetch(`/review-queue/${item.case_id}/decision`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
          case_id:item.case_id,
          decision:"edit",
          curator_id:curatorId,
          override_canonical:{
            cancer_type:item.canonical?.cancer_type,
            gene,
            variant:name || item.canonical?.variant,
          },
          notes:reviewerNotesByCase[item.case_id] || `Edited to selected candidate: ${name || "unknown candidate"}.`
        })
      });
      load();
    } catch(e) { console.error(e); }
    finally { setDeciding(d=>({...d,[item.case_id]:false})); }
  }

  async function editCanonical(item) {
    const edits = canonicalEditsByCase[item.case_id] || {};
    setDeciding(d=>({...d,[item.case_id]:true}));
    try {
      await apiFetch(`/review-queue/${item.case_id}/decision`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
          case_id:item.case_id,
          decision:"edit",
          curator_id:curatorId,
          override_canonical:{
            cancer_type:edits.cancer_type ?? item.canonical?.cancer_type,
            gene:edits.gene ?? item.canonical?.gene,
            variant:edits.variant ?? item.canonical?.variant,
          },
          notes:reviewerNotesByCase[item.case_id] || "Canonical values edited by reviewer."
        })
      });
      load();
    } catch(e) { console.error(e); }
    finally { setDeciding(d=>({...d,[item.case_id]:false})); }
  }

  async function reopenItem(caseId) {
    setDeciding(d=>({...d,[caseId]:true}));
    try {
      await apiFetch(`/review-queue/${caseId}/decision`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
          case_id:caseId,
          decision:"reopen",
          curator_id:curatorId,
          notes:"Reopened for additional human review."
        })
      });
      if (filter !== "pending") {
        setFilter("pending");
      } else {
        load();
      }
    } catch(e) { console.error(e); }
    finally { setDeciding(d=>({...d,[caseId]:false})); }
  }

  async function adjudicate(item) {
    const edits = canonicalEditsByCase[item.case_id] || {};
    setDeciding(d=>({...d,[item.case_id]:true}));
    try {
      await apiFetch(`/review-queue/${item.case_id}/adjudicate`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
          case_id:item.case_id,
          decision:"edit",
          curator_id:curatorId,
          override_canonical:{
            cancer_type:edits.cancer_type ?? item.canonical?.cancer_type,
            gene:edits.gene ?? item.canonical?.gene,
            variant:edits.variant ?? item.canonical?.variant,
          },
          notes:reviewerNotesByCase[item.case_id] || "Final canonical result selected by adjudicator."
        })
      });
      load();
    } catch(e) { console.error(e); }
    finally { setDeciding(d=>({...d,[item.case_id]:false})); }
  }

  return (
    <div>
      <h2 style={{ color:"#028090", marginBottom:4 }}>Human Review Queue</h2>
      <p style={{ color:"#666", fontSize:13 }}>REVIEW_REQUIRED cases awaiting curator decision.</p>

      <div style={{ display:"flex", gap:8, alignItems:"center", flexWrap:"wrap", margin:"12px 0 16px" }}>
        <span style={{ fontSize:12, color:"#555", fontWeight:"bold" }}>Add demo case:</span>
        {REVIEW_EXAMPLES.map(ex=>(
          <button key={ex.label} onClick={()=>seedReviewExample(ex)} disabled={Boolean(seeding)}
            style={{ marginTop:0, fontSize:11, padding:"5px 10px", borderRadius:4, border:"1px solid #9a6700", background:"#fff8dc", cursor:"pointer", color:"#7d4e00", opacity:seeding?0.6:1 }}>
            {seeding === ex.label ? "Adding…" : ex.label}
          </button>
        ))}
      </div>
      {seedError && <p style={{ color:"#cf222e", fontSize:12, marginTop:-8 }}>{seedError}</p>}

      {agreement && (
        <div style={{ display:"flex", gap:14, flexWrap:"wrap", padding:"9px 0", marginBottom:12, borderTop:"1px solid #ddd", borderBottom:"1px solid #ddd" }}>
          <span style={{ fontSize:12 }}>Multi-review cases: <strong>{agreement.cases_with_multiple_reviewers}</strong></span>
          <span style={{ fontSize:12 }}>Agreement: <strong>{agreement.percent_agreement == null ? "N/A" : `${(agreement.percent_agreement*100).toFixed(1)}%`}</strong></span>
          <span style={{ fontSize:12 }}>Cohen's kappa: <strong>{agreement.cohens_kappa == null ? "N/A" : agreement.cohens_kappa.toFixed(2)}</strong></span>
          <span style={{ fontSize:12, color:agreement.adjudication_required ? "#cf222e" : "#555" }}>
            Awaiting adjudication: <strong>{agreement.adjudication_required}</strong>
          </span>
        </div>
      )}

      <div style={{ display:"flex", gap:12, alignItems:"center", marginBottom:16, flexWrap:"wrap" }}>
        <div style={{ display:"flex", gap:8 }}>
          {["pending","reviewed","all"].map(f=>(
            <button key={f} onClick={()=>setFilter(f)}
              style={{ padding:"5px 14px", borderRadius:4, border:`1px solid ${filter===f?"#028090":"#ccc"}`,
                background:filter===f?"#028090":"#fff", color:filter===f?"#fff":"#333", cursor:"pointer", fontSize:12 }}>
              {f.charAt(0).toUpperCase()+f.slice(1)}
            </button>
          ))}
        </div>
        <div style={{ display:"flex", gap:8 }}>
          {[["Total",summary.total,"#555"],["Pending",summary.pending,STATUS_COLOR.REVIEW_REQUIRED],["Reviewed",summary.reviewed,STATUS_COLOR.AUTO_RECONCILE]].map(([l,n,c])=>(
            <span key={l} style={{ fontSize:12, color:c, fontWeight:"bold" }}>{l}: {n}</span>
          ))}
        </div>
        <div style={{ marginLeft:"auto", display:"flex", alignItems:"center", gap:6 }}>
          <label style={{ fontSize:12, color:"#555" }}>Curator ID:</label>
          <input value={curatorId} onChange={e=>setCuratorId(e.target.value)}
            style={{ fontSize:12, padding:"3px 8px", border:"1px solid #ccc", borderRadius:4, width:120 }}/>
        </div>
        <button onClick={load} style={{ fontSize:12, padding:"5px 12px", border:"1px solid #ccc", borderRadius:4, cursor:"pointer" }}>
          ↻ Refresh
        </button>
      </div>

      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {!loading && items.length === 0 && <p style={{ color:"#888" }}>No items in queue.</p>}

      {items.map(item=>{
        const candidateIndex = Number(selectedCandidateByCase[item.case_id] ?? 0);
        const selectedCandidate = item.alternatives?.[candidateIndex] || item.alternatives?.[0];
        const hasLiveEvidence = item.evidence?.some(
          e => e.retrieval_mode?.startsWith("live_") && !e.retrieval_mode?.endsWith("_error")
        );
        const hasCandidateEvidence = item.evidence?.some(e =>
          ["external_candidate_evidence","local_gene_catalog_candidate"].includes(e.evidence_type)
          || ["local_civic_candidate_csv","external_api_or_syntax_candidate","local_gene_variant_catalog_candidate"].includes(e.retrieval_mode)
        );
        const decisionLabel = item.decision === "approve"
          ? "Approved"
          : item.decision === "reject"
            ? "Rejected"
            : item.decision
              ? "Edited"
              : null;
        return (
        <div key={item.case_id} style={{ border:"2px solid #e8a020", borderRadius:8, padding:14, marginBottom:12, background:"#fffdf5" }}>
          <div style={{ display:"flex", gap:10, alignItems:"center", marginBottom:8, flexWrap:"wrap" }}>
            <Badge label={item.review_status} color={STATUS_COLOR[item.review_status]}/>
            <span style={{ fontWeight:"bold", fontSize:14 }}>{item.input?.gene} / {item.input?.variant}</span>
            <span style={{ fontSize:12, color:"#666" }}>{item.input?.cancer_type}</span>
            <span style={{ fontSize:12, color:"#888" }}>Score: {(item.confidence_score*100).toFixed(0)}%</span>
            {hasCandidateEvidence && <Badge label="Candidate Evidence" color="#8250df"/>}
            {hasLiveEvidence && <Badge label="Live API Evidence" color="#0969da"/>}
            {!item.decision && (hasCandidateEvidence || hasLiveEvidence) && <Badge label="Needs Catalog Review" color="#9a6700"/>}
            {decisionLabel && (
              <Badge
                label={decisionLabel}
                color={item.decision==="approve" ? STATUS_COLOR.AUTO_RECONCILE : item.decision==="reject" ? STATUS_COLOR.CANNOT_RECONCILE : "#0969da"}
              />
            )}
            {item.adjudication_status === "REQUIRED" && <Badge label="Adjudication Required" color="#cf222e"/>}
            {item.adjudication_status === "RESOLVED" && <Badge label="Adjudicated" color="#8250df"/>}
          </div>

          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:8, marginBottom:8, fontSize:13 }}>
            {[["Disease",item.canonical?.cancer_type],["Gene",item.canonical?.gene],["Variant",item.canonical?.variant]].map(([k,v])=>(
              <div key={k} style={{ background:"#f5f5f5", borderRadius:4, padding:"6px 10px" }}>
                <span style={{ color:"#888", fontSize:11 }}>{k}</span><br/>
                <strong>{v || "—"}</strong>
              </div>
            ))}
          </div>

          {!item.decision && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(190px,1fr))", gap:8, marginBottom:10 }}>
              {[["cancer_type","Edit disease"],["gene","Edit gene"],["variant","Edit variant"]].map(([field,label])=>(
                <label key={field} style={{ fontSize:11, color:"#666" }}>
                  {label}
                  <input
                    value={canonicalEditsByCase[item.case_id]?.[field] ?? item.canonical?.[field] ?? ""}
                    onChange={e=>setCanonicalEditsByCase(s=>({
                      ...s,
                      [item.case_id]:{...(s[item.case_id] || {}),[field]:e.target.value}
                    }))}
                    style={{ width:"100%", boxSizing:"border-box", marginTop:3, padding:"5px 7px", border:"1px solid #ccc", borderRadius:4, fontSize:12 }}
                  />
                </label>
              ))}
            </div>
          )}

          <div style={{ background:"#f0f4f8", borderRadius:6, padding:8, fontSize:12, marginBottom:10, color:"#444" }}>
            {item.explanation}
          </div>

          {/* Score breakdown mini */}
          {item.score_breakdown && (
            <div style={{ marginBottom:10 }}>
              {Object.entries(item.score_breakdown).map(([k,v])=>(
                <ScoreBar key={k} label={k.replace(/_/g," ")} value={v}/>
              ))}
            </div>
          )}

          {/* Alternatives */}
          {item.alternatives?.length > 0 && (
            <div style={{ marginBottom:10 }}>
              <p style={{ fontSize:11, color:"#888", margin:"0 0 4px" }}>Alternatives considered:</p>
              <div style={{ display:"flex", gap:6, flexWrap:"wrap" }}>
                {item.alternatives.map((a,i)=>(
                  <span key={i} style={{
                    fontSize:11,
                    background:i===candidateIndex?"#ddf4ff":"#eee",
                    border:`1px solid ${i===candidateIndex?"#0969da":"transparent"}`,
                    borderRadius:4,
                    padding:"2px 8px"
                  }}>
                    {a.name || a.id}
                  </span>
                ))}
              </div>
              {!item.decision && (
                <div style={{ display:"flex", gap:8, alignItems:"center", flexWrap:"wrap", marginTop:8 }}>
                  <label style={{ fontSize:11, color:"#666" }}>Edit candidate:</label>
                  <select
                    value={candidateIndex}
                    onChange={e=>setSelectedCandidateByCase(s=>({...s,[item.case_id]:e.target.value}))}
                    style={{ fontSize:12, padding:"4px 8px", border:"1px solid #ccc", borderRadius:4, minWidth:180 }}
                  >
                    {item.alternatives.map((a,i)=>(
                      <option key={i} value={i}>{a.name || a.id}</option>
                    ))}
                  </select>
                </div>
              )}
              <p style={{ fontSize:11, color:"#666", margin:"6px 0 0" }}>
                Edit to Candidate stores the selected alternative as the reviewed canonical result.
              </p>
            </div>
          )}

          {item.notes?.length > 0 && (
            <p style={{ fontSize:12, color:"#9a6700", margin:"0 0 10px" }}>⚠ {item.notes.join(" ")}</p>
          )}

          <button
            onClick={()=>setExpandedAuditByCase(s=>({...s,[item.case_id]:!s[item.case_id]}))}
            style={{ fontSize:12, background:"#fff", border:"1px solid #ccc", borderRadius:4, padding:"4px 10px", cursor:"pointer", margin:"0 0 10px" }}
          >
            {expandedAuditByCase[item.case_id] ? "Hide" : "Show"} evidence & audit trail
          </button>
          {expandedAuditByCase[item.case_id] && (
            <div style={{ border:"1px solid #d0d7de", borderRadius:6, background:"#fff", padding:10, marginBottom:10 }}>
              <EvidenceGroups evidence={item.evidence}/>
              <p style={{ fontSize:12, fontWeight:"bold", margin:"10px 0 4px", color:"#444" }}>Audit trail</p>
              <ol style={{ fontSize:11, color:"#666", paddingLeft:16, margin:0 }}>
                {item.audit_trail?.map((s,i)=><li key={i}>{s}</li>)}
              </ol>
              {item.curator_notes && (
                <p style={{ fontSize:11, color:"#666", margin:"8px 0 0" }}>
                  <strong>Curator notes:</strong> {item.curator_notes}
                </p>
              )}
              {item.review_history?.length > 0 && (
                <>
                  <p style={{ fontSize:12, fontWeight:"bold", margin:"10px 0 4px", color:"#444" }}>Review history</p>
                  <ol style={{ fontSize:11, color:"#666", paddingLeft:16, margin:0 }}>
                    {item.review_history.map((record,i)=>(
                      <li key={i}>
                        {record.role}: {record.curator_id || "unknown"} · {record.decision} · {record.timestamp}
                      </li>
                    ))}
                  </ol>
                </>
              )}
            </div>
          )}

          {/* Decision buttons */}
          {!item.decision && (
            <>
            <label style={{ display:"block", fontSize:11, color:"#666", marginBottom:8 }}>
              Reviewer note
              <textarea
                value={reviewerNotesByCase[item.case_id] || ""}
                onChange={e=>setReviewerNotesByCase(s=>({...s,[item.case_id]:e.target.value}))}
                rows={2}
                style={{ width:"100%", boxSizing:"border-box", marginTop:3, padding:"6px 8px", border:"1px solid #ccc", borderRadius:4, fontSize:12, resize:"vertical" }}
              />
            </label>
            <div style={{ display:"flex", gap:8, flexWrap:"wrap" }}>
              <button onClick={()=>decide(item.case_id,"approve")} disabled={deciding[item.case_id]}
                style={{ padding:"6px 20px", background:STATUS_COLOR.AUTO_RECONCILE, color:"#fff", border:"none", borderRadius:6, cursor:"pointer", fontSize:13 }}>
                ✓ Approve
              </button>
              <button onClick={()=>decide(item.case_id,"reject")} disabled={deciding[item.case_id]}
                style={{ padding:"6px 20px", background:STATUS_COLOR.CANNOT_RECONCILE, color:"#fff", border:"none", borderRadius:6, cursor:"pointer", fontSize:13 }}>
                ✗ Reject
              </button>
              <button onClick={()=>editToCandidate(item, selectedCandidate)} disabled={deciding[item.case_id] || !item.alternatives?.length}
                style={{ padding:"6px 20px", background:"#0969da", color:"#fff", border:"none", borderRadius:6, cursor:"pointer", fontSize:13, opacity:item.alternatives?.length?1:0.5 }}>
                Edit to Candidate
              </button>
              <button onClick={()=>editCanonical(item)} disabled={deciding[item.case_id]}
                style={{ padding:"6px 20px", background:"#8250df", color:"#fff", border:"none", borderRadius:6, cursor:"pointer", fontSize:13 }}>
                Edit Canonical
              </button>
            </div>
            </>
          )}
          {item.decision && item.curator_id && (
            <div style={{ display:"flex", gap:8, alignItems:"center", flexWrap:"wrap" }}>
              <p style={{ fontSize:11, color:"#888", margin:0 }}>Reviewed by {item.curator_id}</p>
              {item.adjudication_status === "REQUIRED" && (
                <button onClick={()=>adjudicate(item)} disabled={deciding[item.case_id]}
                  style={{ marginTop:0, padding:"4px 12px", background:"#8250df", color:"#fff", border:"none", borderRadius:6, cursor:"pointer", fontSize:12 }}>
                  Adjudicate Current Canonical
                </button>
              )}
              <button onClick={()=>reopenItem(item.case_id)} disabled={deciding[item.case_id]}
                style={{ marginTop:0, padding:"4px 12px", background:"#fff", color:"#555", border:"1px solid #ccc", borderRadius:6, cursor:"pointer", fontSize:12 }}>
                Reopen
              </button>
            </div>
          )}
        </div>
      )})}
    </div>
  );
}

// ── PAGE: Benchmark Metrics ──────────────────────────────────────────────────
function BenchmarkPage() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function load() {
    setError(""); setLoading(true);
    try {
      const r = await apiFetch("/benchmark");
      if (!r.ok) throw new Error(`API error ${r.status}`);
      setMetrics(await r.json());
    } catch(e) { setError(e.message); }
    finally { setLoading(false); }
  }

  useEffect(()=>{ load(); }, []);

  const pct = value => `${Math.round((value || 0) * 100)}%`;
  return (
    <div>
      <h2 style={{ color:"#028090", marginBottom:4 }}>Benchmark Validation</h2>
      <p style={{ color:"#666", fontSize:13 }}>Accuracy, coverage, and review-rate validation for the curated MVP benchmark.</p>
      <button onClick={load} disabled={loading}
        style={{ padding:"7px 20px", background:"#028090", color:"#fff", border:"none", borderRadius:6, fontSize:13, cursor:"pointer", opacity:loading?0.6:1 }}>
        {loading ? "Refreshing…" : "Refresh Metrics"}
      </button>
      {error && <p style={{ color:"#cf222e" }}>{error}</p>}
      {metrics && (
        <>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(160px,1fr))", gap:12, marginTop:16 }}>
            {[["Accuracy",pct(metrics.accuracy),metrics.target_status?.accuracy],["Coverage",pct(metrics.coverage),metrics.target_status?.coverage],
              ["Review Rate",pct(metrics.review_rate),true],["Cases",metrics.total_cases,true]].map(([label,value,ok])=>(
              <div key={label} style={{ background:"#fff", border:`2px solid ${ok ? STATUS_COLOR.AUTO_RECONCILE : STATUS_COLOR.CANNOT_RECONCILE}`, borderRadius:8, padding:14 }}>
                <div style={{ fontSize:26, fontWeight:"bold", color:ok ? STATUS_COLOR.AUTO_RECONCILE : STATUS_COLOR.CANNOT_RECONCILE }}>{value}</div>
                <div style={{ fontSize:12, color:"#666" }}>{label}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop:14, background:"#f8fafc", border:"1px solid #e2e8f0", borderRadius:8, padding:12, fontSize:13 }}>
            Target accuracy: {pct(metrics.targets?.accuracy)} · Target coverage: {pct(metrics.targets?.coverage)}
          </div>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(150px,1fr))", gap:10, marginTop:14 }}>
            {[
              ["Auto Reconcile",metrics.counts?.auto_reconcile],
              ["Review Required",metrics.counts?.review_required],
              ["Cannot Reconcile",metrics.counts?.cannot_reconcile],
              ["Candidate Evidence",metrics.counts?.candidate_evidence_cases],
              ["Live Lookups",metrics.counts?.live_external_lookup_attempted],
              ["Live Evidence",metrics.counts?.live_external_evidence_found],
              ["Approved",metrics.counts?.approved_review_cases],
              ["Rejected",metrics.counts?.rejected_review_cases],
              ["Edited",metrics.counts?.edited_review_cases],
            ].map(([label,value])=>(
              <div key={label} style={{ background:"#fff", border:"1px solid #d0d7de", borderRadius:6, padding:10 }}>
                <div style={{ fontSize:20, fontWeight:"bold", color:"#028090" }}>{value ?? 0}</div>
                <div style={{ fontSize:11, color:"#666" }}>{label}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop:14, background:"#fff", border:"1px solid #d0d7de", borderRadius:8, padding:14 }}>
            <p style={{ fontSize:13, fontWeight:"bold", color:"#444", margin:"0 0 8px" }}>How these numbers are calculated</p>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(220px,1fr))", gap:10, fontSize:12, color:"#444" }}>
              <div style={{ background:"#f6f8fa", borderRadius:6, padding:10 }}>
                <strong>Accuracy</strong><br/>
                Full matches / total cases<br/>
                <span style={{ color:"#666" }}>{metrics.counts?.full_correct} / {metrics.total_cases}</span>
              </div>
              <div style={{ background:"#f6f8fa", borderRadius:6, padding:10 }}>
                <strong>Coverage</strong><br/>
                Not CANNOT_RECONCILE / total cases<br/>
                <span style={{ color:"#666" }}>{metrics.counts?.resolved} / {metrics.total_cases}</span>
              </div>
              <div style={{ background:"#f6f8fa", borderRadius:6, padding:10 }}>
                <strong>Review rate</strong><br/>
                REVIEW_REQUIRED / total cases<br/>
                <span style={{ color:"#666" }}>{metrics.counts?.review_required} / {metrics.total_cases}</span>
              </div>
            </div>
            <p style={{ fontSize:12, color:"#666", margin:"10px 0 0" }}>
              Benchmark source: {metrics.benchmark_file}. Cases are manually curated from the local disease, gene, and variant catalog and include auto-reconcile, review-required, and safe-failure examples.
            </p>
            <p style={{ fontSize:12, color:"#666", margin:"6px 0 0" }}>
              This is internal MVP validation, not independent external clinical validation. Future validation should use blinded curator review and larger real-world datasets.
            </p>
          </div>
          {metrics.failures?.length > 0 && (
            <div style={{ marginTop:14 }}>
              <p style={{ fontSize:12, fontWeight:"bold", color:"#555" }}>First failures</p>
              <table style={{ fontSize:12 }}>
                <thead><tr><th>Case</th><th>Expected</th><th>Actual</th></tr></thead>
                <tbody>
                  {metrics.failures.map(f=>(
                    <tr key={f.case_id}><td>{f.case_id}</td><td>{f.expected_status}</td><td>{f.actual_status}</td></tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}

// ── Nav + App shell ───────────────────────────────────────────────────────────
function Nav() {
  const navStyle = { textDecoration:"none", padding:"8px 16px", borderRadius:6, fontSize:13, fontWeight:"bold" };
  const active = { background:"#028090", color:"#fff" };
  const inactive = { background:"#e8f4f6", color:"#028090" };
  return (
    <nav style={{ display:"flex", gap:8, marginBottom:24, paddingBottom:12, borderBottom:"1px solid #e0e0e0", alignItems:"center" }}>
      <span style={{ fontWeight:"bold", fontSize:16, color:"#0A1628", marginRight:8 }}>🧬 OncoReconcile AI</span>
      {[["Single Record","/"],["CSV Upload","/upload"],["Review Queue","/review"],["Benchmark","/benchmark"]].map(([label,path])=>(
        <NavLink key={path} to={path} end={path==="/"}
          style={({isActive})=>({...navStyle,...(isActive?active:inactive)})}>
          {label}
        </NavLink>
      ))}
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Nav/>
        <Routes>
          <Route path="/" element={<SinglePage/>}/>
          <Route path="/upload" element={<UploadPage/>}/>
          <Route path="/review" element={<ReviewQueuePage/>}/>
          <Route path="/benchmark" element={<BenchmarkPage/>}/>
        </Routes>
      </div>
    </BrowserRouter>
  );
}

createRoot(document.getElementById("root")).render(<App/>);
