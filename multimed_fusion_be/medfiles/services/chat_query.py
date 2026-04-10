from typing import List, Optional

from medfiles.models import PatientFile
from medfiles.services.gemini_service import send_chunks_to_gemini, send_documents_to_gemini
from medfiles.utils.retrieval import get_chunks_by_file_ids, top_k_chunks


def build_context(chunks: List[dict], max_chars: int = 7000) -> str:
    parts = []
    current_length = 0
    for chunk in chunks:
        section = (
            f"File(s): {', '.join(chunk.get('source_file_names', []))}\n"
            f"Chunk: {chunk.get('chunk_id', '')}\n"
            f"{(chunk.get('text') or '').strip()}\n"
        )

        parts.append(section)
        current_length += len(section)
    return "\n---\n".join(parts)


def build_fallback_summary(chunks: List[dict]) -> str:
    if not chunks:
        return "Not found in the selected files."
    lines = []
    for chunk in chunks:
        candidate = " ".join((chunk.get("text") or "").split())
        if candidate:
            lines.append(candidate)
    return " ".join(lines) if lines else "Not found in the selected files."


def build_document_payloads(*, patient_id: str, doctor_id: str, file_ids: List[str]) -> List[dict]:
    if not file_ids:
        return []

    files_by_id = {
        str(file_obj.id): file_obj
        for file_obj in PatientFile.objects.filter(
            id__in=[str(file_id) for file_id in file_ids],
            patient_id=patient_id,
            doctor_id=doctor_id,
            is_disposed=False,
        )
    }
    chunks_by_file_id = {}
    for chunk in get_chunks_by_file_ids(patient_id=patient_id, doctor_id=doctor_id, file_ids=file_ids):
        source_file_id = str(chunk.get("source_file_id") or "")
        text_value = (chunk.get("text") or "").strip()
        if not source_file_id or not text_value:
            continue
        chunks_by_file_id.setdefault(source_file_id, []).append(text_value)

    documents = []
    for file_id in file_ids:
        file_obj = files_by_id.get(str(file_id))
        if not file_obj:
            continue
        text = (file_obj.extracted_text or "").strip()
        if not text:
            text = "\n\n".join(chunks_by_file_id.get(str(file_id), [])).strip()
        if not text:
            continue
        documents.append(
            {
                "file_id": str(file_obj.id),
                "file_name": file_obj.original_name,
                "display_name": file_obj.display_name,
                "title": file_obj.title,
                "file_type": file_obj.file_type,
                "file_path": getattr(file_obj.file, "path", ""),
                "text": text,
            }
        )
    return documents


def build_document_fallback_summary(documents: List[dict]) -> str:
    if not documents:
        return "Not found in the selected files."
    excerpts = []
    for document in documents[:3]:
        candidate = " ".join((document.get("text") or "").split())
        if candidate:
            excerpts.append(candidate[:220])
    return " ".join(excerpts) if excerpts else "Not found in the selected files."


def run_chat_query(
    *,
    patient_id: str,
    doctor_id: str,
    message: str,
    file_ids: Optional[List[str]] = None,
    conversation_history: Optional[List[dict]] = None,
    k: int = 6,
    use_gemini: bool = True,
) -> dict:
    if file_ids:
        documents = build_document_payloads(patient_id=patient_id, doctor_id=doctor_id, file_ids=file_ids)
        hits = []
        retrieval_mode = "selected_file_full_context"
    else:
        documents = []
        hits = top_k_chunks(
            patient_id=patient_id,
            doctor_id=doctor_id,
            query=message,
            file_ids=None,
            k=100,
            min_score=-1.0,
        )
        retrieval_mode = "semantic_top_k"
    context = build_context(hits)
    result = {
        "hits": hits,
        "context": context,
        "chunks_used": len(hits),
        "retrieval_mode": retrieval_mode,
        "source_file_ids": [str(file_id) for file_id in (file_ids or [])] if documents else [],
    }

    if file_ids and documents and use_gemini:
        gemini_result = send_documents_to_gemini(
            question=message,
            documents=documents,
            conversation_history=conversation_history or [],
        )
        result.update(
            {
                "gemini_ok": gemini_result.get("ok", False),
                "answer": gemini_result.get("answer") or "Not found in the selected files.",
                "confidence": gemini_result.get("confidence", "medium"),
                "sources": gemini_result.get("sources", []),
                "context": "",
            }
        )
        if gemini_result.get("error"):
            result["error"] = gemini_result["error"]
        return result

    if file_ids and documents:
        result.update(
            {
                "gemini_ok": False,
                "answer": build_document_fallback_summary(documents),
                "confidence": "medium",
                "sources": [document.get("file_name") for document in documents if document.get("file_name")],
                "context": "",
            }
        )
        return result

    if not hits and not documents:
        result.update(
            {
                "gemini_ok": False,
                "answer": "Not found in the selected files.",
                "confidence": "low",
                "sources": [],
                "error": "No relevant chunks found for this query.",
            }
        )
        return result

    if use_gemini:
        gemini_result = send_chunks_to_gemini(
            question=message,
            chunks=hits,
            conversation_history=conversation_history or [],
        )
        result.update(
            {
                "gemini_ok": gemini_result.get("ok", False),
                "answer": gemini_result.get("answer") or build_fallback_summary(hits),
                "confidence": gemini_result.get("confidence", "medium"),
                "sources": gemini_result.get("sources", []),
            }
        )
        if gemini_result.get("error"):
            result["error"] = gemini_result["error"]
        return result

    result.update(
        {
            "gemini_ok": False,
            "answer": build_fallback_summary(hits),
            "confidence": "medium",
            "sources": [],
        }
    )
    return result
