import React, { useState } from "react";

function AIAdvice() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! How can I assist you today?" },
  ]);

  const askAI = async () => {
    if (!query.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: query }]);

    try {
      const response = await fetch("http://localhost:5000/ask-ai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: data.response || "I couldn't understand that." },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error connecting to the AI backend." },
      ]);
    }

    setQuery("");
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-6 rounded-lg shadow-lg max-w-2xl mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4 text-center text-blue-400">
        AI System Advisor
      </h2>
      <div className="chat-box bg-gray-800 p-4 rounded-lg h-96 overflow-y-auto border border-gray-700">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-4 flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                msg.sender === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-700 text-gray-200"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 flex items-center">
        <input
          type="text"
          placeholder="Type your message..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-grow p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 mr-4"
        />
        <button
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold shadow-md transition duration-300"
          onClick={askAI}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default AIAdvice;
