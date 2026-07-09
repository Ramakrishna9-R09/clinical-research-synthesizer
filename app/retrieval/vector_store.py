from __future__ import annotations

import math

from app.config import get_settings
from app.retrieval.document_store import Chunk
from app.retrieval.embeddings import EmbeddingModel


class VectorStore:
    def __init__(self, collection_name: str = "clinical_chunks"):
        self.collection_name = collection_name
        self.embedding_model = EmbeddingModel()
        self._client = None
        self._collection = None
        self._fallback_chunks: list[Chunk] = []
        self._fallback_vectors: list[list[float]] = []
        try:
            import chromadb

            self._client = chromadb.PersistentClient(path=str(get_settings().index_dir))
            self._collection = self._client.get_or_create_collection(collection_name)
        except Exception:
            self._client = None
            self._collection = None

    def upsert(self, chunks: list[Chunk]) -> dict:
        if not chunks:
            return {"chunks_indexed": 0, "backend": self.backend}
        vectors = self.embedding_model.embed([chunk.text for chunk in chunks])
        if self._collection is not None:
            self._collection.upsert(
                ids=[chunk.id for chunk in chunks],
                embeddings=vectors,
                documents=[chunk.text for chunk in chunks],
                metadatas=[_clean_metadata(chunk.metadata | {"parent_id": chunk.parent_id}) for chunk in chunks],
            )
        self._fallback_chunks = chunks
        self._fallback_vectors = vectors
        return {"chunks_indexed": len(chunks), "backend": self.backend}

    def query(self, query: str, top_k: int = 20) -> list[tuple[str, float]]:
        query_vector = self.embedding_model.embed([query])[0]
        if self._collection is not None and self._collection.count() > 0:
            result = self._collection.query(query_embeddings=[query_vector], n_results=top_k)
            ids = result.get("ids", [[]])[0]
            distances = result.get("distances", [[]])[0]
            return [(chunk_id, 1 / (1 + float(distance))) for chunk_id, distance in zip(ids, distances)]
        scores = [
            (chunk.id, _cosine(query_vector, vector))
            for chunk, vector in zip(self._fallback_chunks, self._fallback_vectors)
        ]
        return sorted(scores, key=lambda item: item[1], reverse=True)[:top_k]

    @property
    def backend(self) -> str:
        return "chromadb" if self._collection is not None else "in_memory_hash_embeddings"


def _cosine(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    return sum(a * b for a, b in zip(left, right)) / ((math.sqrt(sum(a * a for a in left)) or 1.0) * (math.sqrt(sum(b * b for b in right)) or 1.0))


def _clean_metadata(metadata: dict) -> dict:
    return {key: value for key, value in metadata.items() if isinstance(value, str | int | float | bool) or value is None}
