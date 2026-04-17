import re


DATE_PATTERNS = [
    re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)"),
    re.compile(r"(?<!\d)\d{2}/\d{2}/\d{4}(?!\d)"),
    re.compile(r"(?<!\d)\d{2}-\d{2}-\d{4}(?!\d)"),
]


# def anonymize_patient_text(text: str, patient=None) -> str:
#     value = text or ""
#     if patient is not None:
#         replacements = {
#             getattr(patient, "username", ""): "[PATIENT]",
#             getattr(patient, "email", ""): "[PATIENT_EMAIL]",
#             str(getattr(patient, "id", "")): "[PATIENT_ID]",
#         }
#         for raw, token in replacements.items():
#             if raw:
#                 value = value.replace(raw, token)
#
#     for pattern in DATE_PATTERNS:
#         value = pattern.sub("[REDACTED_DATE]", value)
#
#     return value

import re
from typing import Optional

# ── Date patterns ────────────────────────────────────────────────────────────
DATE_PATTERNS: list[re.Pattern] = [
    # ISO: 2024-01-31
    re.compile(r'\b\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\b'),
    # US long: January 31, 2024 / Jan 31, 2024
    re.compile(
        r'\b(?:January|February|March|April|May|June|July|August|September|'
        r'October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'\.?\s+\d{1,2},?\s+\d{4}\b',
        re.IGNORECASE,
    ),
    # DD/MM/YYYY or MM/DD/YYYY
    re.compile(r'\b(?:0?[1-9]|[12]\d|3[01])[/\-.](?:0?[1-9]|1[0-2])[/\-.]\d{2,4}\b'),
    # DD Mon YYYY: 31 Jan 2024
    re.compile(
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|'
        r'September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|'
        r'Oct|Nov|Dec)\.?\s+\d{4}\b',
        re.IGNORECASE,
    ),
]

# ── PII patterns ─────────────────────────────────────────────────────────────
_EMAIL_RE   = re.compile(r'\b[\w.+-]+@[\w-]+\.[\w.]+\b')
_PHONE_RE   = re.compile(
    r'(?<!\w)'
    r'(?:\+?1[\s\-.]?)?'                      # optional country code
    r'(?:\(?\d{3}\)?[\s\-.]?)'                # area code
    r'\d{3}[\s\-.]\d{4}'
    r'(?!\w)'
)
_SSN_RE     = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
_MRN_RE     = re.compile(r'\bMRN[:\s#]*\d+\b', re.IGNORECASE)
_ZIP_RE     = re.compile(r'\b\d{5}(?:-\d{4})?\b')
_AGE_RE     = re.compile(r'\b(?:age[d]?[\s:]+)?\d{1,3}(?:\s*-?\s*year(?:s)?(?:\s*-?\s*old)?)\b', re.IGNORECASE)
_INITIALS_RE= re.compile(r'\b[A-Z]\.[A-Z]\.(?:[A-Z]\.)?\b')   # e.g. J.D. or J.D.R.

# Name detection: Title + Capitalized word(s)
_NAME_RE    = re.compile(
    r'\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Mx)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
)

# Street address: number + street name + suffix
_ADDR_RE    = re.compile(
    r'\b\d{1,5}\s+[A-Z][a-zA-Z\s]{2,30}'
    r'(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|'
    r'Court|Ct|Place|Pl|Way|Circle|Cir|Highway|Hwy)\.?\b',
    re.IGNORECASE,
)

# IP addresses
_IP_RE      = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# ── Ordered replacement table ─────────────────────────────────────────────────
# Order matters: more-specific patterns before generic ones.
_PII_RULES: list[tuple[re.Pattern, str]] = [
    (_SSN_RE,      "[REDACTED_SSN]"),
    (_MRN_RE,      "[REDACTED_MRN]"),
    (_EMAIL_RE,    "[REDACTED_EMAIL]"),
    (_PHONE_RE,    "[REDACTED_PHONE]"),
    (_IP_RE,       "[REDACTED_IP]"),
    (_ADDR_RE,     "[REDACTED_ADDRESS]"),
    (_NAME_RE,     "[REDACTED_NAME]"),
    (_INITIALS_RE, "[REDACTED_INITIALS]"),
    (_AGE_RE,      "[REDACTED_AGE]"),
    (_ZIP_RE,      "[REDACTED_ZIP]"),
]


import re

PHONE_PATTERN = re.compile(r'\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
EMAIL_PATTERN = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b')


def anonymize_patient_text(text: str, patient=None) -> str:
    value = text or ""

    if patient is not None:
        replacements = {
            getattr(patient, "username", ""): "[PATIENT]",
            getattr(patient, "email", ""): "[PATIENT_EMAIL]",
        }

        for raw, token in replacements.items():
            if raw:
                value = value.replace(raw, token)

    value = PHONE_PATTERN.sub("[REDACTED_PHONE]", value)
    value = SSN_PATTERN.sub("[REDACTED_SSN]", value)
    value = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", value)

    for pattern in DATE_PATTERNS:
        value = pattern.sub("[REDACTED_DATE]", value)

    return value


def anonymize_filename(filename: str, patient=None) -> str:
    base = anonymize_patient_text(filename or "", patient=patient)
    return re.sub(r"\s+", "_", base).strip("_")


def sanitize_log_value(value: str, patient=None) -> str:
    return anonymize_patient_text(value, patient=patient)
