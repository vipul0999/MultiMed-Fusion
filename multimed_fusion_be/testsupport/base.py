import shutil
import tempfile
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from medfiles.models import PatientDocChunk, PatientFile
from portal.models import PatientDoctorAccess
from testsupport.assets import make_uploaded_file

User = get_user_model()
TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class WorkflowTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = APIClient()
        self.doctor = User.objects.create_user(
            username="doctor11",
            email="doctor11@example.com",
            password="password",
            role="doctor",
        )
        self.patient = User.objects.create_user(
            username="patient11",
            email="patient11@example.com",
            password="password",
            role="patient",
        )
        self.other_doctor = User.objects.create_user(
            username="doctor22",
            email="doctor22@example.com",
            password="password",
            role="doctor",
        )
        self.admin = User.objects.create_user(
            username="admin11",
            email="admin11@example.com",
            password="password",
            role="admin",
        )
        self.rel = PatientDoctorAccess.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            status=PatientDoctorAccess.Status.APPROVED,
            requested_by="patient",
            consent_expires_at=timezone.now() + timedelta(days=7),
            approved_at=timezone.now(),
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def patient_upload(self, filename, *, kind=None, content_type=None, content=None):
        self.authenticate(self.patient)
        response = self.client.post(
            "/api/medfiles/patient/upload/",
            {
                "doctor_id": str(self.doctor.id),
                "files": [make_uploaded_file(filename, kind=kind, content_type=content_type, content=content)],
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        return response

    def patient_upload_many(self, uploads):
        self.authenticate(self.patient)
        files = [
            make_uploaded_file(item["filename"], kind=item.get("kind"), content_type=item.get("content_type"),
                               content=item.get("content"))
            for item in uploads
        ]
        response = self.client.post(
            "/api/medfiles/patient/upload/",
            {"doctor_id": str(self.doctor.id), "files": files},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        return response

    def doctor_upload(self, filename, *, kind=None, content_type=None, content=None):
        self.authenticate(self.doctor)
        response = self.client.post(
            "/api/medfiles/doctor/patient-upload/",
            {
                "patient_id": str(self.patient.id),
                "files": [make_uploaded_file(filename, kind=kind, content_type=content_type, content=content)],
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        return response

    def analyze(self, file_ids):
        self.authenticate(self.doctor)
        response = self.client.post(
            "/api/medfiles/doctor/analyze/",
            {"patient_id": str(self.patient.id), "doctor_id": str(self.doctor.id), "file_ids": file_ids},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        return response

    def chat(self, *, message, file_ids=None, extra=None, expected_status=200):
        self.authenticate(self.doctor)
        payload = {
            "patient_id": str(self.patient.id),
            "doctor_id": str(self.doctor.id),
            "message": message,
            "top_k": 5,
        }
        if file_ids is not None:
            payload["file_ids"] = file_ids
        if extra:
            payload.update(extra)
        response = self.client.post("/api/medfiles/doctor/chat-query/", payload, format="json")
        self.assertEqual(response.status_code, expected_status)
        return response

    def create_chunk(self, *, text, embedding, file_obj, chunk_index=0):
        return PatientDocChunk.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            batch_hash="batch-1",
            chunk_id=f"{file_obj.id}:{chunk_index}",
            chunk_index=chunk_index,
            source_file_id=str(file_obj.id),
            source_file_name=file_obj.display_name or file_obj.original_name,
            text=text,
            embedding=embedding,
            source_file_ids=[str(file_obj.id)],
            source_file_names=[file_obj.display_name or file_obj.original_name],
        )

    def latest_file(self):
        return PatientFile.objects.order_by("-uploaded_at").first()
