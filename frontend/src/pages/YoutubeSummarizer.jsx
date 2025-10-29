import React, { useState } from "react";
import SummaryPage from "./SummaryPage";
import VideoPreview from "../components/VideoPreview";

export default function YoutubeSummarizer() {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!url.trim()) return;
    setLoading(true);

    try {
    const res = await fetch("http://localhost:8000/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await res.json();
    setSummary(data.summary);
  } catch (err) {
    console.error(err);
    setSummary("❌ Failed to connect to backend.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="flex flex-col h-screen"> {/* 🔹 full height container */}
      <h1 className="text-3xl py-2 px-2 font-bold min-h-[50px]">
        Youtube Video Summarizer
      </h1>

      {/* Input */}
      <div className="mb-4 mt-2 flex gap-2 px-2">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste YouTube link..."
          className="flex-1 p-2 rounded bg-gray-800 text-white"
        />
        <button
          onClick={handleSummarize}
          className="px-4 py-2 bg-blue-600 rounded"
        >
          <div>{loading ? "⏳ Summarizing..." : "Summarize"}</div>
        </button>
      </div>

      <div className="grid grid-cols-[400px_1fr] flex-1 min-h-0">
        <VideoPreview url={url} />
        <SummaryPage summary={summary} loading={loading} />
      </div>
    </div>
  );
}

