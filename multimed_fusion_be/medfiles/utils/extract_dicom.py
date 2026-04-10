def extract_text_from_dicom(path: str) -> str:
    try:
        import pydicom  # type: ignore
    except Exception:
        pydicom = None

    if pydicom is not None:
        try:
            ds = pydicom.dcmread(path, force=True)
            parts = []
            for key in ("StudyDescription", "SeriesDescription", "BodyPartExamined", "Modality", "ProtocolName"):
                value = getattr(ds, key, "")
                if value:
                    parts.append(f"{key}: {value}")
            return "\n".join(parts).strip()
        except Exception:
            pass

    try:
        with open(path, "rb") as handle:
            raw = handle.read().decode("latin-1", errors="ignore")
        return raw[:4000].strip()
    except Exception:
        return ""
