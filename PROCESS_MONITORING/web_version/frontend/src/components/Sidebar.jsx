import React, { useState } from "react";
import { motion } from "framer-motion";
import { FaList, FaMicrochip, FaMemory, FaBars } from "react-icons/fa";

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
      {/* Toggle Button */}
      <div
        className="flex items-center justify-end p-2 cursor-pointer"
        onClick={toggleSidebar}
      >
        <FaBars className="text-white text-xl hover:text-sky-500 transition" />
      </div>

      {/* Sidebar Content */}
      <ul className="space-y-4 mt-6">
        {/* All Processes */}
        <li
          className={`flex items-center cursor-pointer p-3 rounded-lg transition ${
            activeSection === "all"
              ? "bg-sky-500 text-white"
              : "hover:bg-gray-700"
          }`}
          onClick={() => handleSectionClick("all")}
        >
          <FaList className="mr-3 text-lg" />
          {!isCollapsed && <span className="text-lg">All Processes</span>}
        </li>

        {/* High CPU Usage */}
        <li
          className={`flex items-center cursor-pointer p-3 rounded-lg transition ${
            activeSection === "highCpu"
              ? "bg-sky-500 text-white"
              : "hover:bg-gray-700"
          }`}
          onClick={() => handleSectionClick("highCpu")}
        >
          <FaMicrochip className="mr-3 text-lg" />
          {!isCollapsed && <span className="text-lg">High CPU Usage</span>}
        </li>

        {/* High Memory Usage */}
        <li
          className={`flex items-center cursor-pointer p-3 rounded-lg transition ${
            activeSection === "highMemory"
              ? "bg-sky-500 text-white"
              : "hover:bg-gray-700"
          }`}
          onClick={() => handleSectionClick("highMemory")}
        >
          <FaMemory className="mr-3 text-lg" />
          {!isCollapsed && <span className="text-lg">High Memory Usage</span>}
        </li>
      </ul>
    </motion.div>
  );
}

export default Sidebar;
