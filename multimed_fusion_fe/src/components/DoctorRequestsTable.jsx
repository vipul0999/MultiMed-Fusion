export default function DoctorRequestsTable({ items }) {
    return (
        <div style={card}>
            <h3 style={{ marginTop: 0 }}>Pending Requests</h3>

            {!items?.length ? (
                <div style={{ opacity: 0.7 }}>No pending requests.</div>
            ) : (
                <table style={table}>
                    <thead>
                    <tr>
                        <th style={th}>Patient</th>
                        <th style={th}>Note</th>
                        <th style={th}>Status</th>
                        <th style={th}>Created</th>
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
                            <td style={td}>{rel.note || "-"}</td>
                            <td style={td}>{rel.status}</td>
                            <td style={td}>
                                {rel.created_at ? new Date(rel.created_at).toLocaleString() : "-"}
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