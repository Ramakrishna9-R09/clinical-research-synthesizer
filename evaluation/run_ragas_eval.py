from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.guardrails.hallucination_detector import estimate_hallucination_risk
from app.graph.workflow import run_workflow
from app.guardrails.chain_of_verification import verify_report


def main() -> None:
    rows = [json.loads(line) for line in Path("evaluation/golden_dataset.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    faithfulness_scores = []
    relevancy_scores = []
    context_precision_scores = []
    hallucination_scores = []
    for row in rows:
        state = run_workflow(row["question"], analysis_mode=row.get("analysis_mode", "auto"), max_evidence=row.get("max_evidence", 20))
        report = state["final_report"]
        verification = verify_report(report["report_markdown"], report["citations"])
        faithfulness_scores.append(1.0 if verification["is_verified"] else 0.5)
        answer_words = set(report["answer"].lower().split())
        expected_words = set(row["expected"].lower().split())
        relevancy_scores.append(len(answer_words & expected_words) / max(len(expected_words), 1))
        query_words = set(row["question"].lower().replace("?", "").split())
        relevant_contexts = 0
        for citation in report["citations"]:
            context_words = set((citation["title"] + " " + citation["text"]).lower().split())
            if query_words & context_words:
                relevant_contexts += 1
        context_precision_scores.append(relevant_contexts / max(len(report["citations"]), 1))
        hallucination_scores.append(1 - estimate_hallucination_risk(report["answer"], report["citations"])["score"])
    metrics = {
        "faithfulness": round(sum(faithfulness_scores) / len(faithfulness_scores), 2),
        "answer_relevancy": round(sum(relevancy_scores) / len(relevancy_scores), 2),
        "context_precision": round(sum(context_precision_scores) / len(context_precision_scores), 2),
        "groundedness": round(sum(hallucination_scores) / len(hallucination_scores), 2),
        "hallucination_rate_proxy": round(1 - (sum(faithfulness_scores) / len(faithfulness_scores)), 2),
        "ragas_note": "Install/configure an evaluator LLM to replace these deterministic proxy metrics with full RAGAS scoring.",
    }
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
