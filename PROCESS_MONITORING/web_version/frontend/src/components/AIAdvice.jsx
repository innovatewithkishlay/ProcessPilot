import React, { useState } from "react";

function AIAdvice() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const askAI = async () => {
    // Simulate AI response
    setResponse("This is a simulated AI response to your query.");
  };

  return (
    <div className="bg-gray-800 text-white p-4 rounded mt-4">
      <h2 className="text-xl font-bold mb-4">Ask AI for Advice</h2>
      <input
        type="text"
        placeholder="Type your question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full p-2 mb-4 rounded bg-gray-700 text-white"
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={askAI}
      >
        Ask AI
      </button>
      {response && <p className="mt-4">{response}</p>}
    </div>
  );
}

export default AIAdvice;
