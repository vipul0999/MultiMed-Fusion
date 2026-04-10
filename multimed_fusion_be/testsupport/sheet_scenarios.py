from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from medfiles.models import PatientDocChunk, PatientFile
from medfiles.services.disposal import dispose_expired_files
from medfiles.utils.retrieval import get_chunks_by_file_ids, top_k_chunks
from medfiles.utils.sanitization import anonymize_filename, anonymize_patient_text, sanitize_log_value
from medfiles.utils.structured_data import build_machine_readable_payload
from portal.models import PatientDoctorAccess
from testsupport.assets import make_uploaded_file

User = get_user_model()


def _upload_and_get_id(testcase, filename, *, kind=None, content_type=None):
    response = testcase.patient_upload(filename, kind=kind, content_type=content_type)
    return response, response.data["data"][0]["id"]


def run_tc1(testcase):
    pdf_response, _ = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    txt_response, _ = _upload_and_get_id(testcase, "lab_report.txt", content_type="text/plain")
    testcase.assertEqual(pdf_response.data["data"][0]["file_type"], "pdf")
    testcase.assertEqual(txt_response.data["data"][0]["file_type"], "text")
    testcase.assertEqual(PatientFile.objects.count(), 2)


def run_tc2(testcase):
    png_response, _ = _upload_and_get_id(testcase, "images2.png", kind="image")
    jpg_response, _ = _upload_and_get_id(testcase, "scan.jpg")
    testcase.assertEqual(png_response.data["data"][0]["file_type"], "image")
    testcase.assertEqual(jpg_response.data["data"][0]["file_type"], "image")


def run_tc3(testcase):
    mp3_response, _ = _upload_and_get_id(testcase, "audios4.mp3", kind="audio")
    wav_response, _ = _upload_and_get_id(testcase, "patient_voice.wav")
    testcase.assertEqual(mp3_response.data["data"][0]["file_type"], "mp3")
    testcase.assertEqual(wav_response.data["data"][0]["file_type"], "wav")


def _analyze_with_mocked_extract(testcase, *, filename, kind=None, content_type=None, extracted_text, embed_return=None):
    embed_return = embed_return or [[0.1, 0.2, 0.3]]
    upload_response, file_id = _upload_and_get_id(testcase, filename, kind=kind, content_type=content_type)
    with patch("medfiles.services.analyze_files.extract_text_by_filetype", return_value=extracted_text), patch(
        "medfiles.services.analyze_files.embed_texts", return_value=embed_return
    ):
        testcase.analyze([file_id])
    return PatientFile.objects.get(id=file_id), upload_response


def run_tc4(testcase):
    file_obj, _ = _analyze_with_mocked_extract(
        testcase,
        filename="pdf_file2.pdf",
        kind="pdf",
        extracted_text="Patient: patient11\nHemoglobin: 13.2\nWBC: 6.5\nPlatelets: 230",
    )
    testcase.assertTrue(file_obj.extracted_payload["machine_readable"])
    testcase.assertEqual(file_obj.processing_status, "processed")
    testcase.assertEqual(file_obj.extracted_payload["fields"]["hemoglobin"], "13.2")


def run_tc5(testcase):
    file_obj, _ = _analyze_with_mocked_extract(
        testcase,
        filename="discharge_summary.txt",
        content_type="text/plain",
        extracted_text="Diagnosis: Flu\nMedication: Rest\nFollow-up: 2 weeks",
    )
    testcase.assertEqual(file_obj.extracted_payload["sections"]["diagnosis"], "Flu")
    testcase.assertEqual(file_obj.extracted_payload["sections"]["medication"], "Rest")
    testcase.assertEqual(file_obj.extracted_payload["sections"]["followup"], "2 weeks")


