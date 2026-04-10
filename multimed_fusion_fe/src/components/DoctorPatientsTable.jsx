import api from "../api/axios";

export default function DoctorPatientsTable({ items, onChanged }) {
    async function revoke(relId) {
        if (!confirm("Revoke access?")) return;
        await api.post(`/api/portal/access/${relId}/revoke/`);
        onChanged?.();
    }

    return (
        <div style={card}>
            <h3 style={{ marginTop: 0 }}>Approved Patients</h3>

            {!items?.length ? (
                <div style={{ opacity: 0.7 }}>No approved patients yet.</div>
            ) : (
                <table style={table}>
                    <thead>
                    <tr>
                        <th style={th}>Patient</th>
                        <th style={th}>Email</th>
                        <th style={th}>Status</th>
                        <th style={th}>Updated</th>
                        <th style={th}>Action</th>
                    </tr>
                    </thead>
                    <tbody>
                    {items.map((rel) => (
                        <tr key={rel.id}>
                            <td style={td}>
                                {rel.patient?.username}
                                <div style={{ fontSize: 12, opacity: 0.7 }}>
                                    id: {rel.patient?.id}
                                </div>
                            </td>
                            <td style={td}>{rel.patient?.email}</td>
                            <td style={td}>{rel.status}</td>
                            <td style={td}>
                                {rel.updated_at ? new Date(rel.updated_at).toLocaleString() : "-"}
                            </td>
                            <td style={td}>
                                <button style={smallBtn} onClick={() => revoke(rel.id)}>
                                    Revoke
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

const card = {
    border: "1px solid #eee",
    borderRadius: 12,
    padding: 16,
    background: "white",
};

const table = { width: "100%", borderCollapse: "collapse" };
const th = { textAlign: "left", padding: "10px 8px", borderBottom: "1px solid #eee" };
const td = { padding: "10px 8px", borderBottom: "1px solid #f2f2f2", verticalAlign: "top" };

const smallBtn = {
    padding: "8px 10px",
    borderRadius: 10,
    border: "1px solid #ddd",
    background: "white",
    cursor: "pointer",
};