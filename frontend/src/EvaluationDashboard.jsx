import React, { useState, useEffect } from "react";
import { apiFetch } from "./api";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell,
  LineChart, Line,
} from "recharts";

const STATUS_COLORS = { AUTO_RECONCILE: "#1a7f37", REVIEW_REQUIRED: "#e8a020", CANNOT_RECONCILE: "#cf222e" };

function pct(v) {
  return `${Math.round((v || 0) * 100)}%`;
}

function MetricCard({ label, value, color, subtitle }) {
  return (
    <div className="bg-white rounded-xl border-2 p-4 flex flex-col" style={{ borderColor: color || "#d0d7de" }}>
      <span className="text-3xl font-bold" style={{ color: color || "#172033" }}>{value}</span>
      <span className="text-xs font-bold text-gray-500 uppercase tracking-wider mt-1">{label}</span>
      {subtitle && <span className="text-[10px] text-gray-400 mt-1">{subtitle}</span>}
    </div>
  );
}

function StatusPie({ data }) {
  const pieData = [
    { name: "Auto Reconcile", value: data.auto_reconcile, color: STATUS_COLORS.AUTO_RECONCILE },
    { name: "Review Required", value: data.review_required, color: STATUS_COLORS.REVIEW_REQUIRED },
    { name: "Cannot Reconcile", value: data.cannot_reconcile, color: STATUS_COLORS.CANNOT_RECONCILE },
  ].filter(d => d.value > 0);

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">Status Distribution</h4>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
            {pieData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

function AccuracyGauge({ accuracy, coverage }) {
  const gaugeData = [
    { name: "Accuracy", value: Math.round(accuracy * 100), fill: accuracy >= 0.9 ? "#1a7f37" : "#e8a020" },
    { name: "Coverage", value: Math.round(coverage * 100), fill: coverage >= 0.95 ? "#1a7f37" : "#e8a020" },
  ];

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">Accuracy & Coverage</h4>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={gaugeData} layout="vertical" margin={{ left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} tickFormatter={v => `${v}%`} />
          <YAxis type="category" dataKey="name" width={80} tick={{ fontSize: 12 }} />
          <Tooltip formatter={v => `${v}%`} />
          <Bar dataKey="value" radius={[0, 8, 8, 0]}>
            {gaugeData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex justify-between text-xs text-gray-500 mt-1">
        <span>Target: ≥90%</span>
        <span>Target: ≥95%</span>
      </div>
    </div>
  );
}

function ReviewRateBar({ reviewRate }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">Review Rate</h4>
      <div className="flex items-center gap-4">
        <span className="text-4xl font-bold text-warning">{pct(reviewRate)}</span>
        <div className="flex-1">
          <div className="h-4 bg-gray-100 rounded-full overflow-hidden">
            <div className="h-full bg-warning rounded-full" style={{ width: `${Math.min(100, reviewRate * 100)}%` }} />
          </div>
        </div>
      </div>
      <p className="text-[10px] text-gray-400 mt-2">
        Proportion of cases routed for human review.
      </p>
    </div>
  );
}

function FalseAutoAcceptRate({ failures, totalCases }) {
  // "False auto-accept rate" = cases that were AUTO_RECONCILE but had incorrect concepts / total auto-reconciled
  // For MVP, we compute from failures where expected_status != actual_status
  if (!failures || !totalCases) return null;
  const falseAuto = failures.filter(f => f.actual_status === "AUTO_RECONCILE" && f.expected_status !== "AUTO_RECONCILE").length;
  const total = totalCases || 1;
  const rate = falseAuto / total;

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">False Auto-Accept Rate</h4>
      <div className="flex items-center gap-4">
        <span className={`text-4xl font-bold ${rate > 0.05 ? "text-danger" : "text-success"}`}>
          {pct(rate)}
        </span>
      </div>
      <p className="text-[10px] text-gray-400 mt-2">
        Cases incorrectly auto-accepted: {falseAuto} of {totalCases} total.
      </p>
    </div>
  );
}

