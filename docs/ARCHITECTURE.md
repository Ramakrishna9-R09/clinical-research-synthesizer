# Architecture

## Goal

This project demonstrates a clinical RAG workflow that does not simply retrieve sources and answer. It explicitly separates drafting, contradiction hunting, adjudication, verification, and audit logging.

## Runtime Flow

```mermaid
sequenceDiagram
  participant U as User
  participant API as FastAPI
  participant I as Ingestion
  participant V as Vector Store
  participant R as Hybrid Retriever
  participant D as Drafter
  participant C as Critic
  participant A as Adjudicator
  participant G as Guardrails

  U->>API: POST /query
  API->>I: Optional POST /ingest
  I->>V: Chunk, embed, persist vectors
  API->>R: Retrieve top evidence
  R->>V: Dense vector query
  R-->>D: Reranked chunks with metadata
  D->>C: Initial cited draft
  C->>R: Review for contradictions
  C-->>A: Feedback and safety-limiting evidence
  A->>A: Weight recency, sample size, study design
  A->>G: Verify cited claims
  G-->>API: Verification status
  API-->>U: Answer, citations, confidence, trace
```

## Key Design Choices

- **Stateful agents:** the workflow keeps `query`, retrieved evidence, critic feedback, revision count, final report, and audit logs in a shared state object.
- **Ingestion/indexing:** PDFs and text files are parsed, semantically chunked, embedded, and indexed into ChromaDB when available.
- **Hybrid retrieval:** BM25-style lexical scores, dense vector search, and lexical semantic overlap are fused using reciprocal rank fusion.
- **Adversarial review:** the critic actively flags contraindications, adverse events, and weak contradictory evidence instead of assuming retrieved evidence is sufficient.
- **Evidence hierarchy:** adjudication weights systematic reviews, guidelines, RCTs, and case reports differently.
- **No paid dependency required:** the deployed serverless demo uses deterministic local logic. Local mode can add Ollama, Tavily, Chroma, and Hugging Face rerankers.
- **Clinical auditability:** every response includes citations, checked citation IDs, confidence, decision factors, and an agent trace.

## Production Extension Path

- Replace lexical semantic overlap with Chroma or Qdrant dense retrieval.
- Add Redis-backed response, embedding, and retrieval caching.
- Enable `app/graph/langgraph_workflow.py` for checkpointed HITL flows.
- Add LangSmith tracing using `.env`.
- Add RAGAS with an evaluator LLM for full faithfulness and context precision.
- Store reports and audit logs in Postgres or object storage.
