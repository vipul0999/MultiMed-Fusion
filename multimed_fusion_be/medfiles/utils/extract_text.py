from .extract_pdf import extract_text_from_pdf
from .extract_docx import extract_text_from_docx
from .transcribe_audio import transcribe_audio_to_text
from .extract_image import extract_text_from_image
from .extract_textfile import extract_text_from_textfile
from .extract_dicom import extract_text_from_dicom

def extract_text_by_filetype(file_type: str, path: str) -> str:
    """
    Extract text from files based on type.
    """
    ft = (file_type or "").lower()

    if ft == "pdf":
        return extract_text_from_pdf(path)
    if ft == "docx":
        return extract_text_from_docx(path)
    if ft == "doc":
        return extract_text_from_textfile(path)
    if ft == "text":
        return extract_text_from_textfile(path)
    if ft == "image":
        return extract_text_from_image(path)
    if ft == "dicom":
        return extract_text_from_dicom(path)
    if ft in {"mp3", "wav", "m4a", "ogg", "flac", "opus", "audio"}:
        return transcribe_audio_to_text(path)
    return ""
