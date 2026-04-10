import re


DATE_PATTERNS = [
    re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)"),
    re.compile(r"(?<!\d)\d{2}/\d{2}/\d{4}(?!\d)"),
    re.compile(r"(?<!\d)\d{2}-\d{2}-\d{4}(?!\d)"),
]


def anonymize_patient_text(text: str, patient=None) -> str:
    value = text or ""
    if patient is not None:
        replacements = {
            getattr(patient, "username", ""): "[PATIENT]",
            getattr(patient, "email", ""): "[PATIENT_EMAIL]",
            str(getattr(patient, "id", "")): "[PATIENT_ID]",
        }
        for raw, token in replacements.items():
            if raw:
                value = value.replace(raw, token)

    for pattern in DATE_PATTERNS:
        value = pattern.sub("[REDACTED_DATE]", value)

    return value


def anonymize_filename(filename: str, patient=None) -> str:
    base = anonymize_patient_text(filename or "", patient=patient)
    return re.sub(r"\s+", "_", base).strip("_")


def sanitize_log_value(value: str, patient=None) -> str:
    return anonymize_patient_text(value, patient=patient)
