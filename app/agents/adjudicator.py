from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.graph.state import AgentState
from app.guardrails.chain_of_verification import verify_report


class AdjudicatorAgent:
    def run(self, state: AgentState) -> AgentState:
        evidence = state.get("research_data", [])
        contradictory = state.get("contradictory_evidence", [])
        score = _confidence(evidence, contradictory)
        verdict = _verdict(score)
        report_md = _render_report(state["query"], verdict, score, evidence, contradictory, state.get("critic_feedback", {}))
        verification = verify_report(report_md, evidence)
        if not verification["is_verified"]:
            score = min(score, 0.65)
            report_md += "\n\n## Verification Warnings\n" + "\n".join(f"- {w}" for w in verification["warnings"])
        report = {
            "answer": verdict,
            "confidence": round(score, 2),
            "citations": evidence,
            "contradictory_evidence": contradictory,
            "report_markdown": report_md,
            "verification": verification,
        }
        report_path = _save_report(report_md)
        report["report_path"] = str(report_path)
        return {
            **state,
            "final_report": report,
            "audit_log": [*state.get("audit_log", []), {"agent": "adjudicator", "confidence": report["confidence"], "report_path": str(report_path)}],
        }


def _confidence(evidence: list[dict], contradictory: list[dict]) -> float:
    if not evidence:
        return 0.2
    support = sum(_score(item) for item in evidence)
    conflict = sum(_score(item) for item in contradictory)
    return max(0.1, min(0.98, support / (support + conflict + 2)))


def _score(item: dict) -> float:
    design = str(item.get("study_design", "")).lower()
    weight = 1.0
    if "guideline" in design:
        weight = 4.5
    elif "rct" in design or "randomized" in design:
        weight = 4.0
    elif "systematic" in design or "meta" in design:
        weight = 5.0
    elif "case" in design:
        weight = 1.0
    year = int(item.get("publication_year") or 2015)
    sample = float(item.get("sample_size") or 1)
    return weight * max(0.5, min(2.0, (year - 2000) / 12)) * min(4.0, max(1.0, sample ** 0.25))


def _verdict(confidence: float) -> str:
    if confidence >= 0.8:
        return "Evidence supports the recommendation with standard monitoring and patient-specific contraindication review."
    if confidence >= 0.55:
        return "Evidence is mixed or incomplete; use shared decision-making and document uncertainty."
    return "Evidence is insufficient for a confident recommendation; seek specialist review or stronger source material."


def _render_report(query: str, verdict: str, confidence: float, evidence: list[dict], contradictory: list[dict], critic_feedback: dict) -> str:
    evidence_lines = [
        f"- [{item['citation_id']}] {item['title']} ({item.get('publication_year', 'n.d.')}, {item.get('study_design', 'unspecified')}, n={item.get('sample_size', 'unknown')}): {item['text'][:280]}"
        for item in evidence
    ]
    contradiction_lines = [
        f"- {item.get('title', 'External or local contrary evidence')}: {item.get('summary', '')[:280]}"
        for item in contradictory
    ] or ["- No stronger contradictory evidence identified in configured sources."]
    return "\n".join(
        [
            "# Clinical Evidence Synthesis Report",
            "",
            f"## Question\n{query}",
            "",
            f"## Final Verdict\n{verdict}",
            "",
            f"## Confidence\n{confidence:.2f}",
            "",
            "## Supporting Evidence",
            *evidence_lines,
            "",
            "## Contradictory Evidence Review",
            *contradiction_lines,
            "",
            "## Critic Assessment",
            critic_feedback.get("feedback", "No critic feedback recorded."),
            "",
            "## Clinical Safety Note",
            "This system supports literature synthesis and does not replace clinician judgment, local policy, or patient-specific assessment.",
        ]
    )


def _save_report(markdown: str) -> Path:
    path = get_settings().report_dir / "clinical_report.md"
    path.write_text(markdown, encoding="utf-8")
    return path
