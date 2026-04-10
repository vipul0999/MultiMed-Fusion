import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { useAuth } from "./state/AuthContext";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { AdminConsolePage } from "./views/AdminConsolePage";
import { DoctorWorkspacePage } from "./views/DoctorWorkspacePage";
import { LoginPage } from "./views/LoginPage";
import { PatientWorkspacePage } from "./views/PatientWorkspacePage";
import { RegisterPage } from "./views/RegisterPage";

function RoleHomeRedirect() {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (user.role === "doctor") {
    return <Navigate to="/app/doctor" replace />;
  }
  if (user.role === "patient") {
    return <Navigate to="/app/patient" replace />;
  }
  if (user.role === "admin") {
    return <Navigate to="/app/admin" replace />;
  }
  return <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RoleHomeRedirect />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route
          path="/app/doctor"
          element={
            <ProtectedRoute allowedRoles={["doctor"]}>
              <DoctorWorkspacePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/app/patient"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <PatientWorkspacePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/app/admin"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <AdminConsolePage />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
