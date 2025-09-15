import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Sidebar from "./components/Sidebar.jsx";
import YouTubeSummarizer from "./pages/YoutubeSummarizer.jsx";
import AudioVideoSummarizer from "./pages/AudioVideoSummarizer.jsx";
import PdfTextSummarizer from "./pages/PdfTextSummarizer.jsx";
import LiveMeetingTranscriber from "./pages/LiveMeetingTranscriber.jsx";

function App() {
  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <div className="flex-1 bg-gray-100 p-4 overflow-auto">
          <Routes>
            <Route path="/yt" element={<YouTubeSummarizer />} />
            <Route path="/audio-video" element={<AudioVideoSummarizer />} />
            <Route path="/pdf-text" element={<PdfTextSummarizer />} />
            <Route path="/meeting" element={<LiveMeetingTranscriber />} />
            <Route path="*" element={<div className="p-6">🏠 Select a feature from the sidebar</div>} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;
