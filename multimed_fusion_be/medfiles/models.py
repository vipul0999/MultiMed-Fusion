import hashlib
import os

from django.conf import settings
from django.db import models
from django_mongodb_backend.fields import ArrayField, ObjectIdAutoField

User = settings.AUTH_USER_MODEL
app = "medfiles"


def safe_patient_token(patient_id: str) -> str:
    raw = f"{patient_id}:{settings.SECRET_KEY}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    token = safe_patient_token(str(instance.patient_id))
    return f"patients/{token}/doctor_{instance.doctor_id}/{instance.id}{ext}"


class PatientFile(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_files")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_files")

    original_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=255, blank=True, default="")
    description = models.CharField(max_length=500, blank=True, default="")
    mime_type = models.CharField(max_length=120, blank=True, default="")
    file_type = models.CharField(max_length=20, default="unknown")
    extension = models.CharField(max_length=20, blank=True, default="")
    file_size = models.BigIntegerField(default=0)
    sha256 = models.CharField(max_length=64, blank=True, default="", db_index=True)
    uploaded_by_role = models.CharField(max_length=20, default="patient")
    file = models.FileField(upload_to=upload_path)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=20, default="uploaded")
    processing_steps = models.JSONField(default=list)
    extracted_text = models.TextField(blank=True, default="")
    extracted_payload = models.JSONField(default=dict)
    summary = models.TextField(blank=True, default="")
    last_error = models.CharField(max_length=500, blank=True, default="")
    last_processed_at = models.DateTimeField(null=True, blank=True)

    authorized_until = models.DateTimeField(null=True, blank=True)
    is_disposed = models.BooleanField(default=False)
    disposed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["patient", "doctor", "uploaded_at"]),
            models.Index(fields=["patient", "doctor", "is_disposed"]),
        ]

    def __str__(self):
        return f"{self.display_name or self.original_name} ({self.patient_id}->{self.doctor_id})"


class PatientDocChunk(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doc_chunks_as_patient")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doc_chunks_as_doctor")
    batch_hash = models.CharField(max_length=64, db_index=True)
    chunk_id = models.CharField(max_length=120, db_index=True, default="")
    chunk_index = models.IntegerField()
    source_file_id = models.CharField(max_length=64, db_index=True, default="")
    source_file_name = models.CharField(max_length=255, default="")
    text = models.TextField()
    source_file_ids = ArrayField(models.CharField(max_length=64), default=list)
    source_file_names = ArrayField(models.CharField(max_length=255), default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = models.JSONField(default=list)
    embedding_model = models.CharField(max_length=80, default="BAAI/bge-small-en-v1.5")
    embedding_norm = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["patient", "doctor", "chunk_id"], name="uniq_patient_doctor_chunkid"),
        ]
        indexes = [
            models.Index(fields=["patient", "doctor", "batch_hash"]),
        ]

    def __str__(self):
        return f"{self.chunk_id} ({self.patient_id}->{self.doctor_id})"
