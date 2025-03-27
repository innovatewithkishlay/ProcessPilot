import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  FaTasks,
  FaChartLine,
  FaMemory,
  FaBars,
  FaRobot,
} from "react-icons/fa";

function Sidebar({ setFilter }) {
  const [activeSection, setActiveSection] = useState("all");
  const [isCollapsed, setIsCollapsed] = useState(false); // State for collapsing sidebar

  const handleSectionClick = (section) => {
    setActiveSection(section);
    setFilter(section);
  };

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <motion.div
      className={`bg-gray-900 text-white h-full fixed shadow-lg ${
        isCollapsed ? "w-20" : "w-64"
      } transition-all duration-300 ease-in-out`}
      initial={{ x: -100 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Sidebar Header */}
      <div className="flex items-center justify-between p-4">
        {!isCollapsed && <h2 className="text-xl font-bold">Options</h2>}
        <FaBars
          className="text-white text-xl cursor-pointer hover:text-sky-500 transition"
          onClick={toggleSidebar}
        />
      </div>

      {/* Decorative Divider */}
      <div className="border-t border-gray-700 my-4"></div>

      {/* Sidebar Content */}
      <ul className="space-y-4">
        {/* All Processes */}
        <li
          className={`flex items-center cursor-pointer p-3 rounded-lg transition ${
            activeSection === "all"
              ? "bg-sky-500 text-white shadow-lg"
              : "hover:bg-gray-700"
          }`}
          onClick={() => handleSectionClick("all")}
        >
          <FaTasks className="mr-3 text-lg" />
          {!isCollapsed && <span className="text-lg">All Processes</span>}
        </li>

        {/* High CPU Usage */}
        <li
          className={`flex items-center cursor-pointer p-3 rounded-lg transition ${
            activeSection === "highCpu"
              ? "bg-sky-500 text-white shadow-lg"
              : "hover:bg-gray-700"
          }`}
          onClick={() => handleSectionClick("highCpu")}
        >
          <FaChartLine className="mr-3 text-lg" />
          {!isCollapsed && <span className="text-lg">High CPU Usage</span>}
        </li>

        {/* High Memory Usage */}
        <li
          className={`flex items-center cursor-pointer p-3 rounded-lg transition ${
            activeSection === "highMemory"
              ? "bg-sky-500 text-white shadow-lg"
              : "hover:bg-gray-700"
          }`}
          onClick={() => handleSectionClick("highMemory")}
        >
          <FaMemory className="mr-3 text-lg" />
          {!isCollapsed && <span className="text-lg">High Memory Usage</span>}
        </li>

        {/* AI Chat */}
        <li
          className={`flex items-center cursor-pointer p-3 rounded-lg transition ${
            activeSection === "aiChat"
              ? "bg-sky-500 text-white shadow-lg"
              : "hover:bg-gray-700"
          }`}
          onClick={() => handleSectionClick("aiChat")}
        >
          <FaRobot className="mr-3 text-lg" />
          {!isCollapsed && <span className="text-lg">AI Chat</span>}
        </li>
      </ul>
    </motion.div>
  );
}

export default Sidebar;
