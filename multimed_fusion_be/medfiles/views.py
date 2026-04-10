import hashlib
import logging
import mimetypes
from pathlib import Path

from django.contrib.auth import get_user_model
from django.http import FileResponse, Http404
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from portal.models import PatientDoctorAccess

from .models import PatientFile
from .permissions import IsDoctor, IsPatient
from .serializers import (
    DoctorAnalyzeSerializer,
    DoctorChatQuerySerializer,
    DoctorPatientUploadSerializer,
    PatientFileMetadataUpdateSerializer,
    PatientFileSerializer,
    PatientUploadSerializer,
    SUPPORTED_EXTENSIONS,
)
from .services.analyze_files import analyze_and_store_chunks
from .services.chat_query import run_chat_query
from .utils.sanitization import anonymize_filename, sanitize_log_value

User = get_user_model()
logger = logging.getLogger(__name__)


def detect_file_type(filename: str) -> str:
    extension = Path(filename or "").suffix.lower()
    return SUPPORTED_EXTENSIONS.get(extension, "unknown")


def file_sha256(uploaded_file) -> str:
    digest = hashlib.sha256()
    for chunk in uploaded_file.chunks():
        digest.update(chunk)
    uploaded_file.seek(0)
    return digest.hexdigest()


def apply_file_metadata(file_obj, *, patient):
    if not file_obj.display_name:
        file_obj.display_name = anonymize_filename(file_obj.original_name, patient=patient)
    if not file_obj.title:
        file_obj.title = file_obj.display_name or file_obj.original_name
    if not file_obj.authorized_until:
        relation = PatientDoctorAccess.objects.filter(
            doctor=file_obj.doctor,
            patient=file_obj.patient,
            status=PatientDoctorAccess.Status.APPROVED,
        ).first()
        if relation and relation.consent_expires_at:
            file_obj.authorized_until = relation.consent_expires_at


def create_patient_file(*, patient, doctor, uploaded_file, uploaded_by_role):
    original_name = uploaded_file.name
    extension = Path(original_name).suffix.lower()
    file_obj = PatientFile.objects.create(
        patient=patient,
        doctor=doctor,
        original_name=original_name,
        mime_type=getattr(uploaded_file, "content_type", "") or mimetypes.guess_type(original_name)[0] or "",
        file_type=detect_file_type(original_name),
        extension=extension,
        file_size=getattr(uploaded_file, "size", 0),
        sha256=file_sha256(uploaded_file),
        uploaded_by_role=uploaded_by_role,
        file=uploaded_file,
    )
    apply_file_metadata(file_obj, patient=patient)
    file_obj.save()
    return file_obj


def ensure_access(*, doctor, patient_id):
    return PatientDoctorAccess.objects.filter(
        doctor=doctor,
        patient_id=patient_id,
        status=PatientDoctorAccess.Status.APPROVED,
    ).exists()


