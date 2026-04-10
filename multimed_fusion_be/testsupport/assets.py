import os
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile


WINDOWS_TEST_DATA_DIR = Path(r"C:\Users\s576701\Documents\gdp files")
WSL_TEST_DATA_DIR = Path("/mnt/c/Users/s576701/Documents/gdp files")

TEST_DATA_DIR = Path(os.getenv("GDP_TEST_DATA_DIR", WSL_TEST_DATA_DIR))
if not TEST_DATA_DIR.exists():
    TEST_DATA_DIR = WSL_TEST_DATA_DIR if WSL_TEST_DATA_DIR.exists() else WINDOWS_TEST_DATA_DIR


ASSET_FILES = {
    "pdf": ("pdf_file2.pdf", "application/pdf"),
    "docx": ("document4.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    "image": ("images2.png", "image/png"),
    "audio": ("audios4.mp3", "audio/mpeg"),
}


FALLBACK_CONTENT = {
    ".txt": b"Diagnosis: Hypertension\nMedication: ACE inhibitor\nFollow-up: 2 weeks\nDOB: 01/01/1990",
    ".jpg": b"\xff\xd8\xff\xe0mockjpg",
    ".jpeg": b"\xff\xd8\xff\xe0mockjpeg",
    ".wav": b"RIFFmockwavefmt ",
    ".dcm": b"DICMmockdicom",
    ".png": b"\x89PNG\r\n\x1a\nmockpng",
    ".pdf": b"%PDF-1.4\nmock pdf",
    ".mp3": b"ID3mockmp3",
}


def resolve_asset_path(kind: str) -> Path | None:
    filename = ASSET_FILES[kind][0]
    path = TEST_DATA_DIR / filename
    return path if path.exists() else None


def make_uploaded_file(filename: str, *, kind: str | None = None, content_type: str | None = None, content: bytes | None = None):
    extension = Path(filename).suffix.lower()

    if kind in ASSET_FILES:
        path = resolve_asset_path(kind)
        if path:
            final_content_type = content_type or ASSET_FILES[kind][1]
            return SimpleUploadedFile(filename, path.read_bytes(), content_type=final_content_type)

    final_content = content if content is not None else FALLBACK_CONTENT.get(extension, b"mock-file")
    final_content_type = content_type or {
        ".txt": "text/plain",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".wav": "audio/wav",
        ".dcm": "application/dicom",
        ".png": "image/png",
        ".pdf": "application/pdf",
        ".mp3": "audio/mpeg",
    }.get(extension, "application/octet-stream")
    return SimpleUploadedFile(filename, final_content, content_type=final_content_type)
