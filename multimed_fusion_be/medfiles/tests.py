import shutil
import tempfile
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from medfiles.models import PatientDocChunk, PatientFile
from medfiles.services.disposal import dispose_expired_files
from portal.models import PatientDoctorAccess

User = get_user_model()
TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class MedfilesWorkflowTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = APIClient()
        self.doctor = User.objects.create_user(
            username="doctor1",
            email="doctor1@example.com",
            password="password123",
            role="doctor",
        )
        self.patient = User.objects.create_user(
            username="john.doe",
            email="john.doe@example.com",
            password="password123",
            role="patient",
        )
        self.rel = PatientDoctorAccess.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            status=PatientDoctorAccess.Status.APPROVED,
            requested_by="patient",
            consent_expires_at=timezone.now() + timedelta(days=7),
        )

    def upload_as_patient(self, name, content=b"sample", content_type="application/octet-stream"):
        self.client.force_authenticate(user=self.patient)
        response = self.client.post(
            "/api/medfiles/patient/upload/",
            {"doctor_id": str(self.doctor.id), "files": [SimpleUploadedFile(name, content, content_type=content_type)]},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        return response

    def test_upload_supports_required_modalities_and_returns_confirmation(self):
        cases = [
            ("lab_report.pdf", b"%PDF-1.4", "application/pdf", "pdf"),
            ("summary.txt", b"Diagnosis: stable", "text/plain", "text"),
            ("scan.png", b"png-bytes", "image/png", "image"),
            ("scan.jpg", b"jpg-bytes", "image/jpeg", "image"),
            ("scan.dcm", b"DICMcontent", "application/dicom", "dicom"),
            ("note.mp3", b"ID3audio", "audio/mpeg", "mp3"),
            ("note.wav", b"RIFFaudio", "audio/wav", "wav"),
        ]
        for filename, content, content_type, expected_type in cases:
            response = self.upload_as_patient(filename, content, content_type)
            self.assertEqual(response.data["message"], "Upload successful")
            self.assertEqual(response.data["data"][0]["file_type"], expected_type)

    @patch("medfiles.services.analyze_files.embed_texts", return_value=[[0.1, 0.2, 0.3]])
    @patch("medfiles.services.analyze_files.extract_text_by_filetype", return_value="Diagnosis: Flu\nMedication: Rest\nFollow-up: 2 weeks")
    def test_analysis_creates_machine_readable_payload_and_embeddings(self, *_mocks):
        upload = self.upload_as_patient("report.txt", b"Diagnosis: Flu")
        file_id = upload.data["data"][0]["id"]
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post(
            "/api/medfiles/doctor/analyze/",
            {"patient_id": str(self.patient.id), "doctor_id": str(self.doctor.id), "file_ids": [file_id]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        file_obj = PatientFile.objects.get(id=file_id)
        self.assertTrue(file_obj.is_processed)
        self.assertEqual(file_obj.processing_status, "processed")
        self.assertTrue(file_obj.extracted_payload["machine_readable"])
        self.assertIn("diagnosis", file_obj.extracted_payload["sections"])
        self.assertEqual(PatientDocChunk.objects.filter(source_file_ids__contains=[file_id]).count(), 1)

    @patch("medfiles.services.analyze_files.extract_text_by_filetype", return_value="")
    @patch("medfiles.services.analyze_files.embed_texts")
    def test_failed_audio_transcription_blocks_vectorization(self, embed_mock, _extract_mock):
        upload = self.upload_as_patient("bad_audio.mp3", b"broken-audio", "audio/mpeg")
        file_id = upload.data["data"][0]["id"]
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post(
            "/api/medfiles/doctor/analyze/",
            {"patient_id": str(self.patient.id), "doctor_id": str(self.doctor.id), "file_ids": [file_id]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        file_obj = PatientFile.objects.get(id=file_id)
        self.assertEqual(file_obj.processing_status, "failed")
        self.assertEqual(PatientDocChunk.objects.count(), 0)
        embed_mock.assert_not_called()

    def test_uploaded_filename_is_anonymized_for_display(self):
        response = self.upload_as_patient("john.doe_1990-10-01_report.pdf", b"%PDF-1.4", "application/pdf")
        display_name = response.data["data"][0]["display_name"]
        self.assertNotIn("john.doe", display_name.lower())
        self.assertNotIn("1990-10-01", display_name)

    def test_authorized_doctor_can_list_patient_files(self):
        self.upload_as_patient("report.pdf", b"%PDF-1.4", "application/pdf")
        self.client.force_authenticate(user=self.doctor)
        response = self.client.get("/api/medfiles/doctor/patients/{}/files/".format(self.patient.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_doctor_is_blocked_from_file_access_and_search(self):
        other_doctor = User.objects.create_user(
            username="doctor2",
            email="doctor2@example.com",
            password="password123",
            role="doctor",
        )
        self.upload_as_patient("report.pdf", b"%PDF-1.4", "application/pdf")
        self.client.force_authenticate(user=other_doctor)
        list_response = self.client.get("/api/medfiles/doctor/patients/{}/files/".format(self.patient.id))
        self.assertEqual(list_response.status_code, 403)
        query_response = self.client.post(
            "/api/medfiles/doctor/chat-query/",
            {
                "patient_id": str(self.patient.id),
                "doctor_id": str(other_doctor.id),
                "message": "What is the diagnosis?",
                "top_k": 5,
            },
            format="json",
        )
        self.assertEqual(query_response.status_code, 403)

    @patch(
        "medfiles.views.run_chat_query",
        return_value={
            "hits": [
                {
                    "score": 0.95,
                    "chunk_id": "a:0",
                    "chunk_index": 0,
                    "text": "Diagnosis: Hypertension",
                    "source_file_ids": [],
                    "source_file_names": [],
                }
            ],
            "context": "Diagnosis: Hypertension",
            "answer": "Unified summary",
            "confidence": "high",
            "gemini_ok": True,
        },
    )
    def test_chat_response_includes_summary_and_source_hyperlinks(self, _mock_run_chat_query):
        first = self.upload_as_patient("report1.pdf", b"%PDF-1.4", "application/pdf")
        second = self.upload_as_patient("report2.txt", b"Diagnosis: HTN", "text/plain")
        file_ids = [first.data["data"][0]["id"], second.data["data"][0]["id"]]

        mocked_hits = [
            {
                "score": 0.95,
                "chunk_id": "a:0",
                "chunk_index": 0,
                "text": "Diagnosis: Hypertension",
                "source_file_ids": file_ids,
                "source_file_names": ["report1.pdf", "report2.txt"],
            }
        ]
        with patch("medfiles.views.run_chat_query") as mock_query:
            mock_query.return_value = {
                "hits": mocked_hits,
                "context": "Diagnosis: Hypertension",
                "answer": "Unified summary",
                "confidence": "high",
                "gemini_ok": True,
            }
            self.client.force_authenticate(user=self.doctor)
            response = self.client.post(
                "/api/medfiles/doctor/chat-query/",
                {
                    "patient_id": str(self.patient.id),
                    "doctor_id": str(self.doctor.id),
                    "message": "Summarize HTN management guidance",
                    "top_k": 5,
                },
                format="json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["summary"], "Unified summary")
        self.assertEqual(len(response.data["sources"]), 2)
        self.assertTrue(all(source["hyperlink"] for source in response.data["sources"]))

    def test_chat_response_uses_selected_file_sources_without_returning_chunk_dump(self):
        first = self.upload_as_patient("report1.pdf", b"%PDF-1.4", "application/pdf")
        second = self.upload_as_patient("report2.txt", b"Diagnosis: HTN", "text/plain")
        file_ids = [first.data["data"][0]["id"], second.data["data"][0]["id"]]

        with patch("medfiles.views.analyze_and_store_chunks") as mock_analyze, patch("medfiles.views.run_chat_query") as mock_query:
            mock_analyze.return_value = {}
            mock_query.return_value = {
                "hits": [],
                "context": "",
                "answer": "Relevant answer only.",
                "confidence": "high",
                "gemini_ok": True,
                "retrieval_mode": "selected_file_full_context",
                "source_file_ids": file_ids,
            }
            self.client.force_authenticate(user=self.doctor)
            response = self.client.post(
                "/api/medfiles/doctor/chat-query/",
                {
                    "patient_id": str(self.patient.id),
                    "doctor_id": str(self.doctor.id),
                    "message": "What is the diagnosis?",
                    "file_ids": file_ids,
                },
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["retrieval_mode"], "selected_file_full_context")
        self.assertEqual(response.data["summary"], "Relevant answer only.")
        self.assertEqual(response.data["chunks"], [])
        self.assertEqual(response.data["context"], "")
        self.assertEqual(len(response.data["sources"]), 2)

    def test_chat_query_accepts_selected_file_ids_alias_from_frontend(self):
        first = self.upload_as_patient("report1.txt", b"Diagnosis: HTN", "text/plain")
        second = self.upload_as_patient("report2.txt", b"Medication: ACE inhibitor", "text/plain")
        file_ids = [first.data["data"][0]["id"], second.data["data"][0]["id"]]

        with patch("medfiles.views.analyze_and_store_chunks") as mock_analyze, patch("medfiles.views.run_chat_query") as mock_query:
            mock_analyze.return_value = {}
            mock_query.return_value = {
                "hits": [],
                "context": "",
                "answer": "Focused answer.",
                "confidence": "high",
                "gemini_ok": True,
                "retrieval_mode": "selected_file_full_context",
                "source_file_ids": file_ids,
            }
            self.client.force_authenticate(user=self.doctor)
            response = self.client.post(
                "/api/medfiles/doctor/chat-query/",
                {
                    "patient_id": str(self.patient.id),
                    "doctor_id": str(self.doctor.id),
                    "message": "What is the diagnosis?",
                    "selected_file_ids": file_ids,
                },
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        called_kwargs = mock_query.call_args.kwargs
        self.assertEqual(called_kwargs["file_ids"], file_ids)
        self.assertEqual(response.data["selected_file_ids"], file_ids)

    def test_chat_query_accepts_selected_files_objects_from_frontend(self):
        first = self.upload_as_patient("report1.txt", b"Diagnosis: HTN", "text/plain")
        second = self.upload_as_patient("report2.txt", b"Medication: ACE inhibitor", "text/plain")
        file_ids = [first.data["data"][0]["id"], second.data["data"][0]["id"]]

        with patch("medfiles.views.analyze_and_store_chunks") as mock_analyze, patch("medfiles.views.run_chat_query") as mock_query:
            mock_analyze.return_value = {}
            mock_query.return_value = {
                "hits": [],
                "context": "",
                "answer": "Focused answer.",
                "confidence": "high",
                "gemini_ok": True,
                "retrieval_mode": "selected_file_full_context",
                "source_file_ids": file_ids,
            }
            self.client.force_authenticate(user=self.doctor)
            response = self.client.post(
                "/api/medfiles/doctor/chat-query/",
                {
                    "patient_id": str(self.patient.id),
                    "doctor_id": str(self.doctor.id),
                    "message": "What is the diagnosis?",
                    "selectedFiles": [{"id": file_ids[0]}, {"file_id": file_ids[1]}],
                },
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        called_kwargs = mock_query.call_args.kwargs
        self.assertEqual(called_kwargs["file_ids"], file_ids)
        self.assertEqual(response.data["selected_file_ids"], file_ids)

    def test_non_english_query_is_handled_gracefully(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post(
            "/api/medfiles/doctor/chat-query/",
            {
                "patient_id": str(self.patient.id),
                "doctor_id": str(self.doctor.id),
                "message": "¿Cuál es el diagnóstico?",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_metadata_update_returns_confirmation(self):
        upload = self.upload_as_patient("report.pdf", b"%PDF-1.4", "application/pdf")
        file_id = upload.data["data"][0]["id"]
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post(
            f"/api/medfiles/doctor/files/{file_id}/update/",
            {"title": "Cardiology Follow-up Report", "description": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Update successful")
        self.assertEqual(response.data["data"]["title"], "Cardiology Follow-up Report")

    def test_logs_do_not_expose_raw_patient_name(self):
        self.client.force_authenticate(user=self.patient)
        with self.assertLogs("medfiles.views", level="INFO") as captured:
            self.client.post(
                "/api/medfiles/patient/upload/",
                {
                    "doctor_id": str(self.doctor.id),
                    "files": [SimpleUploadedFile("report.pdf", b"%PDF-1.4", content_type="application/pdf")],
                },
                format="multipart",
            )
        joined = "\n".join(captured.output)
        self.assertNotIn("john.doe", joined.lower())

    def test_disposal_job_removes_expired_files_and_retains_active_ones(self):
        expired = PatientFile.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            original_name="expired.pdf",
            display_name="expired.pdf",
            file_type="pdf",
            file=SimpleUploadedFile("expired.pdf", b"%PDF-1.4", content_type="application/pdf"),
            authorized_until=timezone.now() - timedelta(days=1),
        )
        active = PatientFile.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            original_name="active.pdf",
            display_name="active.pdf",
            file_type="pdf",
            file=SimpleUploadedFile("active.pdf", b"%PDF-1.4", content_type="application/pdf"),
            authorized_until=timezone.now() + timedelta(days=1),
        )
        disposed = dispose_expired_files()
        expired.refresh_from_db()
        active.refresh_from_db()
        self.assertEqual(disposed, 1)
        self.assertTrue(expired.is_disposed)
        self.assertFalse(active.is_disposed)

    def test_revoking_access_disposes_patient_files(self):
        upload = self.upload_as_patient("report.pdf", b"%PDF-1.4", "application/pdf")
        file_id = upload.data["data"][0]["id"]
        self.client.force_authenticate(user=self.patient)
        response = self.client.post(f"/api/portal/access/{self.rel.id}/revoke/")
        self.assertEqual(response.status_code, 200)
        file_obj = PatientFile.objects.get(id=file_id)
        self.assertTrue(file_obj.is_disposed)
