import re


SECTION_PATTERNS = {
    "diagnosis": re.compile(r"diagnosis[:\-]?\s*(.+)", re.IGNORECASE),
    "medication": re.compile(r"medication[s]?[:\-]?\s*(.+)", re.IGNORECASE),
    "followup": re.compile(r"follow[- ]?up[:\-]?\s*(.+)", re.IGNORECASE),
    "hemoglobin": re.compile(r"hemoglobin[:\-]?\s*([0-9.]+)", re.IGNORECASE),
    "wbc": re.compile(r"\bwbc[:\-]?\s*([0-9.]+)", re.IGNORECASE),
    "platelets": re.compile(r"platelets[:\-]?\s*([0-9.]+)", re.IGNORECASE),
    "glucose": re.compile(r"glucose[:\-]?\s*([0-9.]+)", re.IGNORECASE),
    "cholesterol": re.compile(r"cholesterol[:\-]?\s*([0-9.]+)", re.IGNORECASE),
}


def build_machine_readable_payload(text: str, *, file_type: str) -> dict:
    normalized_text = text or ""
    lines = [line.strip() for line in normalized_text.splitlines() if line.strip()]
    paragraphs = [block.strip() for block in normalized_text.split("\n\n") if block.strip()]
    payload = {
        "file_type": file_type,
        "raw_text": normalized_text,
        "sections": {},
        "fields": {},
        "statistics": {
            "character_count": len(normalized_text),
            "word_count": len(normalized_text.split()),
            "line_count": len(lines),
            "paragraph_count": len(paragraphs),
        },
        "preview_lines": lines[:25],
    }

    content = normalized_text
    for name, pattern in SECTION_PATTERNS.items():
        match = pattern.search(content)
        if not match:
            continue
        value = match.group(1).strip()
        if name in {"diagnosis", "medication", "followup"}:
            payload["sections"][name] = value
        else:
            payload["fields"][name] = value

    payload["machine_readable"] = True
    return payload
