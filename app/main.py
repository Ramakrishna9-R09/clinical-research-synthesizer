from __future__ import annotations

from time import perf_counter

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.graph.workflow import describe_graph, run_workflow
from app.guardrails.hallucination_detector import estimate_hallucination_risk
from app.ui_page import render_ui

app = FastAPI(title="Clinical Research Synthesizer", version="0.3.0")


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    require_human_approval: bool = False
    approved: bool = True


@app.get("/", response_class=HTMLResponse)
def ui() -> str:
    return render_ui()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "clinical-research-synthesizer", "version": app.version}


@app.get("/graph")
def graph() -> dict:
    return describe_graph()


@app.get("/examples")
def examples() -> dict:
    return {
        "queries": [
            "Should eligible adults with heart failure receive an SGLT2 inhibitor?",
            "What should clinicians monitor after starting an SGLT2 inhibitor?",
            "Does one ketoacidosis case report outweigh randomized heart failure trial evidence?",
        ]
    }


@app.post("/query")
def query(request: QueryRequest) -> dict:
    started = perf_counter()
    state = run_workflow(
        request.question,
        require_human_approval=request.require_human_approval,
        approved=request.approved,
    )
    final_report = state.get("final_report", {})
    risk = estimate_hallucination_risk(final_report.get("answer", ""), final_report.get("citations", []))
    execution_ms = round((perf_counter() - started) * 1000)
    return {
        "query": request.question,
        "answer": final_report.get("answer"),
        "confidence": final_report.get("confidence"),
        "evidence_grade": final_report.get("evidence_grade"),
        "decision_factors": final_report.get("decision_factors", []),
        "citations": final_report.get("citations", []),
        "contradictory_evidence": final_report.get("contradictory_evidence", []),
        "verification": final_report.get("verification"),
        "hallucination_risk": risk,
        "report_path": final_report.get("report_path"),
        "audit_log": state.get("audit_log", []),
        "execution_ms": execution_ms,
        "agent_count": len(state.get("audit_log", [])),
        "report_markdown": final_report.get("report_markdown"),
    }
