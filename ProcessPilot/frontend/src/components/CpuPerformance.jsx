import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";
import axios from "axios";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function CpuPerformance() {
  const [cpuData, setCpuData] = useState([]);
  const [labels, setLabels] = useState([]);
  const [cpuDetails, setCpuDetails] = useState({});

  useEffect(() => {
    const fetchCpuDetails = async () => {
      try {
        const response = await axios.get(
          "https://processpilot.onrender.com/api/cpu-details"
        );
        setCpuDetails(response.data);
      } catch (error) {
        console.error("Error fetching CPU details:", error);
      }
    };

    fetchCpuDetails();

    const interval = setInterval(() => {
      const usage = Math.random() * 100; // Simulated CPU usage
      setCpuData((prevData) => [...prevData.slice(-19), usage]);
      setLabels((prevLabels) => [
        ...prevLabels.slice(-19),
        new Date().toLocaleTimeString(),
      ]);
    }, 3000); // Updates every 3 seconds

    return () => clearInterval(interval);
  }, []);

  const data = {
    labels,
    datasets: [
      {
        label: "CPU Usage (%)",
        data: cpuData,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderWidth: 2,
        tension: 0.4, // Smooth transition for the graph
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-lg max-w-full overflow-hidden">
      <div className="relative w-full h-64">
        <Line data={data} options={options} />
      </div>
      <div className="mt-6">
        <h3 className="text-xl font-semibold mb-4">System Details</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-100 rounded-lg shadow">
            <h4 className="text-lg font-semibold text-gray-800">
              Logical Cores
            </h4>
            <p className="text-gray-600">{cpuDetails.cpu_count}</p>
          </div>
          <div className="p-4 bg-gray-100 rounded-lg shadow">
            <h4 className="text-lg font-semibold text-gray-800">
              Physical Cores
            </h4>
            <p className="text-gray-600">{cpuDetails.physical_cores}</p>
          </div>
          <div className="p-4 bg-gray-100 rounded-lg shadow">
            <h4 className="text-lg font-semibold text-gray-800">
              CPU Frequency
            </h4>
            <p className="text-gray-600">{cpuDetails.cpu_frequency}</p>
          </div>
          <div className="p-4 bg-gray-100 rounded-lg shadow">
            <h4 className="text-lg font-semibold text-gray-800">CPU Usage</h4>
            <p className="text-gray-600">{cpuDetails.cpu_usage}</p>
          </div>
          <div className="p-4 bg-gray-100 rounded-lg shadow">
            <h4 className="text-lg font-semibold text-gray-800">
              Total Memory
            </h4>
            <p className="text-gray-600">{cpuDetails.total_memory}</p>
          </div>
          <div className="p-4 bg-gray-100 rounded-lg shadow">
            <h4 className="text-lg font-semibold text-gray-800">
              Available Memory
            </h4>
            <p className="text-gray-600">{cpuDetails.available_memory}</p>
          </div>
          <div className="p-4 bg-gray-100 rounded-lg shadow">
            <h4 className="text-lg font-semibold text-gray-800">Used Memory</h4>
            <p className="text-gray-600">{cpuDetails.used_memory}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CpuPerformance;
