from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Max, Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from medfiles.models import PatientFile
from medfiles.services.disposal import dispose_file

from .models import FileUploadRequest, PatientDoctorAccess
from .permissions import IsDoctor, IsPatient
from .serializers import (
    DoctorRequestAccessCreateSerializer,
    FileUploadRequestSerializer,
    PatientDoctorAccessSerializer,
    PatientGrantDoctorCreateSerializer,
    UserMiniSerializer,
)

User = get_user_model()


def _serialize_relationships(queryset):
    relationships = list(queryset)
    metrics = {}
    for relation in relationships:
        key = (str(relation.doctor_id), str(relation.patient_id))
        metrics[key] = {
            "files_count": PatientFile.objects.filter(
                doctor_id=relation.doctor_id,
                patient_id=relation.patient_id,
                is_disposed=False,
            ).count(),
            "open_upload_requests": FileUploadRequest.objects.filter(
                doctor_id=relation.doctor_id,
                patient_id=relation.patient_id,
                is_open=True,
            ).count(),
            "last_file_uploaded_at": PatientFile.objects.filter(
                doctor_id=relation.doctor_id,
                patient_id=relation.patient_id,
                is_disposed=False,
            ).aggregate(last=Max("uploaded_at"))["last"],
        }
    for relation in relationships:
        relation.files_count = metrics[(str(relation.doctor_id), str(relation.patient_id))]["files_count"]
        relation.open_upload_requests = metrics[(str(relation.doctor_id), str(relation.patient_id))]["open_upload_requests"]
        relation.last_file_uploaded_at = metrics[(str(relation.doctor_id), str(relation.patient_id))]["last_file_uploaded_at"]
    return relationships


class DoctorWorkspaceView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        approved = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                doctor=request.user,
                status=PatientDoctorAccess.Status.APPROVED,
            ).order_by("-updated_at")
        )
        pending = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                doctor=request.user,
                requested_by="doctor",
                status=PatientDoctorAccess.Status.PENDING,
            ).order_by("-created_at")
        )
        return Response(
            {
                "summary": {
                    "approved_patients": len(approved),
                    "pending_requests": len(pending),
                    "open_upload_requests": FileUploadRequest.objects.filter(doctor=request.user, is_open=True).count(),
                    "files_available": PatientFile.objects.filter(doctor=request.user, is_disposed=False).count(),
                },
                "approved_patients": PatientDoctorAccessSerializer(approved, many=True).data,
                "pending_requests": PatientDoctorAccessSerializer(pending, many=True).data,
            }
        )


class PatientWorkspaceView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        pending = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                patient=request.user,
                requested_by="doctor",
                status=PatientDoctorAccess.Status.PENDING,
            ).order_by("-created_at")
        )
        approved = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                patient=request.user,
                status=PatientDoctorAccess.Status.APPROVED,
            ).order_by("-updated_at")
        )
        upload_requests = FileUploadRequest.objects.filter(patient=request.user, is_open=True).order_by("-created_at")
        return Response(
            {
                "summary": {
                    "pending_requests": len(pending),
                    "approved_doctors": len(approved),
                    "open_upload_requests": upload_requests.count(),
                    "files_shared": PatientFile.objects.filter(patient=request.user, is_disposed=False).count(),
                },
                "pending_requests": PatientDoctorAccessSerializer(pending, many=True).data,
                "approved_doctors": PatientDoctorAccessSerializer(approved, many=True).data,
                "upload_requests": FileUploadRequestSerializer(upload_requests, many=True).data,
            }
        )


class DoctorApprovedPatientsView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        relationships = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                doctor=request.user,
                status=PatientDoctorAccess.Status.APPROVED,
            ).order_by("-updated_at")
        )
        return Response(PatientDoctorAccessSerializer(relationships, many=True).data)


class DoctorOutgoingRequestsView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        relationships = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                doctor=request.user,
                requested_by="doctor",
                status=PatientDoctorAccess.Status.PENDING,
            ).order_by("-created_at")
        )
        return Response(PatientDoctorAccessSerializer(relationships, many=True).data)


class DoctorRequestAccessView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request):
        serializer = DoctorRequestAccessCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = User.objects.get(id=serializer.validated_data["patient_id"], role=User.Role.PATIENT)
        note = serializer.validated_data.get("note", "")
        existing = PatientDoctorAccess.objects.filter(doctor=request.user, patient=patient).first()
        if existing:
            if existing.status in [PatientDoctorAccess.Status.REJECTED, PatientDoctorAccess.Status.REVOKED]:
                existing.status = PatientDoctorAccess.Status.PENDING
                existing.requested_by = "doctor"
                existing.note = note
                existing.revoked_at = None
                existing.save()
                return Response(
                    {"message": "Access request re-submitted.", "data": PatientDoctorAccessSerializer(existing).data}
                )
            return Response(
                {"message": "Relationship already exists.", "data": PatientDoctorAccessSerializer(existing).data}
            )

        try:
            relation = PatientDoctorAccess.objects.create(
                doctor=request.user,
                patient=patient,
                status=PatientDoctorAccess.Status.PENDING,
                requested_by="doctor",
                note=note,
            )
        except IntegrityError:
            relation = PatientDoctorAccess.objects.get(doctor=request.user, patient=patient)

        return Response(
            {"message": "Access request sent successfully.", "data": PatientDoctorAccessSerializer(relation).data},
            status=status.HTTP_201_CREATED,
        )


class PatientIncomingRequestsView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        relationships = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                patient=request.user,
                requested_by="doctor",
                status=PatientDoctorAccess.Status.PENDING,
            ).order_by("-created_at")
        )
        return Response(PatientDoctorAccessSerializer(relationships, many=True).data)