def run_tc6(testcase):
    file_obj, _ = _analyze_with_mocked_extract(
        testcase,
        filename="images2.png",
        kind="image",
        extracted_text="Glucose: 105\nCholesterol: 180",
    )
    testcase.assertEqual(file_obj.extracted_payload["fields"]["glucose"], "105")
    testcase.assertEqual(file_obj.extracted_payload["fields"]["cholesterol"], "180")


def run_tc7(testcase):
    _, file_id = _upload_and_get_id(testcase, "audios4.mp3", kind="audio")
    with patch("medfiles.services.analyze_files.extract_text_by_filetype", return_value="Consultation transcript"), patch(
        "medfiles.services.analyze_files.embed_texts", return_value=[[0.2, 0.2, 0.2]]
    ) as embed_mock:
        testcase.analyze([file_id])
    testcase.assertTrue(PatientDocChunk.objects.filter(source_file_ids__contains=[file_id]).exists())
    testcase.assertTrue(embed_mock.called)


def run_tc8(testcase):
    _, file_id = _upload_and_get_id(testcase, "patient_followup.wav")
    with patch("medfiles.services.analyze_files.extract_text_by_filetype", return_value="WAV transcript"), patch(
        "medfiles.services.analyze_files.embed_texts", return_value=[[0.2, 0.2, 0.2]]
    ) as embed_mock:
        testcase.analyze([file_id])
    testcase.assertTrue(PatientDocChunk.objects.filter(source_file_ids__contains=[file_id]).exists())
    testcase.assertTrue(embed_mock.called)


def run_tc9(testcase):
    _, file_id = _upload_and_get_id(testcase, "corrupted_audio.mp3")
    with patch("medfiles.services.analyze_files.extract_text_by_filetype", return_value=""), patch(
        "medfiles.services.analyze_files.embed_texts"
    ) as embed_mock:
        testcase.analyze([file_id])
    file_obj = PatientFile.objects.get(id=file_id)
    testcase.assertEqual(file_obj.processing_status, "failed")
    testcase.assertEqual(PatientDocChunk.objects.count(), 0)
    embed_mock.assert_not_called()


def run_tc10(testcase):
    _analyze_with_mocked_extract(
        testcase,
        filename="pdf_file2.pdf",
        kind="pdf",
        extracted_text="Patient has stage 2 hypertension",
        embed_return=[[0.3, 0.1, 0.5]],
    )
    testcase.assertTrue(settings.VECTOR_DB_ENCRYPTION_AT_REST)
    testcase.assertEqual(PatientDocChunk.objects.count(), 1)


def run_tc11(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "renal contraindications", "answer": "Relevant answer", "confidence": "high", "gemini_ok": True},
    ):
        response = testcase.chat(message="renal contraindications", file_ids=[file_id])
    testcase.assertEqual(response.status_code, 200)

    testcase.authenticate(testcase.other_doctor)
    denied = testcase.client.post(
        "/api/medfiles/doctor/chat-query/",
        {"patient_id": str(testcase.patient.id), "doctor_id": str(testcase.other_doctor.id), "message": "renal contraindications"},
        format="json",
    )
    testcase.assertEqual(denied.status_code, 403)


def run_tc12(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    file_obj = PatientFile.objects.get(id=file_id)
    for index, score in enumerate([0.99, 0.95, 0.9, 0.85, 0.8, 0.5]):
        testcase.create_chunk(text=f"chunk {index}", embedding=[score, 0.0, 0.0], file_obj=file_obj, chunk_index=index)
    with patch("medfiles.utils.retrieval.embed_query", return_value=[1.0, 0.0, 0.0]):
        results = top_k_chunks(patient_id=str(testcase.patient.id), doctor_id=str(testcase.doctor.id), query="cardiology", k=5, min_score=0.75)
    testcase.assertEqual(len(results), 5)
    testcase.assertTrue(all(results[idx]["score"] >= results[idx + 1]["score"] for idx in range(4)))


def run_tc13(testcase):
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "summary", "answer": "English query accepted", "confidence": "high", "gemini_ok": True},
    ):
        response = testcase.chat(message="What are the current findings?")
    testcase.assertEqual(response.data["summary"], "English query accepted")