def is_english_query(message: str) -> bool:
    text = (message or "").strip()
    if not text:
        return False
    ascii_letters = sum(1 for char in text if ("a" <= char.lower() <= "z"))
    non_ascii = sum(1 for char in text if ord(char) > 127)
    return ascii_letters > 0 and non_ascii <= max(2, len(text) // 10)


class PatientUploadFilesView(APIView):
    permission_classes = [IsPatient]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = PatientUploadSerializer(
            data={"doctor_id": (request.data.get("doctor_id") or "").strip(), "files": request.FILES.getlist("files")}
        )
        serializer.is_valid(raise_exception=True)

        doctor = User.objects.filter(id=serializer.validated_data["doctor_id"], role=User.Role.DOCTOR).first()
        if not doctor:
            return Response({"detail": "Doctor not found."}, status=404)
        if not ensure_access(doctor=doctor, patient_id=request.user.id):
            return Response({"detail": "You must approve this doctor before uploading files."}, status=403)

        created = [
            create_patient_file(patient=request.user, doctor=doctor, uploaded_file=file_obj, uploaded_by_role="patient")
            for file_obj in serializer.validated_data["files"]
        ]
        logger.info("Upload completed for patient=%s", str(request.user.id)[-6:])
        return Response(
            {"message": "Upload successful", "data": PatientFileSerializer(created, many=True, context={"request": request}).data},
            status=status.HTTP_201_CREATED,
        )


class DoctorUploadFilesForPatientView(APIView):
    permission_classes = [IsDoctor]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DoctorPatientUploadSerializer(
            data={"patient_id": (request.data.get("patient_id") or "").strip(), "files": request.FILES.getlist("files")}
        )
        serializer.is_valid(raise_exception=True)

        patient = User.objects.filter(id=serializer.validated_data["patient_id"], role=User.Role.PATIENT).first()
        if not patient:
            return Response({"detail": "Patient not found."}, status=404)
        if not ensure_access(doctor=request.user, patient_id=patient.id):
            return Response({"detail": "Access not approved for this patient."}, status=403)

        created = [
            create_patient_file(patient=patient, doctor=request.user, uploaded_file=file_obj, uploaded_by_role="doctor")
            for file_obj in serializer.validated_data["files"]
        ]
        return Response(
            {"message": "Upload successful", "data": PatientFileSerializer(created, many=True, context={"request": request}).data},
            status=status.HTTP_201_CREATED,
        )


class DoctorListPatientFilesView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = PatientFileSerializer

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        if not ensure_access(doctor=self.request.user, patient_id=patient_id):
            return PatientFile.objects.none()

        queryset = PatientFile.objects.filter(
            doctor=self.request.user,
            patient_id=patient_id,
            is_disposed=False,
        ).order_by("-uploaded_at")
        file_type = (self.request.query_params.get("type") or "").strip().lower()
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        return queryset

    def list(self, request, *args, **kwargs):
        patient_id = self.kwargs["patient_id"]
        if not ensure_access(doctor=request.user, patient_id=patient_id):
            return Response({"detail": "Access not approved for this patient."}, status=403)
        return super().list(request, *args, **kwargs)


class PatientListDoctorFilesView(generics.ListAPIView):
    permission_classes = [IsPatient]
    serializer_class = PatientFileSerializer

    def get_queryset(self):
        doctor_id = self.kwargs["doctor_id"]
        relation_ok = PatientDoctorAccess.objects.filter(
            doctor_id=doctor_id,
            patient=self.request.user,
            status=PatientDoctorAccess.Status.APPROVED,
        ).exists()
        if not relation_ok:
            return PatientFile.objects.none()
        return PatientFile.objects.filter(
            doctor_id=doctor_id,
            patient=self.request.user,
            is_disposed=False,
        ).order_by("-uploaded_at")

    def list(self, request, *args, **kwargs):
        doctor_id = self.kwargs["doctor_id"]
        relation_ok = PatientDoctorAccess.objects.filter(
            doctor_id=doctor_id,
            patient=request.user,
            status=PatientDoctorAccess.Status.APPROVED,
        ).exists()
        if not relation_ok:
            return Response({"detail": "Access not approved for this doctor."}, status=403)
        return super().list(request, *args, **kwargs)


class PatientFileMetadataUpdateView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request, file_id):
        serializer = PatientFileMetadataUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_obj = PatientFile.objects.filter(id=file_id, doctor=request.user, is_disposed=False).first()
        if not file_obj:
            return Response({"detail": "File not found."}, status=404)

        for field, value in serializer.validated_data.items():
            setattr(file_obj, field, value)
        file_obj.save()
        return Response(
            {"message": "Update successful", "data": PatientFileSerializer(file_obj, context={"request": request}).data}
        )


class DoctorAnalyzeFilesView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request):
        serializer = DoctorAnalyzeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data["patient_id"]
        file_ids = serializer.validated_data["file_ids"]

        if not ensure_access(doctor=request.user, patient_id=patient_id):
            return Response({"detail": "Access not approved for this patient."}, status=403)

        patient = User.objects.filter(id=patient_id, role=User.Role.PATIENT).first()
        if not patient:
            return Response({"detail": "Patient not found."}, status=404)

        files = list(
            PatientFile.objects.filter(
                id__in=file_ids,
                doctor=request.user,
                patient=patient,
                is_disposed=False,
            )
        )
        if len(files) != len(set(file_ids)):
            return Response({"detail": "One or more file_ids are invalid for this patient."}, status=400)

        result = analyze_and_store_chunks(doctor=request.user, patient=patient, files=files)
        logger.info(
            "Analyze request doctor=%s patient=%s file_count=%s",
            str(request.user.id)[-6:],
            str(patient_id)[-6:],
            len(files),
        )
        return Response(
            {
                "message": "Files analyzed successfully.",
                "patient_id": patient_id,
                "doctor_id": str(request.user.id),
                **result,
                "files": PatientFileSerializer(files, many=True, context={"request": request}).data,
            }
        )