class PatientApproveRejectRequestView(APIView):
    permission_classes = [IsPatient]

    def post(self, request, rel_id):
        decision = (request.data.get("decision") or "").strip().lower()
        if decision not in ["approved", "rejected"]:
            return Response({"detail": "decision must be 'approved' or 'rejected'."}, status=400)

        relation = PatientDoctorAccess.objects.filter(id=rel_id, patient=request.user).first()
        if not relation:
            return Response({"detail": "Request not found."}, status=404)
        if relation.status != PatientDoctorAccess.Status.PENDING:
            return Response({"detail": f"Cannot change a non-pending request ({relation.status})."}, status=400)

        relation.status = (
            PatientDoctorAccess.Status.APPROVED if decision == "approved" else PatientDoctorAccess.Status.REJECTED
        )
        relation.approved_at = timezone.now() if decision == "approved" else None
        relation.save()

        return Response(
            {
                "message": "Access approved." if decision == "approved" else "Access rejected.",
                "data": PatientDoctorAccessSerializer(relation).data,
            }
        )


class PatientApprovedDoctorsView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        relationships = _serialize_relationships(
            PatientDoctorAccess.objects.filter(
                patient=request.user,
                status=PatientDoctorAccess.Status.APPROVED,
            ).order_by("-updated_at")
        )
        return Response(PatientDoctorAccessSerializer(relationships, many=True).data)


class PatientGrantDoctorAccessView(APIView):
    permission_classes = [IsPatient]

    def post(self, request):
        serializer = PatientGrantDoctorCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        doctor = User.objects.get(id=serializer.validated_data["doctor_id"], role=User.Role.DOCTOR)
        note = serializer.validated_data.get("note", "")
        existing = PatientDoctorAccess.objects.filter(doctor=doctor, patient=request.user).first()
        if existing:
            existing.status = PatientDoctorAccess.Status.APPROVED
            existing.requested_by = "patient"
            existing.note = note
            existing.revoked_at = None
            existing.approved_at = timezone.now()
            existing.save()
            return Response(
                {"message": "Doctor access updated.", "data": PatientDoctorAccessSerializer(existing).data}
            )

        relation = PatientDoctorAccess.objects.create(
            doctor=doctor,
            patient=request.user,
            status=PatientDoctorAccess.Status.APPROVED,
            requested_by="patient",
            note=note,
            approved_at=timezone.now(),
        )
        return Response(
            {"message": "Doctor access granted successfully.", "data": PatientDoctorAccessSerializer(relation).data},
            status=status.HTTP_201_CREATED,
        )


class RevokeAccessView(APIView):
    def post(self, request, rel_id):
        relation = PatientDoctorAccess.objects.filter(id=rel_id).first()
        if not relation:
            return Response({"detail": "Relationship not found."}, status=404)
        if str(relation.doctor_id) != str(request.user.id) and str(relation.patient_id) != str(request.user.id):
            return Response({"detail": "Not authorized."}, status=403)

        relation.status = PatientDoctorAccess.Status.REVOKED
        relation.revoked_at = timezone.now()
        relation.save()

        for file_obj in PatientFile.objects.filter(doctor=relation.doctor, patient=relation.patient, is_disposed=False):
            dispose_file(file_obj, reason="Patient authorization revoked")

        return Response({"message": "Access revoked.", "data": PatientDoctorAccessSerializer(relation).data})


class DoctorPatientSearchView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        q = (self.request.query_params.get("q") or "").strip()
        if not q:
            return User.objects.none()
        return User.objects.filter(role=User.Role.PATIENT).filter(
            Q(username__icontains=q) | Q(email__icontains=q)
        ).order_by("username")[:20]


class PatientDoctorSearchView(generics.ListAPIView):
    permission_classes = [IsPatient]
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        q = (self.request.query_params.get("q") or "").strip()
        if not q:
            return User.objects.none()
        return User.objects.filter(role=User.Role.DOCTOR).filter(
            Q(username__icontains=q) | Q(email__icontains=q)
        ).order_by("username")[:20]


class DoctorCreateUploadRequestView(APIView):
    permission_classes = [IsDoctor]

    def post(self, request):
        patient_id = (request.data.get("patient_id") or "").strip()
        message = (request.data.get("message") or "").strip()
        if not patient_id:
            return Response({"detail": "patient_id is required."}, status=400)

        has_access = PatientDoctorAccess.objects.filter(
            doctor=request.user,
            patient_id=patient_id,
            status=PatientDoctorAccess.Status.APPROVED,
        ).exists()
        if not has_access:
            return Response({"detail": "You must have approved access first."}, status=403)

        upload_request = FileUploadRequest.objects.create(
            doctor=request.user,
            patient_id=patient_id,
            message=message,
        )
        return Response(
            {"message": "Upload request sent.", "data": FileUploadRequestSerializer(upload_request).data},
            status=status.HTTP_201_CREATED,
        )


class PatientListUploadRequestsView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        queryset = FileUploadRequest.objects.filter(patient=request.user, is_open=True).order_by("-created_at")
        return Response(FileUploadRequestSerializer(queryset, many=True).data)


class PatientCloseUploadRequestView(APIView):
    permission_classes = [IsPatient]

    def post(self, request, req_id):
        upload_request = FileUploadRequest.objects.filter(id=req_id, patient=request.user).first()
        if not upload_request:
            return Response({"detail": "Request not found."}, status=404)
        upload_request.is_open = False
        upload_request.closed_at = timezone.now()
        upload_request.save()
        return Response({"message": "Request closed."})
