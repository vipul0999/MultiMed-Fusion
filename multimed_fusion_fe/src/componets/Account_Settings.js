import React, { useState, useEffect, ChangeEvent } from "react";



import { Avatar } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Dialog, DialogContent, DialogHeader, DialogFooter, DialogTitle } from "@/components/ui/dialog";
import { Separator } from "@/components/ui/separator";
import { Label } from "@/components/ui/label";

type UserProfile = {
  id: string;
  fullName: string;
  email: string;
  phone?: string;
  avatarUrl?: string;
  notifications: {
    email: boolean;
    push: boolean;
  };
};

export default function AccountSettings() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  const [passwords, setPasswords] = useState({ current: "", newPassword: "", confirm: "" });
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    // fetch user profile on mount — replace with real API endpoint
    setLoading(true);
    (async () => {
      try {
        const res = await fetch("/api/user/profile");
        if (!res.ok) throw new Error("Failed to load profile");
        const data: UserProfile = await res.json();
        setProfile(data);
      } catch (err) {
        console.error(err);
        setMessage("Could not load profile. You might be offline or not logged in.");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  useEffect(() => {
    // generate avatar preview when avatarFile changes
    if (!avatarFile) return setAvatarPreview(null);
    const url = URL.createObjectURL(avatarFile);
    setAvatarPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [avatarFile]);

  function handleInputChange(e: ChangeEvent<HTMLInputElement>) {
    if (!profile) return;
    const { name, value } = e.target;
    setProfile({ ...profile, [name]: value } as UserProfile);
  }

  function handleToggle(name: keyof UserProfile["notifications"]) {
    if (!profile) return;
    setProfile({ ...profile, notifications: { ...profile.notifications, [name]: !profile.notifications[name] } });
  }

  function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0] ?? null;
    setAvatarFile(f);
  }

  async function handleSaveProfile() {
    if (!profile) return;
    setSaving(true);
    setMessage(null);
    try {
      // If avatar was changed, upload first
      let avatarUrl = profile.avatarUrl;
      if (avatarFile) {
        const form = new FormData();
        form.append("file", avatarFile);
        const upload = await fetch("/api/user/avatar", { method: "POST", body: form });
        if (!upload.ok) throw new Error("Avatar upload failed");
        const body = await upload.json();
        avatarUrl = body.url; // expected response { url: string }
      }

      // Patch profile
      const res = await fetch("/api/user/profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fullName: profile.fullName,
          phone: profile.phone,
          notifications: profile.notifications,
          avatarUrl,
        }),
      });

      if (!res.ok) throw new Error("Save failed");
      const updated = await res.json();
      setProfile(updated);
      setAvatarFile(null);
      setMessage("Profile updated successfully");
    } catch (err) {
      console.error(err);
      setMessage((err as Error).message ?? "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  function validatePasswords() {
    if (!passwords.current || !passwords.newPassword || !passwords.confirm) {
      setPasswordError("Fill all password fields to change password.");
      return false;
    }
    if (passwords.newPassword !== passwords.confirm) {
      setPasswordError("New password and confirmation do not match.");
      return false;
    }
    if (passwords.newPassword.length < 8) {
      setPasswordError("Password must be at least 8 characters.");
      return false;
    }
    setPasswordError(null);
    return true;
  }

  async function handleChangePassword() {
    if (!validatePasswords()) return;
    setSaving(true);
    setMessage(null);
    try {
      const res = await fetch("/api/user/change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ current: passwords.current, newPassword: passwords.newPassword }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.message || "Password change failed");
      }
      setPasswords({ current: "", newPassword: "", confirm: "" });
      setMessage("Password updated successfully.");
    } catch (err) {
      console.error(err);
      setMessage((err as Error).message ?? "Failed to change password");
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteAccount() {
    setSaving(true);
    setMessage(null);
    try {
      const res = await fetch("/api/user", { method: "DELETE" });
      if (!res.ok) throw new Error("Could not delete account");
      // Redirect or update UI after account deletion
      setMessage("Account deleted — redirecting...");
      // for example: window.location.href = "/goodbye";
    } catch (err) {
      console.error(err);
      setMessage((err as Error).message ?? "Failed to delete account");
    } finally {
      setSaving(false);
      setShowDeleteDialog(false);
    }
  }

  if (loading) return <div className="p-6">Loading profile...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Account settings</h1>
      {message && <div className="mb-4 text-sm text-muted-foreground">{message}</div>}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left column: avatar + delete */}
        <div className="col-span-1 bg-card p-4 rounded-lg">
          <div className="flex flex-col items-center gap-3">
            <Avatar className="w-24 h-24">
              <img src={avatarPreview ?? profile?.avatarUrl ?? "/images/avatar-placeholder.png"} alt="avatar" />
            </Avatar>
            <div className="w-full">
              <Label>Profile picture</Label>
              <input type="file" accept="image/*" onChange={handleFileChange} className="mt-2 w-full" />
              {avatarPreview && <p className="text-xs mt-2">Preview shown — remember to Save changes.</p>}
            </div>

            <Separator className="my-3" />

            <div className="w-full">
              <Label>Danger zone</Label>
              <p className="text-xs mt-1 mb-2">You can deactivate or permanently delete your account here.</p>
              <Button variant="destructive" onClick={() => setShowDeleteDialog(true)} className="w-full">
                Delete account
              </Button>
            </div>
          </div>
        </div>

        {/* Right column: form */}
        <div className="col-span-2 bg-card p-6 rounded-lg">
          <section className="mb-6">
            <h2 className="text-lg font-medium mb-2">Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Full name</Label>
                <Input name="fullName" value={profile?.fullName ?? ""} onChange={handleInputChange} />
              </div>
              <div>
                <Label>Email (read-only)</Label>
                <Input value={profile?.email ?? ""} readOnly />
              </div>
              <div>
                <Label>Phone</Label>
                <Input name="phone" value={profile?.phone ?? ""} onChange={handleInputChange} />
              </div>
            </div>

            <div className="mt-4 flex items-center gap-2">
              <Button onClick={handleSaveProfile} disabled={saving}>
                {saving ? "Saving..." : "Save changes"}
              </Button>
              <Button variant="ghost" onClick={() => window.location.reload()}>
                Cancel
              </Button>
            </div>
          </section>

          <Separator className="my-6" />

          <section className="mb-6">
            <h2 className="text-lg font-medium mb-2">Security</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label>Current password</Label>
                <Input type="password" value={passwords.current} onChange={(e) => setPasswords({ ...passwords, current: e.target.value })} />
              </div>
              <div>
                <Label>New password</Label>
                <Input type="password" value={passwords.newPassword} onChange={(e) => setPasswords({ ...passwords, newPassword: e.target.value })} />
              </div>
              <div>
                <Label>Confirm new password</Label>
                <Input type="password" value={passwords.confirm} onChange={(e) => setPasswords({ ...passwords, confirm: e.target.value })} />
              </div>
            </div>
            {passwordError && <div className="text-sm text-destructive mt-2">{passwordError}</div>}

            <div className="mt-4 flex items-center gap-2">
              <Button onClick={handleChangePassword} disabled={saving}>
                {saving ? "Updating..." : "Change password"}
              </Button>
            </div>
          </section>

          <Separator className="my-6" />

          <section>
            <h2 className="text-lg font-medium mb-2">Notifications</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">Email notifications</div>
                  <div className="text-xs text-muted-foreground">Get notifications via email</div>
                </div>
                <Switch checked={profile?.notifications.email ?? false} onCheckedChange={() => handleToggle("email")} />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">Push notifications</div>
                  <div className="text-xs text-muted-foreground">Receive push notifications</div>
                </div>
                <Switch checked={profile?.notifications.push ?? false} onCheckedChange={() => handleToggle("push")} />
              </div>
            </div>
          </section>
        </div>
      </div>

      {/* Delete confirmation dialog */}
      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete account</DialogTitle>
            <p className="text-sm text-muted-foreground mt-2">This action is permanent. All your data will be deleted.</p>
          </DialogHeader>
          <DialogFooter className="mt-4">
            <Button variant="ghost" onClick={() => setShowDeleteDialog(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDeleteAccount} disabled={saving}>
              {saving ? "Deleting..." : "Delete account"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
