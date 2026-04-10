from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import FileUploadRequest, PatientDoctorAccess

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class PatientDoctorAccessSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    doctor = UserMiniSerializer(read_only=True)
    patient = UserMiniSerializer(read_only=True)
    files_count = serializers.IntegerField(read_only=True, default=0)
    open_upload_requests = serializers.IntegerField(read_only=True, default=0)
    last_file_uploaded_at = serializers.DateTimeField(read_only=True, default=None)

    class Meta:
        model = PatientDoctorAccess
        fields = [
            "id",
            "doctor",
            "patient",
            "status",
            "requested_by",
            "note",
            "consent_expires_at",
            "approved_at",
            "revoked_at",
            "created_at",
            "updated_at",
            "files_count",
            "open_upload_requests",
            "last_file_uploaded_at",
        ]


class DoctorRequestAccessCreateSerializer(serializers.Serializer):
    patient_id = serializers.CharField()
    note = serializers.CharField(required=False, allow_blank=True, max_length=500)

    def validate_patient_id(self, value):
        try:
            user = User.objects.get(id=value)
        except Exception as exc:
            raise serializers.ValidationError("Patient not found.") from exc
        if user.role != User.Role.PATIENT:
            raise serializers.ValidationError("Target user is not a patient.")
        return value


class PatientGrantDoctorCreateSerializer(serializers.Serializer):
    doctor_id = serializers.CharField()
    note = serializers.CharField(required=False, allow_blank=True, max_length=500)

    def validate_doctor_id(self, value):
        try:
            user = User.objects.get(id=value)
        except Exception as exc:
            raise serializers.ValidationError("Doctor not found.") from exc
        if user.role != User.Role.DOCTOR:
            raise serializers.ValidationError("Target user is not a doctor.")
        return value


class FileUploadRequestSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    doctor = UserMiniSerializer(read_only=True)
    patient = UserMiniSerializer(read_only=True)

    class Meta:
        model = FileUploadRequest
        fields = ["id", "doctor", "patient", "message", "is_open", "closed_at", "created_at"]
