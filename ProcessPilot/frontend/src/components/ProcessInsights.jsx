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

        const validProcesses = response.data.filter(
          (process) =>
            process.name &&
            process.cpu_usage !== undefined &&
            process.memory_usage !== undefined
        );

        setInsights(validProcesses);
      } catch (error) {
        console.error("Error fetching process insights:", error);
      }
    };

    fetchInsights();
  }, []);

  const getRecommendationStyle = (recommendation) => {
    if (recommendation.toLowerCase().includes("normal")) {
      return "bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-semibold";
    }
    return "bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-semibold";
  };

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
            {insights.length > 0 ? (
              insights.map((process) => (
                <tr key={process.pid} className="hover:bg-gray-50">
                  <td className="p-2 border">{process.pid}</td>
                  <td className="p-2 border">{process.name}</td>
                  <td className="p-2 border">{process.cpu_usage}</td>
                  <td className="p-2 border">{process.memory_usage}</td>
                  <td className="p-2 border">
                    <span
                      className={getRecommendationStyle(process.recommendation)}
                    >
                      {process.recommendation}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan="5"
                  className="p-4 text-center text-gray-500 border"
                >
                  No valid processes found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ProcessInsights;
