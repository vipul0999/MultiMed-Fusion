from django.db import models
from django.conf import settings
from django_mongodb_backend.fields import ObjectIdAutoField

User = settings.AUTH_USER_MODEL
app = "portal"


class PatientDoctorAccess(models.Model):
    """
    Access relationship between a Doctor and a Patient.
    Status flow:
      - pending: doctor requested, patient must approve/reject
      - approved: patient approved OR patient granted directly
      - rejected: patient rejected
      - revoked: either side revoked (optional)
    """
    id = ObjectIdAutoField(primary_key=True)

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        REVOKED = "revoked", "Revoked"

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_links")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_links")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    requested_by = models.CharField(
        max_length=20,
        choices=[("doctor", "Doctor"), ("patient", "Patient")],
    )
    note = models.CharField(max_length=500, blank=True, default="")
    consent_expires_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["doctor", "patient"], name="uniq_doctor_patient")
        ]

    def __str__(self):
        return f"{self.doctor_id} <-> {self.patient_id} ({self.status})"


from django_mongodb_backend.fields import ObjectIdAutoField
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class FileUploadRequest(models.Model):
    id = ObjectIdAutoField(primary_key=True)

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="upload_requests_sent")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="upload_requests_received")

    message = models.CharField(max_length=500, blank=True, default="")
    is_open = models.BooleanField(default=True)  # still active?
    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
