from __future__ import annotations

from app.retrieval.document_store import Chunk


class CrossEncoderReranker:
    def __init__(self) -> None:
        self._model = None
        try:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        except Exception:
            self._model = None

    def rerank(self, query: str, chunks: list[Chunk], top_k: int = 5) -> list[Chunk]:
        if not chunks:
            return []
        if self._model is None:
            return chunks[:top_k]
        scores = self._model.predict([(query, chunk.text) for chunk in chunks])
        ranked = sorted(zip(chunks, scores), key=lambda item: float(item[1]), reverse=True)
        return [chunk for chunk, _ in ranked[:top_k]]
