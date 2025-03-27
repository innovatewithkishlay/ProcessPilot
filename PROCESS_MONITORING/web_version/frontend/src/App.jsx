import React, { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "./components/Sidebar";
import ProcessTable from "./components/ProcessTable";
import Popup from "./components/Popup";
import AIAdvice from "./components/AIAdvice";

function App() {
  const [processes, setProcesses] = useState([]);
  const [filter, setFilter] = useState("all");
  const [message, setMessage] = useState("");
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    fetchProcesses();
  }, []);

  const fetchProcesses = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/processes");
      console.log("Backend Response:", response.data.processes);
      setProcesses(response.data.processes);
    } catch (error) {
      console.error("Error fetching processes:", error);
    }
  };

  const filterValidProcesses = (processList) => {
    return processList.filter(
      (process) =>
        process.name &&
        process.cpu_percent !== undefined &&
        process.memory_usage !== undefined
    );
  };

  const killProcess = async (pid) => {
    try {
      setMessage("Processing your request...");
      setShowPopup(true);

      const response = await axios.post("http://127.0.0.1:5000/api/kill", {
        pid,
      });

      if (response.data.success) {
        setMessage(response.data.message || "Successfully killed the process.");
        fetchProcesses();
      } else {
        setMessage(response.data.message || "Failed to kill the process.");
      }
    } catch (error) {
      console.error("Error in killProcess:", error); // Debugging log
      setMessage("An error occurred while trying to kill the process.");
    }
  };

  const filteredProcesses = processes.filter((process) => {
    if (filter === "highCpu") return process.cpu_percent > 50; // Show processes with CPU usage > 50%
    if (filter === "highMemory") return parseFloat(process.memory_usage) > 100; // Show processes with memory usage > 100 MB
    return true; // Show all processes for "all"
  });

  const getTitle = () => {
    if (filter === "all") return "All Processes";
    if (filter === "highCpu") return "High CPU Usage";
    if (filter === "highMemory") return "High Memory Usage";
    if (filter === "aiChat") return "AI Chat";
    return "ProcessPilot";
  };

  return (
    <div className="flex">
      <Sidebar setFilter={setFilter} />
      <div className="ml-64 p-4 w-full">
        {/* Project Name with Gradient */}
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 mb-4">
          ProcessPilot
        </h1>

        <h2 className="text-2xl font-bold mb-6">{getTitle()}</h2>

        {/* Render Content Based on Filter */}
        {filter === "all" && (
          <ProcessTable
            processes={filteredProcesses}
            fetchProcesses={fetchProcesses}
            killProcess={killProcess}
          />
        )}
        {filter === "highCpu" && (
          <ProcessTable
            processes={filteredProcesses}
            fetchProcesses={fetchProcesses}
            killProcess={killProcess}
          />
        )}
        {filter === "highMemory" && (
          <ProcessTable
            processes={filteredProcesses}
            fetchProcesses={fetchProcesses}
            killProcess={killProcess}
          />
        )}
        {filter === "aiChat" && <AIAdvice />}
        {showPopup && (
          <Popup message={message} onClose={() => setShowPopup(false)} />
        )}
      </div>
    </div>
  );
}

export default App;
