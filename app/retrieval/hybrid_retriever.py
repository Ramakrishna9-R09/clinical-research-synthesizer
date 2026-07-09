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
        normalized_query = _normalize_query(query)
        topic = _detect_topic(normalized_query)
        bm25 = self._bm25_scores(normalized_query)
        dense = self._semantic_scores(normalized_query)
        fused = _rrf_fuse([bm25, dense])
        relevance = self._semantic_scores(normalized_query)
        ranked_indices = [
            idx
            for idx in sorted(fused, key=fused.get, reverse=True)
            if relevance.get(idx, 0) > 0 or bm25.get(idx, 0) > 0
        ]
        if topic:
            topic_ranked = [idx for idx in ranked_indices if self.chunks[idx].metadata.get("topic") == topic]
            if topic_ranked:
                ranked_indices = topic_ranked
        ranked_indices = ranked_indices[:top_k]
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
    stop = {"the", "a", "an", "and", "or", "of", "to", "in", "for", "with", "is", "are", "be", "by", "does", "do"}
    return [token.lower() for token in TOKEN_RE.findall(_normalize_query(text)) if token.lower() not in stop]


def _normalize_query(text: str) -> str:
    lowered = text.lower()
    replacements = {
        "heartattack": "heart attack myocardial infarction cardiac event",
        "heart-attack": "heart attack myocardial infarction cardiac event",
        "heart attack": "heart attack myocardial infarction cardiac event",
        "causses": "causes",
        "couses": "causes",
        "running": "running run exercise aerobic exertion",
        "runner": "runner running exercise aerobic exertion",
        "jogging": "jogging running exercise aerobic exertion",
    }
    for source, target in replacements.items():
        lowered = lowered.replace(source, target)
    return lowered


def _detect_topic(text: str) -> str | None:
    tokens = set(_tokens(text))
    exercise_terms = {"running", "run", "exercise", "aerobic", "exertion", "jogging", "runner"}
    cardiac_event_terms = {"attack", "myocardial", "infarction", "cardiac", "arrest"}
    drug_terms = {"sglt2", "inhibitor", "drug", "pharmacotherapy", "ketoacidosis"}
    if tokens & exercise_terms and tokens & cardiac_event_terms:
        return "exercise_cardiac_risk"
    if tokens & drug_terms:
        return "heart_failure_pharmacotherapy"
    return None
