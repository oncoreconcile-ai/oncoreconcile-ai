import React, { useState, useEffect } from "react";
import { apiFetch } from "./api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts";

const SYSTEM_COLORS = {
  "SNOMED CT": "#0369a1",
  "NCIt": "#d946ef",
  "LOINC": "#d97706",
  "RxNorm": "#7c3aed",
  "HGNC": "#059669",
  "ATC": "#0891b2",
  "ClinVar": "#dc2626",
  "ClinGen": "#9333ea",
  "ICD-10-CM": "#e11d48",
  "OncoTree": "#ca8a04",
  "HGVS": "#0d9488",
  "NDC": "#4f46e5",
};

const CATEGORY_EMOJIS = {
  "variant alias": "🧬",
  "textual variant": "📝",
  "HGVS protein notation": "🔬",
  "gene alias": "🧪",
  "disease abbreviation": "🏥",
  "histology abbreviation": "🔬",
  "brand to generic drug": "💊",
};

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

function SystemCodeCard({ system, code, display, confidence }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-3 flex items-center gap-3">
      <div className="w-2 h-10 rounded-full" style={{ background: SYSTEM_COLORS[system] || "#64748b" }} />
      <div className="flex-1 min-w-0">
        <div className="text-xs font-bold text-gray-500 uppercase">{system}</div>
        <div className="font-mono font-bold text-sm">{code}</div>
        <div className="text-xs text-gray-500 truncate">{display}</div>
      </div>
      <div className="text-right">
        <div className="text-xs font-bold" style={{ color: confidence >= 0.95 ? "#1a7f37" : confidence >= 0.85 ? "#e8a020" : "#cf222e" }}>
          {pct(confidence)}
        </div>
        <div className="text-[10px] text-gray-400">confidence</div>
      </div>
    </div>
  );
}

