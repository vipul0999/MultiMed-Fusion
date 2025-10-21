from rest_framework import serializers
from .models import PatientFile

class PatientFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientFile
        fields = ['id', 'patient', 'doctor', 'file', 'filename', 'mime_type', 'upload_time']
        read_only_fields = ['patient', 'upload_time']

    def validate_file(self, value):
        allowed_types = ['application/pdf', 'image/png', 'image/jpeg', 'text/plain', 'audio/mpeg', 'audio/wav']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("File type not allowed.")
        if value.size > 25 * 1024 * 1024:
            raise serializers.ValidationError("File too large. Max 25 MB.")
        return value

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        validated_data['filename'] = validated_data['file'].name
        validated_data['mime_type'] = validated_data['file'].content_type
        return super().create(validated_data)


class PatientFileSearchResultSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    text = serializers.CharField()
    chunk_index = serializers.IntegerField()
    score = serializers.FloatField()
