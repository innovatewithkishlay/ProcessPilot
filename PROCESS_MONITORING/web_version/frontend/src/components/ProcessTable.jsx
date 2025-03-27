import React from "react";
import { motion } from "framer-motion";

function ProcessTable({ processes, killProcess }) {
  return (
    <motion.table
      className="table-auto w-full text-left border-collapse border border-gray-700"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <thead>
        <tr className="bg-gray-700">
          <th className="p-2 border border-gray-600">Name</th>
          <th className="p-2 border border-gray-600">PID</th>
          <th className="p-2 border border-gray-600">CPU %</th>
          <th className="p-2 border border-gray-600">Memory</th>
          <th className="p-2 border border-gray-100">Actions</th>
        </tr>
      </thead>
      <motion.tbody>
        {processes.map((process) => (
          <motion.tr
            key={process.pid}
            className="hover:bg-gray-600 hover:text-white transition duration-200 ease-in-out"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <td className="p-2 border border-gray-600">
              {process.name || "Unknown"}
            </td>
            <td className="p-2 border border-gray-600">{process.pid}</td>
            <td className="p-2 border border-gray-600">
              {process.cpu_percent}
            </td>
            <td className="p-2 border border-gray-600">
              {process.memory_usage}
            </td>
            <td className="p-2 border border-gray-600">
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
  );
}

export default ProcessTable;
