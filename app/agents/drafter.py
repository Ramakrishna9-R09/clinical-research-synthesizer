from __future__ import annotations

from app.graph.state import AgentState
from app.models.llm_client import LLMClient
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker


class DrafterAgent:
    def __init__(self, retriever: HybridRetriever | None = None, reranker: CrossEncoderReranker | None = None, llm: LLMClient | None = None):
        self.retriever = retriever or HybridRetriever()
        self.reranker = reranker or CrossEncoderReranker()
        self.llm = llm or LLMClient()

    def run(self, state: AgentState) -> AgentState:
        query = state["query"]
        max_evidence = max(1, min(int(state.get("max_evidence", 12)), 100))
        retrieval_query = _mode_expanded_query(query, state.get("analysis_mode", "auto"))
        candidates = self.retriever.search(retrieval_query, top_k=max(20, max_evidence))
        chunks = self.reranker.rerank(retrieval_query, candidates, top_k=max_evidence)
        citations = [_citation(chunk, index + 1) for index, chunk in enumerate(chunks)]
        evidence = "\n\n".join(f"[{item['citation_id']}] {item['text']}" for item in citations)
        prompt = (
            f"Clinical question: {query}\n\n"
            f"Evidence:\n{evidence}\n\n"
            "Draft a cautious, evidence-grounded clinical recommendation with inline citations."
        )
        llm_text = self.llm.complete(prompt, system="You are a clinical evidence synthesis assistant. Never invent uncited facts.")
        draft = _fallback_draft(query, citations, llm_text)
        return {
            **state,
            "retrieved_chunks": citations,
            "research_data": citations,
            "draft": draft,
            "audit_log": [
                *state.get("audit_log", []),
                {
                    "agent": "drafter",
                    "analysis_mode": state.get("analysis_mode", "auto"),
                    "requested_evidence": max_evidence,
                    "retrieved_evidence": len(citations),
                    "citations": [c["citation_id"] for c in citations],
                },
            ],
        }


def _citation(chunk, citation_number: int) -> dict:
    metadata = dict(chunk.metadata)
    return {
        "citation_id": f"C{citation_number}",
        "chunk_id": chunk.id,
        "parent_id": chunk.parent_id,
        "title": str(metadata.get("title", "Untitled source")),
        "source": str(metadata.get("source", "unknown")),
        "publication_year": metadata.get("publication_year") or _coerce_year(metadata.get("publication_date")),
        "sample_size": metadata.get("sample_size"),
        "study_design": metadata.get("study_design", "Unspecified"),
        "topic": metadata.get("topic"),
        "text": chunk.text,
    }


def _fallback_draft(query: str, citations: list[dict], llm_text: str) -> str:
    source_ids = ", ".join(c["citation_id"] for c in citations) or "no citations"
    return (
        f"Initial recommendation for '{query}': current local evidence supports a cautious, monitored intervention when the patient "
        f"matches trial or guideline eligibility. Key support comes from {source_ids}. {llm_text}"
    )


def _coerce_year(value):
    try:
        return int(str(value)[:4])
    except Exception:
        return None


def _mode_expanded_query(query: str, analysis_mode: str | None) -> str:
    mode_terms = {
        "monitoring": "monitoring follow-up adverse effects safety labs warning symptoms contraindications",
        "conflict": "contradictory evidence conflicting studies adverse events contraindications no benefit harm",
        "safety": "risk safety adverse events contraindications warning symptoms emergency red flags",
        "evidence_map": "guideline randomized trial systematic review meta-analysis observational registry evidence",
    }
    return f"{query} {mode_terms.get(analysis_mode or 'auto', '')}".strip()
