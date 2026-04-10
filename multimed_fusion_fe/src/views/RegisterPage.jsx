import { useState } from "react";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";

import { normalizeApiError } from "../lib/errors";
import { useAuth } from "../state/AuthContext";

export function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [form, setForm] = useState({ username: "", email: "", password: "", role: "patient" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await register(form);
      toast.success("Account created. Please sign in.");
      navigate("/login");
    } catch (err) {
      const message = normalizeApiError(err, "Unable to create account.");
      setError(message);
      toast.error(message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <section className="auth-hero">
        <span className="eyebrow">Create account</span>
        <h1>Set up the right role before entering the portal.</h1>
        <p>
          Doctors get a patient review workspace and grounded assistant. Patients get a clean dashboard for approvals,
          uploads, and file visibility.
        </p>
      </section>

      <form className="auth-card" onSubmit={handleSubmit}>
        <div>
          <span className="eyebrow">Registration</span>
          <h2>Create portal access</h2>
        </div>

        <label className="field">
          <span>Username</span>
          <input
            value={form.username}
            onChange={(event) => setForm((current) => ({ ...current, username: event.target.value }))}
            required
          />
        </label>

        <label className="field">
          <span>Email</span>
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
            required
          />
        </label>

        <label className="field">
          <span>Password</span>
          <input
            type="password"
            value={form.password}
            onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))}
            required
          />
        </label>

        <label className="field">
          <span>Role</span>
          <select value={form.role} onChange={(event) => setForm((current) => ({ ...current, role: event.target.value }))}>
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
            <option value="admin">Admin</option>
          </select>
        </label>

        {error ? <div className="form-message form-message--error">{error}</div> : null}

        <button type="submit" className="primary-button" disabled={submitting}>
          {submitting ? "Creating..." : "Create account"}
        </button>

        <p className="auth-footnote">
          Already registered? <Link to="/login">Back to sign in</Link>
        </p>
      </form>
    </div>
  );
}
