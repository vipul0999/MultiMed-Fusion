import React, {useState} from "react";
import {
    FiUser, FiUploadCloud, FiSend, FiFileText, FiImage, FiLogOut,
} from "react-icons/fi";

const initialPatients = [{
    id: 1, name: "John Doe", note: "Diabetes follow-up", files: [], messages: [], analyzed: false, summary: "",
}, {
    id: 2, name: "Jane Miller", note: "Chest pain evaluation", files: [], messages: [], analyzed: false, summary: "",
},];

// DEMO CREDENTIALS
const DEFAULT_EMAIL = "doctor@example.com";
const DEFAULT_PASSWORD = "doctor123";

// Hardcoded summaries (Gemini-like)
const PATIENT_SUMMARIES = {
    1: `Files analyzed. Summary for John Doe:
- Long-standing type 2 diabetes with moderate HbA1c elevation.
- Recent labs show slightly elevated fasting glucose.
- No acute red-flag findings in current reports.
- Recommended focus: medication adherence, diet, and follow-up labs in 3 months.`, 2: `Files analyzed. Summary for Jane Miller:
- Recent chest pain workup with normal ECG and troponin.
- Mildly elevated cholesterol and blood pressure.
- No evidence of acute coronary syndrome in current documents.
- Recommended focus: risk factor modification and outpatient cardiology follow-up.`,
};

