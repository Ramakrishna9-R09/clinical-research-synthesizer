from __future__ import annotations

import os

from app.graph.state import AgentState


class CriticAgent:
    def run(self, state: AgentState) -> AgentState:
        query = state["query"]
        contradictory = self._local_contradictions(query, state.get("research_data", []))
        contradictory.extend(self._tavily_search(query))
        is_sufficient = len(contradictory) == 0 or _has_stronger_support(state.get("research_data", []), contradictory)
        feedback = {
            "is_sufficient": is_sufficient,
            "feedback": (
                "Primary evidence appears stronger than contradictory evidence."
                if is_sufficient
                else "Contradictory evidence may materially change the recommendation; revise with explicit limitations."
            ),
            "contradictory_evidence": contradictory,
        }
        return {
            **state,
            "critic_feedback": feedback,
            "contradictory_evidence": contradictory,
            "is_sufficient": is_sufficient,
            "revision_count": state.get("revision_count", 0) + 1,
            "audit_log": [*state.get("audit_log", []), {"agent": "critic", "is_sufficient": is_sufficient, "contradictions": len(contradictory)}],
        }

    def _local_contradictions(self, query: str, evidence: list[dict]) -> list[dict]:
        contradiction_terms = ("not effective", "no benefit", "harm", "ketoacidosis", "contraindication", "avoid")
        results = []
        for item in evidence:
            text = item.get("text", "").lower()
            if any(term in text for term in contradiction_terms):
                results.append({
                    "title": item.get("title"),
                    "source": item.get("source"),
                    "publication_year": item.get("publication_year"),
                    "study_design": item.get("study_design"),
                    "sample_size": item.get("sample_size"),
                    "summary": item.get("text", "")[:500],
                })
        return results

    def _tavily_search(self, query: str) -> list[dict]:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return []
        try:
            from tavily import TavilyClient

            client = TavilyClient(api_key=api_key)
            response = client.search(f"contradictory evidence guideline adverse events {query}", max_results=3)
            return [
                {"title": r.get("title"), "source": r.get("url"), "summary": r.get("content"), "study_design": "External search"}
                for r in response.get("results", [])
            ]
        except Exception:
            return []


def _has_stronger_support(supporting: list[dict], contradictory: list[dict]) -> bool:
    support_score = sum(_evidence_score(item) for item in supporting)
    contradiction_score = sum(_evidence_score(item) for item in contradictory)
    return support_score >= contradiction_score


def _evidence_score(item: dict) -> float:
    design = str(item.get("study_design", "")).lower()
    design_weight = 1.0
    if "systematic" in design or "meta" in design:
        design_weight = 5.0
    elif "guideline" in design:
        design_weight = 4.5
    elif "rct" in design or "randomized" in design:
        design_weight = 4.0
    elif "case" in design:
        design_weight = 1.0
    sample = item.get("sample_size") or 1
    year = item.get("publication_year") or 2010
    recency = max(0.5, min(2.0, (int(year) - 2000) / 12))
    return design_weight * recency * min(5.0, max(1.0, float(sample) ** 0.25))