function FailureBreakdown({ failures }) {
  if (!failures || failures.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h4 className="text-sm font-bold text-gray-700 mb-3">Failure Breakdown</h4>
        <p className="text-green-600 text-sm font-semibold">✓ No failures — all cases pass validation.</p>
      </div>
    );
  }

  // Group failures by what went wrong
  const groups = {};
  failures.forEach(f => {
    const key = `${f.expected_status ?? "unknown"} → ${f.actual_status ?? "unknown"}`;
    if (!groups[key]) groups[key] = { count: 0, cases: [] };
    groups[key].count++;
    groups[key].cases.push(f.case_id);
  });

  const chartData = Object.entries(groups).map(([key, val]) => ({
    name: key,
    value: val.count,
  }));

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">Failure Breakdown</h4>
      <p className="text-xs text-gray-500 mb-3">Expected → Actual status transitions</p>
      <ResponsiveContainer width="100%" height={chartData.length * 50 + 40}>
        <BarChart data={chartData} layout="vertical" margin={{ left: 130 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" />
          <YAxis type="category" dataKey="name" width={125} tick={{ fontSize: 10 }} />
          <Tooltip />
          <Bar dataKey="value" fill="#cf222e" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>

      <details className="mt-3">
        <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-700">
          Show detail ({failures.length} failures)
        </summary>
        <div className="mt-2 max-h-48 overflow-y-auto">
          <table className="w-full text-xs border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="text-left p-1 border">Case</th>
                <th className="text-left p-1 border">Expected</th>
                <th className="text-left p-1 border">Actual</th>
              </tr>
            </thead>
            <tbody>
              {failures.map((f, i) => (
                <tr key={i} className="border-b">
                  <td className="p-1 border font-mono text-[10px]">{f.case_id}</td>
                  <td className="p-1 border">{f.expected_status}</td>
                  <td className="p-1 border">{f.actual_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </div>
  );
}

function ReviewMetricsPanel({ metrics }) {
  if (!metrics) return null;
  const casesWithReviewers = metrics.cases_with_multiple_reviewers || 0;
  const agreement = metrics.percent_agreement;
  const kappa = metrics.cohens_kappa;

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">Reviewer Agreement</h4>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <span className="text-xs text-gray-500">Agreement</span>
          <div className="text-2xl font-bold" style={{ color: agreement != null && agreement >= 0.8 ? "#1a7f37" : "#e8a020" }}>
            {agreement != null ? `${(agreement * 100).toFixed(1)}%` : "N/A"}
          </div>
        </div>
        <div>
          <span className="text-xs text-gray-500">Cohen's κ</span>
          <div className="text-2xl font-bold" style={{ color: kappa != null && kappa >= 0.6 ? "#1a7f37" : kappa != null && kappa >= 0.4 ? "#e8a020" : "#cf222e" }}>
            {kappa != null ? kappa.toFixed(2) : "N/A"}
          </div>
        </div>
      </div>
      <p className="text-[10px] text-gray-400 mt-2">
        Multi-review cases: {casesWithReviewers} · Adjudication required: {metrics.adjudication_required}
      </p>
    </div>
  );
}

function EvidenceSourceChart({ counts }) {
  const evidenceData = [
    { name: "Candidate Evidence", value: counts?.candidate_evidence_cases || 0, color: "#8250df" },
    { name: "Live Lookups Attempted", value: counts?.live_external_lookup_attempted || 0, color: "#0969da" },
    { name: "Live Evidence Found", value: counts?.live_external_evidence_found || 0, color: "#1a7f37" },
  ].filter(d => d.value > 0);

  if (evidenceData.length === 0) return null;

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">Evidence Sources</h4>
      <ResponsiveContainer width="100%" height={160}>
        <BarChart data={evidenceData} margin={{ left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" tick={{ fontSize: 10 }} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" radius={[4, 4, 0, 0]}>
            {evidenceData.map((e, i) => <Cell key={i} fill={e.color} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function ReviewDecisionPie({ counts }) {
  const decisions = [
    { name: "Approved", value: counts?.approved_review_cases || 0, color: "#1a7f37" },
    { name: "Rejected", value: counts?.rejected_review_cases || 0, color: "#cf222e" },
    { name: "Edited", value: counts?.edited_review_cases || 0, color: "#0969da" },
  ].filter(d => d.value > 0);

  if (decisions.length === 0) return null;

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h4 className="text-sm font-bold text-gray-700 mb-3">Review Decisions</h4>
      <ResponsiveContainer width="100%" height={160}>
        <PieChart>
          <Pie data={decisions} cx="50%" cy="50%" innerRadius={35} outerRadius={65} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
            {decisions.map((d, i) => <Cell key={i} fill={d.color} />)}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function EvaluationDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [reviewMetrics, setReviewMetrics] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [history, setHistory] = useState([]);

  async function load() {
    setError("");
    setLoading(true);
    try {
      const r = await apiFetch("/benchmark");
      if (!r.ok) throw new Error(`API error ${r.status}`);
      const data = await r.json();
      setMetrics(data);
      setLastUpdated(new Date().toLocaleTimeString());

      // Append to history for trend view
      setHistory(prev => {
        const next = [...prev, {
          time: new Date().toLocaleTimeString(),
          accuracy: data.accuracy,
          coverage: data.coverage,
          reviewRate: data.review_rate,
        }];
        return next.slice(-10);
      });

      // Load review metrics
      try {
        const rm = await apiFetch("/review-queue-metrics");
        if (rm.ok) setReviewMetrics(await rm.json());
      } catch (_) { /* ignore */ }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  const isEmpty = !metrics;
  const statusCounts = metrics?.counts;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <span className="eyebrow">Quality monitoring</span>
          <h1 className="text-3xl font-bold text-gray-900 mt-1">Evaluation Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">
            Benchmark validation, reviewer agreement, and failure analysis for the curated MVP.
          </p>
        </div>
        <button
          onClick={load}
          disabled={loading}
          className="mt-0 px-5 py-2.5 bg-primary text-white rounded-lg text-sm font-bold hover:bg-primary-dark disabled:opacity-60 transition-colors"
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm mb-4">
          {error}
        </div>
      )}

      {isEmpty && loading && (
        <div className="text-center py-12 text-gray-400">Loading benchmark data...</div>
      )}

      {isEmpty && !loading && (
        <div className="text-center py-12 text-gray-400">
          No benchmark data loaded. Click "Refresh" to fetch from the API.
        </div>
      )}

      {metrics && (
        <>
          {/* KPI Row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <MetricCard
              label="Accuracy"
              value={pct(metrics.accuracy)}
              color={metrics.target_status?.accuracy ? "#1a7f37" : "#cf222e"}
              subtitle={`${metrics.counts?.full_correct} / ${metrics.total_cases} correct`}
            />
            <MetricCard
              label="Coverage"
              value={pct(metrics.coverage)}
              color={metrics.target_status?.coverage ? "#1a7f37" : "#cf222e"}
              subtitle={`${metrics.counts?.resolved} / ${metrics.total_cases} resolved`}
            />
            <MetricCard
              label="Review Rate"
              value={pct(metrics.review_rate)}
              color="#e8a020"
              subtitle={`${metrics.counts?.review_required} of ${metrics.total_cases} cases`}
            />
            <MetricCard
              label="Total Cases"
              value={metrics.total_cases}
              color="#028090"
            />
          </div>

          {/* Charts Row 1 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {statusCounts && <StatusPie data={statusCounts} />}
            <AccuracyGauge accuracy={metrics.accuracy} coverage={metrics.coverage} />
            <ReviewRateBar reviewRate={metrics.review_rate} />
          </div>

          {/* Charts Row 2 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <FalseAutoAcceptRate failures={metrics.failures} totalCases={metrics.total_cases} />
            {statusCounts && <EvidenceSourceChart counts={statusCounts} />}
          </div>

          {/* Charts Row 3 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {reviewMetrics && <ReviewMetricsPanel metrics={reviewMetrics} />}
            {statusCounts && <ReviewDecisionPie counts={statusCounts} />}
          </div>

          {/* Failure Breakdown */}
          <div className="mb-6">
            <FailureBreakdown failures={metrics.failures} />
          </div>

          {/* Trend chart (if history has enough data) */}
          {history.length >= 2 && (
            <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
              <h4 className="text-sm font-bold text-gray-700 mb-3">Trend (last {history.length} refreshes)</h4>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={history}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" tick={{ fontSize: 10 }} />
                  <YAxis domain={[0, 1]} tickFormatter={v => `${Math.round(v * 100)}%`} />
                  <Tooltip formatter={v => `${(v * 100).toFixed(1)}%`} />
                  <Legend />
                  <Line type="monotone" dataKey="accuracy" stroke="#1a7f37" name="Accuracy" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="coverage" stroke="#0969da" name="Coverage" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="reviewRate" stroke="#e8a020" name="Review Rate" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Footer info */}
          <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 text-xs text-gray-500">
            <p>Benchmark source: {metrics.benchmark_file}</p>
            <p>Status accuracy: {pct(metrics.status_accuracy)}</p>
            <p>Targets: accuracy ≥90% ({metrics.target_status?.accuracy ? "✓ met" : "✗ not met"}), coverage ≥95% ({metrics.target_status?.coverage ? "✓ met" : "✗ not met"})</p>
            {lastUpdated && <p className="mt-1">Last refreshed: {lastUpdated}</p>}
            <p className="mt-1">This is internal MVP validation, not independent clinical validation.</p>
          </div>
        </>
      )}
    </div>
  );
}
