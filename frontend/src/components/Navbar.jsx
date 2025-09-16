import React from "react";
import {  Plus } from "lucide-react";

const Navbar = () => {
  return (
    <nav className="h-16 flex items-center justify-between px-6 border-b border-gray-700 bg-[#0f1117] text-white">
      <h2 className="text-2xl ml-3 font-bold text-yellow-400">Dashboard</h2>
      <div className="flex items-center gap-4">
        
        <button className="flex items-center gap-2 cursor-pointer bg-blue-600 px-4 py-2 rounded-lg">
          <Plus size={18} /> New Summary
        </button>
        
      </div>
    </nav>
  );
};

export default Navbar;
