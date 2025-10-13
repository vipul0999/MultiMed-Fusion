import React, { useState, useRef } from "react";


export default function AccountSettings() {
  const [avatar, setAvatar] = useState(null); // { file, url }
  const [fullName, setFullName] = useState("Prasanna Rana");
  const [email, setEmail] = useState("prasanna@example.com");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [twoFAEnabled, setTwoFAEnabled] = useState(false);
  const [notifications, setNotifications] = useState({
    email: true,
    sms: false,
    productUpdates: true,
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const fileInputRef = useRef(null);

  // ======= Helpers =======
  function validateEmail(e) {
    // simple email regex (sufficient for client-side validation)
    return /^\S+@\S+\.\S+$/.test(e);
  }

  function passwordStrength(pw) {
    if (!pw) return 0;
    let score = 0;
    if (pw.length >= 8) score += 1;
    if (/[A-Z]/.test(pw)) score += 1;
    if (/[0-9]/.test(pw)) score += 1;
    if (/[^A-Za-z0-9]/.test(pw)) score += 1;
    return score; // 0..4
  }

  // Mock API - need to with real fetch/axios calls
  async function fakeApiSave(payload) {
    // emulate network latency
    await new Promise((r) => setTimeout(r, 800));
    // emulate success
    return { ok: true, data: payload };
  }

  async function fakeApiDelete() {
    await new Promise((r) => setTimeout(r, 800));
    return { ok: true };
  }

  // ======= Handlers =======
  function handleAvatarChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    // cleanup previous object URL when overwritten
    if (avatar?.url) URL.revokeObjectURL(avatar.url);
    setAvatar({ file, url });
  }

  function handleRemoveAvatar() {
    if (avatar?.url) URL.revokeObjectURL(avatar.url);
    setAvatar(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function toggleNotification(key) {
    setNotifications((prev) => ({ ...prev, [key]: !prev[key] }));
  }

  async function handleSave(e) {
    e.preventDefault();
    setError(null);
    setMessage(null);

    if (!fullName.trim()) {
      setError("Full name is required.");
      return;
    }
    if (!validateEmail(email)) {
      setError("Please enter a valid email address.");
      return;
    }
    if (newPassword || confirmPassword) {
      if (newPassword !== confirmPassword) {
        setError("New password and confirmation do not match.");
        return;
      }
      if (passwordStrength(newPassword) < 3) {
        setError(
          "Password is too weak. Use at least 8 characters, include numbers, and mix case/symbols."
        );
        return;
      }
    }

    setSaving(true);

    try {
      // Build payload
      const payload = new FormData();
      payload.append("fullName", fullName);
      payload.append("email", email);
      payload.append("twoFAEnabled", String(twoFAEnabled));
      payload.append("notifications", JSON.stringify(notifications));
      if (avatar?.file) payload.append("avatar", avatar.file);
      if (newPassword) payload.append("newPassword", newPassword);

      // Replace with real API call
      const res = await fakeApiSave(payload);
      if (!res.ok) throw new Error("Failed to save settings.");

      setMessage("Settings saved successfully.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteAccount() {
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      const res = await fakeApiDelete();
      if (!res.ok) throw new Error("Failed to delete account.");
      setMessage("Your account was deleted. We're sorry to see you go.");
      // In real app: redirect to logged-out landing page
    } catch (err) {
      setError(err.message || "Unable to delete account.");
    } finally {
      setSaving(false);
      setShowDeleteConfirm(false);
    }
  }

  const pwStrength = passwordStrength(newPassword);
  const pwLabels = ["Very weak", "Weak", "Fair", "Good", "Strong"];

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white shadow-md rounded-2xl p-6">
        <h1 className="text-2xl font-semibold mb-4">Account settings</h1>

        <form onSubmit={handleSave} className="space-y-6">
          {/* Profile row */}
          <div className="flex gap-6 items-center">
            <div className="w-28">
              <div className="rounded-full w-28 h-28 overflow-hidden border border-gray-200 bg-gray-50 flex items-center justify-center">
                {avatar ? (
                  // eslint-disable-next-line jsx-a11y/img-redundant-alt
                  <img src={avatar.url} alt="avatar preview" className="w-full h-full object-cover" />
                ) : (
                  <span className="text-sm text-gray-500">No avatar</span>
                )}
              </div>
              <div className="mt-3 flex gap-2">
                <label className="inline-flex items-center px-3 py-1 bg-gray-100 rounded-md text-sm cursor-pointer">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarChange}
                    className="hidden"
                  />
                  <span>Upload</span>
                </label>
                <button type="button" onClick={handleRemoveAvatar} className="px-3 py-1 bg-red-50 rounded-md text-sm text-red-600">
                  Remove
                </button>
              </div>
            </div>

            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700">Full name</label>
              <input
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-200 shadow-sm p-2"
                placeholder="Your full name"
              />

              <label className="block text-sm font-medium text-gray-700 mt-3">Email</label>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-200 shadow-sm p-2"
                placeholder="you@example.com"
              />
            </div>
          </div>

          {/* Password change */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h2 className="text-lg font-medium">Change password</h2>
            <p className="text-sm text-gray-600">Leave blank to keep your current password.</p>

            <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="block text-sm">Current password</label>
                <input
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-200 shadow-sm p-2"
                />
              </div>

              <div>
                <label className="block text-sm">New password</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-200 shadow-sm p-2"
                />
                <div className="text-xs mt-1">Strength: {pwLabels[pwStrength]}</div>
                <div className="w-full bg-gray-200 h-1 rounded-full mt-2">
                  <div style={{ width: `${(pwStrength / 4) * 100}%` }} className="h-1 rounded-full bg-green-500" />
                </div>
              </div>

              <div>
                <label className="block text-sm">Confirm new password</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-200 shadow-sm p-2"
                />
              </div>
            </div>
          </div>

          {/* Security toggles */}
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-white rounded-lg border">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-medium">Two-factor authentication</h3>
                  <p className="text-xs text-gray-500">Protect your account with an additional verification step.</p>
                </div>
                <div>
                  <label className="inline-flex items-center">
                    <input
                      type="checkbox"
                      checked={twoFAEnabled}
                      onChange={() => setTwoFAEnabled((v) => !v)}
                      className="form-checkbox h-5 w-5 rounded"
                    />
                  </label>
                </div>
              </div>

              {twoFAEnabled && (
                <div className="mt-3 text-sm text-gray-600">
                  Two-factor is enabled. You can manage your authenticator apps from your profile on the mobile app.
                </div>
              )}
            </div>

            <div className="p-4 bg-white rounded-lg border">
              <h3 className="text-sm font-medium">Notifications</h3>
              <p className="text-xs text-gray-500">Choose how we contact you</p>

              <div className="mt-3 space-y-2">
                <label className="flex items-center justify-between">
                  <div className="text-sm">Email notifications</div>
                  <input
                    type="checkbox"
                    checked={notifications.email}
                    onChange={() => toggleNotification("email")}
                    className="form-checkbox h-5 w-5 rounded"
                  />
                </label>

                <label className="flex items-center justify-between">
                  <div className="text-sm">SMS notifications</div>
                  <input
                    type="checkbox"
                    checked={notifications.sms}
                    onChange={() => toggleNotification("sms")}
                    className="form-checkbox h-5 w-5 rounded"
                  />
                </label>

                <label className="flex items-center justify-between">
                  <div className="text-sm">Product updates</div>
                  <input
                    type="checkbox"
                    checked={notifications.productUpdates}
                    onChange={() => toggleNotification("productUpdates")}
                    className="form-checkbox h-5 w-5 rounded"
                  />
                </label>
              </div>
            </div>
          </div>

          {/* messages */}
          {error && <div className="text-red-600">{error}</div>}
          {message && <div className="text-green-600">{message}</div>}

          {/* Actions */}
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <button
                type="submit"
                disabled={saving}
                className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:opacity-95 disabled:opacity-60"
              >
                {saving ? "Saving..." : "Save changes"}
              </button>

              <button
                type="button"
                onClick={() => {
                  // Reset form (for demo)
                  setFullName("Prasanna Rana");
                  setEmail("prasanna@example.com");
                  setAvatar(null);
                  setTwoFAEnabled(false);
                  setNotifications({ email: true, sms: false, productUpdates: true });
                  setMessage(null);
                  setError(null);
                }}
                className="px-3 py-2 border rounded-md text-sm"
              >
                Reset
              </button>
            </div>

            <div>
              <button
                type="button"
                onClick={() => setShowDeleteConfirm(true)}
                className="px-3 py-2 bg-red-50 text-red-600 border rounded-md text-sm"
              >
                Delete account
              </button>
            </div>
          </div>
        </form>

        {/* Delete confirm modal (simple inline) */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 flex items-center justify-center bg-black/40">
            <div className="bg-white p-6 rounded-lg w-full max-w-md">
              <h3 className="text-lg font-medium">Confirm account deletion</h3>
              <p className="mt-2 text-sm text-gray-600">This action is irreversible. Type <strong>DELETE</strong> to confirm.</p>

              <DeleteConfirm onConfirm={handleDeleteAccount} onCancel={() => setShowDeleteConfirm(false)} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function DeleteConfirm({ onConfirm, onCancel }) {
  const [value, setValue] = useState("");
  return (
    <div className="mt-4">
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Type DELETE to confirm"
        className="w-full p-2 border rounded-md"
      />

      <div className="mt-3 flex justify-end gap-2">
        <button onClick={onCancel} className="px-3 py-2 border rounded-md">
          Cancel
        </button>
        <button
          onClick={() => value === "DELETE" && onConfirm()}
          disabled={value !== "DELETE"}
          className="px-3 py-2 bg-red-600 text-white rounded-md disabled:opacity-60"
        >
          Confirm delete
        </button>
      </div>
    </div>
  );
}
