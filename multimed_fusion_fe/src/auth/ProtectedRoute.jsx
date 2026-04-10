import { Navigate } from "react-router-dom";
import { getUser, isLoggedIn } from "./auth";

export default function ProtectedRoute({ children, allowedRoles }) {
    if (!isLoggedIn()) return <Navigate to="/login" replace />;

    const user = getUser();
    if (allowedRoles && user && !allowedRoles.includes(user.role)) {
        return <Navigate to="/login" replace />;
    }

    return children;
}