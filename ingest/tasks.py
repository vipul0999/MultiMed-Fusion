from celery import shared_task
from uploads.models import PatientFile
from ingest.utils import extract_text
from ingest.vectorize import store_text_in_qdrant


@shared_task
def ingest_patient_file(file_id):
    """
    Async task that extracts text from any patient file type,
    vectorizes it, and stores in Qdrant with patient/doctor context.
    """
    from uploads.models import PatientFile  # avoid circular imports

    try:
        pf = PatientFile.objects.get(id=file_id)

        # Extract text (PDF, audio, etc.)
        text = extract_text(pf.file.path)
        if not text.strip():
            return f"No text extracted from {pf.filename}"

        # Prepare metadata
        payload = {
            "file_id": pf.id,
            "patient_id": pf.patient.id if pf.patient else None,
            "doctor_id": pf.doctor.id if pf.doctor else None,
            "filename": pf.filename,
            "mime_type": pf.mime_type,
        }

        # Store in Qdrant
        n_points = store_text_in_qdrant(pf.id, text, payload)

        return f"Ingested {n_points} vectors for file {pf.filename}"

    except Exception as e:
        return f"Error ingesting file {file_id}: {e}"
