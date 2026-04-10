#medfiles/urls.py

from django.urls import path

from .views import (
    DoctorAnalyzeFilesView,
    DoctorChatQueryView,
    DoctorListPatientFilesView,
    DoctorUploadFilesForPatientView,
    PatientFileMetadataUpdateView,
    PatientListDoctorFilesView,
    PatientUploadFilesView,
    SecureFileDownloadView,
)

urlpatterns = [
    path("patient/upload/", PatientUploadFilesView.as_view()),
    path("patient/doctors/<str:doctor_id>/files/", PatientListDoctorFilesView.as_view()),
    path("doctor/patients/<str:patient_id>/files/", DoctorListPatientFilesView.as_view()),
    path("doctor/files/<str:file_id>/update/", PatientFileMetadataUpdateView.as_view()),
    path("doctor/analyze/", DoctorAnalyzeFilesView.as_view()),
    path("doctor/patient-upload/", DoctorUploadFilesForPatientView.as_view()),
    path("doctor/chat-query/", DoctorChatQueryView.as_view()),
    path("files/<str:file_id>/download/", SecureFileDownloadView.as_view()),
]
