import React, { useState, useEffect } from "react";
import axios from "axios";

function ProcessInsights() {
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/process-insights"
        );
        setInsights(response.data);
      } catch (error) {
        console.error("Error fetching process insights:", error);
      }
    };

    fetchInsights();
  }, []);

  return (
    <div className="p-4 bg-white rounded-lg shadow-lg">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 border">PID</th>
              <th className="p-2 border">Name</th>
              <th className="p-2 border">CPU Usage</th>
              <th className="p-2 border">Memory Usage</th>
              <th className="p-2 border">Recommendation</th>
            </tr>
          </thead>
          <tbody>
            {insights.map((process) => (
              <tr key={process.pid} className="hover:bg-gray-50">
                <td className="p-2 border">{process.pid}</td>
                <td className="p-2 border">{process.name}</td>
                <td className="p-2 border">{process.cpu_usage}</td>
                <td className="p-2 border">{process.memory_usage}</td>
                <td className="p-2 border text-sm text-gray-600">
                  {process.recommendation}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ProcessInsights;
