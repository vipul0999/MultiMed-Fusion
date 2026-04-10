import numpy as np
from django.db.models import Q

from medfiles.models import PatientDocChunk
from medfiles.utils.embeddings import embed_query


def _serialize_chunk(chunk, *, score=None):
    return {
        "score": score,
        "chunk_id": chunk.chunk_id,
        "chunk_index": chunk.chunk_index,
        "source_file_id": chunk.source_file_id,
        "source_file_name": chunk.source_file_name,
        "text": chunk.text,
        "source_file_ids": chunk.source_file_ids,
        "source_file_names": chunk.source_file_names,
    }


def top_k_chunks(
    *,
    patient_id: str,
    doctor_id: str,
    query: str,
    file_ids: list[str] = None,
    k: int = 5,
    min_score: float = -1.0,
) -> list[dict]:
    q = (query or "").strip()
    if not q:
        return []

    qv = np.array(embed_query(q), dtype=np.float32)
    queryset = PatientDocChunk.objects.filter(patient_id=patient_id, doctor_id=doctor_id)

    if file_ids:
        queryset = queryset.filter(source_file_id__in=[str(file_id) for file_id in file_ids])

    scored = []
    for chunk in queryset:
        if not chunk.embedding:
            continue
        ev = np.array(chunk.embedding, dtype=np.float32)
        score = float(np.dot(qv, ev))
        if score < float(min_score):
            continue

        scored.append(_serialize_chunk(chunk, score=score))

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:k]


def get_chunks_by_file_ids(*, patient_id: str, doctor_id: str, file_ids: list[str]) -> list[dict]:
    if not file_ids:
        return []

    queryset = (
        PatientDocChunk.objects.filter(
            patient_id=patient_id,
            doctor_id=doctor_id,
            source_file_id__in=[str(file_id) for file_id in file_ids],
        )
        .order_by("source_file_id", "chunk_index")
    )
    return [_serialize_chunk(chunk, score=1.0) for chunk in queryset]
