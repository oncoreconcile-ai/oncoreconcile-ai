import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

function App() {
  const [form, setForm] = useState({
    cancer_type: "NSCLC",
    gene: "HER2",
    variant: "Amplification",
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function submitRecord() {
    setError("");
    setIsLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/reconcile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Failed to call backend API");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="container">
      <h1>OncoReconcile AI</h1>
      <p>Human-Governed Oncology Reconciliation Workbench</p>

      <section className="card">
        <h2>Manual Input</h2>

        <label>Cancer Type</label>
        <input
          value={form.cancer_type}
          onChange={(e) => setForm({ ...form, cancer_type: e.target.value })}
        />

        <label>Gene</label>
        <input
          value={form.gene}
          onChange={(e) => setForm({ ...form, gene: e.target.value })}
        />

        <label>Variant</label>
        <input
          value={form.variant}
          onChange={(e) => setForm({ ...form, variant: e.target.value })}
        />

        <button onClick={submitRecord} disabled={isLoading}>
          {isLoading ? "Reconciling..." : "Reconcile"}
        </button>
        {error && <p>{error}</p>}
      </section>

      {result && (
        <section className="card">
          <h2>Result</h2>
          <table>
            <tbody>
              <tr>
                <th>Canonical Cancer Type</th>
                <td>{result.canonical?.cancer_type || ""}</td>
              </tr>
              <tr>
                <th>Canonical Gene</th>
                <td>{result.canonical?.gene || ""}</td>
              </tr>
              <tr>
                <th>Canonical Variant</th>
                <td>{result.canonical?.variant || ""}</td>
              </tr>
              <tr>
                <th>Confidence</th>
                <td>{result.confidence}</td>
              </tr>
              <tr>
                <th>Review Status</th>
                <td>{result.review_status}</td>
              </tr>
              <tr>
                <th>Explanation</th>
                <td>{result.explanation}</td>
              </tr>
            </tbody>
          </table>
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