def run_tc14(testcase):
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "BP elevated", "answer": "HTN follow-up required", "confidence": "high", "gemini_ok": True},
    ):
        response = testcase.chat(message="Summarize HTN and BP follow-up recommendations")
    testcase.assertIn("HTN", response.data["summary"])


def run_tc15(testcase):
    response = testcase.chat(message="¿Cuál es el diagnóstico?", expected_status=400)
    testcase.assertIn("Only English", response.data["detail"])


def run_tc16(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    file_obj = PatientFile.objects.get(id=file_id)
    for index, score in enumerate([0.9, 0.7, 0.6, 0.4]):
        testcase.create_chunk(text=f"relevant chunk {index}", embedding=[score, 0.0, 0.0], file_obj=file_obj, chunk_index=index)
    with patch("medfiles.utils.retrieval.embed_query", return_value=[1.0, 0.0, 0.0]):
        results = top_k_chunks(patient_id=str(testcase.patient.id), doctor_id=str(testcase.doctor.id), query="top chunks", k=3)
    testcase.assertEqual([item["chunk_index"] for item in results], [0, 1, 2])


def run_tc17(testcase):
    _, first_id = _upload_and_get_id(testcase, "report1.pdf", kind="pdf")
    _, second_id = _upload_and_get_id(testcase, "report2.txt", content_type="text/plain")
    first_obj = PatientFile.objects.get(id=first_id)
    second_obj = PatientFile.objects.get(id=second_id)
    testcase.create_chunk(text="cardiology finding", embedding=[0.9, 0.0, 0.0], file_obj=first_obj, chunk_index=0)
    testcase.create_chunk(text="medication note", embedding=[0.8, 0.0, 0.0], file_obj=second_obj, chunk_index=0)
    results = get_chunks_by_file_ids(
        patient_id=str(testcase.patient.id), doctor_id=str(testcase.doctor.id), file_ids=[str(first_obj.id), str(second_obj.id)]
    )
    testcase.assertEqual(len(results), 2)


def run_tc18(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    file_obj = PatientFile.objects.get(id=file_id)
    testcase.create_chunk(text="weak match", embedding=[0.1, 0.0, 0.0], file_obj=file_obj)
    with patch("medfiles.utils.retrieval.embed_query", return_value=[1.0, 0.0, 0.0]):
        results = top_k_chunks(patient_id=str(testcase.patient.id), doctor_id=str(testcase.doctor.id), query="cardiology", min_score=0.75)
    testcase.assertEqual(results, [])


def run_tc19(testcase):
    _, first_id = _upload_and_get_id(testcase, "report1.pdf", kind="pdf")
    _, second_id = _upload_and_get_id(testcase, "report2.txt", content_type="text/plain")
    with patch(
        "medfiles.views.run_chat_query",
        return_value={
            "hits": [{"source_file_ids": [first_id, second_id], "source_file_names": ["report1.pdf", "report2.txt"], "text": "combined", "chunk_id": "1", "chunk_index": 0, "score": 0.95}],
            "context": "combined",
            "answer": "Unified summary across sources",
            "confidence": "high",
            "gemini_ok": True,
            "source_file_ids": [first_id, second_id],
        },
    ):
        response = testcase.chat(message="Summarize the chart", file_ids=[first_id, second_id])
    testcase.assertEqual(response.data["summary"], "Unified summary across sources")
    testcase.assertEqual(len(response.data["sources"]), 2)


def run_tc20(testcase):
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "duplicate-free", "answer": "Single coherent summary sentence.", "confidence": "high", "gemini_ok": True},
    ):
        response = testcase.chat(message="Provide one concise summary")
    testcase.assertEqual(response.data["summary"], "Single coherent summary sentence.")


