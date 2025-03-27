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
      setProcesses(response.data.processes);
    } catch (error) {
      console.error("Error fetching processes:", error);
    }
  };

  const killProcess = async (pid) => {
    try {
      await axios.post("http://127.0.0.1:5000/api/kill", { pid });
      setMessage("Process killed successfully!");
      setShowPopup(true);
      fetchProcesses();
    } catch (error) {
      setMessage("Error killing process.");
      setShowPopup(true);
    }
  };

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
        <ProcessTable processes={filteredProcesses} killProcess={killProcess} />
        <AIAdvice />
        {showPopup && (
          <Popup message={message} onClose={() => setShowPopup(false)} />
        )}
      </div>
    </div>
  );
}

export default App;
