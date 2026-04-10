import { useState } from "react";
import toast from "react-hot-toast";
import { useNavigate, Link } from "react-router-dom";

import { normalizeApiError } from "../lib/errors";
import { useAuth } from "../state/AuthContext";

export function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ username: "", password: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const user = await login(form);
      toast.success("Signed in successfully.");
      navigate(user.role === "doctor" ? "/app/doctor" : user.role === "patient" ? "/app/patient" : "/app/admin");
    } catch (err) {
      const message = normalizeApiError(err, "Unable to sign in.");
      setError(message);
      toast.error(message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <section className="auth-hero">
        <span className="eyebrow">Clinical retrieval workspace</span>
        <h1>One simple chart for secure file sharing and grounded medical review.</h1>
        <p>
          Patients control access. Doctors review only approved records. The assistant answers from selected files
          only, including PDFs, documents, images, and audio transcripts.
        </p>
      </section>

      <form className="auth-card" onSubmit={handleSubmit}>
        <div>
          <span className="eyebrow">Sign in</span>
          <h2>Open your workspace</h2>
        </div>

        <label className="field">
          <span>Username</span>
          <input
            data-testid="login-username"
            value={form.username}
            onChange={(event) => setForm((current) => ({ ...current, username: event.target.value }))}
            autoComplete="username"
            required
          />
        </label>

        <label className="field">
          <span>Password</span>
          <input
            data-testid="login-password"
            type="password"
            value={form.password}
            onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))}
            autoComplete="current-password"
            required
          />
        </label>

        {error ? <div data-testid="login-error" className="form-message form-message--error">{error}</div> : null}

        <button data-testid="login-submit" type="submit" className="primary-button" disabled={submitting}>
          {submitting ? "Signing in..." : "Sign in"}
        </button>

        <p className="auth-footnote">
          Need an account? <Link to="/register">Create one</Link>
        </p>
      </form>
    </div>
  );
}
