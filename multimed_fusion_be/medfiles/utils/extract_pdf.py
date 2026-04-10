def extract_text_from_pdf(path: str) -> str:
    """
    Extract text from PDF file using pypdf.
    Returns empty string if extraction fails.
    """
    try:
        from pypdf import PdfReader

        reader = PdfReader(path)
        parts = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                parts.append(text)

        return "\n".join(parts).strip()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""
