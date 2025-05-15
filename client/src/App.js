// src/App.js
import React from "react";
import Dashboard from "./components/dashboard/Dashboard";
import Chatbot from "./components/chatbot/Chatbot";
import "./App.css";

function App() {
  return (
    <div className="app-wrapper">
      <h1>📊 Financial Dashboard</h1>
      <Dashboard />
      <div className="chatbot-section">
        <h2>💬 Financial Chatbot</h2>
        <Chatbot />
      </div>
    </div>
  );
}

export default App;
