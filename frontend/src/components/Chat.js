import React, { useState } from "react";
import { askQuestion } from "../api";
import Loader from "./Loader";

const Chat = ({ sessionId }) => {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMessage = { role: "user", content: question };
    setMessages(prev => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await askQuestion(question, sessionId);
      const assistantMessage = { role: "assistant", content: res.answer };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = { role: "assistant", content: "Error getting response" };
      setMessages(prev => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h3>Ask Question</h3>

      <div style={{ maxHeight: "400px", overflowY: "auto", marginBottom: "10px", border: "1px solid #ddd", padding: "10px", borderRadius: "5px" }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: "10px", textAlign: msg.role === "user" ? "right" : "left" }}>
            <span style={{ 
              display: "inline-block", 
              padding: "8px 12px", 
              borderRadius: "5px",
              backgroundColor: msg.role === "user" ? "#007bff" : "#e9ecef",
              color: msg.role === "user" ? "white" : "black",
              maxWidth: "80%"
            }}>
              {msg.content}
            </span>
          </div>
        ))}
        {loading && (
          <div style={{ marginBottom: "10px", textAlign: "left" }}>
            <span style={{ 
              display: "inline-block", 
              padding: "8px 12px", 
              borderRadius: "5px",
              backgroundColor: "#e9ecef"
            }}>
              <Loader />
            </span>
          </div>
        )}
      </div>

      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && handleAsk()}
        placeholder="Ask a question about your documents..."
        style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
      />

      <button onClick={handleAsk} disabled={loading}>
        {loading ? <Loader /> : "Ask"}
      </button>
    </div>
  );
};

export default Chat;