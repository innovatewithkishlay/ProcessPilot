import React from "react";

function Sidebar({ setFilter }) {
  return (
    <div className="bg-gray-800 text-white w-64 p-4 h-full fixed">
      <h2 className="text-xl font-bold mb-4">Options</h2>
      <ul>
        <li
          className="cursor-pointer hover:bg-gray-700 p-2 rounded"
          onClick={() => setFilter("all")}
        >
          All Processes
        </li>
        <li
          className="cursor-pointer hover:bg-gray-700 p-2 rounded"
          onClick={() => setFilter("highCpu")}
        >
          High CPU Usage
        </li>
        <li
          className="cursor-pointer hover:bg-gray-700 p-2 rounded"
          onClick={() => setFilter("highMemory")}
        >
          High Memory Usage
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;
