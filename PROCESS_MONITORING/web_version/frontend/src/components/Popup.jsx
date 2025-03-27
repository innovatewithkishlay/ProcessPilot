import React from "react";
import { motion } from "framer-motion";

function Popup({ message, onClose, children }) {
  return (
    <motion.div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="bg-white text-black p-4 rounded shadow-lg w-96">
        <p>{message}</p>
        {children}
        <button
          className="bg-blue-500 text-white px-4 py-2 mt-4 rounded"
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </motion.div>
  );
}

export default Popup;
