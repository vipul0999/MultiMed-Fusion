def extract_text_from_textfile(path: str) -> str:
    encodings = ["utf-8", "utf-16", "latin-1"]
    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding, errors="ignore") as handle:
                return handle.read().strip()
        except UnicodeDecodeError:
            continue
        except Exception:
            return ""
    return ""