export default function CodingCoverageDashboard() {
  const [harmonization, setHarmonization] = useState(null);
  const [terminology, setTerminology] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { load(); }, []);

  async function load() {
    setLoading(true);
    setError("");
    try {
      // Load harmonization data via API
      const resp = await apiFetch("/enterprise/semantic-harmonization");
      const harm = await resp.json();
      setHarmonization(harm);

      // Load terminology metrics from API
      const termResp = await apiFetch("/enterprise/analytics/terminology");
      if (termResp.ok) setTerminology(await termResp.json());
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  }

  if (loading && !harmonization) return <div className="text-center py-12 text-gray-400">Loading coding coverage...</div>;
  if (error) return <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">{error}</div>;
  if (!harmonization) return <div className="text-center py-12 text-gray-400">No harmonization data available.</div>;

  // Extract variant alias mappings
  const variantAliases = harmonization.variant_aliases || {};
  const variantCanonicalMappings = harmonization.variant_canonical_mappings || [];

  // Count coding systems across all mappings
  const systemCounts = {};
  const systemDetails = [];

  // Walk all disease, gene, drug, histology, biomarker, lab test mappings
  for (const category of ["diseases", "histologies", "genes", "drugs", "biomarkers", "lab_tests"]) {
    const catData = harmonization[category] || {};
    for (const [entity, entityData] of Object.entries(catData)) {
      for (const m of entityData.mappings || []) {
        const sys = m.coding_system;
        if (!systemCounts[sys]) systemCounts[sys] = { count: 0, entities: new Set() };
        systemCounts[sys].count += 1;
        systemCounts[sys].entities.add(`${category}:${entity}`);
      }
    }
  }

  // Count variant alias mappings
  for (const [alias, aliasData] of Object.entries(variantAliases)) {
    for (const m of aliasData.mappings || []) {
      const sys = m.coding_system;
      if (!systemCounts[sys]) systemCounts[sys] = { count: 0, entities: new Set() };
      systemCounts[sys].count += 1;
      systemCounts[sys].entities.add(`variant_aliases:${alias}`);
    }
  }

  const systemChartData = Object.entries(systemCounts)
    .sort((a, b) => b[1].count - a[1].count)
    .map(([sys, data]) => ({
      name: sys,
      mappings: data.count,
      entities: data.entities.size,
      fill: SYSTEM_COLORS[sys] || "#64748b",
    }));

  // Variant canonical mapping chart
  const mappingChartData = variantCanonicalMappings.map(m => ({
    name: m.original,
    canonical: m.canonical,
    category: m.category,
    systems: m.coding_systems.length,
  }));

  // Build a list of all unique mappings across categories for the full display
  const allMappings = [];

  for (const category of ["diseases", "histologies", "drugs", "biomarkers", "lab_tests"]) {
    const catData = harmonization[category] || {};
    for (const [entity, entityData] of Object.entries(catData)) {
      const original = entity;
      const canonical = entityData.canonical_value || entity;
      for (const m of entityData.mappings || []) {
        allMappings.push({
          original,
          canonical,
          coding_system: m.coding_system,
          code: m.code,
          display_name: m.display_name,
          confidence: m.confidence || entityData.confidence || 0.85,
          category,
        });
      }
    }
  }

  // Add variant alias mappings
  for (const [alias, aliasData] of Object.entries(variantAliases)) {
    const canonical = aliasData.canonical_value || alias;
    for (const m of aliasData.mappings || []) {
      allMappings.push({
        original: alias,
        canonical,
        coding_system: m.coding_system,
        code: m.code,
        display_name: m.display_name,
        confidence: m.confidence || aliasData.confidence || 0.85,
        category: "variant_aliases",
      });
    }
  }

  const coveringSystems = Object.keys(systemCounts).length;
  const totalMappings = allMappings.length;

  return (
    <div>
      <div className="mb-6">
        <span className="eyebrow">Semantic Interoperability</span>
        <h1 className="text-3xl font-bold text-gray-900 mt-1">Coding System Alignment</h1>
        <p className="text-sm text-gray-500 mt-1">
          Semantic harmonization mappings across clinical and genomic coding systems.
          Prototype demonstration — not a complete terminology service.
        </p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <MetricCard label="Coding Systems" value={coveringSystems} color="#028090" />
        <MetricCard label="Total Mappings" value={totalMappings} color="#7c3aed" />
        <MetricCard label="Variant Aliases" value={Object.keys(variantAliases).length} color="#059669" subtitle="Canonical mappings" />
        <MetricCard label="Variant Canonical Maps" value={variantCanonicalMappings.length} color="#d97706" subtitle="Part 3 demo mappings" />
      </div>

      {/* Coding System Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h4 className="text-sm font-bold text-gray-700 mb-3">Mappings by Coding System</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={systemChartData} layout="vertical" margin={{ left: 90 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" />
              <YAxis type="category" dataKey="name" width={85} tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v, name, props) => [v, name === "mappings" ? "Total Mappings" : "Unique Entities"]} />
              <Legend />
              <Bar dataKey="mappings" name="Mappings" radius={[0, 4, 4, 0]}>
                {systemChartData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Variant Canonical Mappings */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h4 className="text-sm font-bold text-gray-700 mb-3">Semantic Harmonization Examples</h4>
          <div className="space-y-3 max-h-[300px] overflow-y-auto">
            {mappingChartData.map((m, i) => (
              <div key={i} className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                <div className="flex items-center gap-2 mb-1">
                  <span>{CATEGORY_EMOJIS[m.category] || "🔗"}</span>
                  <span className="text-xs font-bold text-gray-500 uppercase">{m.category}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <span className="font-mono bg-white px-2 py-0.5 rounded border border-gray-200 text-xs">{m.name}</span>
                  <span className="text-gray-400">→</span>
                  <span className="font-bold text-primary text-xs">{m.canonical}</span>
                </div>
                {m.systems > 0 && (
                  <div className="flex gap-1 mt-1">
                    {m.systems > 0 && <span className="text-[10px] text-gray-400">{m.systems} coding system{m.systems > 1 ? "s" : ""} mapped</span>}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Full Coverage Table */}
      <div className="bg-white rounded-xl border-2 border-gray-200 p-5 mb-6">
        <h3 className="text-base font-bold text-gray-700 mb-4">Complete Mapping Coverage</h3>
        <p className="text-xs text-gray-500 mb-4">
          All mapped entities showing original value, canonical value, coding system, code, and mapping confidence.
          This is a demonstration layer — not complete production vocabulary coverage.
        </p>
        <div className="overflow-x-auto max-h-[500px] overflow-y-auto">
          <table className="w-full text-xs border-collapse">
            <thead>
              <tr className="bg-gray-50 sticky top-0">
                <th className="text-left p-2 border-b font-bold text-gray-600">Category</th>
                <th className="text-left p-2 border-b font-bold text-gray-600">Original Value</th>
                <th className="text-left p-2 border-b font-bold text-gray-600">Canonical Value</th>
                <th className="text-left p-2 border-b font-bold text-gray-600">Coding System</th>
                <th className="text-left p-2 border-b font-bold text-gray-600">Code</th>
                <th className="text-left p-2 border-b font-bold text-gray-600">Display Name</th>
                <th className="text-left p-2 border-b font-bold text-gray-600">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {allMappings.map((m, i) => (
                <tr key={i} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="p-2 text-gray-500 font-medium">{m.category.replace(/_/g, " ")}</td>
                  <td className="p-2 font-mono">{m.original}</td>
                  <td className="p-2 text-primary font-medium">{m.canonical}</td>
                  <td className="p-2">
                    <span className="inline-block px-2 py-0.5 rounded text-[10px] font-bold"
                      style={{ background: SYSTEM_COLORS[m.coding_system] + "20" || "#f0f0f0", color: SYSTEM_COLORS[m.coding_system] || "#333" }}>
                      {m.coding_system}
                    </span>
                  </td>
                  <td className="p-2 font-mono text-[11px]">{m.code}</td>
                  <td className="p-2 text-gray-600 max-w-[200px] truncate" title={m.display_name}>{m.display_name}</td>
                  <td className="p-2">
                    <span className={`font-bold ${
                      m.confidence >= 0.95 ? "text-green-600" :
                      m.confidence >= 0.85 ? "text-amber-600" :
                      "text-red-600"
                    }`}>
                      {pct(m.confidence)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-[10px] text-gray-400 mt-3">
          Prototype mappings for enterprise demonstration. Source codes and concept_ids are illustrative.
          Connect a terminology server for production use.
        </p>
      </div>

      {/* Coding System Descriptions */}
      {harmonization.coding_system_descriptions && (
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-base font-bold text-gray-700 mb-4">Reference Resources</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {Object.entries(harmonization.coding_system_descriptions).map(([sys, desc]) => (
              <div key={sys} className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                <div className="flex items-center gap-2 mb-1">
                  <div className="w-2 h-2 rounded-full" style={{ background: SYSTEM_COLORS[sys] || "#64748b" }} />
                  <span className="font-bold text-sm">{sys}</span>
                </div>
                <p className="text-xs text-gray-600">{desc}</p>
              </div>
            ))}
          </div>
          <p className="text-[10px] text-gray-400 mt-3">
            This platform aligns with these standards but does not replace them.
            Full conformance requires implementation-specific validation.
          </p>
        </div>
      )}
    </div>
  );
}
