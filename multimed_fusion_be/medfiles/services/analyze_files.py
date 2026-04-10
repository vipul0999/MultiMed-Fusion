from datetime import datetime
from typing import List

from django.db import transaction
from django.utils import timezone

from medfiles.models import PatientDocChunk, PatientFile
from medfiles.utils.chunking import chunk_text
from medfiles.utils.embeddings import embed_texts, embedding_model_name
from medfiles.utils.extract_text import extract_text_by_filetype
from medfiles.utils.hashing import sha256_hex
from medfiles.utils.sanitization import anonymize_patient_text
from medfiles.utils.structured_data import build_machine_readable_payload


def build_chunk_id_for_file(file_id: str, idx: int) -> str:
    return f"{file_id}:{idx}"


def summarize_text(text: str, *, limit: int = 320) -> str:
    compact = " ".join((text or "").split())
    if len(compact) <= limit:
        return compact
    return f"{compact[: limit - 3]}..."


@transaction.atomic
def analyze_and_store_chunks(*, doctor, patient, files: List[PatientFile]) -> dict:
    created_count = 0
    errors = []
    chunk_payloads = []

    all_file_ids = sorted(str(file_obj.id) for file_obj in files)
    batch_hash = sha256_hex("||".join(all_file_ids))

    for file_obj in files:
        try:
            file_obj.processing_status = "extracting"
            file_obj.processing_steps = ["extract_text_started"]
            file_obj.last_error = ""
            file_obj.save()

            PatientDocChunk.objects.filter(
                patient=patient,
                doctor=doctor,
                source_file_ids__contains=[str(file_obj.id)],
            ).delete()

            extracted_text = extract_text_by_filetype(file_obj.file_type, file_obj.file.path)
            if not extracted_text.strip():
                raise ValueError("No text could be extracted from this file.")

            sanitized_text = anonymize_patient_text(extracted_text, patient=patient)
            payload = build_machine_readable_payload(sanitized_text, file_type=file_obj.file_type)
            display_name = file_obj.display_name or file_obj.original_name
            wrapped_text = f"[SOURCE_FILE={display_name}]\n{sanitized_text}"
            chunks = chunk_text(wrapped_text, chunk_size=1100, overlap=180)
            if not chunks:
                raise ValueError("No retrieval chunks were generated from this file.")

            payload["extraction"] = {
                "source_file_id": str(file_obj.id),
                "source_file_name": display_name,
                "mime_type": file_obj.mime_type,
                "file_type": file_obj.file_type,
                "extension": file_obj.extension,
                "uploaded_by_role": file_obj.uploaded_by_role,
                "chunk_count": len(chunks),
            }

            file_obj.extracted_text = sanitized_text
            file_obj.extracted_payload = payload
            file_obj.summary = summarize_text(sanitized_text)
            file_obj.processing_status = "embedding"
            file_obj.processing_steps = ["extract_text_started", "extract_text_completed", "chunking_completed"]
            file_obj.save()

            for chunk_index, text_value in enumerate(chunks):
                chunk_payloads.append(
                    {
                        "file_obj": file_obj,
                        "chunk_index": chunk_index,
                        "text": text_value,
                    }
                )
        except Exception as exc:
            file_obj.processing_status = "failed"
            file_obj.last_error = str(exc)
            file_obj.processing_steps = file_obj.processing_steps + ["processing_failed"]
            file_obj.is_processed = False
            file_obj.last_processed_at = timezone.now()
            file_obj.save()
            errors.append(
                {
                    "file_id": str(file_obj.id),
                    "file_name": file_obj.original_name,
                    "error": str(exc),
                }
            )

    if not chunk_payloads:
        return {
            "batch_hash": batch_hash,
            "chunks_created": 0,
            "errors": errors,
            "embedding_model": embedding_model_name(),
        }

    embeddings = []
    batch_size = 24
    for idx in range(0, len(chunk_payloads), batch_size):
        batch = chunk_payloads[idx : idx + batch_size]
        embeddings.extend(embed_texts([item["text"] for item in batch]))

    for item, vector in zip(chunk_payloads, embeddings):
        file_obj = item["file_obj"]
        PatientDocChunk.objects.create(
            patient=patient,
            doctor=doctor,
            batch_hash=batch_hash,
            chunk_id=build_chunk_id_for_file(str(file_obj.id), item["chunk_index"]),
            chunk_index=item["chunk_index"],
            source_file_id=str(file_obj.id),
            source_file_name=file_obj.display_name or file_obj.original_name,
            text=item["text"],
            embedding=vector,
            embedding_model=embedding_model_name(),
            embedding_norm=True,
            source_file_ids=[str(file_obj.id)],
            source_file_names=[file_obj.display_name or file_obj.original_name],
        )
        created_count += 1

    processed_at = timezone.now()
    for file_obj in files:
        if not file_obj.last_error:
            file_obj.processing_status = "processed"
            file_obj.processing_steps = file_obj.processing_steps + ["embedding_completed"]
            file_obj.is_processed = True
            file_obj.last_processed_at = processed_at
            file_obj.save()

    return {
        "batch_hash": batch_hash,
        "chunks_created": created_count,
        "embedding_model": embedding_model_name(),
        "errors": errors,
        "processed_at": processed_at.isoformat(),
    }
