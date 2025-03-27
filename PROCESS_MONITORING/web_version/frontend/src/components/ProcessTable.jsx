import React, { useEffect } from "react";
import { motion } from "framer-motion";

function ProcessTable({ processes, killProcess, fetchProcesses }) {
  useEffect(() => {
    const interval = setInterval(() => {
      fetchProcesses();
    }, 2000);
    return () => clearInterval(interval);
  }, [fetchProcesses]);

  return (
    <motion.div
      className="overflow-x-auto bg-gray-900 text-white rounded-lg shadow-lg p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <motion.table
        className="table-auto w-full text-left border-collapse"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Table Header */}
        <thead>
          <tr className="bg-sky-500 text-white">
            <th className="p-3 border border-gray-600">Name</th>
            <th className="p-3 border border-gray-600">PID</th>
            <th className="p-3 border border-gray-600">CPU %</th>
            <th className="p-3 border border-gray-600">Memory</th>
            <th className="p-3 border border-gray-600">Actions</th>
          </tr>
        </thead>

        {/* Table Body */}
        <motion.tbody>
          {processes.map((process) => (
            <motion.tr
              key={process.pid}
              className="hover:bg-sky-100 hover:text-gray-900 transition duration-200 ease-in-out"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <td className="p-3 border border-gray-600">
                {process.name || "Unknown"}
              </td>
              <td className="p-3 border border-gray-600">{process.pid}</td>
              <td className="p-3 border border-gray-600">
                {process.cpu_percent}
              </td>
              <td className="p-3 border border-gray-600">
                {process.memory_usage}
              </td>
              <td className="p-3 border border-gray-600">
                <motion.button
                  onClick={() => killProcess(process.pid)}
                  className="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  Kill
                </motion.button>
              </td>
            </motion.tr>
          ))}
        </motion.tbody>
      </motion.table>
    </motion.div>
  );
}

export default ProcessTable;
