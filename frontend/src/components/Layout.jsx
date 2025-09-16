import React from "react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import { Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="grid grid-cols-[250px_1fr] h-screen">
      {/* Ledt side - Sidebar*/}
      <Sidebar/>

      {/* Right Side  */}
      <div className="flex flex-col bg-[#0f1117] text-white h-[calc(100vh-0px)]">
        {/* Main Content */}
        <main className="flex-1 bg-black p-6 h-[calc(100vh-44px)] overflow-y-auto">
          <Outlet/>
        </main>
      </div>
    </div>
  );
}