def run_tc21(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "grounded", "answer": "Grounded answer", "confidence": "high", "gemini_ok": True, "source_file_ids": [file_id]},
    ):
        response = testcase.chat(message="What is the diagnosis?", file_ids=[file_id])
    testcase.assertEqual(response.data["confidence"], "high")
    testcase.assertEqual(response.data["sources"][0]["file_id"], file_id)


def run_tc22(testcase):
    _analyze_with_mocked_extract(testcase, filename="pdf_file2.pdf", kind="pdf", extracted_text="CBC findings in document")
    testcase.assertEqual(PatientDocChunk.objects.count(), 1)


def run_tc23(testcase):
    _analyze_with_mocked_extract(testcase, filename="images2.png", kind="image", extracted_text="OCR note from image")
    testcase.assertEqual(PatientDocChunk.objects.count(), 1)


def run_tc24(testcase):
    _analyze_with_mocked_extract(testcase, filename="audios4.mp3", kind="audio", extracted_text="Audio transcript content")
    testcase.assertEqual(PatientDocChunk.objects.count(), 1)


def run_tc25(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "one source", "answer": "Single source answer", "confidence": "high", "gemini_ok": True, "source_file_ids": [file_id]},
    ):
        response = testcase.chat(message="Single source question", file_ids=[file_id])
    testcase.assertEqual(len(response.data["sources"]), 1)
    testcase.assertTrue(response.data["sources"][0]["hyperlink"].endswith(f"/api/medfiles/files/{file_id}/download/"))


def run_tc26(testcase):
    _, first_id = _upload_and_get_id(testcase, "report1.pdf", kind="pdf")
    _, second_id = _upload_and_get_id(testcase, "report2.txt", content_type="text/plain")
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "many sources", "answer": "Multi source answer", "confidence": "high", "gemini_ok": True, "source_file_ids": [first_id, second_id]},
    ):
        response = testcase.chat(message="Multi source question", file_ids=[first_id, second_id])
    testcase.assertEqual(len(response.data["sources"]), 2)
    testcase.assertTrue(all(source["hyperlink"] for source in response.data["sources"]))


