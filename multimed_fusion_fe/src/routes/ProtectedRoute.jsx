import { Navigate } from "react-router-dom";

import { useAuth } from "../state/AuthContext";

export function ProtectedRoute({ children, allowedRoles }) {
  const { booting, user } = useAuth();

  if (booting) {
    return (
      <div className="app-loader">
        <div className="app-loader__card">
          <div className="pulse-dot" />
          <div>Preparing secure workspace...</div>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
