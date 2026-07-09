from __future__ import annotations


def estimate_hallucination_risk(answer: str, citations: list[dict]) -> dict:
    if not citations:
        return {"risk": "high", "score": 0.9, "reason": "No citations were supplied."}
    grounded_terms = set()
    for citation in citations:
        grounded_terms.update(citation.get("text", "").lower().split())
    answer_terms = {term.strip(".,;:()[]").lower() for term in answer.split() if len(term) > 5}
    unsupported = [term for term in answer_terms if term not in grounded_terms]
    score = min(0.95, len(unsupported) / max(len(answer_terms), 1))
    risk = "low" if score < 0.25 else "medium" if score < 0.55 else "high"
    return {"risk": risk, "score": round(score, 2), "unsupported_terms_sample": unsupported[:10]}
