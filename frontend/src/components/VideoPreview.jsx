import React, { useState } from "react";
import { Copy } from "lucide-react";

export default function VideoPreview({ url }) {
  const [copied, setCopied] = useState(false);

  // Mock transcript — replace with backend transcript API
  const transcript = [
    { time: "00:00", text: "Intro about the topic" },
    { time: "01:15", text: "Main point number one explained" },
    { time: "02:30", text: "Supporting details with examples" },
    { time: "04:10", text: "Conclusion and summary" },
    { time: "00:00", text: "Intro about the topic" },
    { time: "01:15", text: "Main point number one explained" },
    { time: "02:30", text: "Supporting details with examples" },
    { time: "00:00", text: "Intro about the topic" },
    { time: "01:15", text: "Main point number one explained" },
    { time: "02:30", text: "Supporting details with examples" },
    { time: "04:10", text: "Conclusion and summary" },
    { time: "00:00", text: "Intro about the topic" },
    { time: "01:15", text: "Main point number one explained" },
    { time: "02:30", text: "Supporting details with examples" },
    { time: "00:00", text: "Intro about the topic" },
    { time: "01:15", text: "Main point number one explained" },
    { time: "02:30", text: "Supporting details with examples" },
    { time: "04:10", text: "Conclusion and summary" },
    { time: "00:00", text: "Intro about the topic" },
    { time: "01:15", text: "Main point number one explained" },
    { time: "02:30", text: "Supporting details with examples" },
  ];

  const getYouTubeId = (ytUrl) => {
    if (!ytUrl) return null;
    try {
      // Handle youtu.be links
      if (ytUrl.includes("youtu.be/")) {
        return ytUrl.split("youtu.be/")[1].split(/[?&]/)[0];
      }

      // Handle youtube.com/watch?v= links
      if (ytUrl.includes("youtube.com/watch")) {
        const urlObj = new URL(ytUrl);
        return urlObj.searchParams.get("v");
      }

      // Handle youtube.com/embed/ links
      if (ytUrl.includes("youtube.com/embed/")) {
        return ytUrl.split("embed/")[1].split(/[?&]/)[0];
      }

      // Handle youtube.com/shorts/ links
      if (ytUrl.includes("youtube.com/shorts/")) {
        return ytUrl.split("shorts/")[1].split(/[?&]/)[0];
      }

      return null;
    } catch {
      return null;
    }
  };

  const videoId = getYouTubeId(url);

  const handleCopyAll = () => {
    const textToCopy = transcript
      .map((line) => `${line.time} - ${line.text}`)
      .join("\n");
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col p-2 border-r h border-gray-700 ">
      {/* Video Mini Player */}
      <div className="aspect-video min-h-[200px] w-full bg-black rounded-lg overflow-hidden">
        {videoId ? (
          <iframe
            src={`https://www.youtube.com/embed/${videoId}`}
            title="YouTube video"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="w-full h-full"
          ></iframe>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            Paste a valid YouTube link to preview
          </div>
        )}
      </div>

      {/* Transcript */}
      <div className="mt-4">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-lg font-semibold">Transcript</h2>
          <button
            onClick={handleCopyAll}
            className="flex items-center gap-1 px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded text-sm"
          >
            {copied ? (
              <span className="text-green-400">Copied!</span>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy All
              </>
            )}
          </button>
        </div>

        {/* Scrollable transcript section */}
        <div className="max-h-85 overflow-y-auto space-y-2 [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden">
          {transcript.map((line, i) => (
            <div key={i} className="p-2 bg-gray-900 rounded-lg">
              <span className="text-sm text-blue-400 mr-2">{line.time}</span>
              <span>{line.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
