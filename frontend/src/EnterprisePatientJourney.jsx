import React, { useState, useEffect } from "react";
import { apiFetch } from "./api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from "recharts";

const STATUS_COLORS = { AUTO_RECONCILE: "#1a7f37", REVIEW_REQUIRED: "#e8a020", CANNOT_RECONCILE: "#cf222e" };
const CANCER_COLORS = { "Non-Small Cell Lung Cancer": "#0369a1", "Breast Cancer": "#d946ef", "Colorectal Cancer": "#d97706", "Melanoma": "#7c3aed", "Acute Myeloid Leukemia": "#dc2626" };

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

function Timeline({ events }) {
  if (!events?.length) return <p className="text-gray-400 text-sm">No timeline events.</p>;
  return (
    <div className="relative pl-6 border-l-2 border-primary-light">
      {events.map((evt, i) => (
        <div key={i} className="mb-6 relative">
          <div className={`absolute -left-[25px] w-4 h-4 rounded-full border-2 ${
            evt.event_type === "diagnosis" ? "bg-blue-500 border-blue-500" :
            evt.event_type === "biomarker_test" ? "bg-purple-400 border-purple-400" :
            evt.event_type === "treatment" ? "bg-green-500 border-green-500" :
            evt.event_type === "response" ? "bg-amber-400 border-amber-400" :
            evt.event_type === "progression" ? "bg-red-500 border-red-500" :
            "bg-gray-300 border-gray-300"
          }`} />
          <div className="bg-white p-3 rounded-lg border border-gray-200 shadow-sm">
            <div className="flex justify-between items-start gap-2">
              <span className="text-xs font-bold text-gray-500">{evt.date}</span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                evt.event_type === "diagnosis" ? "bg-blue-100 text-blue-700" :
                evt.event_type === "biomarker_test" ? "bg-purple-100 text-purple-700" :
                evt.event_type === "treatment" ? "bg-green-100 text-green-700" :
                evt.event_type === "response" ? "bg-amber-100 text-amber-700" :
                evt.event_type === "progression" ? "bg-red-100 text-red-700" :
                "bg-gray-100 text-gray-700"
              }`}>{evt.event_type}</span>
            </div>
            <p className="font-bold text-sm mt-1">{evt.title}</p>
            {evt.description && <p className="text-xs text-gray-500 mt-0.5">{evt.description}</p>}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function EnterprisePatientJourney() {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { loadPatients(); }, []);

  async function loadPatients() {
    setLoading(true);
    try {
      const r = await apiFetch("/enterprise/patient-journey");
      const data = await r.json();
      setPatients(data.patients || []);
      if (data.patients?.length > 0) loadDetail(data.patients[0].patient_id);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  }

  async function loadDetail(pid) {
    setDetailLoading(true);
    setError("");
    try {
      const r = await apiFetch(`/enterprise/patient-journey/${pid}`);
      if (!r.ok) { setError(`Patient ${pid} not found`); setSelectedPatient(null); return; }
      setSelectedPatient(await r.json());
    } catch (e) { setError(e.message); }
    finally { setDetailLoading(false); }
  }

  return (
    <div>
      <div className="mb-6">
        <span className="eyebrow">Enterprise Platform</span>
        <h1 className="text-3xl font-bold text-gray-900 mt-1">Patient Journey</h1>
        <p className="text-sm text-gray-500 mt-1">Longitudinal oncology patient journeys with semantic harmonization and coding system mappings.</p>
      </div>

      {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm mb-4">{error}</div>}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-6">
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl border border-gray-200 p-4">
            <h3 className="text-sm font-bold text-gray-700 mb-3">Patients ({patients.length})</h3>
            {loading && <p className="text-gray-400 text-sm">Loading...</p>}
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {patients.map(p => (
                <button key={p.patient_id} onClick={() => loadDetail(p.patient_id)}
                  className={`w-full text-left p-3 rounded-lg border text-sm transition-colors ${
                    selectedPatient?.patient?.patient_id === p.patient_id
                      ? "bg-primary text-white border-primary"
                      : "bg-gray-50 border-gray-200 hover:bg-gray-100"
                  }`}>
                  <div className="font-bold">{p.patient_id}</div>
                  <div className="text-xs opacity-80">{p.diagnosis} · {p.stage}</div>
                  <div className="text-xs opacity-70 mt-1">{p.sex} · {p.age_group}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-3">
          {detailLoading && <p className="text-gray-400">Loading patient details...</p>}
          {!detailLoading && !selectedPatient && <p className="text-gray-400 text-center py-12">Select a patient to view journey.</p>}
          {!detailLoading && selectedPatient && (
            <div className="space-y-4">
              {/* Patient Hero */}
              <div className="bg-white rounded-xl border-2 border-primary p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-xs font-bold text-primary uppercase tracking-wider">Patient Summary</span>
                    <h2 className="text-2xl font-bold mt-1">{selectedPatient.patient.patient_id}</h2>
                    <p className="text-gray-600 mt-1">{selectedPatient.patient.diagnosis} · {selectedPatient.patient.histology} · Stage {selectedPatient.patient.stage}</p>
                  </div>
                  <div className="text-right">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                      selectedPatient.patient.reconciliation_status === "AUTO_RECONCILE" ? "bg-green-100 text-green-800" :
                      selectedPatient.patient.reconciliation_status === "REVIEW_REQUIRED" ? "bg-amber-100 text-amber-800" : "bg-red-100 text-red-800"
                    }`}>{selectedPatient.patient.reconciliation_status}</span>
                  </div>
                </div>
                <div className="grid grid-cols-4 gap-4 mt-4">
                  <div><span className="text-xs text-gray-500">Sex</span><p className="font-bold">{selectedPatient.patient.sex}</p></div>
                  <div><span className="text-xs text-gray-500">Age Group</span><p className="font-bold">{selectedPatient.patient.age_group}</p></div>
                  <div><span className="text-xs text-gray-500">Line of Therapy</span><p className="font-bold">{selectedPatient.patient.line_of_therapy}</p></div>
                  <div><span className="text-xs text-gray-500">Data Quality</span><p className="font-bold">{pct(selectedPatient.patient.data_quality_score)}</p></div>
                </div>
              </div>

              {/* Genes and Variants */}
              <div className="bg-white rounded-xl border border-gray-200 p-4">
                <h3 className="text-sm font-bold text-gray-700 mb-3">Biomarkers & Genomic Findings</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="text-xs text-gray-500 font-bold uppercase mb-2">Variants</h4>
                    {selectedPatient.patient.variants?.map((v, i) => (
                      <div key={i} className="bg-gray-50 rounded-lg p-3 mb-2 border border-gray-100">
                        <div className="font-bold text-sm">{v.gene} {v.variant}</div>
                        <div className="text-xs text-gray-500">{v.classification} · AF: {v.allele_frequency || 'N/A'}</div>
                      </div>
                    ))}
                    {selectedPatient.patient.fusions?.map((f, i) => (
                      <div key={`f${i}`} className="bg-purple-50 rounded-lg p-3 mb-2 border border-purple-100">
                        <div className="font-bold text-sm">Fusion: {f.fusion}</div>
                        <div className="text-xs text-gray-500">{f.type} · {f.functional_class}</div>
                      </div>
                    ))}
                  </div>
                  <div>
                    <h4 className="text-xs text-gray-500 font-bold uppercase mb-2">Copy Number Alterations</h4>
                    {selectedPatient.patient.copy_number_alterations?.map((c, i) => (
                      <div key={i} className="bg-orange-50 rounded-lg p-3 mb-2 border border-orange-100">
                        <div className="font-bold text-sm">{c.gene} {c.alteration}</div>
                        <div className="text-xs text-gray-500">CN: {c.copy_number || "N/A"}</div>
                      </div>
                    ))}
                    {(!selectedPatient.patient.copy_number_alterations?.length) && <p className="text-xs text-gray-400">None detected</p>}
                  </div>
                </div>
              </div>

              {/* Timeline */}
              <div className="bg-white rounded-xl border border-gray-200 p-4">
                <h3 className="text-sm font-bold text-gray-700 mb-3">Treatment Timeline</h3>
                <Timeline events={selectedPatient.journey_timeline} />
              </div>

              {/* Semantic Harmonization */}
              {selectedPatient.harmonization && (
                <div className="bg-white rounded-xl border border-gray-200 p-4">
                  <h3 className="text-sm font-bold text-gray-700 mb-3">Semantic Harmonization</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-xs text-gray-500 font-bold uppercase mb-2">Disease</h4>
                      <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                        <div className="text-sm"><span className="text-gray-500">Original:</span> <strong>{selectedPatient.harmonization.disease.original}</strong></div>
                        <div className="text-sm"><span className="text-gray-500">Canonical:</span> <strong>{selectedPatient.harmonization.disease.canonical_value}</strong></div>
                        <div className="text-xs text-gray-500 mt-1">Confidence: {pct(selectedPatient.harmonization.disease.confidence)}</div>
                        {selectedPatient.harmonization.disease.mappings?.slice(0, 3).map((m, i) => (
                          <div key={i} className="text-xs text-gray-600 mt-1">
                            {m.coding_system}: {m.code} ({m.display_name})
                          </div>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="text-xs text-gray-500 font-bold uppercase mb-2">Genes</h4>
                      {selectedPatient.harmonization.genes?.map((g, i) => (
                        <div key={i} className="bg-gray-50 rounded-lg p-2 mb-2 border border-gray-100">
                          <div className="text-xs">{g.original} → <strong>{g.canonical_value}</strong></div>
                          <div className="text-[10px] text-gray-400">{g.hgnc_id} · {g.hgnc_name}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Clinical Trials */}
              <div className="bg-white rounded-xl border border-gray-200 p-4">
                <h3 className="text-sm font-bold text-gray-700 mb-3">Clinical Trial Eligibility</h3>
                {selectedPatient.patient.clinical_trial_flags?.map((flag, i) => (
                  <div key={i} className="bg-green-50 rounded-lg p-3 mb-2 border border-green-100 text-sm">
                    🧪 {flag}
                  </div>
                ))}
              </div>

              {/* Treatment History */}
              <div className="bg-white rounded-xl border border-gray-200 p-4">
                <h3 className="text-sm font-bold text-gray-700 mb-3">Treatment History</h3>
                <div className="space-y-2">
                  {selectedPatient.patient.treatments?.map((tx, i) => (
                    <div key={i} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg border border-gray-100">
                      <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-bold text-xs">{tx.line_of_therapy}</div>
                      <div className="flex-1">
                        <div className="font-bold text-sm">{tx.drug}</div>
                        <div className="text-xs text-gray-500">{tx.class} · {tx.regimen}</div>
                      </div>
                      <div className="text-xs text-gray-400 text-right">
                        <div>Start: {tx.start_date}</div>
                        {tx.end_date && <div>End: {tx.end_date}</div>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Progression Events */}
              {selectedPatient.patient.progression_events?.length > 0 && (
                <div className="bg-white rounded-xl border-2 border-red-200 p-4">
                  <h3 className="text-sm font-bold text-red-700 mb-3">Progression Events</h3>
                  {selectedPatient.patient.progression_events.map((pe, i) => (
                    <div key={i} className="bg-red-50 rounded-lg p-3 mb-2 border border-red-100">
                      <div className="font-bold text-sm">{pe.event}</div>
                      <div className="text-xs text-gray-500">{pe.type} · {pe.date}</div>
                      {pe.notes && <div className="text-xs text-gray-600 mt-1">{pe.notes}</div>}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
