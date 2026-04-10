from django.urls import path
from .views import (
    DoctorWorkspaceView,
    PatientWorkspaceView,
    DoctorApprovedPatientsView,
    DoctorOutgoingRequestsView,
    DoctorRequestAccessView,
    PatientIncomingRequestsView,
    PatientApproveRejectRequestView,
    PatientApprovedDoctorsView,
    PatientGrantDoctorAccessView,
    RevokeAccessView, DoctorPatientSearchView, PatientDoctorSearchView, DoctorCreateUploadRequestView, PatientListUploadRequestsView,
    PatientCloseUploadRequestView,
)

urlpatterns = [
    path("doctor/workspace/", DoctorWorkspaceView.as_view()),
    path("patient/workspace/", PatientWorkspaceView.as_view()),
    path("doctor/patients/", DoctorApprovedPatientsView.as_view()),
    path("doctor/requests/", DoctorOutgoingRequestsView.as_view()),
    path("doctor/request-access/", DoctorRequestAccessView.as_view()),
    path("patient/requests/", PatientIncomingRequestsView.as_view()),
    path("patient/requests/<str:rel_id>/decision/", PatientApproveRejectRequestView.as_view()),
    path("patient/doctors/", PatientApprovedDoctorsView.as_view()),
    path("patient/grant-doctor/", PatientGrantDoctorAccessView.as_view()),
    path("doctor/patient-search/", DoctorPatientSearchView.as_view()),
    path("patient/doctor-search/", PatientDoctorSearchView.as_view()),
    path("doctor/upload-request/", DoctorCreateUploadRequestView.as_view()),
    path("patient/upload-requests/", PatientListUploadRequestsView.as_view()),
    path("patient/upload-requests/<str:req_id>/close/", PatientCloseUploadRequestView.as_view()),
    path("access/<str:rel_id>/revoke/", RevokeAccessView.as_view()),
]