class DoctorChatQueryView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request):
        serializer = DoctorChatQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_id = serializer.validated_data["patient_id"]
        message = serializer.validated_data["message"].strip()
        file_ids = serializer.validated_data.get("file_ids") or []
        conversation_history = serializer.validated_data.get("conversation_history") or []
        top_k = serializer.validated_data["top_k"]

        if not ensure_access(doctor=request.user, patient_id=patient_id):
            return Response({"detail": "Access not approved for this patient."}, status=403)

        patient = User.objects.filter(id=patient_id, role=User.Role.PATIENT).first()
        if not patient:
            return Response({"detail": "Patient not found."}, status=404)
        doctor_id = (request.data.get("doctor_id") or "").strip()
        if doctor_id and doctor_id != str(request.user.id):
            return Response({"detail": "doctor_id does not match authenticated doctor."}, status=403)
        if not is_english_query(message):
            return Response({"detail": "Only English natural language queries are supported."}, status=400)

        logger.info(
            "Chat query doctor=%s patient=%s top_k=%s message=%s",
            str(request.user.id)[-6:],
            str(patient.id)[-6:],
            top_k,
            sanitize_log_value(message, patient=patient),
        )

        allowed_files = PatientFile.objects.filter(
            doctor=request.user,
            patient=patient,
            is_disposed=False,
        )
        if file_ids:
            files = list(allowed_files.filter(id__in=file_ids))
            if len(files) != len(set(file_ids)):
                return Response({"detail": "One or more selected files are invalid for this patient."}, status=400)
        else:
            files = list(allowed_files)
            file_ids = [str(file_obj.id) for file_obj in files]

        unprocessed_files = [file_obj for file_obj in files if not file_obj.is_processed]
        if unprocessed_files:
            analyze_and_store_chunks(doctor=request.user, patient=patient, files=unprocessed_files)

        result = run_chat_query(
            patient_id=str(patient.id),
            doctor_id=str(request.user.id),
            message=message,
            file_ids=file_ids,
            conversation_history=conversation_history,
            k=top_k,
            use_gemini=True,
        )

        source_ids = []
        for file_id in result.get("source_file_ids", []):
            if file_id not in source_ids:
                source_ids.append(file_id)
        for hit in result.get("hits", []):
            for file_id in hit.get("source_file_ids", []):
                if file_id not in source_ids:
                    source_ids.append(file_id)

        source_map = {
            str(file_obj.id): file_obj
            for file_obj in PatientFile.objects.filter(id__in=source_ids, doctor=request.user, patient=patient, is_disposed=False)
        }
        sources = [
            {
                "file_id": file_id,
                "name": source_map[file_id].display_name or source_map[file_id].original_name,
                "hyperlink": request.build_absolute_uri(f"/api/medfiles/files/{file_id}/download/"),
                "download_url": request.build_absolute_uri(f"/api/medfiles/files/{file_id}/download/"),
                "uploaded_by_role": source_map[file_id].uploaded_by_role,
            }
            for file_id in source_ids
            if file_id in source_map
        ]

        return Response(
            {
                "message": "Query processed successfully.",
                "patient_id": str(patient.id),
                "doctor_id": str(request.user.id),
                "query": message,
                "chunks_retrieved": len(result.get("hits", [])),
                "chunks": result.get("hits", []) if result.get("retrieval_mode") != "selected_file_full_context" else [],
                "context": result.get("context", "") if result.get("retrieval_mode") != "selected_file_full_context" else "",
                "summary": result.get("answer", ""),
                "confidence": result.get("confidence", "medium"),
                "gemini_ok": result.get("gemini_ok", False),
                "retrieval_mode": result.get("retrieval_mode", "semantic_top_k"),
                "sources": sources,
                "selected_file_ids": file_ids,
            }
        )


class SecureFileDownloadView(APIView):
    def get(self, request, file_id):
        file_obj = PatientFile.objects.filter(id=file_id, is_disposed=False).first()
        if not file_obj or not file_obj.file:
            raise Http404("File not found.")

        is_authorized = False
        if getattr(request.user, "role", None) == User.Role.DOCTOR:
            is_authorized = ensure_access(doctor=request.user, patient_id=file_obj.patient_id) and str(file_obj.doctor_id) == str(
                request.user.id
            )
        elif getattr(request.user, "role", None) == User.Role.PATIENT:
            is_authorized = str(file_obj.patient_id) == str(request.user.id) and PatientDoctorAccess.objects.filter(
                doctor_id=file_obj.doctor_id,
                patient=request.user,
                status=PatientDoctorAccess.Status.APPROVED,
            ).exists()

        if not is_authorized:
            return Response({"detail": "Not authorized to access this file."}, status=403)

        response = FileResponse(open(file_obj.file.path, "rb"), as_attachment=False)
        response["Content-Type"] = file_obj.mime_type or mimetypes.guess_type(file_obj.original_name)[0] or "application/octet-stream"
        return response
