import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

import { authService } from "../api/services";
import { normalizeApiError } from "../lib/errors";
import { useAuth } from "../state/AuthContext";

function Stat({ label, value, hint }) {
  return (
    <article className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{hint}</small>
    </article>
  );
}

function SimpleTable({ title, rows, columns }) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>{title}</h2>
      </div>
      <div className="simple-table">
        <div className="simple-table__head">
          {columns.map((column) => (
            <span key={column.key}>{column.label}</span>
          ))}
        </div>
        {(rows || []).map((row, index) => (
          <div key={row.id || index} className="simple-table__row">
            {columns.map((column) => (
              <span key={column.key}>{column.render ? column.render(row) : row[column.key] ?? "-"}</span>
            ))}
          </div>
        ))}
        {!rows?.length ? <p className="subtle-text">No records available.</p> : null}
      </div>
    </section>
  );
}

export function AdminConsolePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [dashboard, setDashboard] = useState(null);

  async function loadDashboard() {
    try {
      const data = await authService.adminDashboard();
      setDashboard(data);
    } catch (error) {
      toast.error(normalizeApiError(error, "Unable to load admin dashboard."));
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadDashboard();
  }, []);

  const summary = dashboard?.summary || {};
  const recent = dashboard?.recent || {};

  return (
    <div className="portal-page">
      <header className="portal-header">
        <div>
          <span className="eyebrow">Admin workspace</span>
          <h1>Platform health overview</h1>
          <p>{user?.email}</p>
        </div>
        <div className="header-actions">
          <button type="button" className="secondary-button" onClick={loadDashboard}>
            Refresh
          </button>
          <button
            type="button"
            className="secondary-button"
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            Sign out
          </button>
        </div>
      </header>

      <section className="stats-grid">
        <Stat label="Users" value={summary.users_total || 0} hint="All accounts" />
        <Stat label="Files" value={summary.files_total || 0} hint={`Processed ${summary.files_processed || 0}`} />
        <Stat label="Chunks" value={summary.chunks_total || 0} hint="Retrieval records" />
        <Stat label="Upload requests" value={(summary.upload_requests_by_open || []).length} hint="Grouped by open state" />
      </section>

      <div className="two-column-grid">
        <SimpleTable
          title="Recent users"
          rows={recent.users}
          columns={[
            { key: "username", label: "Username" },
            { key: "role", label: "Role" },
            { key: "email", label: "Email" },
          ]}
        />
        <SimpleTable
          title="Access links"
          rows={recent.access_links}
          columns={[
            { key: "doctor_id", label: "Doctor" },
            { key: "patient_id", label: "Patient" },
            { key: "status", label: "Status" },
          ]}
        />
        <SimpleTable
          title="Recent files"
          rows={recent.files}
          columns={[
            { key: "display_name", label: "Name", render: (row) => row.display_name || row.original_name || "-" },
            { key: "file_type", label: "Type" },
            { key: "is_processed", label: "Processed" },
          ]}
        />
        <SimpleTable
          title="Recent chunks"
          rows={recent.chunks}
          columns={[
            { key: "chunk_id", label: "Chunk" },
            { key: "embedding_model", label: "Model" },
            {
              key: "source_file_names",
              label: "Sources",
              render: (row) => (Array.isArray(row.source_file_names) ? row.source_file_names.join(", ") : "-"),
            },
          ]}
        />
      </div>
    </div>
  );
}
