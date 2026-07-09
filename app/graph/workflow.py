from __future__ import annotations

from app.agents.orchestrator import ClinicalOrchestrator
from app.graph.state import AgentState


def run_workflow(query: str, require_human_approval: bool = False, approved: bool = True) -> AgentState:
    return ClinicalOrchestrator().run(query, require_human_approval=require_human_approval, approved=approved)


def describe_graph() -> dict:
    return {
        "nodes": ["drafter", "critic", "adjudicator"],
        "edges": [
            {"from": "drafter", "to": "critic"},
            {"from": "critic", "to": "drafter", "condition": "is_sufficient=false and revision_count<3"},
            {"from": "critic", "to": "adjudicator", "condition": "is_sufficient=true or revision_count>=3"},
        ],
        "hitl": "Set require_human_approval=true to pause before adjudicator.",
    }
