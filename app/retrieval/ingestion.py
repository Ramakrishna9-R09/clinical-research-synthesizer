from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.observability import timed_span
from app.retrieval.chunking import semantic_chunk_documents
from app.retrieval.document_store import ClinicalDocument, load_documents
from app.retrieval.vector_store import VectorStore


def ingest_data_dir(data_dir: Path | None = None, rebuild: bool = True) -> dict:
    settings = get_settings()
    source_dir = data_dir or settings.data_dir
    with timed_span("ingestion", data_dir=str(source_dir)):
        documents = load_documents(source_dir)
        chunks = semantic_chunk_documents(documents)
        vector_store = VectorStore()
        index_result = vector_store.upsert(chunks)
        return {
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "rebuild": rebuild,
            **index_result,
        }


def ingest_text(title: str, text: str, metadata: dict | None = None) -> dict:
    document = ClinicalDocument(id=f"api:{title}", text=text, metadata={"title": title, "source": "api", **(metadata or {})})
    chunks = semantic_chunk_documents([document])
    return {"documents_loaded": 1, "chunks_created": len(chunks), **VectorStore().upsert(chunks)}
