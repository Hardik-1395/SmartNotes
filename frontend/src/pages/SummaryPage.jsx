import React, { useState } from "react";
import ChatAssistant from "../components/ChatAssistant.jsx";

export default function SummaryPage({ summary, loading }) {
  const [activeTab, setActiveTab] = useState("summary");

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white p-4 rounded-lg shadow-lg">
      {/* Tabs */}
      <div className="flex mb-4">
        <button
          onClick={() => setActiveTab("summary")}
          className={`px-4 py-2 rounded ${
            activeTab === "summary"
              ? "bg-blue-600 text-white"
              : "bg-gray-700 text-gray-300"
          }`}
        >
          Summary
        </button>
        <button
          onClick={() => setActiveTab("chat")}
          disabled={!summary}
          className={`px-4 py-2 rounded ml-2 ${
            activeTab === "chat"
              ? "bg-blue-600 text-white"
              : "bg-gray-700 text-gray-300"
          } ${!summary && "opacity-50 cursor-not-allowed"}`}
        >
          Ask AI
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === "summary" && (
          <div className="bg-gray-800 p-4 rounded-lg shadow-inner whitespace-pre-wrap">
            {loading
              ? "⏳ Generating summary..."
              : summary || "No summary yet."}
          </div>
        )}
        {activeTab === "chat" && summary && <ChatAssistant summary={summary} />}
      </div>
    </div>
  );
}
