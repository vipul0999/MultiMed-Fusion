import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

import { patientService } from "../api/services";
import { normalizeApiError } from "../lib/errors";
import { useAuth } from "../state/AuthContext";

function formatDate(value) {
  if (!value) return "Not available";
  return new Date(value).toLocaleString();
}

export function PatientWorkspacePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [workspace, setWorkspace] = useState(null);
  const [selectedRelationship, setSelectedRelationship] = useState(null);
  const [doctorFiles, setDoctorFiles] = useState([]);
  const [doctorQuery, setDoctorQuery] = useState("");
  const [doctorMatches, setDoctorMatches] = useState([]);
  const [grantNote, setGrantNote] = useState("");
  const [filesToUpload, setFilesToUpload] = useState([]);

  async function loadWorkspace() {
    try {
      const data = await patientService.workspace();
      setWorkspace(data);
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to load patient workspace."));
    }
  }

  async function loadDoctorFiles(relationship) {
    try {
      const data = await patientService.listDoctorFiles(relationship.doctor.id);
      setSelectedRelationship(relationship);
      setDoctorFiles(data);
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to load shared files."));
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadWorkspace();
  }, []);

  useEffect(() => {
    let cancelled = false;
    async function runSearch() {
      if (!doctorQuery.trim()) {
        setDoctorMatches([]);
        return;
      }
      try {
        const data = await patientService.searchDoctors(doctorQuery.trim());
        if (!cancelled) setDoctorMatches(data);
      } catch (error) {
        if (!cancelled) toast.error(normalizeApiError(error, "Unable to search doctors."));
      }
    }
    void runSearch();
    return () => {
      cancelled = true;
    };
  }, [doctorQuery]);

  async function handleDecision(relationshipId, decision) {
    try {
      await patientService.decideRequest(relationshipId, decision);
      toast.success(`Request ${decision}.`);
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to update request."));
    }
  }

  async function handleGrantDoctor(doctorId) {
    try {
      await patientService.grantDoctor({ doctor_id: doctorId, note: grantNote });
      toast.success("Doctor added.");
      setGrantNote("");
      setDoctorQuery("");
      setDoctorMatches([]);
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to grant access."));
    }
  }

  async function handleUpload() {
    if (!selectedRelationship) {
      toast.error("Select a doctor first.");
      return;
    }
    if (!filesToUpload.length) {
      toast.error("Choose files to upload.");
      return;
    }
    const formData = new FormData();
    formData.append("doctor_id", selectedRelationship.doctor.id);
    filesToUpload.forEach((file) => formData.append("files", file));
    try {
      await patientService.uploadFiles(formData);
      setFilesToUpload([]);
      toast.success("Files uploaded.");
      await loadDoctorFiles(selectedRelationship);
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to upload files."));
    }
  }

  async function handleCloseUploadRequest(requestId) {
    try {
      await patientService.closeUploadRequest(requestId);
      toast.success("Request marked complete.");
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to close request."));
    }
  }

  async function handleRevoke(relationshipId) {
    try {
      await patientService.revokeAccess(relationshipId);
      setSelectedRelationship(null);
      setDoctorFiles([]);
      toast.success("Access revoked.");
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to revoke access."));
    }
  }

  const pendingRequests = workspace?.pending_requests || [];
  const approvedDoctors = workspace?.approved_doctors || [];
  const uploadRequests = workspace?.upload_requests || [];

  return (
    <div className="app-page" data-testid="patient-workspace">
      <header className="topbar">
        <div>
          <h1>Patient Workspace</h1>
          <p>{user?.email}</p>
        </div>
        <div className="topbar-actions">
          <button data-testid="patient-refresh" className="button button-secondary" type="button" onClick={loadWorkspace}>
            Refresh
          </button>
          <button
            data-testid="patient-signout"
            className="button button-secondary"
            type="button"
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            Sign out
          </button>
        </div>
      </header>

      <div className="simple-layout">
        <aside className="sidebar">
          <section className="card">
            <h2>Pending doctor requests</h2>
            <div className="stack">
              {pendingRequests.map((relationship) => (
                <div key={relationship.id} className="row" data-testid={`patient-pending-request-${relationship.doctor.username}`}>
                  <div>
                    <strong>{relationship.doctor.username}</strong>
                    <p>{relationship.note || relationship.doctor.email}</p>
                  </div>
                  <div className="row-actions">
                    <button
                      data-testid={`patient-approve-request-${relationship.doctor.username}`}
                      className="button"
                      type="button"
                      onClick={() => handleDecision(relationship.id, "approved")}
                    >
                      Approve
                    </button>
                    <button
                      data-testid={`patient-reject-request-${relationship.doctor.username}`}
                      className="button button-secondary"
                      type="button"
                      onClick={() => handleDecision(relationship.id, "rejected")}
                    >
                      Reject
                    </button>
                  </div>
                </div>
              ))}
              {!pendingRequests.length ? <p>No pending requests.</p> : null}
            </div>
          </section>

          <section className="card">
            <h2>Add doctor</h2>
            <input
              data-testid="patient-search-doctor"
              value={doctorQuery}
              onChange={(event) => setDoctorQuery(event.target.value)}
              placeholder="Search doctor"
            />
            <textarea
              data-testid="patient-grant-note"
              rows={3}
              value={grantNote}
              onChange={(event) => setGrantNote(event.target.value)}
              placeholder="Optional note"
            />
            <div className="stack">
              {doctorMatches.map((doctor) => (
                <div key={doctor.id} className="row" data-testid={`patient-search-result-${doctor.username}`}>
                  <div>
                    <strong>{doctor.username}</strong>
                    <p>{doctor.email}</p>
                  </div>
                  <button
                    data-testid={`patient-add-doctor-${doctor.username}`}
                    className="button button-secondary"
                    type="button"
                    onClick={() => handleGrantDoctor(doctor.id)}
                  >
                    Add
                  </button>
                </div>
              ))}
            </div>
          </section>

          <section className="card">
            <h2>Doctors</h2>
            <div className="stack">
              {approvedDoctors.map((relationship) => (
                <button
                  data-testid={`patient-approved-doctor-${relationship.doctor.username}`}
                  type="button"
                  key={relationship.id}
                  className={`row row-button ${selectedRelationship?.id === relationship.id ? "row-active" : ""}`}
                  onClick={() => loadDoctorFiles(relationship)}
                >
                  <div>
                    <strong>{relationship.doctor.username}</strong>
                    <p>{relationship.files_count || 0} files</p>
                  </div>
                </button>
              ))}
              {!approvedDoctors.length ? <p>No approved doctors.</p> : null}
            </div>
          </section>
        </aside>

        <main className="content">
          <section className="card">
            <h2>{selectedRelationship ? selectedRelationship.doctor.username : "Select a doctor"}</h2>
            <p>
              {selectedRelationship
                ? `Connected ${formatDate(selectedRelationship.approved_at || selectedRelationship.created_at)}`
                : "Choose a doctor from the left to view shared files."}
            </p>
            {selectedRelationship ? (
              <button data-testid="patient-revoke-access" className="button button-secondary" type="button" onClick={() => handleRevoke(selectedRelationship.id)}>
                Revoke access
              </button>
            ) : null}
          </section>

          <section className="grid-2">
            <section className="card">
              <h2>Upload files</h2>
              <input
                data-testid="patient-upload-files-input"
                type="file"
                multiple
                accept=".pdf,.txt,.md,.log,.csv,.json,.xml,.doc,.docx,.rtf,.png,.jpg,.jpeg,.bmp,.tif,.tiff,.webp,.dcm,.mp3,.wav,.m4a,.ogg,.flac,.opus"
                onChange={(event) => setFilesToUpload(Array.from(event.target.files || []))}
              />
              <button data-testid="patient-upload-submit" className="button" type="button" onClick={handleUpload}>
                Upload
              </button>
            </section>

            <section className="card">
              <h2>Open upload requests</h2>
              <div className="stack">
                {uploadRequests.map((request) => (
                  <div key={request.id} className="row" data-testid={`patient-upload-request-${request.doctor.username}`}>
                    <div>
                      <strong>{request.doctor.username}</strong>
                      <p>{request.message || "Please upload records."}</p>
                    </div>
                    <button
                      data-testid={`patient-close-upload-request-${request.doctor.username}`}
                      className="button button-secondary"
                      type="button"
                      onClick={() => handleCloseUploadRequest(request.id)}
                    >
                      Done
                    </button>
                  </div>
                ))}
                {!uploadRequests.length ? <p>No open upload requests.</p> : null}
              </div>
            </section>
          </section>

          <section className="card">
            <h2>Shared files</h2>
            <div className="stack">
              {doctorFiles.map((file) => (
                <div key={file.id} className="row">
                  <div>
                    <strong>{file.display_name || file.original_name}</strong>
                    <p>
                      {file.file_type} · {file.uploaded_by_role} · {formatDate(file.uploaded_at)}
                    </p>
                  </div>
                  {file.download_url ? (
                    <a className="button button-secondary" href={file.download_url} target="_blank" rel="noreferrer">
                      Open
                    </a>
                  ) : null}
                </div>
              ))}
              {!doctorFiles.length ? <p>No files shared in this connection.</p> : null}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
