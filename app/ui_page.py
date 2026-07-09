def render_ui() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#102b3c" />
  <title>Clinical Research Synthesizer</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4f7f9;
      --surface: #ffffff;
      --surface-2: #eef4f6;
      --ink: #15232f;
      --muted: #647482;
      --line: #d8e1e6;
      --line-strong: #b8c8d1;
      --nav: #102b3c;
      --nav-2: #173d50;
      --teal: #0f766e;
      --teal-2: #dff3ef;
      --blue: #245b9b;
      --amber: #9a5b13;
      --red: #b42318;
      --green: #166534;
      --shadow: 0 14px 35px rgba(16, 43, 60, .10);
    }
    * { box-sizing: border-box; }
    html { min-width: 320px; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      background: var(--bg);
      color: var(--ink);
      letter-spacing: 0;
    }
    a { color: inherit; }
    .shell { min-height: 100vh; display: grid; grid-template-columns: 280px minmax(0, 1fr); }
    .sidebar {
      position: sticky;
      top: 0;
      height: 100vh;
      background: var(--nav);
      color: #f6fbfc;
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .brand { display: flex; gap: 12px; align-items: center; }
    .brand-mark {
      width: 42px;
      height: 42px;
      border-radius: 8px;
      background: #dff3ef;
      color: var(--nav);
      display: grid;
      place-items: center;
      font-weight: 800;
      font-size: 17px;
    }
    .brand h1 { margin: 0; font-size: 17px; line-height: 1.2; }
    .brand span { display: block; color: #b9d6dc; font-size: 12px; margin-top: 2px; }
    .nav-group { border-top: 1px solid rgba(255,255,255,.14); padding-top: 14px; display: grid; gap: 9px; }
    .nav-link {
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 10px;
      border-radius: 7px;
      color: #d9e8eb;
      text-decoration: none;
      font-size: 14px;
      background: rgba(255,255,255,.04);
    }
    .nav-link strong { color: white; font-weight: 700; }
    .side-note {
      margin-top: auto;
      border: 1px solid rgba(255,255,255,.14);
      border-radius: 8px;
      padding: 13px;
      background: var(--nav-2);
      color: #d7e9ed;
      font-size: 13px;
      line-height: 1.45;
    }
    .main { min-width: 0; }
    .topbar {
      min-height: 68px;
      background: rgba(255,255,255,.86);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 28px;
      position: sticky;
      top: 0;
      z-index: 5;
    }
    .topbar-title { display: grid; gap: 2px; }
    .topbar-title strong { font-size: 15px; }
    .topbar-title span { color: var(--muted); font-size: 13px; }
    .top-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }
    .container { max-width: 1380px; margin: 0 auto; padding: 24px 28px 38px; }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 390px;
      gap: 18px;
      align-items: stretch;
      margin-bottom: 18px;
    }
    .hero-copy {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 24px;
      box-shadow: var(--shadow);
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      padding: 0 10px;
      border-radius: 999px;
      background: var(--teal-2);
      color: #0a5c55;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }
    h2 { margin: 0; font-size: 15px; }
    .hero h2 { margin: 14px 0 8px; font-size: 32px; line-height: 1.1; max-width: 850px; }
    .hero p { color: var(--muted); line-height: 1.58; margin: 0; max-width: 880px; }
    .hero-metrics {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 20px;
    }
    .mini-metric {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px;
      background: #fbfdfe;
      min-height: 82px;
    }
    .mini-metric span { color: var(--muted); font-size: 12px; text-transform: uppercase; font-weight: 800; }
    .mini-metric strong { display: block; margin-top: 8px; font-size: 21px; }
    .workflow-card {
      background: var(--nav);
      color: white;
      border-radius: 8px;
      padding: 20px;
      box-shadow: var(--shadow);
      display: grid;
      align-content: space-between;
      gap: 18px;
      min-height: 260px;
    }
    .workflow-card h2 { font-size: 18px; }
    .agent-rail { display: grid; gap: 10px; }
    .agent-node {
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr);
      gap: 10px;
      align-items: center;
      min-height: 44px;
      padding: 8px;
      border-radius: 7px;
      background: rgba(255,255,255,.08);
    }
    .agent-node span {
      width: 34px;
      height: 34px;
      border-radius: 7px;
      display: grid;
      place-items: center;
      background: rgba(223,243,239,.16);
      color: #dff3ef;
      font-weight: 800;
      font-size: 12px;
    }
    .agent-node strong { display: block; font-size: 14px; }
    .agent-node small { color: #bdd6dc; }
    .workspace { display: grid; grid-template-columns: 430px minmax(0, 1fr); gap: 18px; align-items: start; }
    .panel {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(16, 43, 60, .04);
      overflow: hidden;
    }
    .panel-head {
      min-height: 54px;
      padding: 15px 17px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .panel-body { padding: 17px; }
    .query-box { display: grid; gap: 12px; }
    label { font-size: 13px; color: var(--muted); font-weight: 700; }
    textarea {
      width: 100%;
      min-height: 190px;
      resize: vertical;
      border: 1px solid var(--line-strong);
      border-radius: 8px;
      padding: 13px;
      font: inherit;
      line-height: 1.45;
      color: var(--ink);
      outline: none;
    }
    textarea:focus { border-color: var(--teal); box-shadow: 0 0 0 3px rgba(15, 118, 110, .12); }
    .button-row { display: grid; gap: 10px; }
    .primary, .secondary, .ghost, .tab {
      border: 0;
      border-radius: 7px;
      min-height: 42px;
      padding: 0 14px;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
      letter-spacing: 0;
    }
    .primary { background: var(--teal); color: white; }
    .primary:disabled { opacity: .7; cursor: wait; }
    .secondary { background: #e8f3f1; color: #0a5c55; border: 1px solid #b6d8d2; text-align: left; }
    .ghost { background: #f3f6f8; color: var(--ink); border: 1px solid var(--line); }
    .button-grid { display: grid; grid-template-columns: 1fr; gap: 8px; }
    .control-grid { display: grid; gap: 12px; }
    .mode-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .mode-card {
      min-height: 64px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fbfc;
      padding: 10px;
      text-align: left;
      cursor: pointer;
      color: var(--ink);
    }
    .mode-card strong { display: block; font-size: 13px; margin-bottom: 4px; }
    .mode-card span { display: block; color: var(--muted); font-size: 12px; line-height: 1.35; }
    .mode-card.active { border-color: var(--teal); background: var(--teal-2); box-shadow: 0 0 0 3px rgba(15, 118, 110, .10); }
    .scope-row { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 10px; align-items: center; }
    input[type="range"] { width: 100%; accent-color: var(--teal); }
    .toggle {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      user-select: none;
    }
    .toggle input { width: 16px; height: 16px; accent-color: var(--teal); }
    .status-line {
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      border-radius: 8px;
      background: var(--surface-2);
      padding: 0 12px;
      color: var(--muted);
      font-size: 13px;
    }
    .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--muted); display: inline-block; margin-right: 8px; }
    .dot.live { background: var(--green); }
    .dot.busy { background: var(--amber); }
    .dot.error { background: var(--red); }
    .metrics { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-bottom: 14px; }
    .metric {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px;
      min-height: 84px;
    }
    .metric span { color: var(--muted); font-size: 12px; font-weight: 800; text-transform: uppercase; }
    .metric strong { display: block; margin-top: 8px; font-size: 22px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .tabs { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
    .tab { background: #e9eef2; color: #334552; border: 1px solid var(--line); min-height: 38px; }
    .tab.active { background: var(--nav); color: white; border-color: var(--nav); }
    .result-grid { display: grid; gap: 14px; }
    .answer-box {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: #fbfdfe;
      line-height: 1.6;
      min-height: 118px;
      white-space: pre-wrap;
    }
    .empty { color: var(--muted); }
    .factor-grid, .citation-grid, .trace-grid { display: grid; gap: 10px; }
    .factor, .citation, .trace-item {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px;
      background: white;
    }
    .factor { display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 12px; align-items: start; }
    .factor strong, .citation strong, .trace-item strong { display: block; margin-bottom: 5px; }
    .factor span, .citation span, .trace-item span { color: var(--muted); font-size: 13px; line-height: 1.45; }
    .citation-head { display: flex; justify-content: space-between; gap: 12px; align-items: start; margin-bottom: 8px; }
    .citation-id {
      min-width: 38px;
      min-height: 28px;
      border-radius: 999px;
      background: var(--teal-2);
      color: #0a5c55;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 12px;
    }
    .chip-row { display: flex; gap: 7px; flex-wrap: wrap; margin-top: 8px; }
    .chip {
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      padding: 0 9px;
      border-radius: 999px;
      background: #eef3f6;
      color: #445663;
      font-size: 12px;
      font-weight: 700;
    }
    .risk-low { color: var(--green); }
    .risk-medium { color: var(--amber); }
    .risk-high { color: var(--red); }
    pre {
      margin: 0;
      white-space: pre-wrap;
      line-height: 1.52;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 13px;
      color: #243444;
    }
    .hidden { display: none; }
    .footer-note { color: var(--muted); font-size: 12px; line-height: 1.45; margin-top: 14px; }
    @media (max-width: 1120px) {
      .shell { grid-template-columns: 1fr; }
      .sidebar { position: static; height: auto; }
      .side-note { margin-top: 0; }
      .hero, .workspace { grid-template-columns: 1fr; }
    }
    @media (max-width: 760px) {
      .topbar { align-items: flex-start; padding: 14px 18px; flex-direction: column; }
      .container { padding: 18px; }
      .hero h2 { font-size: 26px; }
      .hero-metrics, .metrics { grid-template-columns: 1fr 1fr; }
      .factor { grid-template-columns: 1fr; }
    }
    @media (max-width: 480px) {
      .hero-metrics, .metrics { grid-template-columns: 1fr; }
      .sidebar { padding: 18px; }
      .hero-copy, .panel-body { padding: 15px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">CR</div>
        <div>
          <h1>Clinical Research Synthesizer</h1>
          <span>Agentic RAG portfolio system</span>
        </div>
      </div>
      <div class="nav-group">
        <a class="nav-link" href="/docs"><strong>OpenAPI</strong><span>/docs</span></a>
        <a class="nav-link" href="/graph"><strong>Agent Graph</strong><span>/graph</span></a>
        <a class="nav-link" href="/examples"><strong>Examples</strong><span>/examples</span></a>
        <a class="nav-link" href="https://github.com/Ramakrishna9-R09/clinical-research-synthesizer"><strong>GitHub</strong><span>repo</span></a>
      </div>
      <div class="nav-group">
        <div class="agent-node"><span>01</span><div><strong>Drafter</strong><small>retrieves and cites evidence</small></div></div>
        <div class="agent-node"><span>02</span><div><strong>Critic</strong><small>hunts for contradictions</small></div></div>
        <div class="agent-node"><span>03</span><div><strong>Adjudicator</strong><small>weighs evidence quality</small></div></div>
      </div>
      <div class="side-note">
        Portfolio focus: multi-agent RAG, retrieval, guardrails, confidence scoring, auditability, API delivery, and deployment.
      </div>
    </aside>
    <main class="main">
      <div class="topbar">
        <div class="topbar-title">
          <strong>Production Evidence Workspace</strong>
          <span>Live FastAPI deployment with browser UI and structured JSON output</span>
        </div>
        <div class="top-actions">
          <button class="ghost" id="sample-monitor">Monitoring Query</button>
          <button class="ghost" id="sample-conflict">Conflict Query</button>
        </div>
      </div>
      <div class="container">
        <section class="hero">
          <div class="hero-copy">
            <span class="eyebrow">Clinical multi-agent RAG</span>
            <h2>Evidence synthesis that shows retrieval, critique, adjudication, and verification in one workflow.</h2>
            <p>
              This interface is built for portfolio review: it exposes the answer, source quality, contradiction review,
              agent trace, latency, and final report instead of hiding the system behind a chatbot box.
            </p>
            <div class="hero-metrics">
              <div class="mini-metric"><span>Modes</span><strong>5 workflows</strong></div>
              <div class="mini-metric"><span>Guardrail</span><strong>Citation check</strong></div>
              <div class="mini-metric"><span>Evidence</span><strong>All matching</strong></div>
              <div class="mini-metric"><span>Deploy</span><strong>Vercel API</strong></div>
            </div>
          </div>
          <div class="workflow-card">
            <h2>Current Run</h2>
            <div class="agent-rail" id="agent-rail">
              <div class="agent-node"><span id="stage-drafter">--</span><div><strong>Drafter</strong><small id="copy-drafter">Waiting for query</small></div></div>
              <div class="agent-node"><span id="stage-critic">--</span><div><strong>Critic</strong><small id="copy-critic">Waiting for evidence</small></div></div>
              <div class="agent-node"><span id="stage-adjudicator">--</span><div><strong>Adjudicator</strong><small id="copy-adjudicator">Waiting for review</small></div></div>
            </div>
            <div class="status-line"><span><i class="dot live" id="status-dot"></i><span id="status">Ready</span></span><span id="run-id">No run yet</span></div>
          </div>
        </section>

        <section class="workspace">
          <div class="panel">
            <div class="panel-head">
              <h2>Clinical Question</h2>
              <span class="chip">POST /query</span>
            </div>
            <div class="panel-body">
              <div class="query-box">
                <label for="question">Question</label>
                <textarea id="question">Should eligible adults with heart failure receive an SGLT2 inhibitor?</textarea>
                <div class="control-grid">
                  <label>Analysis mode</label>
                  <div class="mode-grid" id="mode-grid">
                    <button class="mode-card active" type="button" data-mode="auto"><strong>Auto triage</strong><span>Detect intent and route evidence.</span></button>
                    <button class="mode-card" type="button" data-mode="monitoring"><strong>Monitoring</strong><span>Follow-up, warning signs, labs.</span></button>
                    <button class="mode-card" type="button" data-mode="conflict"><strong>Conflict review</strong><span>Challenge the first answer.</span></button>
                    <button class="mode-card" type="button" data-mode="safety"><strong>Safety/Risk</strong><span>Red flags and contraindications.</span></button>
                    <button class="mode-card" type="button" data-mode="evidence_map"><strong>Evidence map</strong><span>Broad source landscape.</span></button>
                  </div>
                  <label for="evidence-limit">Evidence scope: <span id="evidence-label">12 sources</span></label>
                  <div class="scope-row">
                    <input id="evidence-limit" type="range" min="3" max="100" step="1" value="12" />
                    <label class="toggle"><input id="all-evidence" type="checkbox" checked /> All matching</label>
                  </div>
                </div>
                <div class="button-row">
                  <button class="primary" id="run">Run multi-agent synthesis</button>
                  <div class="button-grid">
                    <button class="secondary example" data-mode="monitoring" data-q="What should clinicians monitor after starting an SGLT2 inhibitor?">Use monitoring example</button>
                    <button class="secondary example" data-mode="conflict" data-q="Does one ketoacidosis case report outweigh randomized heart failure trial evidence?">Use conflict example</button>
                    <button class="secondary example" data-mode="safety" data-q="Does running cause heart attacks?">Use running cardiac-risk example</button>
                    <button class="secondary example" data-mode="evidence_map" data-q="What does the evidence say about SGLT2 inhibitor safety tradeoffs in heart failure?">Use evidence-map example</button>
                  </div>
                </div>
                <p class="footer-note">
                  Built-in demo data is synthetic and public. Local mode can ingest PDFs, Markdown, and text files from the repository data folder.
                </p>
              </div>
            </div>
          </div>

          <div>
            <div class="metrics">
              <div class="metric"><span>Confidence</span><strong id="confidence">--</strong></div>
              <div class="metric"><span>Evidence Grade</span><strong id="grade">--</strong></div>
              <div class="metric"><span>Verification</span><strong id="verification">--</strong></div>
              <div class="metric"><span>Latency</span><strong id="latency">--</strong></div>
              <div class="metric"><span>Evidence Count</span><strong id="evidence-count">--</strong></div>
              <div class="metric"><span>Mode</span><strong id="mode-readout">Auto</strong></div>
            </div>
            <div class="panel">
              <div class="panel-head">
                <h2>Clinical Output</h2>
                <span class="chip" id="risk-chip">Risk pending</span>
              </div>
              <div class="panel-body">
                <div class="tabs">
                  <button class="tab active" data-tab="summary">Summary</button>
                  <button class="tab" data-tab="evidence">Evidence</button>
                  <button class="tab" data-tab="conflicts">Conflicts</button>
                  <button class="tab" data-tab="trace">Trace</button>
                  <button class="tab" data-tab="report">Report</button>
                </div>
                <div id="summary" class="tab-panel result-grid">
                  <div class="answer-box empty" id="answer">Run a query to generate a clinical synthesis.</div>
                  <div class="factor-grid" id="factors"></div>
                </div>
                <div id="evidence" class="tab-panel hidden">
                  <div class="citation-grid" id="citations"><div class="answer-box empty">No citations yet.</div></div>
                </div>
                <div id="conflicts" class="tab-panel hidden">
                  <div class="citation-grid" id="contradictions"><div class="answer-box empty">No contradictory evidence yet.</div></div>
                </div>
                <div id="trace" class="tab-panel hidden">
                  <div class="trace-grid" id="audit"><div class="answer-box empty">No audit trail yet.</div></div>
                </div>
                <div id="report" class="tab-panel hidden">
                  <div class="answer-box"><pre id="markdown">No report yet.</pre></div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
  <script>
    const run = document.getElementById("run");
    const statusEl = document.getElementById("status");
    const statusDot = document.getElementById("status-dot");
    const question = document.getElementById("question");
    let selectedMode = "auto";
    const evidenceLimit = document.getElementById("evidence-limit");
    const evidenceLabel = document.getElementById("evidence-label");
    const allEvidence = document.getElementById("all-evidence");
    const stageMap = {
      drafter: document.getElementById("stage-drafter"),
      critic: document.getElementById("stage-critic"),
      adjudicator: document.getElementById("stage-adjudicator")
    };
    const copyMap = {
      drafter: document.getElementById("copy-drafter"),
      critic: document.getElementById("copy-critic"),
      adjudicator: document.getElementById("copy-adjudicator")
    };
    document.querySelectorAll(".example").forEach(button => {
      button.addEventListener("click", () => {
        question.value = button.dataset.q;
        chooseMode(button.dataset.mode || "auto");
        question.focus();
      });
    });
    document.querySelectorAll(".mode-card").forEach(button => {
      button.addEventListener("click", () => chooseMode(button.dataset.mode));
    });
    evidenceLimit.addEventListener("input", updateEvidenceLabel);
    allEvidence.addEventListener("change", updateEvidenceLabel);
    updateEvidenceLabel();
    document.getElementById("sample-monitor").addEventListener("click", () => {
      question.value = "What should clinicians monitor after starting an SGLT2 inhibitor?";
      chooseMode("monitoring");
      run.click();
    });
    document.getElementById("sample-conflict").addEventListener("click", () => {
      question.value = "Does one ketoacidosis case report outweigh randomized heart failure trial evidence?";
      chooseMode("conflict");
      run.click();
    });
    document.querySelectorAll(".tab").forEach(button => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
        document.querySelectorAll(".tab-panel").forEach(panel => panel.classList.add("hidden"));
        button.classList.add("active");
        document.getElementById(button.dataset.tab).classList.remove("hidden");
      });
    });
    run.addEventListener("click", async () => {
      setBusy();
      try {
        const response = await fetch("/query?v=4", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            question: question.value,
            analysis_mode: selectedMode,
            max_evidence: allEvidence.checked ? 100 : Number(evidenceLimit.value)
          })
        });
        if (!response.ok) throw new Error(await response.text());
        const data = await response.json();
        renderResult(data);
        setReady("Complete");
      } catch (error) {
        setError(String(error));
      }
    });
    function setBusy() {
      run.disabled = true;
      statusEl.textContent = "Running agents";
      statusDot.className = "dot busy";
      document.getElementById("run-id").textContent = `Run ${new Date().toLocaleTimeString()}`;
      stageMap.drafter.textContent = "...";
      stageMap.critic.textContent = "...";
      stageMap.adjudicator.textContent = "...";
      copyMap.drafter.textContent = "Retrieving and drafting";
      copyMap.critic.textContent = "Checking contradictions";
      copyMap.adjudicator.textContent = "Preparing verdict";
    }
    function setReady(message) {
      run.disabled = false;
      statusEl.textContent = message;
      statusDot.className = "dot live";
    }
    function setError(message) {
      run.disabled = false;
      statusEl.textContent = "Request failed";
      statusDot.className = "dot error";
      document.getElementById("answer").textContent = message;
      document.getElementById("answer").className = "answer-box";
    }
    function renderResult(data) {
      document.getElementById("confidence").textContent = data.confidence ?? "--";
      document.getElementById("grade").textContent = data.evidence_grade || "--";
      document.getElementById("verification").textContent = data.verification?.is_verified ? "Verified" : "Warnings";
      document.getElementById("latency").textContent = data.execution_ms ? `${data.execution_ms} ms` : "--";
      document.getElementById("evidence-count").textContent = data.evidence_count ?? "--";
      document.getElementById("mode-readout").textContent = formatLabel(data.analysis_mode || selectedMode);
      const risk = data.hallucination_risk?.risk || "pending";
      const riskChip = document.getElementById("risk-chip");
      riskChip.textContent = `Hallucination risk: ${risk}`;
      riskChip.className = `chip risk-${risk}`;
      document.getElementById("answer").textContent = data.answer || "No answer returned.";
      document.getElementById("answer").className = "answer-box";
      document.getElementById("factors").innerHTML = renderFactors(data.decision_factors || []);
      document.getElementById("citations").innerHTML = renderCitations(data.citations || []);
      document.getElementById("contradictions").innerHTML = renderContradictions(data.contradictory_evidence || []);
      document.getElementById("audit").innerHTML = renderAudit(data.audit_log || []);
      document.getElementById("markdown").textContent = data.report_markdown || "No report returned.";
      markStages(data.audit_log || []);
    }
    function markStages(audit) {
      const seen = new Set(audit.map(item => item.agent));
      ["drafter", "critic", "adjudicator"].forEach(agent => {
        stageMap[agent].textContent = seen.has(agent) ? "OK" : "--";
      });
      if (seen.has("drafter")) copyMap.drafter.textContent = "Evidence selected and cited";
      if (seen.has("critic")) copyMap.critic.textContent = "Contradictions reviewed";
      if (seen.has("adjudicator")) copyMap.adjudicator.textContent = "Final report generated";
    }
    function renderFactors(items) {
      if (!items.length) return `<div class="answer-box empty">No decision factors returned.</div>`;
      return items.map(item => `
        <div class="factor">
          <div><strong>${escapeHtml(formatLabel(item.factor))}</strong><span>${escapeHtml(item.value)}</span></div>
          <span>${escapeHtml(item.rationale)}</span>
        </div>
      `).join("");
    }
    function renderCitations(items) {
      if (!items.length) return `<div class="answer-box empty">No citations returned.</div>`;
      return items.map(item => `
        <article class="citation">
          <div class="citation-head">
            <div><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.text).slice(0, 420)}${item.text && item.text.length > 420 ? "..." : ""}</span></div>
            <span class="citation-id">${escapeHtml(item.citation_id)}</span>
          </div>
          <div class="chip-row">
            <span class="chip">${escapeHtml(item.study_design || "Unspecified")}</span>
            <span class="chip">${escapeHtml(item.publication_year || "n.d.")}</span>
            <span class="chip">n=${escapeHtml(item.sample_size ?? "unknown")}</span>
          </div>
        </article>
      `).join("");
    }
    function renderContradictions(items) {
      if (!items.length) return `<div class="answer-box empty">No contradictory evidence returned.</div>`;
      return items.map(item => `
        <article class="citation">
          <div class="citation-head">
            <div><strong>${escapeHtml(item.title || "Contradictory evidence")}</strong><span>${escapeHtml(item.summary || "")}</span></div>
            <span class="citation-id">!</span>
          </div>
          <div class="chip-row">
            <span class="chip">${escapeHtml(item.study_design || "Unspecified")}</span>
            <span class="chip">${escapeHtml(item.publication_year || "n.d.")}</span>
          </div>
        </article>
      `).join("");
    }
    function renderAudit(items) {
      if (!items.length) return `<div class="answer-box empty">No audit trail returned.</div>`;
      return items.map((item, index) => `
        <div class="trace-item">
          <strong>${String(index + 1).padStart(2, "0")} ${escapeHtml(formatLabel(item.agent || "agent"))}</strong>
          <span><pre>${escapeHtml(JSON.stringify(item, null, 2))}</pre></span>
        </div>
      `).join("");
    }
    function chooseMode(mode) {
      selectedMode = mode || "auto";
      document.querySelectorAll(".mode-card").forEach(card => {
        card.classList.toggle("active", card.dataset.mode === selectedMode);
      });
      document.getElementById("mode-readout").textContent = formatLabel(selectedMode);
    }
    function updateEvidenceLabel() {
      evidenceLimit.disabled = allEvidence.checked;
      evidenceLabel.textContent = allEvidence.checked ? "all matching sources" : `${evidenceLimit.value} sources`;
    }
    function formatLabel(value) {
      return String(value ?? "").replace(/_/g, " ").replace(/\\b\\w/g, char => char.toUpperCase());
    }
    function escapeHtml(value) {
      return String(value ?? "").replace(/[&<>"']/g, char => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;" }[char]));
    }
  </script>
</body>
</html>
"""
