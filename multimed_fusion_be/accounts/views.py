from bson import ObjectId
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from medfiles.models import PatientDocChunk, PatientFile
from portal.models import FileUploadRequest, PatientDoctorAccess

from .permissions import IsAdminRole
from .serializers import PasswordUpdateSerializer, RegisterSerializer, UserMeSerializer

User = get_user_model()


def _json_safe(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    return obj


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer

    def get_object(self):
        return self.request.user


class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordUpdateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": str(self.user.id),
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
        }
        return data


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class AdminDashboardDataView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request, *args, **kwargs):
        users_by_role = User.objects.values("role").annotate(count=Count("id")).order_by("role")
        links_by_status = (
            PatientDoctorAccess.objects.values("status").annotate(count=Count("id")).order_by("status")
        )
        reqs_by_open = FileUploadRequest.objects.values("is_open").annotate(count=Count("id")).order_by("is_open")

        payload = {
            "summary": {
                "users_total": User.objects.count(),
                "users_by_role": list(users_by_role),
                "links_by_status": list(links_by_status),
                "upload_requests_by_open": list(reqs_by_open),
                "files_total": PatientFile.objects.count(),
                "files_processed": PatientFile.objects.filter(is_processed=True).count(),
                "chunks_total": PatientDocChunk.objects.count(),
            },
            "recent": {
                "users": list(
                    User.objects.order_by("-date_joined").values(
                        "id", "username", "email", "role", "is_active", "date_joined"
                    )[:50]
                ),
                "access_links": list(
                    PatientDoctorAccess.objects.order_by("-updated_at").values(
                        "id",
                        "status",
                        "requested_by",
                        "note",
                        "created_at",
                        "updated_at",
                        "doctor_id",
                        "patient_id",
                    )[:100]
                ),
                "upload_requests": list(
                    FileUploadRequest.objects.order_by("-created_at").values(
                        "id", "doctor_id", "patient_id", "message", "is_open", "created_at"
                    )[:100]
                ),
                "files": list(
                    PatientFile.objects.order_by("-uploaded_at").values(
                        "id",
                        "patient_id",
                        "doctor_id",
                        "display_name",
                        "mime_type",
                        "file_type",
                        "uploaded_at",
                        "is_processed",
                        "is_disposed",
                    )[:100]
                ),
                "chunks": list(
                    PatientDocChunk.objects.order_by("-created_at").values(
                        "id",
                        "patient_id",
                        "doctor_id",
                        "batch_hash",
                        "chunk_id",
                        "chunk_index",
                        "source_file_ids",
                        "source_file_names",
                        "created_at",
                        "embedding_model",
                        "embedding_norm",
                    )[:100]
                ),
            },
        }
        return Response(_json_safe(payload), status=200)
