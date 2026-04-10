import { useNavigate } from "react-router-dom";
import { getUser, logout } from "../auth/auth";

export default function TopBar() {
    const nav = useNavigate();
    const user = getUser();

    function handleLogout() {
        logout();
        nav("/login");
    }

    return (
        <div
            style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "14px 18px",
                borderBottom: "1px solid #eee",
                fontFamily: "sans-serif",
            }}
        >
            <div>
                <div style={{ fontSize: 18, fontWeight: 700 }}>Doctor Portal</div>
                <div style={{ fontSize: 13, opacity: 0.7 }}>
                    Logged in as: {user?.username} ({user?.role})
                </div>
            </div>

            <button
                onClick={handleLogout}
                style={{
                    padding: "8px 12px",
                    border: "1px solid #ddd",
                    background: "white",
                    cursor: "pointer",
                    borderRadius: 8,
                }}
            >
                Logout
            </button>
        </div>
    );
}