def run_tc27(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    testcase.authenticate(testcase.patient)
    response = testcase.client.get(f"/api/medfiles/files/{file_id}/download/")
    testcase.assertEqual(response.status_code, 200)
    testcase.assertEqual(response.get("Content-Type"), "application/pdf")


def run_tc28(testcase):
    anonymized = anonymize_filename("patient11_report.pdf", patient=testcase.patient)
    testcase.assertNotIn("patient11", anonymized)
    testcase.assertIn("[PATIENT]", anonymized)


def run_tc29(testcase):
    sanitized = anonymize_patient_text("DOB: 01/01/1990", patient=testcase.patient)
    testcase.assertNotIn("01/01/1990", sanitized)
    testcase.assertIn("[REDACTED_DATE]", sanitized)


def run_tc30(testcase):
    file_obj, _ = _analyze_with_mocked_extract(
        testcase,
        filename="pdf_file2.pdf",
        kind="pdf",
        extracted_text="patient11 DOB: 01/01/1990 diagnosis: stable",
    )
    testcase.assertNotIn("patient11", file_obj.extracted_text)
    testcase.assertNotIn("01/01/1990", file_obj.extracted_text)


def run_tc31(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    testcase.authenticate(testcase.doctor)
    list_response = testcase.client.get(f"/api/medfiles/doctor/patients/{testcase.patient.id}/files/")
    download_response = testcase.client.get(f"/api/medfiles/files/{file_id}/download/")
    testcase.assertEqual(list_response.status_code, 200)
    testcase.assertEqual(download_response.status_code, 200)


def run_tc32(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    testcase.authenticate(testcase.other_doctor)
    list_response = testcase.client.get(f"/api/medfiles/doctor/patients/{testcase.patient.id}/files/")
    download_response = testcase.client.get(f"/api/medfiles/files/{file_id}/download/")
    testcase.assertEqual(list_response.status_code, 403)
    testcase.assertEqual(download_response.status_code, 403)


def run_tc33(testcase):
    testcase.patient_upload("pdf_file2.pdf", kind="pdf")
    testcase.authenticate(testcase.other_doctor)
    response = testcase.client.get(f"/api/medfiles/doctor/patients/{testcase.patient.id}/files/")
    testcase.assertEqual(response.status_code, 403)


def run_tc34(testcase):
    testcase.authenticate(testcase.patient)
    with testcase.assertLogs("medfiles.views", level="INFO") as captured:
        testcase.client.post(
            "/api/medfiles/patient/upload/",
            {"doctor_id": str(testcase.doctor.id), "files": [make_uploaded_file("pdf_file2.pdf", kind="pdf")]},
            format="multipart",
        )
    testcase.assertNotIn("patient11", "\n".join(captured.output))


def run_tc35(testcase):
    sanitized = sanitize_log_value("Patient DOB 01/01/1990", patient=testcase.patient)
    testcase.assertNotIn("01/01/1990", sanitized)
    testcase.assertIn("[REDACTED_DATE]", sanitized)


def run_tc36(testcase):
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "summary", "answer": "ok", "confidence": "high", "gemini_ok": True},
    ):
        with testcase.assertLogs("medfiles.views", level="INFO") as captured:
            testcase.chat(message="patient11 DOB 01/01/1990 what is the diagnosis?")
    joined = "\n".join(captured.output)
    testcase.assertNotIn("patient11", joined)
    testcase.assertNotIn("01/01/1990", joined)


def run_tc37(testcase):
    testcase.patient_upload("pdf_file2.pdf", kind="pdf")
    file_obj = testcase.latest_file()
    file_obj.authorized_until = timezone.now() - timedelta(days=1)
    file_obj.save()
    disposed = dispose_expired_files()
    file_obj.refresh_from_db()
    testcase.assertEqual(disposed, 1)
    testcase.assertTrue(file_obj.is_disposed)


def run_tc38(testcase):
    testcase.patient_upload("pdf_file2.pdf", kind="pdf")
    file_obj = testcase.latest_file()
    file_obj.authorized_until = timezone.now() + timedelta(days=1)
    file_obj.save()
    disposed = dispose_expired_files()
    file_obj.refresh_from_db()
    testcase.assertEqual(disposed, 0)
    testcase.assertFalse(file_obj.is_disposed)


def run_tc39(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    testcase.authenticate(testcase.patient)
    response = testcase.client.post(f"/api/portal/access/{testcase.rel.id}/revoke/")
    testcase.assertEqual(response.status_code, 200)
    file_obj = PatientFile.objects.get(id=file_id)
    testcase.assertTrue(file_obj.is_disposed)


def run_tc40(testcase):
    response = testcase.client.post(
        "/api/auth/register/",
        {"username": "patient_a", "email": "patient@example.com", "password": "StrongPass@123", "role": "patient"},
        format="json",
    )
    testcase.assertEqual(response.status_code, 201)
    user = User.objects.get(username="patient_a")
    testcase.assertNotEqual(user.password, "StrongPass@123")
    testcase.assertTrue(user.check_password("StrongPass@123"))


def run_tc41(testcase):
    user = User.objects.create_user(username="patient_b", email="patientb@example.com", password="OldPass@123", role="patient")
    testcase.client.force_authenticate(user=user)
    response = testcase.client.post(
        "/api/auth/password/update/",
        {"old_password": "OldPass@123", "new_password": "NewPass@456"},
        format="json",
    )
    testcase.assertEqual(response.status_code, 200)
    user.refresh_from_db()
    testcase.assertNotEqual(user.password, "NewPass@456")
    testcase.assertTrue(user.check_password("NewPass@456"))


def run_tc42(testcase):
    User.objects.create_user(username="doctor_login", email="doctor@example.com", password="Secure@789", role="doctor")
    response = testcase.client.post("/api/auth/login/", {"username": "doctor_login", "password": "Secure@789"}, format="json")
    testcase.assertEqual(response.status_code, 200)
    testcase.assertNotIn("Secure@789", str(response.data))
    testcase.assertNotIn("password", response.data)


def run_tc43(testcase):
    response, _ = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    testcase.assertEqual(response.data["message"], "Upload successful")


def run_tc44(testcase):
    _, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    testcase.authenticate(testcase.doctor)
    response = testcase.client.post(
        f"/api/medfiles/doctor/files/{file_id}/update/",
        {"title": "Cardiology Follow-up Report", "description": "Updated"},
        format="json",
    )
    testcase.assertEqual(response.status_code, 200)
    testcase.assertEqual(response.data["message"], "Update successful")


def run_tc45(testcase):
    upload_response, file_id = _upload_and_get_id(testcase, "pdf_file2.pdf", kind="pdf")
    testcase.authenticate(testcase.doctor)
    update_response = testcase.client.post(
        f"/api/medfiles/doctor/files/{file_id}/update/",
        {"title": "Updated title"},
        format="json",
    )
    testcase.assertEqual(upload_response.data["message"], "Upload successful")
    testcase.assertEqual(update_response.data["message"], "Update successful")


def run_tc46(testcase):
    testcase.patient_upload_many(
        [
            {"filename": "document4.docx", "kind": "docx"},
            {"filename": "audios4.mp3", "kind": "audio"},
        ]
    )
    files = list(PatientFile.objects.order_by("uploaded_at"))
    with patch("medfiles.services.analyze_files.extract_text_by_filetype", side_effect=["Diagnosis: stable", "Audio transcript"]), patch(
        "medfiles.services.analyze_files.embed_texts", return_value=[[0.1, 0.1, 0.1], [0.2, 0.2, 0.2]]
    ):
        testcase.analyze([str(file_obj.id) for file_obj in files])
    testcase.assertEqual(PatientDocChunk.objects.count(), 2)


def run_tc47(testcase):
    testcase.patient_upload_many(
        [
            {"filename": "images2.png", "kind": "image"},
            {"filename": "document4.docx", "kind": "docx"},
        ]
    )
    files = list(PatientFile.objects.order_by("uploaded_at"))
    with patch("medfiles.services.analyze_files.extract_text_by_filetype", side_effect=["Image note", "Doctor note"]), patch(
        "medfiles.services.analyze_files.embed_texts", return_value=[[0.1, 0.1, 0.1], [0.2, 0.2, 0.2]]
    ):
        testcase.analyze([str(file_obj.id) for file_obj in files])
    testcase.assertEqual(PatientDocChunk.objects.count(), 2)


def run_tc48(testcase):
    testcase.patient_upload_many(
        [
            {"filename": "document4.docx", "kind": "docx"},
            {"filename": "audios4.mp3", "kind": "audio"},
            {"filename": "images2.png", "kind": "image"},
        ]
    )
    files = list(PatientFile.objects.order_by("uploaded_at"))
    with patch("medfiles.services.analyze_files.extract_text_by_filetype", side_effect=["Diagnosis: stable", "Audio transcript", "Image note"]), patch(
        "medfiles.services.analyze_files.embed_texts", return_value=[[0.1, 0.1, 0.1], [0.2, 0.2, 0.2], [0.3, 0.3, 0.3]]
    ):
        testcase.analyze([str(file_obj.id) for file_obj in files])
    with patch(
        "medfiles.views.run_chat_query",
        return_value={"hits": [], "context": "combined multimodal context", "answer": "End-to-end multimodal summary", "confidence": "high", "gemini_ok": True},
    ):
        response = testcase.chat(message="Provide end-to-end multimodal summary", file_ids=[str(file_obj.id) for file_obj in files])
    testcase.assertEqual(response.data["summary"], "End-to-end multimodal summary")

