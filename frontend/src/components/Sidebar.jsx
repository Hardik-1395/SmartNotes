import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X ,Youtube, BoomBox, FileText} from "lucide-react"; // install: npm install lucide-react

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="flex">
      {/* Sidebar */}
      <div
        className={`${
          isOpen ? "w-64" : "w-16"
        } bg-gray-800 text-white h-[calc(100vh-44px)] flex flex-col transition-all duration-400`}
      >
        {/* Hamburger Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-4 focus:outline-none"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        {/* Menu Links */}
        <nav className="flex flex-col p-2 space-y-2">
          <Link to="/yt" className="hover:bg-gray-700 p-2 rounded">
            {isOpen ? "Youtube Summarizer" : <Youtube/>}
          </Link>
          <Link to="/audio-video" className="hover:bg-gray-700 p-2 rounded">
            {isOpen ? "Audio & Video Summarizer" : <BoomBox/>}
          </Link>
          <Link to="/pdf-text" className="hover:bg-gray-700 p-2 rounded">
            {isOpen ? "PDF & Text Summarizer" : <FileText/>}
          </Link>
          <Link to="/meeting" className="hover:bg-gray-700 p-2 rounded">
            {isOpen ? "Live Meeting Transcriber" : "Live"}
          </Link>
        </nav>
      </div>
    </div>
  );
}
