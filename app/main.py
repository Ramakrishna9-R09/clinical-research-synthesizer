from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.graph.workflow import describe_graph, run_workflow
from app.guardrails.hallucination_detector import estimate_hallucination_risk

app = FastAPI(title="Clinical Research Synthesizer", version="0.1.0")


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    require_human_approval: bool = False
    approved: bool = True


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
