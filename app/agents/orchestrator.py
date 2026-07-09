from __future__ import annotations

from app.agents.adjudicator import AdjudicatorAgent
from app.agents.critic import CriticAgent
from app.agents.drafter import DrafterAgent
from app.graph.state import AgentState


class ClinicalOrchestrator:
    def __init__(self, max_revisions: int = 3):
        self.drafter = DrafterAgent()
        self.critic = CriticAgent()
        self.adjudicator = AdjudicatorAgent()
        self.max_revisions = max_revisions

    def run(self, query: str, require_human_approval: bool = False, approved: bool = True) -> AgentState:
        state: AgentState = {"query": query, "revision_count": 0, "audit_log": []}
        while True:
            state = self.drafter.run(state)
            state = self.critic.run(state)
            if state.get("is_sufficient") or state.get("revision_count", 0) >= self.max_revisions:
                break
        if require_human_approval and not approved:
            return {**state, "final_report": {"status": "awaiting_clinician_approval"}}
        return self.adjudicator.run(state)
