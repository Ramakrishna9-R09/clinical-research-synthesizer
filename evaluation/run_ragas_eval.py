from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.graph.workflow import run_workflow
from app.guardrails.chain_of_verification import verify_report


def main() -> None:
    rows = [json.loads(line) for line in Path("evaluation/golden_dataset.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    faithfulness_scores = []
    relevancy_scores = []
    for row in rows:
        state = run_workflow(row["question"])
        report = state["final_report"]
        verification = verify_report(report["report_markdown"], report["citations"])
        faithfulness_scores.append(1.0 if verification["is_verified"] else 0.5)
        answer_words = set(report["answer"].lower().split())
        expected_words = set(row["expected"].lower().split())
        relevancy_scores.append(len(answer_words & expected_words) / max(len(expected_words), 1))
    metrics = {
        "faithfulness": round(sum(faithfulness_scores) / len(faithfulness_scores), 2),
        "answer_relevancy_proxy": round(sum(relevancy_scores) / len(relevancy_scores), 2),
        "hallucination_rate_proxy": round(1 - (sum(faithfulness_scores) / len(faithfulness_scores)), 2),
    }
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
