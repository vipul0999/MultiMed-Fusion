import React, { useState } from "react";

// ForgotPassword.jsx
// Default-exported React component (Tailwind CSS classes used)
// Usage: import ForgotPassword from "./ForgotPassword" and render <ForgotPassword />

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const validateEmail = (value) => {
    // simple email regex
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    setError(null);

    if (!email) {
      setError("Email is required.");
      return;
    }
    if (!validateEmail(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    setLoading(true);
    try {
      // TODO: change endpoint to your backend endpoint
      const res = await fetch("/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.message || `Request failed: ${res.status}`);
      }

      const data = await res.json();
      // Backend should return a friendly message (e.g. "If that email exists, we've sent a reset link.")
      setMessage(data.message || "If that email exists, you'll receive a reset link shortly.");
      setEmail("");
    } catch (err) {
      console.error(err);
      setError(err.message || "Something went wrong. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white rounded-2xl shadow-lg">
      <h1 className="text-2xl font-semibold mb-2">Forgot password</h1>
      <p className="text-sm text-muted-foreground mb-6">
        Enter the email associated with your account and we'll send a link to reset your
        password.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block">
          <span className="text-sm font-medium">Email</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="mt-1 block w-full rounded-lg border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-indigo-400"
            aria-label="Email address"
          />
        </label>

        {error && (
          <div className="text-sm text-red-600" role="alert">
            {error}
          </div>
        )}

        {message && (
          <div className="text-sm text-green-700" role="status">
            {message}
          </div>
        )}

        <div className="flex items-center justify-between">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center px-4 py-2 rounded-lg bg-indigo-600 text-white font-medium disabled:opacity-60"
          >
            {loading ? "Sending..." : "Send reset link"}
          </button>
        </div>
      </form>

      <hr className="my-6" />

      <div className="text-sm text-center text-gray-600">
        <a href="/login" className="underline">
          Back to login
        </a>
      </div>
    </div>
  );
}
