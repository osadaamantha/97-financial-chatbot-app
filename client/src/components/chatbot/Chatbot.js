import React, { useState } from "react";
import "./Chatbot.css";

function Chatbot() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8800/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setResponse(data.answer || "Sorry, I couldn't find an answer.");
    } catch (err) {
      setResponse("⚠️ Error: Could not connect to chatbot service.");
    }
    setLoading(false);
  };

  return (
    <div className="chatbot-container">
      <h2>💬 Ask your financial data anything</h2>
      <input
        type="text"
        placeholder="e.g., What was the revenue in Q3 2023?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="chatbot-input"
      />
      <button onClick={askQuestion} disabled={loading} className="chatbot-button">
        {loading ? "Thinking..." : "Ask"}
      </button>
      {response && <div className="chatbot-response">{response}</div>}
    </div>
  );
}

export default Chatbot;
