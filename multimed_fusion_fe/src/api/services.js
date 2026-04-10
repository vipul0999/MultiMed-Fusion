import { api } from "./client";

export const authService = {
  login: (payload) => api.post("/api/auth/login/", payload).then((res) => res.data),
  register: (payload) => api.post("/api/auth/register/", payload).then((res) => res.data),
  refresh: (refresh) => api.post("/api/auth/token/refresh/", { refresh }).then((res) => res.data),
  me: () => api.get("/api/auth/me/").then((res) => res.data),
  updatePassword: (payload) => api.post("/api/auth/password/update/", payload).then((res) => res.data),
  adminDashboard: () => api.get("/api/auth/admin/dashboard-data/").then((res) => res.data),
};

export const doctorService = {
  workspace: () => api.get("/api/portal/doctor/workspace/").then((res) => res.data),
  approvedPatients: () => api.get("/api/portal/doctor/patients/").then((res) => res.data),
  outgoingRequests: () => api.get("/api/portal/doctor/requests/").then((res) => res.data),
  searchPatients: (query) =>
    api.get("/api/portal/doctor/patient-search/", { params: { q: query } }).then((res) => res.data),
  requestAccess: (payload) => api.post("/api/portal/doctor/request-access/", payload).then((res) => res.data),
  requestUpload: (payload) => api.post("/api/portal/doctor/upload-request/", payload).then((res) => res.data),
  listPatientFiles: (patientId) => api.get(`/api/medfiles/doctor/patients/${patientId}/files/`).then((res) => res.data),
  uploadForPatient: (formData) =>
    api
      .post("/api/medfiles/doctor/patient-upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => res.data),
  updateFileMetadata: (fileId, payload) =>
    api.post(`/api/medfiles/doctor/files/${fileId}/update/`, payload).then((res) => res.data),
  analyzeFiles: (payload) => api.post("/api/medfiles/doctor/analyze/", payload).then((res) => res.data),
  askQuestion: (payload) => api.post("/api/medfiles/doctor/chat-query/", payload).then((res) => res.data),
};

export const patientService = {
  workspace: () => api.get("/api/portal/patient/workspace/").then((res) => res.data),
  incomingRequests: () => api.get("/api/portal/patient/requests/").then((res) => res.data),
  approvedDoctors: () => api.get("/api/portal/patient/doctors/").then((res) => res.data),
  searchDoctors: (query) =>
    api.get("/api/portal/patient/doctor-search/", { params: { q: query } }).then((res) => res.data),
  uploadRequests: () => api.get("/api/portal/patient/upload-requests/").then((res) => res.data),
  decideRequest: (relationshipId, decision) =>
    api.post(`/api/portal/patient/requests/${relationshipId}/decision/`, { decision }).then((res) => res.data),
  grantDoctor: (payload) => api.post("/api/portal/patient/grant-doctor/", payload).then((res) => res.data),
  listDoctorFiles: (doctorId) =>
    api.get(`/api/medfiles/patient/doctors/${doctorId}/files/`).then((res) => res.data),
  uploadFiles: (formData) =>
    api
      .post("/api/medfiles/patient/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => res.data),
  closeUploadRequest: (requestId) =>
    api.post(`/api/portal/patient/upload-requests/${requestId}/close/`).then((res) => res.data),
  revokeAccess: (relationshipId) => api.post(`/api/portal/access/${relationshipId}/revoke/`).then((res) => res.data),
};
