// src/App.js
import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "안녕하세요 👋 학사공지 AI입니다. 무엇을 도와드릴까요?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", { question: input });
      const botMessage = {
        sender: "bot",
        text: res.data.answer || "답변을 불러올 수 없습니다 🥲",
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ 서버 오류가 발생했습니다." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            <div className="bubble">{msg.text}</div>
          </div>
        ))}
        {loading && <div className="chat-message bot"><div className="bubble typing">...</div></div>}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="학사 관련 질문을 입력하세요 (예: 수강신청 일정)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={sendMessage}>전송</button>
      </div>
    </div>
  );
}

export default App;
