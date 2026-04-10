import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Toaster } from "react-hot-toast";

import App from "./App";
import { AuthProvider } from "./state/AuthContext";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <AuthProvider>
      <App />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3200,
          style: {
            borderRadius: "18px",
            border: "1px solid rgba(18, 32, 54, 0.08)",
            background: "#fffdf8",
            color: "#17324d",
            boxShadow: "0 18px 50px rgba(17, 34, 54, 0.12)",
          },
        }}
      />
    </AuthProvider>
  </StrictMode>,
);
