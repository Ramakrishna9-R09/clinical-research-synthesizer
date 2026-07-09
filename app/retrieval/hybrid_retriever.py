from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

from app.retrieval.chunking import semantic_chunk_documents
from app.retrieval.document_store import Chunk, load_documents
from app.config import get_settings


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9-]+")


class HybridRetriever:
    def __init__(self, chunks: list[Chunk] | None = None):
        if chunks is None:
            docs = load_documents(get_settings().data_dir)
            chunks = semantic_chunk_documents(docs)
        self.chunks = chunks
        self._tokenized = [_tokens(chunk.text) for chunk in chunks]
        self._doc_freq = Counter(term for terms in self._tokenized for term in set(terms))
        self._avg_len = sum(len(terms) for terms in self._tokenized) / max(len(self._tokenized), 1)

    def search(self, query: str, top_k: int = 8) -> list[Chunk]:
        if not self.chunks:
            return []
        bm25 = self._bm25_scores(query)
        dense = self._semantic_scores(query)
        fused = _rrf_fuse([bm25, dense])
        ranked_indices = sorted(fused, key=fused.get, reverse=True)[:top_k]
        return [self.chunks[i] for i in ranked_indices]

    def _bm25_scores(self, query: str) -> dict[int, float]:
        q_terms = _tokens(query)
        scores: dict[int, float] = defaultdict(float)
        total_docs = len(self.chunks)
        for idx, terms in enumerate(self._tokenized):
            counts = Counter(terms)
            doc_len = len(terms) or 1
            for term in q_terms:
                if not counts[term]:
                    continue
                idf = math.log(1 + (total_docs - self._doc_freq[term] + 0.5) / (self._doc_freq[term] + 0.5))
                denom = counts[term] + 1.5 * (1 - 0.75 + 0.75 * doc_len / max(self._avg_len, 1))
                scores[idx] += idf * (counts[term] * 2.5 / denom)
        return dict(scores)

    def _semantic_scores(self, query: str) -> dict[int, float]:
        q_terms = set(_tokens(query))
        scores = {}
        for idx, terms in enumerate(self._tokenized):
            term_set = set(terms)
            overlap = len(q_terms & term_set)
            union = len(q_terms | term_set) or 1
            scores[idx] = overlap / union
        return scores


def _rrf_fuse(score_maps: list[dict[int, float]], k: int = 60) -> dict[int, float]:
    fused: dict[int, float] = defaultdict(float)
    for scores in score_maps:
        for rank, idx in enumerate(sorted(scores, key=scores.get, reverse=True), start=1):
            fused[idx] += 1 / (k + rank)
    return dict(fused)


def _tokens(text: str) -> list[str]:
    stop = {"the", "a", "an", "and", "or", "of", "to", "in", "for", "with", "is", "are", "be", "by"}
    return [token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in stop]
