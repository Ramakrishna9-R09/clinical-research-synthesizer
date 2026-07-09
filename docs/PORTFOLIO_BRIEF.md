# Portfolio Brief

## Project Positioning

**Clinical Research Synthesizer** is a production-style multi-agent RAG system for high-stakes evidence synthesis. It is designed to show AI engineering skills that matter in GenAI teams: retrieval, orchestration, verification, observability, deployment, and practical product polish.

## Skills Demonstrated

| Area | Evidence in project |
| --- | --- |
| RAG architecture | Semantic chunking, hybrid retrieval, reranking interface, parent metadata preservation |
| Ingestion | PDF/text ingestion, metadata preservation, Chroma-compatible indexing |
| Agentic workflows | Drafter, critic, adjudicator, shared state, revision loop |
| Guardrails | Chain-of-verification, citation checks, hallucination risk proxy |
| Evaluation | Golden dataset and evaluation smoke test |
| Backend engineering | FastAPI, typed request models, OpenAPI docs |
| Frontend/product | Hosted UI with evidence, trace, report, and examples |
| DevOps | GitHub Actions CI, Docker, Vercel production deploy |
| Responsible AI | Clinical safety disclaimer, audit trail, source grounding |

## Interview Talking Points

- Why naive RAG is unsafe when evidence conflicts.
- How the critic agent changes behavior compared with single-pass generation.
- How evidence quality is scored using study design, sample size, and recency.
- How the system can run fully free locally, then scale to Chroma, Qdrant, LangGraph, Ollama, and LangSmith.
- What would be required before real healthcare use: validation, PHI controls, clinical governance, access control, monitoring, and regulatory review.
