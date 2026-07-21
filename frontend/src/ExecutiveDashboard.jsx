import React, { useState, useEffect } from "react";
import { apiFetch } from "./api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts";

function pct(v) { return `${Math.round((v || 0) * 100)}%`; }

function MetricCard({ label, value, color, subtitle, icon }) {
  return (
    <div className="bg-white rounded-xl border-2 p-5 flex flex-col" style={{ borderColor: color || "#d0d7de" }}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">{label}</span>
        {icon && <span className="text-xl">{icon}</span>}
      </div>
      <span className="text-4xl font-bold" style={{ color: color || "#172033" }}>{value}</span>
      {subtitle && <span className="text-[10px] text-gray-400 mt-1">{subtitle}</span>}
    </div>
  );
}

export default function ExecutiveDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const r = await apiFetch("/enterprise/executive-dashboard");
        setData(await r.json());
      } catch (e) { setError(e.message); }
      finally { setLoading(false); }
    }
    load();
  }, []);

  if (loading) return <div className="text-center py-12 text-gray-400">Loading executive dashboard...</div>;
  if (error) return <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">{error}</div>;
  if (!data) return <div className="text-center py-12 text-gray-400">No data available.</div>;

  const radarData = [
    { metric: "Data Quality", value: Math.round(data.data_quality_score * 100) },
    { metric: "Governance", value: Math.round(data.governance_score * 100) },
    { metric: "Reconciliation", value: Math.round(data.reconciliation_coverage * 100) },
    { metric: "Coding Coverage", value: Math.round(data.coding_coverage * 100) },
    { metric: "Evidence", value: Math.round(data.evidence_coverage * 100) },
    { metric: "Semantic Harm.", value: Math.round(data.semantic_harmonization_coverage * 100) },
    { metric: "AI Readiness", value: Math.round(data.ai_readiness_score * 100) },
  ];

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <span className="eyebrow">Enterprise Platform</span>
        <h1 className="text-4xl font-bold text-gray-900 mt-1">Executive Dashboard</h1>
        <p className="text-base text-gray-500 mt-2 max-w-2xl">
          Enterprise overview demonstrating platform value for cancer centers, pharmaceutical companies, 
          research organizations, and healthcare data platforms.
        </p>
      </div>

      {/* Hero KPI Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <MetricCard label="Patients Managed" value={data.patients_managed} color="#028090" icon="🧬" />
        <MetricCard label="Data Quality" value={pct(data.data_quality_score)} color={data.data_quality_score >= 0.9 ? "#1a7f37" : "#e8a020"} subtitle="Average across cohort" icon="📊" />
        <MetricCard label="Governance Score" value={pct(data.governance_score)} color={data.governance_score >= 0.8 ? "#1a7f37" : "#e8a020"} icon="🔬" />
        <MetricCard label="AI Readiness" value={pct(data.ai_readiness_score)} color={data.ai_readiness_score >= 0.8 ? "#1a7f37" : "#e8a020"} subtitle="Composite index" icon="🤖" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Coverage Radar Chart */}
        <div className="bg-white rounded-xl border-2 border-primary p-6">
          <h3 className="text-base font-bold text-gray-800 mb-4">Platform Coverage Scorecard</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e5e7eb" />
              <PolarAngleAxis dataKey="metric" tick={{ fontSize: 11 }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fontSize: 10 }} />
              <Radar dataKey="value" stroke="#028090" fill="#028090" fillOpacity={0.2} strokeWidth={2} />
              <Tooltip formatter={v => `${v}%`} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-2 gap-4">
          <MetricCard label="Reconciliation Coverage" value={pct(data.reconciliation_coverage)} color={data.reconciliation_coverage >= 0.8 ? "#1a7f37" : "#e8a020"} icon="✅" />
          <MetricCard label="Coding Coverage" value={pct(data.coding_coverage)} color={data.coding_coverage >= 0.8 ? "#1a7f37" : "#e8a020"} icon="📋" />
          <MetricCard label="Evidence Coverage" value={pct(data.evidence_coverage)} color={data.evidence_coverage >= 0.8 ? "#1a7f37" : "#e8a020"} icon="🔍" />
          <MetricCard label="Semantic Harmonization" value={pct(data.semantic_harmonization_coverage)} color={data.semantic_harmonization_coverage >= 0.8 ? "#1a7f37" : "#e8a020"} icon="🔗" />
        </div>
      </div>

      {/* Most Common Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-bold text-gray-700 mb-4">Most Common Cancer Types</h3>
          <div className="space-y-2">
            {data.most_common_cancer_types?.map((ct, i) => (
              <div key={ct} className="flex items-center gap-3 bg-gray-50 rounded-lg p-3">
                <span className="w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">#{i + 1}</span>
                <span className="font-bold text-sm">{ct}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-sm font-bold text-gray-700 mb-4">Most Common Biomarkers</h3>
          <div className="space-y-2">
            {data.most_common_biomarkers?.map((b, i) => (
              <div key={b} className="flex items-center gap-3 bg-purple-50 rounded-lg p-3">
                <span className="w-6 h-6 rounded-full bg-purple-500 text-white flex items-center justify-center text-xs font-bold">#{i + 1}</span>
                <span className="font-bold text-sm">{b}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Terminology Mappings */}
      <div className="bg-white rounded-xl border-2 border-gray-200 p-6 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-gray-800">Terminology Mappings</h3>
            <p className="text-sm text-gray-500 mt-1">Total coding system mappings created across the semantic harmonization layer.</p>
          </div>
          <div className="text-right">
            <span className="text-4xl font-bold text-primary">{data.total_terminology_mappings}</span>
            <p className="text-xs text-gray-500">total mappings</p>
          </div>
        </div>
      </div>

      {/* Value Proposition */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-5 border border-blue-200">
          <h4 className="font-bold text-sm text-blue-800">Cancer Centers</h4>
          <p className="text-xs text-blue-600 mt-2">Harmonized patient data, governance workflows, and AI-ready datasets for precision oncology programs.</p>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-5 border border-purple-200">
          <h4 className="font-bold text-sm text-purple-800">Pharma</h4>
          <p className="text-xs text-purple-600 mt-2">Cohort analytics, real-world evidence pipelines, clinical trial matching, and standardized outputs.</p>
        </div>
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-5 border border-green-200">
          <h4 className="font-bold text-sm text-green-800">Research Organizations</h4>
          <p className="text-xs text-green-600 mt-2">Semantic harmonization, FHIR/OMOP exports, and knowledge graphs for multi-institutional studies.</p>
        </div>
        <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-xl p-5 border border-amber-200">
          <h4 className="font-bold text-sm text-amber-800">Healthcare Data Platforms</h4>
          <p className="text-xs text-amber-600 mt-2">Interoperability, terminology mapping, coding standardization, and governance-ready data pipelines.</p>
        </div>
      </div>

      <p className="text-[10px] text-gray-400 text-center mt-8">
        OncoReconcile AI Enterprise Platform · Synthetic data demonstration · Not for clinical use
      </p>
    </div>
  );
}
