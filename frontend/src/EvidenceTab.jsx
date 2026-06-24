import React, { useState } from "react";
import { json } from "react-router-dom";

const SOURCE_COLORS = {
  "ClinVar": "#0969da",
  "CIViC": "#8250df",
  "Local Catalog": "#1a7f37",
  "MyVariant": "#9a6700",
};

const SOURCE_ORDER = ["ClinVar", "CIViC", "Local Catalog", "MyVariant"];

function SourceBadge({ source }) {
  const color = SOURCE_COLORS[source] || "#64748b";
  return (
    <span
      className="evidence-badge"
      style={{ background: `${color}14`, color, border: `1px solid ${color}44` }}
    >
      {source}
    </span>
  );
}

function EvidenceCard({ item, defaultExpanded }) {
  const [expanded, setExpanded] = useState(defaultExpanded || false);
  const confidence = item.confidence || 0;
  const confPct = Math.round(confidence * 100);
  const confColor = confPct >= 75 ? "#1a7f37" : confPct >= 45 ? "#9a6700" : "#cf222e";

  return (
    <div className="evidence-card">
      <div className="evidence-card-header" onClick={() => setExpanded(!expanded)}>
        <div className="evidence-card-badges">
          <SourceBadge source={item.source_badge || item.source} />
          {item.evidence_type && (
            <span className="evidence-type-label">{item.evidence_type.replace(/_/g, " ")}</span>
          )}
        </div>
        <div className="evidence-card-meta">
          <span className="evidence-confidence" style={{ color: confColor }}>
            {confPct}%
          </span>
          <span className="evidence-expand-icon">{expanded ? "▲" : "▼"}</span>
        </div>
      </div>

      <div className="evidence-card-summary">
        <p>{item.summary || "No summary available."}</p>
      </div>

      {expanded && (
        <div className="evidence-card-details">
          {item.url && (
            <a
              href={item.url}
              target="_blank"
              rel="noreferrer"
              className="evidence-source-link"
            >
              View source ↗
            </a>
          )}

          {item.metadata && Object.keys(item.metadata).length > 0 && (
            <div className="evidence-metadata-grid">
              {item.metadata.civic_evidence_id && (
                <div className="meta-item">
                  <span className="meta-label">CIViC Evidence ID</span>
                  <span className="meta-value">{item.metadata.civic_evidence_id}</span>
                </div>
              )}
              {item.metadata.variation_id && (
                <div className="meta-item">
                  <span className="meta-label">ClinVar Variation ID</span>
                  <span className="meta-value">{item.metadata.variation_id}</span>
                </div>
              )}
              {item.metadata.accession && (
                <div className="meta-item">
                  <span className="meta-label">Accession</span>
                  <span className="meta-value">{item.metadata.accession}</span>
                </div>
              )}
              {item.metadata.clinical_significance && (
                <div className="meta-item">
                  <span className="meta-label">Clinical Significance</span>
                  <span className="meta-value">{item.metadata.clinical_significance}</span>
                </div>
              )}
              {item.metadata.review_status && (
                <div className="meta-item">
                  <span className="meta-label">Review Status</span>
                  <span className="meta-value">{item.metadata.review_status}</span>
                </div>
              )}
              {item.metadata.evidence_level && (
                <div className="meta-item">
                  <span className="meta-label">Evidence Level</span>
                  <span className="meta-value">{item.metadata.evidence_level}</span>
                </div>
              )}
              {item.metadata.evidence_direction && (
                <div className="meta-item">
                  <span className="meta-label">Direction</span>
                  <span className="meta-value">{item.metadata.evidence_direction}</span>
                </div>
              )}
              {item.metadata.disease && (
                <div className="meta-item">
                  <span className="meta-label">Disease</span>
                  <span className="meta-value">{item.metadata.disease}</span>
                </div>
              )}
              {item.metadata.therapies && item.metadata.therapies.length > 0 && (
                <div className="meta-item">
                  <span className="meta-label">Therapies</span>
                  <span className="meta-value">{item.metadata.therapies.join(", ")}</span>
                </div>
              )}
              {item.metadata.pubmed_id && (
                <div className="meta-item">
                  <span className="meta-label">PubMed</span>
                  <a
                    href={`https://pubmed.ncbi.nlm.nih.gov/${item.metadata.pubmed_id}/`}
                    target="_blank"
                    rel="noreferrer"
                    className="meta-value meta-link"
                  >
                    PMID:{item.metadata.pubmed_id}
                  </a>
                </div>
              )}
              {item.metadata.citation && (
                <div className="meta-item meta-full">
                  <span className="meta-label">Citation</span>
                  <span className="meta-value">{item.metadata.citation}</span>
                </div>
              )}
              {item.metadata.citations_count != null && (
                <div className="meta-item">
                  <span className="meta-label">Supporting Submissions</span>
                  <span className="meta-value">{item.metadata.citations_count}</span>
                </div>
              )}
            </div>
          )}

          <div className="evidence-retrieval-info">
            <span>Retrieved via: {item.retrieval_mode || "N/A"}</span>
            <span>Timestamp: {item.timestamp ? new Date(item.timestamp).toLocaleString() : "N/A"}</span>
          </div>
        </div>
      )}
    </div>
  );
}

