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
  const [adminConfirmation, setAdminConfirmation] = useState(null); // For admin confirmation

  useEffect(() => {
    fetchProcesses();
  }, []);

  // Fetch processes from the backend
  const fetchProcesses = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/processes");
      const filteredProcesses = filterValidProcesses(response.data.processes);
      setProcesses(filteredProcesses);
    } catch (error) {
      console.error("Error fetching processes:", error);
    }
  };

  // Filter out invalid or useless processes
  const filterValidProcesses = (processList) => {
    return processList.filter(
      (process) =>
        process.name && // Ensure the process has a valid name
        process.name.toLowerCase() !== "unknown" && // Exclude "Unknown" processes
        process.cpu_percent !== undefined && // Ensure CPU usage is defined
        process.memory_usage !== undefined // Ensure memory usage is defined
    );
  };

  // Kill a process by PID
  const killProcess = async (pid) => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/kill", {
        pid,
      });
      if (response.data.success) {
        setMessage(response.data.message); // Display success or "already terminated" message
        fetchProcesses(); // Refresh the process list
      } else if (response.data.requires_admin) {
        // Admin privileges required
        setAdminConfirmation({ pid, message: response.data.message });
      } else {
        setMessage(response.data.message); // Display the error message from the backend
      }
      setShowPopup(true);
    } catch (error) {
      setMessage(`Error killing process with PID ${pid}.`);
      setShowPopup(true);
    }
  };

  // Confirm admin privilege and kill the process
  const confirmAdminKill = async (pid) => {
    setAdminConfirmation(null); // Clear the admin confirmation
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/kill", {
        pid,
      });
      if (response.data.success) {
        setMessage(response.data.message); // Display success message
        fetchProcesses(); // Refresh the process list
      } else {
        setMessage(response.data.message); // Display the error message from the backend
      }
      setShowPopup(true);
    } catch (error) {
      setMessage(`Error killing process with PID ${pid}.`);
      setShowPopup(true);
    }
  };

  // Filter processes based on the selected filter
  const filteredProcesses = processes.filter((process) => {
    if (filter === "highCpu") return process.cpu_percent > 50;
    if (filter === "highMemory") return parseFloat(process.memory_usage) > 100;
    return true;
  });

  return (
    <div className="flex">
      <Sidebar setFilter={setFilter} />
      <div className="ml-64 p-4 w-full">
        <h1 className="text-3xl font-bold mb-4">Process Monitor</h1>
        <ProcessTable
          processes={filteredProcesses}
          killProcess={killProcess}
          fetchProcesses={fetchProcesses} // Pass fetchProcesses for auto-refresh
        />
        <AIAdvice />
        {showPopup && (
          <Popup message={message} onClose={() => setShowPopup(false)} />
        )}
        {adminConfirmation && (
          <Popup
            message={adminConfirmation.message}
            onClose={() => setAdminConfirmation(null)}
          >
            <button
              className="bg-red-600 text-white px-4 py-2 rounded mt-4"
              onClick={() => confirmAdminKill(adminConfirmation.pid)}
            >
              Yes, Kill
            </button>
          </Popup>
        )}
      </div>
    </div>
  );
}

export default App;
