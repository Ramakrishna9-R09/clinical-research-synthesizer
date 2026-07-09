from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from uuid import uuid4

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None


@dataclass
class ClinicalDocument:
    id: str
    text: str
    metadata: dict[str, str | int | float] = field(default_factory=dict)


@dataclass
class Chunk:
    id: str
    parent_id: str
    text: str
    metadata: dict[str, str | int | float] = field(default_factory=dict)


def parse_pdf(path: Path) -> ClinicalDocument:
    if PdfReader is None:
        return ClinicalDocument(
            id=str(uuid4()),
            text=f"PDF parsing requires pypdf. Source file available at {path}.",
            metadata={"title": path.stem, "source": str(path), "document_type": "pdf"},
        )
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    metadata = {
        "title": reader.metadata.title or path.stem,
        "source": str(path),
        "document_type": "pdf",
    }
    return ClinicalDocument(id=str(uuid4()), text=text, metadata=metadata)


def parse_text(path: Path) -> ClinicalDocument:
    return ClinicalDocument(
        id=str(uuid4()),
        text=path.read_text(encoding="utf-8", errors="ignore"),
        metadata={"title": path.stem, "source": str(path), "document_type": path.suffix.lstrip(".")},
    )


def load_documents(data_dir: Path) -> list[ClinicalDocument]:
    docs: list[ClinicalDocument] = []
    for path in sorted(data_dir.glob("**/*")):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".pdf":
            docs.append(parse_pdf(path))
        elif path.suffix.lower() in {".txt", ".md"}:
            docs.append(parse_text(path))
    if docs:
        return docs
    return seed_documents()


def seed_documents() -> list[ClinicalDocument]:
    samples = [
        (
            "SGLT2 inhibitors in heart failure, randomized trial, 2024",
            "Background\nA multicenter randomized controlled trial studied SGLT2 inhibitors in adults with heart failure. "
            "Methods\nSample size n=4744. Outcomes included hospitalization and cardiovascular mortality. "
            "Results\nSGLT2 inhibitors reduced heart-failure hospitalization versus placebo with consistent benefit across diabetic status. "
            "Safety\nGenital infections were increased, while severe hypoglycemia was not increased. "
            "Conclusion\nFor eligible adults with heart failure, SGLT2 inhibitors are supported by high-quality randomized evidence.",
        ),
        (
            "Early case report of SGLT2 inhibitor ketoacidosis, 2017",
            "Background\nA case report described euglycemic ketoacidosis after SGLT2 inhibitor initiation. "
            "Methods\nSingle patient observation, sample size n=1. "
            "Results\nThe event resolved after drug discontinuation and supportive care. "
            "Conclusion\nClinicians should screen for ketoacidosis risk, but this case report does not outweigh randomized trial benefit.",
        ),
        (
            "Hospital guideline for heart failure pharmacotherapy, 2025",
            "Recommendation\nAdults with symptomatic heart failure and adequate renal function should be considered for SGLT2 inhibitor therapy. "
            "Evidence basis\nGuideline panel prioritized randomized trials, meta-analyses, recency, patient comorbidity, and safety monitoring. "
            "Contraindications\nAvoid in active ketoacidosis, severe intolerance, or settings with high dehydration risk. "
            "Monitoring\nAssess renal function, volume status, and infection symptoms after initiation.",
        ),
    ]
    return [
        ClinicalDocument(id=str(uuid4()), text=text, metadata={"title": title, "source": "built-in-seed", "publication_date": title[-4:]})
        for title, text in samples
    ]


def extract_metadata_from_text(text: str) -> dict[str, str | int]:
    metadata: dict[str, str | int] = {}
    year = re.search(r"\b(19|20)\d{2}\b", text)
    sample = re.search(r"\bn\s*[=:]\s*([0-9,]+)\b", text, re.IGNORECASE)
    if year:
        metadata["publication_year"] = int(year.group(0))
    if sample:
        metadata["sample_size"] = int(sample.group(1).replace(",", ""))
    lower = text.lower()
    if "randomized" in lower or "rct" in lower:
        metadata["study_design"] = "RCT"
    elif "meta-analysis" in lower or "systematic review" in lower:
        metadata["study_design"] = "Systematic review"
    elif "guideline" in lower or "recommendation" in lower:
        metadata["study_design"] = "Guideline"
    elif "case report" in lower:
        metadata["study_design"] = "Case report"
    return metadata
