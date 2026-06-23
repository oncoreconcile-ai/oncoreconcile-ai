import React, { useState, useEffect } from "react";
import { apiFetch } from "./api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from "recharts";

const STATUS_COLORS = { AUTO_RECONCILE: "#1a7f37", REVIEW_REQUIRED: "#e8a020", CANNOT_RECONCILE: "#cf222e" };
const CANCER_COLORS = ["#0369a1", "#d946ef", "#d97706", "#7c3aed", "#dc2626", "#059669", "#0891b2", "#9333ea"];

function pct(v) { return `${Math.round((v || 0) * 100)}%`; }

function MetricCard({ label, value, color, subtitle }) {
  return (
    <div className="bg-white rounded-xl border-2 p-4 flex flex-col" style={{ borderColor: color || "#d0d7de" }}>
      <span className="text-3xl font-bold" style={{ color: color || "#172033" }}>{value}</span>
      <span className="text-xs font-bold text-gray-500 uppercase tracking-wider mt-1">{label}</span>
      {subtitle && <span className="text-[10px] text-gray-400 mt-1">{subtitle}</span>}
    </div>
  );
}

function Indicator({ value }) {
  const colors = { green: "bg-green-500", yellow: "bg-yellow-500", red: "bg-red-500" };
  return <span className={`inline-block w-3 h-3 rounded-full ${colors[value] || 'bg-gray-300'}`} />;
}

