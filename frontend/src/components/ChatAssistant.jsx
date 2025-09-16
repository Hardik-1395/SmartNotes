import React, { useState,useEffect } from "react";
import { Send } from "lucide-react";


const ChatAssistant = ({ summary }) => {
  const [chatMessages, setChatMessages] = useState([
    { from: "bot", text: "Hi! 👋 Ask me anything about the summary." },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [prompts, setPrompts] = useState([]);

  useEffect(() => {
    const fetchPrompts = async () => {
      try {
        const res = await fetch("http://localhost:5000/prompts", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ summary }), // send summary so backend can generate context-aware prompts
        });

        const data = await res.json();
        setPrompts(data.prompts || []); // fallback empty if none
      } catch (err) {
        console.error("Failed to fetch prompts:", err);
        setPrompts([]);
      }
    };

    if (summary) fetchPrompts();
  }, [summary]);

   const handleSendMessage = async () => {
    if (!chatInput.trim()) return;

    setChatInput("");
    const userMsg = { from: "user", text: chatInput };
    setChatMessages((prev) => [...prev, userMsg]);

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: chatInput,
          summary, 
        }),
      });

      const data = await res.json();

      const botMsg = { from: "bot", text: data.reply || "⚠️ No reply received." };
      setChatMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Error in chat:", err);
      setChatMessages((prev) => [
        ...prev,
        { from: "bot", text: "❌ Failed to get response from server." },
      ]);
    }

    
  };

  return (
    <div className="flex flex-col h-full relative">
      {/* Chat Messages */}
      <div className="space-y-2 h-full overflow-y-auto mb-20 ">
        {chatMessages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
              msg.from === "bot"
                ? "bg-gray-700 text-white self-start"
                : "bg-green-600 text-white self-end ml-auto"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* Clickable Bot Prompts */}
      {prompts.length > 0 && (
        <div className="mb-16 flex flex-wrap gap-2">
          {prompts.map((msg, idx) => (
            <div
              key={idx}
              onClick={() => {
                setChatInput(msg.text);
                setTimeout(() => handleSendMessage(), 0);
              }}
              className="bg-blue-600 text-white px-3 py-1 rounded-lg text-sm cursor-pointer"
            >
              {msg.text}
            </div>
          ))}
        </div>
      )}

      {/* Input Box */}
      <div className="flex absolute bottom-0 w-full bg-gray-900 p-2">
        <input
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          placeholder="Ask about the summary..."
          className="flex-1 p-2 rounded-l bg-gray-800 text-white"
        />
        <button onClick={handleSendMessage}>
          <Send className="bg-yellow-400 size-10 p-2 text-black rounded-md" />
        </button>
      </div>
    </div>
  );
};

export default ChatAssistant;
