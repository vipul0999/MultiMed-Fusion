import { useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

import { doctorService } from "../api/services";
import { normalizeApiError } from "../lib/errors";
import { useAuth } from "../state/AuthContext";

const CHAT_STORAGE_KEY = "doctor_chat_threads_v1";

function formatDate(value) {
  if (!value) return "Not available";
  return new Date(value).toLocaleString();
}

function readStoredThreads() {
  try {
    return JSON.parse(sessionStorage.getItem(CHAT_STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function writeStoredThreads(threads) {
  sessionStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(threads));
}

export function DoctorWorkspacePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [workspace, setWorkspace] = useState(null);
  const [selectedRelationship, setSelectedRelationship] = useState(null);
  const [files, setFiles] = useState([]);
  const [selectedFileIds, setSelectedFileIds] = useState([]);
  const [patientQuery, setPatientQuery] = useState("");
  const [patientMatches, setPatientMatches] = useState([]);
  const [doctorUploadFiles, setDoctorUploadFiles] = useState([]);
  const [uploadRequestMessage, setUploadRequestMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [threads, setThreads] = useState(() => readStoredThreads());

  async function loadWorkspace() {
    try {
      const data = await doctorService.workspace();
      setWorkspace(data);
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to load doctor workspace."));
    }
  }

  async function loadPatientFiles(relationship) {
    try {
      const data = await doctorService.listPatientFiles(relationship.patient.id);
      setSelectedRelationship(relationship);
      setFiles(data);
      setSelectedFileIds([]);
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to load patient files."));
    }
  }

  useEffect(() => {
    void loadWorkspace();
  }, []);

  useEffect(() => {
    writeStoredThreads(threads);
  }, [threads]);

  useEffect(() => {
    let cancelled = false;
    async function runSearch() {
      if (!patientQuery.trim()) {
        setPatientMatches([]);
        return;
      }
      try {
        const data = await doctorService.searchPatients(patientQuery.trim());
        if (!cancelled) setPatientMatches(data);
      } catch (error) {
        if (!cancelled) toast.error(normalizeApiError(error, "Unable to search patients."));
      }
    }
    void runSearch();
    return () => {
      cancelled = true;
    };
  }, [patientQuery]);

  async function handleRequestAccess(patientId) {
    try {
      await doctorService.requestAccess({ patient_id: patientId, note: "Requesting chart access." });
      toast.success("Access request sent.");
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to request access."));
    }
  }

  async function handleUpload() {
    if (!selectedRelationship) {
      toast.error("Select a patient first.");
      return;
    }
    if (!doctorUploadFiles.length) {
      toast.error("Choose files to upload.");
      return;
    }
    const formData = new FormData();
    formData.append("patient_id", selectedRelationship.patient.id);
    doctorUploadFiles.forEach((file) => formData.append("files", file));
    try {
      await doctorService.uploadForPatient(formData);
      setDoctorUploadFiles([]);
      toast.success("Files uploaded.");
      await loadPatientFiles(selectedRelationship);
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to upload files."));
    }
  }

  async function handleUploadRequest() {
    if (!selectedRelationship) {
      toast.error("Select a patient first.");
      return;
    }
    try {
      await doctorService.requestUpload({
        patient_id: selectedRelationship.patient.id,
        message: uploadRequestMessage || "Please upload the requested records.",
      });
      setUploadRequestMessage("");
      toast.success("Upload request sent.");
      await loadWorkspace();
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to send request."));
    }
  }

  async function handleAnalyze() {
    if (!selectedRelationship || !selectedFileIds.length) {
      toast.error("Select files first.");
      return;
    }
    try {
      await doctorService.analyzeFiles({ patient_id: selectedRelationship.patient.id, file_ids: selectedFileIds });
      toast.success("Files analyzed.");
      await loadPatientFiles(selectedRelationship);
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to analyze files."));
    }
  }

  async function handleAsk(event) {
    event.preventDefault();
    if (!selectedRelationship) {
      toast.error("Select a patient first.");
      return;
    }
    if (!question.trim()) {
      toast.error("Enter a question.");
      return;
    }

    const patientId = selectedRelationship.patient.id;
    const nextUserMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      content: question.trim(),
      createdAt: new Date().toISOString(),
      fileIds: [...selectedFileIds],
    };

    const historyForBackend = [...(threads[patientId] || []), nextUserMessage].map((item) => ({
      role: item.role,
      content: item.content,
    }));

    setThreads((current) => ({
      ...current,
      [patientId]: [...(current[patientId] || []), nextUserMessage],
    }));
    setQuestion("");
    setChatLoading(true);

    try {
      const result = await doctorService.askQuestion({
        patient_id: patientId,
        message: nextUserMessage.content,
        file_ids: selectedFileIds,
        conversation_history: historyForBackend,
        top_k: 6,
      });

      const assistantMessage = {
        id: `${Date.now()}-assistant`,
        role: "assistant",
        content: result.summary,
        createdAt: new Date().toISOString(),
        sources: result.sources || [],
        confidence: result.confidence,
      };

      setThreads((current) => ({
        ...current,
        [patientId]: [...(current[patientId] || []), assistantMessage],
      }));
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to get answer."));
      setThreads((current) => ({
        ...current,
        [patientId]: (current[patientId] || []).filter((item) => item.id !== nextUserMessage.id),
      }));
    } finally {
      setChatLoading(false);
    }
  }

  function clearConversation() {
    if (!selectedRelationship) return;
    const patientId = selectedRelationship.patient.id;
    setThreads((current) => ({ ...current, [patientId]: [] }));
  }

  const approvedPatients = workspace?.approved_patients || [];
  const pendingRequests = workspace?.pending_requests || [];
  const activeThread = useMemo(() => {
    if (!selectedRelationship) return [];
    return threads[selectedRelationship.patient.id] || [];
  }, [selectedRelationship, threads]);

  return (
    <div className="app-page" data-testid="doctor-workspace">
      <header className="topbar">
        <div>
          <h1>Doctor Workspace</h1>
          <p>{user?.email}</p>
        </div>
        <div className="topbar-actions">
          <button data-testid="doctor-refresh" className="button button-secondary" type="button" onClick={loadWorkspace}>
            Refresh
          </button>
          <button
            data-testid="doctor-signout"
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
            <h2>Find patient</h2>
            <input
              data-testid="doctor-search-patient"
              value={patientQuery}
              onChange={(event) => setPatientQuery(event.target.value)}
              placeholder="Search patient"
            />
            <div className="stack">
              {patientMatches.map((patient) => (
                <div key={patient.id} className="row" data-testid={`doctor-search-result-${patient.username}`}>
                  <div>
                    <strong>{patient.username}</strong>
                    <p>{patient.email}</p>
                  </div>
                  <button
                    data-testid={`doctor-request-access-${patient.username}`}
                    className="button button-secondary"
                    type="button"
                    onClick={() => handleRequestAccess(patient.id)}
                  >
                    Request
                  </button>
                </div>
              ))}
            </div>
          </section>

          <section className="card">
            <h2>Patients</h2>
            <div className="stack">
              {approvedPatients.map((relationship) => (
                <button
                  data-testid={`doctor-approved-patient-${relationship.patient.username}`}
                  type="button"
                  key={relationship.id}
                  className={`row row-button ${selectedRelationship?.id === relationship.id ? "row-active" : ""}`}
                  onClick={() => loadPatientFiles(relationship)}
                >
                  <div>
                    <strong>{relationship.patient.username}</strong>
                    <p>{relationship.files_count || 0} files</p>
                  </div>
                </button>
              ))}
              {!approvedPatients.length ? <p>No approved patients.</p> : null}
            </div>
          </section>

          <section className="card">
            <h2>Pending requests</h2>
            <div className="stack">
              {pendingRequests.map((relationship) => (
                <div key={relationship.id} className="row" data-testid={`doctor-pending-request-${relationship.patient.username}`}>
                  <div>
                    <strong>{relationship.patient.username}</strong>
                    <p>{relationship.note || "Waiting for patient approval"}</p>
                  </div>
                </div>
              ))}
              {!pendingRequests.length ? <p>No pending requests.</p> : null}
            </div>
          </section>
        </aside>

        <main className="content">
          <section className="card">
            <h2>{selectedRelationship ? selectedRelationship.patient.username : "Select a patient"}</h2>
            <p>
              {selectedRelationship
                ? `Connected ${formatDate(selectedRelationship.approved_at || selectedRelationship.created_at)}`
                : "Choose a patient from the left to view files and ask questions."}
            </p>
          </section>

          <section className="grid-2">
            <section className="card">
              <h2>Upload files</h2>
              <input
                data-testid="doctor-upload-files-input"
                type="file"
                multiple
                accept=".pdf,.txt,.md,.log,.csv,.json,.xml,.doc,.docx,.rtf,.png,.jpg,.jpeg,.bmp,.tif,.tiff,.webp,.dcm,.mp3,.wav,.m4a,.ogg,.flac,.opus"
                onChange={(event) => setDoctorUploadFiles(Array.from(event.target.files || []))}
              />
              <button data-testid="doctor-upload-submit" className="button" type="button" onClick={handleUpload}>
                Upload
              </button>
            </section>

            <section className="card">
              <h2>Request files from patient</h2>
              <textarea
                data-testid="doctor-upload-request-message"
                rows={4}
                value={uploadRequestMessage}
                onChange={(event) => setUploadRequestMessage(event.target.value)}
                placeholder="Ask the patient to upload records"
              />
              <button data-testid="doctor-upload-request-submit" className="button button-secondary" type="button" onClick={handleUploadRequest}>
                Send request
              </button>
            </section>
          </section>

          <section className="card">
            <div className="section-head">
              <h2>Files</h2>
              <button data-testid="doctor-analyze-selected" className="button" type="button" onClick={handleAnalyze}>
                Analyze selected
              </button>
            </div>
            <div className="stack">
              {files.map((file) => (
                <label key={file.id} className="file-row" data-testid={`doctor-file-row-${file.id}`}>
                  <div className="file-check">
                    <input
                      data-testid={`doctor-file-checkbox-${file.id}`}
                      type="checkbox"
                      checked={selectedFileIds.includes(file.id)}
                      onChange={() =>
                        setSelectedFileIds((current) =>
                          current.includes(file.id) ? current.filter((value) => value !== file.id) : [...current, file.id],
                        )
                      }
                    />
                    <div>
                      <strong>{file.display_name || file.original_name}</strong>
                      <p>
                        {file.file_type} · {file.processing_status}
                      </p>
                    </div>
                  </div>
                  {file.download_url ? (
                    <a className="button button-secondary" href={file.download_url} target="_blank" rel="noreferrer">
                      Open
                    </a>
                  ) : null}
                </label>
              ))}
              {!files.length ? <p>No files available for this patient.</p> : null}
            </div>
          </section>

          <section className="card chat-card">
            <div className="section-head">
              <h2>Clinical assistant</h2>
              <button className="button button-secondary" type="button" onClick={clearConversation} disabled={!activeThread.length}>
                Clear conversation
              </button>
            </div>

            <div className="chat-window">
              {activeThread.length ? (
                activeThread.map((message) => (
                  <article
                    key={message.id}
                    className={`chat-bubble ${message.role === "assistant" ? "chat-bubble-assistant" : "chat-bubble-user"}`}
                  >
                    <div className="chat-meta">
                      <strong>{message.role === "assistant" ? "Assistant" : "Doctor"}</strong>
                      <span>{formatDate(message.createdAt)}</span>
                    </div>
                    <p>{message.content}</p>
                    {message.role === "assistant" && message.sources?.length ? (
                      <div className="chat-sources">
                        {message.sources.map((source) => (
                          <a
                            key={source.file_id}
                            className="source-chip"
                            href={source.download_url || source.hyperlink}
                            target="_blank"
                            rel="noreferrer"
                          >
                            {source.name}
                          </a>
                        ))}
                      </div>
                    ) : null}
                  </article>
                ))
              ) : (
                <div className="chat-empty">
                  <p>Ask about the selected files. Previous messages for this patient will stay visible here.</p>
                </div>
              )}
            </div>

            <form className="chat-composer" onSubmit={handleAsk}>
              <textarea
                data-testid="doctor-chat-question"
                rows={3}
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Ask a clinical question about the selected files"
              />
              <button data-testid="doctor-chat-send" className="button" type="submit" disabled={chatLoading}>
                {chatLoading ? "Thinking..." : "Send"}
              </button>
            </form>
          </section>
        </main>
      </div>
    </div>
  );
}
