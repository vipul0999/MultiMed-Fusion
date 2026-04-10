import { useState } from "react";
import api from "../api/axios";

export default function RequestAccessForm({ onSuccess }) {
    const [patientId, setPatientId] = useState("");
    const [note, setNote] = useState("");
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState("");
    const [err, setErr] = useState("");

    async function submit(e) {
        e.preventDefault();
        setMsg("");
        setErr("");
        setLoading(true);

        try {
            const res = await api.post("/api/portal/doctor/request-access/", {
                patient_id: patientId.trim(),
                note: note.trim(),
            });
            setMsg(res.data?.message || "Request sent");
            setPatientId("");
            setNote("");
            onSuccess?.();
        } catch (error) {
            setErr(
                error?.response?.data?.detail ||
                JSON.stringify(error?.response?.data || "Request failed")
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div style={card}>
            <h3 style={{ marginTop: 0 }}>Request Patient Access</h3>

            <form onSubmit={submit} style={{ display: "grid", gap: 10 }}>
                <input
                    style={input}
                    value={patientId}
                    onChange={(e) => setPatientId(e.target.value)}
                    placeholder="Patient ObjectId (e.g. 6997e83cdefbf7ec1d6f6211)"
                    required
                />
                <input
                    style={input}
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                    placeholder="Note (optional)"
                />

                {err && <div style={{ color: "crimson" }}>{err}</div>}
                {msg && <div style={{ color: "green" }}>{msg}</div>}

                <button style={btn} disabled={loading}>
                    {loading ? "Sending..." : "Send Request"}
                </button>
            </form>
        </div>
    );
}

const card = {
    border: "1px solid #eee",
    borderRadius: 12,
    padding: 16,
    background: "white",
};

const input = {
    padding: 10,
    borderRadius: 10,
    border: "1px solid #ddd",
    outline: "none",
};

const btn = {
    padding: 10,
    borderRadius: 10,
    border: "1px solid #ddd",
    background: "white",
    cursor: "pointer",
};