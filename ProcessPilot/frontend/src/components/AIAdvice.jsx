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
      const response = await fetch("http://127.0.0.1:5000/ask-ai", {
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
    <div className="h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white overflow-hidden">
      {/* Chatbot Container */}
      <div className="relative flex flex-col h-full w-full max-w-4xl mx-auto bg-gray-800 rounded-lg shadow-lg">
        {/* Header */}
        <header className="text-center py-4 bg-gray-700 rounded-t-lg">
          <h1 className="text-3xl font-bold text-blue-400">
            AI System Advisor
          </h1>
        </header>

        {/* Chat Area */}
        <div className="flex-grow overflow-y-auto p-6 mb-20">
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-lg px-4 py-2 rounded-lg ${
                    msg.sender === "user"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-700 text-gray-200"
                  }`}
                  dangerouslySetInnerHTML={{ __html: msg.text }} // Render HTML response
                ></div>
              </div>
            ))}
          </div>
        </div>

        {/* Input Area */}
        <footer className="absolute bottom-0 left-0 w-full bg-gray-700 p-4 rounded-b-lg">
          <div className="flex items-center">
            <input
              type="text"
              placeholder="Type your message..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-grow p-3 rounded-lg bg-gray-600 text-white border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 mr-4 blinking-cursor"
            />
            <button
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold shadow-md transition duration-300"
              onClick={askAI}
            >
              Send
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default AIAdvice;