export default function EnterpriseAnalytics() {
  const [summary, setSummary] = useState(null);
  const [biomarkers, setBiomarkers] = useState(null);
  const [treatments, setTreatments] = useState(null);
  const [outcomes, setOutcomes] = useState(null);
  const [dataQuality, setDataQuality] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { loadAll(); }, []);

  async function loadAll() {
    setLoading(true);
    setError("");
    try {
      const [s, b, t, o, dq] = await Promise.all([
        apiFetch("/enterprise/analytics/summary").then(r => r.json()),
        apiFetch("/enterprise/analytics/biomarkers").then(r => r.json()),
        apiFetch("/enterprise/analytics/treatments").then(r => r.json()),
        apiFetch("/enterprise/analytics/outcomes").then(r => r.json()),
        apiFetch("/enterprise/analytics/data-quality").then(r => r.json()),
      ]);
      setSummary(s);
      setBiomarkers(b);
      setTreatments(t);
      setOutcomes(o);
      setDataQuality(dq);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  }

  if (loading && !summary) return <div className="text-center py-12 text-gray-400">Loading enterprise analytics...</div>;
  if (error) return <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">{error}</div>;

  const cancerChartData = summary?.cancer_type_distribution ? Object.entries(summary.cancer_type_distribution).map(([k, v]) => ({ name: k, value: v })) : [];
  const geneChartData = summary?.gene_frequency ? Object.entries(summary.gene_frequency).map(([k, v]) => ({ name: k, value: v })) : [];
  const drugChartData = summary?.drug_frequency ? Object.entries(summary.drug_frequency).map(([k, v]) => ({ name: k.length > 25 ? k.substring(0, 25) + "..." : k, value: v, fullName: k })) : [];
  const stageChartData = summary?.stage_distribution ? Object.entries(summary.stage_distribution).map(([k, v]) => ({ name: k, value: v })) : [];
  const lotChartData = summary?.line_of_therapy_distribution ? Object.entries(summary.line_of_therapy_distribution).map(([k, v]) => ({ name: `Line ${k}`, value: v })) : [];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <span className="eyebrow">Enterprise Platform</span>
          <h1 className="text-3xl font-bold text-gray-900 mt-1">Cohort Analytics Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">Comprehensive analytics, data quality, governance, and terminology metrics.</p>
        </div>
        <button onClick={loadAll} className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-bold hover:bg-primary-dark transition-colors">
          {loading ? "Refreshing..." : "Refresh All"}
        </button>
      </div>

      {/* KPI Row */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <MetricCard label="Total Patients" value={summary.total_patients} color="#028090" />
          <MetricCard label="Avg Data Quality" value={pct(summary.average_data_quality_score)} color={summary.average_data_quality_score >= 0.9 ? "#1a7f37" : "#e8a020"} />
          <MetricCard label="Biomarker Testing" value={pct(summary.biomarker_testing_rate)} color={`hsl(${summary.biomarker_testing_rate * 120}, 70%, 40%)`} />
          <MetricCard label="AI Readiness" value={pct(summary.ai_readiness_score)} color={summary.ai_readiness_score >= 0.8 ? "#1a7f37" : "#e8a020"} />
          <MetricCard label="Review Required" value={pct(summary.review_required_rate)} color={summary.review_required_rate > 0.3 ? "#cf222e" : "#e8a020"} />
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Cancer Type Distribution */}
        {cancerChartData.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h4 className="text-sm font-bold text-gray-700 mb-3">Cancer Type Distribution</h4>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={cancerChartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {cancerChartData.map((e, i) => <Cell key={i} fill={CANCER_COLORS[i % CANCER_COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Stage Distribution */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h4 className="text-sm font-bold text-gray-700 mb-3">Stage Distribution</h4>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={stageChartData} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                {stageChartData.map((e, i) => <Cell key={i} fill={CANCER_COLORS[i % CANCER_COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Most Common Genes */}
        {geneChartData.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h4 className="text-sm font-bold text-gray-700 mb-3">Most Common Genes</h4>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={geneChartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" />
                <YAxis type="category" dataKey="name" width={60} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#0369a1" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Most Common Drugs */}
        {drugChartData.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h4 className="text-sm font-bold text-gray-700 mb-3">Most Common Drugs</h4>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={drugChartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" />
                <YAxis type="category" dataKey="name" width={130} tick={{ fontSize: 9 }} />
                <Tooltip formatter={(v, name, props) => [v, props.payload.fullName]} />
                <Bar dataKey="value" fill="#d946ef" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Lines of Therapy */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h4 className="text-sm font-bold text-gray-700 mb-3">Lines of Therapy</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={lotChartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#7c3aed" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Response Distribution */}
        {summary?.response_distribution && (
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h4 className="text-sm font-bold text-gray-700 mb-3">Response Distribution</h4>
            <div className="space-y-2">
              {Object.entries(summary.response_distribution).map(([k, v]) => (
                <div key={k} className="flex items-center gap-3">
                  <span className="text-xs text-gray-600 w-40">{k}</span>
                  <div className="flex-1 bg-gray-100 rounded-full h-5 overflow-hidden">
                    <div className="h-full bg-primary rounded-full" style={{ width: `${Math.min(100, (v / summary.total_patients) * 100)}%` }} />
                  </div>
                  <span className="text-xs font-bold">{v}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Data Quality Dashboard */}
      {dataQuality && (
        <div className="bg-white rounded-xl border-2 border-gray-200 p-5 mb-6">
          <h3 className="text-base font-bold text-gray-700 mb-4">Data Quality & Governance</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <MetricCard label="Data Completeness" value={pct(dataQuality.quality_scores?.data_completeness)} color={dataQuality.quality_scores?.data_completeness >= 0.9 ? "#1a7f37" : "#e8a020"} />
            <MetricCard label="Coding Coverage" value={pct(dataQuality.quality_scores?.coding_coverage)} color={dataQuality.quality_scores?.coding_coverage >= 0.9 ? "#1a7f37" : "#e8a020"} />
            <MetricCard label="Semantic Harmonization" value={pct(dataQuality.quality_scores?.semantic_harmonization_coverage)} color={dataQuality.quality_scores?.semantic_harmonization_coverage >= 0.9 ? "#1a7f37" : "#e8a020"} />
            <MetricCard label="Evidence Coverage" value={pct(dataQuality.quality_scores?.evidence_coverage)} color={dataQuality.quality_scores?.evidence_coverage >= 0.9 ? "#1a7f37" : "#e8a020"} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="text-xs font-bold text-gray-500 uppercase mb-2">Missing Data Rates</h4>
              {Object.entries(dataQuality.missing_data_rates || {}).map(([k, v]) => {
                const val = typeof v === 'number' ? v : 0;
                return (
                  <div key={k} className="flex items-center gap-2 mb-1">
                    <Indicator value={val < 0.1 ? "green" : val < 0.3 ? "yellow" : "red"} />
                    <span className="text-xs text-gray-600">{k.replace(/_/g, ' ')}: {pct(1 - val)}</span>
                  </div>
                );
              })}
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="text-xs font-bold text-gray-500 uppercase mb-2">Harmonization Summary</h4>
              <div className="text-sm space-y-1">
                <p>Diseases: <strong>{dataQuality.harmonization?.diseases_mapped || 0}</strong></p>
                <p>Histologies: <strong>{dataQuality.harmonization?.histologies_mapped || 0}</strong></p>
                <p>Genes: <strong>{dataQuality.harmonization?.genes_mapped || 0}</strong></p>
                <p>Drugs: <strong>{dataQuality.harmonization?.drugs_mapped || 0}</strong></p>
                <p>Total Mappings: <strong>{dataQuality.harmonization?.total_mappings || 0}</strong></p>
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="text-xs font-bold text-gray-500 uppercase mb-2">Review Metrics</h4>
              <div className="text-sm space-y-1">
                <p>Review Required Cases: <strong>{dataQuality.review_metrics?.review_required_cases || 0}</strong></p>
                <p>Total Review Items: <strong>{dataQuality.review_metrics?.total_review_items || 0}</strong></p>
                <p>Review Rate: <strong>{pct(dataQuality.review_metrics?.review_required_rate)}</strong></p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Outcomes Section */}
      {outcomes && (
        <div className="bg-white rounded-xl border-2 border-gray-200 p-5">
          <h3 className="text-base font-bold text-gray-700 mb-4">Outcomes Analysis</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="text-xs font-bold text-gray-500 uppercase mb-2">Outcome by Cancer Type</h4>
              {Object.entries(outcomes.outcome_by_diagnosis || {}).map(([diag, counts]) => (
                <div key={diag} className="mb-2 bg-gray-50 rounded-lg p-3">
                  <p className="font-bold text-xs">{diag}</p>
                  <div className="flex gap-2 text-xs mt-1">
                    <span className="text-green-600">CR: {counts.CR}</span>
                    <span className="text-blue-600">PR: {counts.PR}</span>
                    <span className="text-amber-600">SD: {counts.SD}</span>
                    <span className="text-red-600">PD: {counts.PD}</span>
                  </div>
                </div>
              ))}
            </div>
            <div>
              <h4 className="text-xs font-bold text-gray-500 uppercase mb-2">Progression Rate by Cancer Type</h4>
              {Object.entries(outcomes.progression_by_diagnosis || {}).map(([diag, data]) => (
                <div key={diag} className="mb-2 bg-gray-50 rounded-lg p-3">
                  <p className="font-bold text-xs">{diag}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="flex-1 bg-gray-100 rounded-full h-4 overflow-hidden">
                      <div className="h-full bg-red-500 rounded-full" style={{ width: `${(data.progressed / data.total) * 100}%` }} />
                    </div>
                    <span className="text-xs">{data.progressed}/{data.total} progressed</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <p className="text-[10px] text-gray-400 text-center mt-6">
        Synthetic data for enterprise platform demonstration. All analytics are computed from the longitudinal patient journey dataset.
      </p>
    </div>
  );
}