function HGVSDisplay({ hgvs }) {
  if (!hgvs) return null;
  const hasHgvs = hgvs.protein_hgvs || hgvs.coding_hgvs || hgvs.genomic_hgvs;
  if (!hasHgvs) return null;

  return (
    <div className="hgvs-panel">
      <h4>Canonical HGVS Representations</h4>
      <div className="hgvs-grid">
        {hgvs.protein_hgvs && (
          <div className="hgvs-item">
            <span>Protein</span>
            <code>{hgvs.protein_hgvs}</code>
          </div>
        )}
        {hgvs.coding_hgvs && (
          <div className="hgvs-item">
            <span>Coding</span>
            <code>{hgvs.coding_hgvs}</code>
          </div>
        )}
        {hgvs.genomic_hgvs && (
          <div className="hgvs-item">
            <span>Genomic</span>
            <code>{hgvs.genomic_hgvs}</code>
          </div>
        )}
        {hgvs.vrs_ready && hgvs.vrs_id && (
          <div className="hgvs-item hgvs-vrs">
            <span>GA4GH VRS</span>
            <code>VRS ID: {hgvs.vrs_id}</code>
          </div>
        )}
        {!hgvs.vrs_ready && (
          <div className="hgvs-item hgvs-future">
            <span>GA4GH VRS</span>
            <span className="hgvs-future-label">VRS ready (future)</span>
          </div>
        )}
      </div>
    </div>
  );
}

function EvidenceBoostBreakdown({ evidenceScoreBreakdown }) {
  if (!evidenceScoreBreakdown || !evidenceScoreBreakdown.evidence_boost) return null;

  const boost = evidenceScoreBreakdown.evidence_boost;
  const breakdown = evidenceScoreBreakdown.evidence_breakdown || {};
  const details = evidenceScoreBreakdown.evidence_details || [];
  const boostPct = Math.round(boost * 100);

  return (
    <div className="boost-panel">
      <div className="boost-header">
        <h4>Evidence-Based Confidence Boost</h4>
        <span className="boost-value" style={{ color: boostPct >= 25 ? "#1a7f37" : boostPct >= 10 ? "#9a6700" : "#64748b" }}>
          +{boostPct}%
        </span>
      </div>
      {Object.keys(breakdown).length > 0 && (
        <div className="boost-breakdown">
          {Object.entries(breakdown).map(([source, value]) => {
            const pct = Math.round(value * 100);
            return (
              <div key={source} className="boost-source-row">
                <span className="boost-source-label">{source}</span>
                <div className="boost-track">
                  <div
                    className="boost-bar"
                    style={{ width: `${Math.min(100, pct)}%`, background: SOURCE_COLORS[source] || "#64748b" }}
                  />
                </div>
                <span className="boost-source-value">+{pct}%</span>
              </div>
            );
          })}
        </div>
      )}
      {details.length > 0 && (
        <details className="boost-details">
          <summary>Calculation details ({details.length})</summary>
          <ul>
            {details.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

export default function EvidenceTab({ result }) {
  if (!result) {
    return (
      <div className="evidence-tab-empty">
        <p>No reconciliation result available. Run a reconciliation first to view evidence.</p>
      </div>
    );
  }

  const federation = result.federation;
  const bySource = federation?.by_source || {};
  const unified = federation?.unified_evidence || result.unified_evidence || [];
  const hgvs = federation?.hgvs || result.canonical_hgvs;
  const evidenceBoost = result.evidence_score_breakdown;

  // Build source stats
  const sourceStats = {};
  SOURCE_ORDER.forEach(src => {
    const items = bySource[src] || [];
    if (items.length > 0) {
      sourceStats[src] = items.length;
    }
  });

  const hasErrors = federation?.errors?.length > 0;

  return (
    <div className="evidence-tab">
      {/* HGVS Section */}
      <HGVSDisplay hgvs={hgvs} />

      {/* Evidence Boost Section */}
      <EvidenceBoostBreakdown evidenceScoreBreakdown={evidenceBoost} />

      {/* Source Summary */}
      <div className="evidence-source-summary">
        <h4>Evidence Sources</h4>
        <div className="source-summary-grid">
          {SOURCE_ORDER.map(source => {
            const items = bySource[source] || [];
            if (items.length === 0) return null;
            return (
              <div key={source} className="source-summary-card" style={{ borderTop: `3px solid ${SOURCE_COLORS[source] || "#64748b"}` }}>
                <div className="source-summary-header">
                  <SourceBadge source={source} />
                  <span className="source-count">{items.length} item{items.length !== 1 ? "s" : ""}</span>
                </div>
                <div className="source-mini-bars">
                  {items.slice(0, 5).map((item, i) => {
                    const pct = Math.round((item.confidence || 0) * 100);
                    return (
                      <div key={i} className="source-mini-bar" title={`${item.evidence_type}: ${pct}%`}>
                        <div
                          className="source-mini-fill"
                          style={{
                            height: `${Math.max(10, pct)}%`,
                            background: SOURCE_COLORS[source] || "#64748b",
                          }}
                        />
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Errors */}
      {hasErrors && (
        <div className="evidence-errors">
          <h4>Evidence Retrieval Errors</h4>
          <ul>
            {federation.errors.map((err, i) => (
              <li key={i}>{err}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Evidence by Source */}
      <div className="evidence-by-source">
        {SOURCE_ORDER.map(source => {
          const items = bySource[source] || [];
          if (items.length === 0) return null;
          return (
            <section key={source} className="evidence-source-group">
              <div className="evidence-source-group-header">
                <SourceBadge source={source} />
                <span className="evidence-source-count">{items.length} item{items.length !== 1 ? "s" : ""}</span>
              </div>
              <div className="evidence-cards">
                {items.map((item, i) => (
                  <EvidenceCard key={i} item={item} defaultExpanded={i === 0} />
                ))}
              </div>
            </section>
          );
        })}
      </div>

      {/* Raw unified evidence count */}
      {unified.length === 0 && (
        <div className="evidence-empty">
          <p>No federated evidence was retrieved for this variant.</p>
        </div>
      )}
    </div>
  );
}
