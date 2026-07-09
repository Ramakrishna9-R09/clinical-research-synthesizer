from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.graph.workflow import describe_graph, run_workflow
from app.guardrails.hallucination_detector import estimate_hallucination_risk

app = FastAPI(title="Clinical Research Synthesizer", version="0.1.0")


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    require_human_approval: bool = False
    approved: bool = True


@app.get("/", response_class=HTMLResponse)
def ui() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Clinical Research Synthesizer</title>
  <style>
    :root { color-scheme: light; --ink:#17202a; --muted:#5d6d7e; --line:#d7dde5; --brand:#0f766e; --bg:#f7f9fb; --panel:#ffffff; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Arial, sans-serif; background:var(--bg); color:var(--ink); }
    header { background:#0b3b3f; color:white; padding:28px 24px; }
    main { max-width:1120px; margin:0 auto; padding:24px; }
    h1 { margin:0 0 8px; font-size:30px; font-weight:750; letter-spacing:0; }
    h2 { margin:0 0 14px; font-size:18px; }
    p { line-height:1.55; }
    .sub { margin:0; color:#c7f3ed; max-width:860px; }
    .grid { display:grid; grid-template-columns: minmax(0, 1fr) 360px; gap:20px; align-items:start; }
    .panel { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:18px; box-shadow:0 1px 2px rgba(20,30,40,.04); }
    textarea { width:100%; min-height:132px; resize:vertical; border:1px solid var(--line); border-radius:6px; padding:12px; font:inherit; line-height:1.45; }
    button { display:inline-flex; align-items:center; justify-content:center; min-height:42px; padding:0 16px; border:0; border-radius:6px; background:var(--brand); color:white; font-weight:700; cursor:pointer; }
    button:disabled { opacity:.65; cursor:wait; }
    .row { display:flex; gap:10px; align-items:center; margin-top:12px; flex-wrap:wrap; }
    .metric { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
    .metric div { border:1px solid var(--line); border-radius:8px; padding:12px; background:#fbfcfd; }
    .metric strong { display:block; font-size:22px; margin-top:4px; }
    .muted { color:var(--muted); font-size:14px; }
    .result { white-space:pre-wrap; line-height:1.5; }
    table { width:100%; border-collapse:collapse; font-size:14px; }
    th, td { text-align:left; border-bottom:1px solid var(--line); padding:9px 7px; vertical-align:top; }
    th { color:var(--muted); font-size:12px; text-transform:uppercase; }
    code { background:#edf2f7; padding:2px 5px; border-radius:4px; }
    .status { margin-top:12px; color:var(--muted); }
    .error { color:#b42318; }
    @media (max-width: 860px) { .grid { grid-template-columns:1fr; } header { padding:22px 18px; } main { padding:18px; } }
  </style>
</head>
<body>
  <header>
    <h1>Clinical Research Synthesizer</h1>
    <p class="sub">Multi-agent clinical evidence synthesis with retrieval, adversarial review, adjudication, citations, and verification.</p>
  </header>
  <main>
    <div class="grid">
      <section class="panel">
        <h2>Run Evidence Synthesis</h2>
        <textarea id="question">Should eligible adults with heart failure receive an SGLT2 inhibitor?</textarea>
        <div class="row">
          <button id="run">Run synthesis</button>
          <span id="status" class="status">Ready</span>
        </div>
      </section>
      <aside class="panel">
        <h2>API</h2>
        <p class="muted">The backend is live on the same deployment.</p>
        <p><a href="/docs">Open API docs</a></p>
        <p><code>POST /query</code></p>
      </aside>
    </div>
    <section class="panel" style="margin-top:20px;">
      <h2>Output</h2>
      <div class="metric">
        <div><span class="muted">Confidence</span><strong id="confidence">-</strong></div>
        <div><span class="muted">Verification</span><strong id="verification">-</strong></div>
      </div>
      <h2 style="margin-top:18px;">Final Answer</h2>
      <div id="answer" class="result muted">Run a query to generate a clinical synthesis.</div>
      <h2 style="margin-top:18px;">Citations</h2>
      <div id="citations" class="muted">No citations yet.</div>
      <h2 style="margin-top:18px;">Audit Trail</h2>
      <pre id="audit" class="result muted">No audit trail yet.</pre>
    </section>
  </main>
  <script>
    const run = document.getElementById("run");
    const statusEl = document.getElementById("status");
    run.addEventListener("click", async () => {
      run.disabled = true;
      statusEl.textContent = "Running agents...";
      statusEl.className = "status";
      try {
        const response = await fetch("/query", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: document.getElementById("question").value })
        });
        if (!response.ok) throw new Error(await response.text());
        const data = await response.json();
        document.getElementById("confidence").textContent = data.confidence ?? "-";
        document.getElementById("verification").textContent = data.verification?.is_verified ? "Verified" : "Warnings";
        document.getElementById("answer").textContent = data.answer || "No answer returned.";
        document.getElementById("answer").className = "result";
        document.getElementById("audit").textContent = JSON.stringify(data.audit_log || [], null, 2);
        document.getElementById("audit").className = "result";
        document.getElementById("citations").innerHTML = renderCitations(data.citations || []);
        statusEl.textContent = "Complete";
      } catch (error) {
        statusEl.textContent = "Request failed";
        statusEl.className = "status error";
        document.getElementById("answer").textContent = String(error);
      } finally {
        run.disabled = false;
      }
    });
    function renderCitations(items) {
      if (!items.length) return "<p class='muted'>No citations returned.</p>";
      return `<table><thead><tr><th>ID</th><th>Title</th><th>Design</th><th>Year</th></tr></thead><tbody>${items.map(item => `
        <tr><td>${escapeHtml(item.citation_id)}</td><td>${escapeHtml(item.title)}</td><td>${escapeHtml(item.study_design)}</td><td>${escapeHtml(item.publication_year ?? "")}</td></tr>
      `).join("")}</tbody></table>`;
    }
    function escapeHtml(value) {
      return String(value ?? "").replace(/[&<>"']/g, char => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;" }[char]));
    }
  </script>
</body>
</html>
"""


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/graph")
def graph() -> dict:
    return describe_graph()


@app.post("/query")
def query(request: QueryRequest) -> dict:
    state = run_workflow(
        request.question,
        require_human_approval=request.require_human_approval,
        approved=request.approved,
    )
    final_report = state.get("final_report", {})
    risk = estimate_hallucination_risk(final_report.get("answer", ""), final_report.get("citations", []))
    return {
        "query": request.question,
        "answer": final_report.get("answer"),
        "confidence": final_report.get("confidence"),
        "citations": final_report.get("citations", []),
        "contradictory_evidence": final_report.get("contradictory_evidence", []),
        "verification": final_report.get("verification"),
        "hallucination_risk": risk,
        "report_path": final_report.get("report_path"),
        "audit_log": state.get("audit_log", []),
        "report_markdown": final_report.get("report_markdown"),
    }
