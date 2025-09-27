// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

// Import pages/components
import Home from "./pages/Home";
import Exercises from "./pages/Exercises";
import ExerciseDetail from "./pages/ExerciseDetail";
import Progress from "./pages/Progress";
import Settings from "./pages/Settings";

function App() {
  return (
    <Router>
      <div>
        {/* Navigation Bar */}
        <nav style={{ padding: "10px", background: "#f0f0f0" }}>
          <Link to="/" style={{ margin: "0 10px" }}>Home</Link>
          <Link to="/exercises" style={{ margin: "0 10px" }}>Exercises</Link>
          <Link to="/progress" style={{ margin: "0 10px" }}>Progress</Link>
          <Link to="/settings" style={{ margin: "0 10px" }}>Settings</Link>
        </nav>

        {/* Define Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/exercises" element={<Exercises />} />
          <Route path="/exercises/:id" element={<ExerciseDetail />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/settings" element={<Settings />} />
          {/* Fallback route */}
          <Route path="*" element={<h2>404 - Page Not Found</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
