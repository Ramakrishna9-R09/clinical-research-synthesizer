from __future__ import annotations

import re

from app.retrieval.document_store import Chunk, ClinicalDocument, extract_metadata_from_text

HEADING_RE = re.compile(r"(?m)^(background|methods|results|safety|conclusion|recommendation|contraindications|monitoring|evidence basis)\s*$", re.IGNORECASE)


def semantic_chunk_document(document: ClinicalDocument, max_chars: int = 1200) -> list[Chunk]:
    sections: list[str] = []
    matches = list(HEADING_RE.finditer(document.text))
    if not matches:
        sections = _window_text(document.text, max_chars)
    else:
        for idx, match in enumerate(matches):
            start = match.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(document.text)
            sections.extend(_window_text(document.text[start:end].strip(), max_chars))

    chunks: list[Chunk] = []
    for index, section in enumerate(s for s in sections if s.strip()):
        metadata = {**document.metadata, **extract_metadata_from_text(section), "chunk_index": index}
        chunks.append(Chunk(id=f"{document.id}:{index}", parent_id=document.id, text=section, metadata=metadata))
    return chunks


def semantic_chunk_documents(documents: list[ClinicalDocument]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(semantic_chunk_document(document))
    return chunks


def _window_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n|(?<=[.!?])\s+(?=[A-Z])", text) if p.strip()]
    windows: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 1 <= max_chars:
            current = f"{current} {paragraph}".strip()
        else:
            if current:
                windows.append(current)
            current = paragraph
    if current:
        windows.append(current)
    return windows
