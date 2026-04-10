def extract_text_from_docx(path: str) -> str:
    """
    Extract text from DOCX file using python-docx.
    Returns empty string if extraction fails.
    """
    try:
        import docx

        doc = docx.Document(path)
        parts = [p.text for p in doc.paragraphs if (p.text or "").strip()]
        return "\n".join(parts).strip()
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""
