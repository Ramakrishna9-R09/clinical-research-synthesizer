from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    query: str
    analysis_mode: str
    max_evidence: int
    retrieved_chunks: list[dict[str, Any]]
    research_data: list[dict[str, Any]]
    draft: str
    critic_feedback: dict[str, Any]
    contradictory_evidence: list[dict[str, Any]]
    revision_count: int
    final_report: dict[str, Any]
    is_sufficient: bool
    audit_log: list[dict[str, Any]]
