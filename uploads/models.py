from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FileUpload(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.file.name} ({self.owner})"

from django.db import models
from django.conf import settings
import uuid
import os

def upload_to_patient_folder(instance, filename):
    # Files stored in MEDIA_ROOT/patient_uploads/<patient_id>/<uuid>_<filename>
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('patient_uploads', str(instance.patient.id), new_filename)

class PatientFile(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_files')
    file = models.FileField(upload_to=upload_to_patient_folder)
    filename = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=50)
    upload_time = models.DateTimeField(auto_now_add=True)
    # Optional: encrypted_path if you implement encryption
    encrypted_path = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return f"{self.filename} ({self.patient.username})"
