from django.contrib import admin
from .models import FileUpload, PatientFile


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file','owner','uploaded_at','content_type')


@admin.register(PatientFile)
class PatientFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'patient', 'doctor', 'upload_time')
    list_filter = ('patient', 'doctor', 'upload_time')
    search_fields = ('filename', 'patient__username', 'doctor__username')
