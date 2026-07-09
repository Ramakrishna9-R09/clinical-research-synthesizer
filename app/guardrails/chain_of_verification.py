from __future__ import annotations

import re


def verify_report(report_markdown: str, evidence: list[dict]) -> dict:
    warnings: list[str] = []
    cited_ids = set(re.findall(r"\[(C\d+)\]", report_markdown))
    known_ids = {item.get("citation_id") for item in evidence}
    missing = cited_ids - known_ids
    if missing:
        warnings.append(f"Unknown citation ids found: {', '.join(sorted(missing))}.")
    if "## Supporting Evidence" not in report_markdown:
        warnings.append("Report is missing a Supporting Evidence section.")
    if evidence and not cited_ids:
        warnings.append("Report contains evidence but no inline citation identifiers.")
    return {"is_verified": not warnings, "warnings": warnings, "checked_citations": sorted(cited_ids)}
