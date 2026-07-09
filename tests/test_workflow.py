from __future__ import annotations

from app.graph.workflow import describe_graph, run_workflow
from app.retrieval.chunking import semantic_chunk_document
from app.retrieval.document_store import ClinicalDocument


def test_semantic_chunking_preserves_heading_sections():
    doc = ClinicalDocument(id="doc-1", text="Background\nAlpha evidence.\nResults\nBenefit shown.", metadata={"title": "Trial"})
    chunks = semantic_chunk_document(doc)
    assert len(chunks) == 2
    assert chunks[0].metadata["title"] == "Trial"


def test_workflow_returns_report_with_citations():
    state = run_workflow("Should eligible adults with heart failure receive an SGLT2 inhibitor?")
    report = state["final_report"]
    assert report["answer"]
    assert report["confidence"] > 0
    assert report["citations"]
    assert report["verification"]["is_verified"]


def test_graph_description_documents_agent_loop():
    graph = describe_graph()
    assert graph["nodes"] == ["drafter", "critic", "adjudicator"]
    assert any(edge["from"] == "critic" and edge["to"] == "drafter" for edge in graph["edges"])