export default function App() {
    // LOGIN STATE
    const [loggedIn, setLoggedIn] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loginError, setLoginError] = useState("");

    // PATIENT STATE
    const [patients, setPatients] = useState(initialPatients);
    const [selectedId, setSelectedId] = useState(initialPatients[0].id);
    const [chatInput, setChatInput] = useState("");

    const selectedPatient = patients.find((p) => p.id === selectedId) || patients[0];

    // LOGIN HANDLERS
    const handleLogin = (e) => {
        e.preventDefault();

        if (email === DEFAULT_EMAIL && password === DEFAULT_PASSWORD) {
            setLoggedIn(true);
            setLoginError("");
        } else {
            setLoginError("Invalid email or password.");
        }
    };

    const handleLogout = () => {
        setLoggedIn(false);
        setEmail("");
        setPassword("");
        setLoginError("");
    };

    // FILE UPLOAD
    const handleFileUpload = (e) => {
        const files = Array.from(e.target.files || []);
        if (!files.length) return;

        setPatients((prev) => prev.map((p) => p.id === selectedId ? {
            ...p, files: [...p.files, ...files.map((f, i) => ({
                id: p.files.length + i + 1,
                name: f.name,
                size: `${(f.size / 1024).toFixed(1)} KB`,
                type: f.type.includes("image") ? "image" : "pdf",
            })),],
        } : p));

        e.target.value = "";
    };

    // ANALYZE → SET SUMMARY + INITIAL MESSAGE
    const handleAnalyze = () => {
        setPatients((prev) => prev.map((p) => {
            if (p.id !== selectedId) return p;

            const hardcodedSummary = PATIENT_SUMMARIES[p.id] || `Files analyzed. Summary for ${p.name}:
- All documents processed successfully.
- No critical red flags detected in this demo.
- This is placeholder text for your eventual real AI summary.`;

            return {
                ...p, analyzed: true, summary: hardcodedSummary, messages: p.messages.length > 0 ? p.messages : [{
                    from: "ai",
                    text: "I’ve finished analyzing the uploaded files. You can now ask follow-up questions about this patient.",
                },],
            };
        }));
    };

    // CHAT SEND
    const handleSend = () => {
        if (!chatInput.trim() || !selectedPatient.analyzed) return;

        const doctorMsg = {from: "doctor", text: chatInput.trim()};
        const aiMsg = {
            from: "ai",
            text: `The medication he is taking is Metformin ${selectedPatient.name}.`,
        };

        setPatients((prev) => prev.map((p) => p.id === selectedId ? {
            ...p, messages: [...p.messages, doctorMsg, aiMsg]
        } : p));

        setChatInput("");
    };

    // ---------------------------------------------------------------
    // LOGIN SCREEN
    // ---------------------------------------------------------------
    if (!loggedIn) {
        return (<div
            style={{
                height: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                background: "radial-gradient(circle at 0 0,#020617,transparent 55%), #020617",
            }}
        >
            <form
                onSubmit={handleLogin}
                style={{
                    background: "radial-gradient(circle at 0 0,rgba(56,189,248,0.15),transparent), #0f172a",
                    padding: 30,
                    borderRadius: 16,
                    width: 320,
                    color: "#e2e8f0",
                    display: "flex",
                    flexDirection: "column",
                    gap: 12,
                    border: "1px solid rgba(148,163,184,0.4)",
                    boxShadow: "0 18px 40px rgba(15,23,42,0.9)",
                }}
            >
                <h2
                    style={{
                        textAlign: "center", marginBottom: 4, fontSize: 20,
                    }}
                >
                    Doctor Login
                </h2>

                <p
                    style={{
                        fontSize: 12, opacity: 0.8, marginTop: 0, marginBottom: 8,
                    }}
                >
                    Demo credentials:
                    <br/>
                    <strong>Email:</strong> {DEFAULT_EMAIL}
                    <br/>
                    <strong>Password:</strong> {DEFAULT_PASSWORD}
                </p>

                <input
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{
                        padding: 10,
                        borderRadius: 999,
                        border: "1px solid #475569",
                        background: "#020617",
                        color: "white",
                        fontSize: 13,
                    }}
                    required
                />

                <input
                    placeholder="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{
                        padding: 10,
                        borderRadius: 999,
                        border: "1px solid #475569",
                        background: "#020617",
                        color: "white",
                        fontSize: 13,
                    }}
                    required
                />

                {loginError && (<div
                    style={{
                        color: "#fecaca",
                        background: "rgba(239,68,68,0.15)",
                        borderRadius: 8,
                        padding: "6px 8px",
                        fontSize: 12,
                    }}
                >
                    {loginError}
                </div>)}

                <button
                    type="submit"
                    style={{
                        marginTop: 10,
                        padding: 10,
                        borderRadius: 999,
                        background: "linear-gradient(135deg,#22c55e,#4ade80)",
                        border: "none",
                        fontWeight: 600,
                        cursor: "pointer",
                        color: "#022c22",
                    }}
                >
                    Login
                </button>
            </form>
        </div>);
    }

    // ---------------------------------------------------------------
    // MAIN APP AFTER LOGIN
    // ---------------------------------------------------------------
    return (<div
        style={{
            minHeight: "100vh",
            display: "flex",
            justifyContent: "center",
            background: "radial-gradient(circle at 0 0,#0b1120,transparent 55%), radial-gradient(circle at 100% 100%,#022c22,transparent 55%), #020617",
            padding: 16,
            color: "#e5e7eb",
        }}
    >
        <div
            style={{
                display: "grid", gridTemplateColumns: "260px minmax(0,1fr)", gap: 16, maxWidth: 1200, width: "100%",
            }}
        >
            {/* SIDEBAR */}
            <aside
                style={{
                    background: "rgba(15,23,42,0.96)",
                    padding: 16,
                    borderRadius: 20,
                    border: "1px solid rgba(148,163,184,0.6)",
                    display: "flex",
                    flexDirection: "column",
                    gap: 12,
                }}
            >
                <h3 style={{margin: 0, fontSize: 16}}>Patients</h3>

                {patients.map((p) => {
                    const active = p.id === selectedId;
                    return (<button
                        key={p.id}
                        onClick={() => setSelectedId(p.id)}
                        style={{
                            borderRadius: 999,
                            padding: "8px 10px",
                            background: active ? "linear-gradient(135deg,#4f46e5,#0ea5e9)" : "transparent",
                            color: active ? "#fff" : "#cbd5f5",
                            border: "none",
                            textAlign: "left",
                            cursor: "pointer",
                            display: "flex",
                            alignItems: "center",
                            gap: 8,
                        }}
                    >
                        <FiUser/>
                        <div>
                            <div style={{fontWeight: 500}}>
                                {p.name}
                            </div>
                            <div
                                style={{
                                    fontSize: 11, opacity: 0.7,
                                }}
                            >
                                {p.note}
                            </div>
                        </div>
                    </button>);
                })}
            </aside>

            {/* MAIN PANEL */}
            <main
                style={{
                    background: "rgba(15,23,42,0.96)",
                    padding: 16,
                    borderRadius: 20,
                    border: "1px solid rgba(148,163,184,0.6)",
                    display: "flex",
                    flexDirection: "column",
                    gap: 16,
                }}
            >
                {/* TOP BAR + LOGOUT */}
                <div
                    style={{
                        display: "flex", justifyContent: "space-between", alignItems: "center",
                    }}
                >
                    <div>
                        <div style={{fontSize: 17, fontWeight: 600}}>
                            {selectedPatient.name}
                        </div>
                        <div
                            style={{
                                fontSize: 12, opacity: 0.7,
                            }}
                        >
                            Files & AI summary are stored per patient
                        </div>
                    </div>

                    <button
                        onClick={handleLogout}
                        style={{
                            padding: "8px 12px",
                            borderRadius: 999,
                            background: "rgba(239,68,68,0.18)",
                            border: "1px solid rgba(239,68,68,0.4)",
                            color: "#fecaca",
                            cursor: "pointer",
                            display: "flex",
                            alignItems: "center",
                            gap: 6,
                            fontSize: 13,
                        }}
                    >
                        <FiLogOut/>
                        Logout
                    </button>
                </div>

                <div
                    style={{
                        display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16,
                    }}
                >
                    {/* LEFT: UPLOAD + ANALYZE */}
                    <section
                        style={{
                            background: "rgba(15,23,42,1)",
                            padding: 14,
                            borderRadius: 16,
                            border: "1px solid rgba(148,163,184,0.6)",
                            display: "flex",
                            flexDirection: "column",
                            gap: 10,
                        }}
                    >
                        <h3 style={{margin: 0, fontSize: 15}}>
                            Upload files
                        </h3>

                        <label
                            style={{
                                padding: 14,
                                borderRadius: 14,
                                border: "1px dashed rgba(148,163,184,0.6)",
                                textAlign: "center",
                                cursor: "pointer",
                                display: "flex",
                                flexDirection: "column",
                                alignItems: "center",
                                gap: 4,
                                background: "radial-gradient(circle at 0 0,rgba(59,130,246,0.18),transparent), rgba(15,23,42,0.9)",
                            }}
                        >
                            <FiUploadCloud size={20}/>
                            <div style={{fontSize: 13}}>
                                Select PDFs / images
                            </div>
                            <input
                                type="file"
                                multiple
                                hidden
                                onChange={handleFileUpload}
                            />
                        </label>

                        <button
                            onClick={handleAnalyze}
                            style={{
                                padding: "8px 14px",
                                borderRadius: 999,
                                border: "none",
                                background: "linear-gradient(135deg,#22c55e,#4ade80)",
                                color: "#022c22",
                                cursor: "pointer",
                                fontSize: 13,
                                fontWeight: 600,
                            }}
                        >
                            Analyze files
                        </button>

                        <h4 style={{margin: "4px 0", fontSize: 14}}>
                            Files
                        </h4>

                        <div
                            style={{
                                maxHeight: 180, overflowY: "auto", display: "flex", flexDirection: "column", gap: 6,
                            }}
                        >
                            {selectedPatient.files.length === 0 && (<div
                                style={{
                                    fontSize: 12, opacity: 0.6,
                                }}
                            >
                                No files uploaded yet.
                            </div>)}

                            {selectedPatient.files.map((f) => (<div
                                key={f.id}
                                style={{
                                    padding: "6px 8px",
                                    borderRadius: 10,
                                    background: "rgba(15,23,42,0.95)",
                                    border: "1px solid rgba(148,163,184,0.4)",
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 10,
                                }}
                            >
                                {f.type === "image" ? (<FiImage/>) : (<FiFileText/>)}
                                <div style={{fontSize: 12}}>
                                    {f.name}
                                    <div
                                        style={{
                                            opacity: 0.7, fontSize: 11,
                                        }}
                                    >
                                        {f.size}
                                    </div>
                                </div>
                            </div>))}
                        </div>
                    </section>

                    {/* RIGHT: GEMINI-LIKE CHAT + SUMMARY */}
                    <section
                        style={{
                            background: "rgba(15,23,42,1)",
                            padding: 14,
                            borderRadius: 16,
                            border: "1px solid rgba(148,163,184,0.6)",
                            display: "flex",
                            flexDirection: "column",
                            gap: 10,
                        }}
                    >
                        <h3 style={{margin: 0, fontSize: 15}}>
                            AI summary & chat
                        </h3>

                        {/* SUMMARY CARD AFTER ANALYZE */}
                        {selectedPatient.analyzed ? (<div
                            style={{
                                borderRadius: 16,
                                padding: 12,
                                background: "radial-gradient(circle at 0 0,rgba(129,140,248,0.2),transparent), rgba(15,23,42,0.95)",
                                border: "1px solid rgba(129,140,248,0.7)",
                            }}
                        >
                            <div
                                style={{
                                    fontSize: 12, color: "#a5b4fc", fontWeight: 600, marginBottom: 4,
                                }}
                            >
                                Files analyzed — following is the summary
                            </div>
                            <div
                                style={{
                                    fontSize: 13, whiteSpace: "pre-wrap", color: "#e5e7eb",
                                }}
                            >
                                {selectedPatient.summary}
                            </div>
                        </div>) : (<div
                            style={{
                                borderRadius: 16,
                                padding: 12,
                                background: "rgba(15,23,42,0.95)",
                                border: "1px dashed rgba(148,163,184,0.7)",
                                fontSize: 12,
                                textAlign: "center",
                                opacity: 0.8,
                            }}
                        >
                            Upload at least one file and click{" "}
                            <strong>Analyze files</strong> to see the
                            AI summary and chat.
                        </div>)}

                        {/* CHAT WINDOW */}
                        <div
                            style={{
                                height: 200,
                                overflowY: "auto",
                                borderRadius: 12,
                                padding: 8,
                                background: "rgba(15,23,42,0.98)",
                                border: "1px solid rgba(148,163,184,0.4)",
                                display: "flex",
                                flexDirection: "column",
                                gap: 8,
                            }}
                        >
                            {!selectedPatient.analyzed && (<div
                                style={{
                                    textAlign: "center", opacity: 0.6, marginTop: 50, fontSize: 12,
                                }}
                            >
                                Chat will be available after files are
                                analyzed.
                            </div>)}

                            {selectedPatient.analyzed && selectedPatient.messages.map((m, i) => (<div
                                key={i}
                                style={{
                                    display: "flex", justifyContent: m.from === "doctor" ? "flex-end" : "flex-start",
                                }}
                            >
                                <div
                                    style={{
                                        padding: "8px 10px",
                                        borderRadius: 12,
                                        maxWidth: "70%",
                                        background: m.from === "doctor" ? "linear-gradient(135deg,#22c55e,#4ade80)" : "rgba(15,23,42,0.95)",
                                        color: m.from === "doctor" ? "#022c22" : "#e5e7eb",
                                        border: m.from === "doctor" ? "none" : "1px solid rgba(129,140,248,0.6)",
                                        fontSize: 13,
                                    }}
                                >
                                    {m.text}
                                </div>
                            </div>))}
                        </div>

                        {/* CHAT INPUT ROW */}
                        <div style={{display: "flex", gap: 8}}>
                                <textarea
                                    disabled={!selectedPatient.analyzed}
                                    rows={2}
                                    placeholder={selectedPatient.analyzed ? "Ask a question about this patient’s summary…" : "Analyze files first"}
                                    value={chatInput}
                                    onChange={(e) => setChatInput(e.target.value)}
                                    style={{
                                        flex: 1,
                                        borderRadius: 12,
                                        padding: 10,
                                        background: "rgba(15,23,42,0.98)",
                                        border: "1px solid rgba(148,163,184,0.4)",
                                        color: "#fff",
                                        resize: "none",
                                        fontSize: 13,
                                    }}
                                />

                            <button
                                onClick={handleSend}
                                disabled={!selectedPatient.analyzed}
                                style={{
                                    width: 44,
                                    height: 44,
                                    borderRadius: "50%",
                                    background: "linear-gradient(135deg,#22c55e,#4ade80)",
                                    color: "#022c22",
                                    border: "none",
                                    display: "flex",
                                    justifyContent: "center",
                                    alignItems: "center",
                                    cursor: selectedPatient.analyzed ? "pointer" : "default",
                                    opacity: selectedPatient.analyzed ? 1 : 0.4,
                                }}
                            >
                                <FiSend/>
                            </button>
                        </div>
                    </section>
                </div>
            </main>
        </div>
    </div>);
}
