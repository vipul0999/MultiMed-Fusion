from django.urls import path
from .views import PatientFileUploadView, PatientFileSearchView

urlpatterns = [
    path('upload/', PatientFileUploadView.as_view(), name='patient_file_upload'),
    path("search/", PatientFileSearchView.as_view(), name="patient-file-search"),

]
