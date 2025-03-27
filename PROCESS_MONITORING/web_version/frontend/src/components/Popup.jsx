import React from "react";
import { motion } from "framer-motion";

function Popup({ message, onClose }) {
  return (
    <motion.div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="bg-white text-gray-800 p-6 rounded-lg shadow-xl w-96">
        <h2 className="text-xl font-semibold mb-4 text-center text-gray-900">
          Notification
        </h2>
        <p className="text-center text-gray-700">{message}</p>
        <div className="flex justify-center mt-6">
          <button
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg shadow-md transition duration-200"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </motion.div>
  );
}

export default Popup;
