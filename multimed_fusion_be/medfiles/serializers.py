from pathlib import Path

from rest_framework import serializers

from .models import PatientFile

SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".txt": "text",
    ".md": "text",
    ".log": "text",
    ".csv": "text",
    ".json": "text",
    ".xml": "text",
    ".docx": "docx",
    ".doc": "doc",
    ".rtf": "doc",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".bmp": "image",
    ".tif": "image",
    ".tiff": "image",
    ".webp": "image",
    ".dcm": "dicom",
    ".mp3": "mp3",
    ".wav": "wav",
    ".m4a": "audio",
    ".ogg": "audio",
    ".flac": "audio",
    ".opus": "audio",
}


def validate_uploaded_files(files):
    if not files:
        raise serializers.ValidationError("At least one file is required.")
    for file_obj in files:
        suffix = Path(file_obj.name or "").suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise serializers.ValidationError(
                f"Unsupported file: {file_obj.name}. Allowed types include PDF, office/text documents, images, DICOM, and audio."
            )
        if getattr(file_obj, "size", 0) <= 0:
            raise serializers.ValidationError(f"File {file_obj.name} is empty.")
        if getattr(file_obj, "size", 0) > 25 * 1024 * 1024:
            raise serializers.ValidationError(f"File {file_obj.name} exceeds the 25 MB upload limit.")


class PatientFileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    patient_id = serializers.CharField(source="patient.id", read_only=True)
    doctor_id = serializers.CharField(source="doctor.id", read_only=True)
    download_url = serializers.SerializerMethodField()
    text_preview = serializers.SerializerMethodField()

    class Meta:
        model = PatientFile
        fields = [
            "id",
            "patient_id",
            "doctor_id",
            "original_name",
            "display_name",
            "title",
            "description",
            "summary",
            "mime_type",
            "file_type",
            "extension",
            "file_size",
            "uploaded_by_role",
            "download_url",
            "uploaded_at",
            "is_processed",
            "processing_status",
            "processing_steps",
            "extracted_payload",
            "text_preview",
            "authorized_until",
            "is_disposed",
            "disposed_at",
            "last_error",
            "last_processed_at",
        ]

    def get_download_url(self, obj):
        request = self.context.get("request")
        if not request or obj.is_disposed:
            return None
        return request.build_absolute_uri(f"/api/medfiles/files/{obj.id}/download/")

    def get_text_preview(self, obj):
        preview = (obj.summary or obj.extracted_text or "").strip()
        return preview[:400] if preview else ""


class PatientUploadSerializer(serializers.Serializer):
    doctor_id = serializers.CharField()
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False)

    def validate(self, attrs):
        validate_uploaded_files(attrs.get("files") or [])
        return attrs


class DoctorPatientUploadSerializer(serializers.Serializer):
    patient_id = serializers.CharField()
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False)

    def validate(self, attrs):
        validate_uploaded_files(attrs.get("files") or [])
        return attrs


class DoctorAnalyzeSerializer(serializers.Serializer):
    patient_id = serializers.CharField()
    file_ids = serializers.ListField(child=serializers.CharField(), allow_empty=False)


class DoctorChatQuerySerializer(serializers.Serializer):
    patient_id = serializers.CharField()
    message = serializers.CharField()
    file_ids = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, default=list)
    selected_file_ids = serializers.ListField(child=serializers.JSONField(), required=False, allow_empty=True)
    selectedFiles = serializers.ListField(child=serializers.JSONField(), required=False, allow_empty=True)
    conversation_history = serializers.ListField(child=serializers.JSONField(), required=False, default=list)
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=20, default=6)

    def validate(self, attrs):
        raw_file_ids = (
            attrs.get("file_ids")
            or attrs.get("selected_file_ids")
            or attrs.get("selectedFiles")
            or self.initial_data.get("file_ids")
            or self.initial_data.get("selected_file_ids")
            or self.initial_data.get("selectedFiles")
            or []
        )

        normalized_file_ids = []
        for item in raw_file_ids:
            value = item
            if isinstance(item, dict):
                value = item.get("id") or item.get("file_id") or item.get("value")
            if value is None:
                continue
            value = str(value).strip()
            if value:
                normalized_file_ids.append(value)

        attrs["file_ids"] = normalized_file_ids
        return attrs


class PatientFileMetadataUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, max_length=500)
    display_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
