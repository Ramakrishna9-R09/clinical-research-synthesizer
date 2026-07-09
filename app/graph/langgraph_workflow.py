from __future__ import annotations

from app.agents.adjudicator import AdjudicatorAgent
from app.agents.critic import CriticAgent
from app.agents.drafter import DrafterAgent
from app.graph.state import AgentState


def build_langgraph():
    """Compile the production LangGraph workflow when langgraph is installed."""
    try:
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.graph import END, StateGraph
    except Exception as exc:
        raise RuntimeError("Install langgraph to compile the stateful HITL workflow.") from exc

    drafter = DrafterAgent()
    critic = CriticAgent()
    adjudicator = AdjudicatorAgent()

    graph = StateGraph(AgentState)
    graph.add_node("drafter", drafter.run)
    graph.add_node("critic", critic.run)
    graph.add_node("adjudicator", adjudicator.run)
    graph.set_entry_point("drafter")
    graph.add_edge("drafter", "critic")
    graph.add_conditional_edges(
        "critic",
        lambda state: "adjudicator" if state.get("is_sufficient") or state.get("revision_count", 0) >= 3 else "drafter",
        {"drafter": "drafter", "adjudicator": "adjudicator"},
    )
    graph.add_edge("adjudicator", END)
    return graph.compile(checkpointer=MemorySaver(), interrupt_before=["adjudicator"])
