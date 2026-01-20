"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2, Stethoscope } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user" as const, content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Connect to Backend (Environment Variable or Localhost fallback)
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userMessage.content }),
      });

      if (!response.ok) throw new Error("Network response was not ok");
      
      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Error: Could not connect to the medical brain. Make sure 'api.py' is running." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50">
      {/* Header */}
      <header className="p-4 bg-white border-b border-slate-200 shadow-sm flex items-center gap-3">
        <div className="bg-blue-600 p-2 rounded-lg">
            <Stethoscope className="w-6 h-6 text-white" />
        </div>
        <h1 className="text-xl font-bold text-slate-800">MediBot Pro</h1>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-slate-400 mt-10">
            <Bot className="w-20 h-20 mb-4 opacity-20" />
            <p className="text-lg font-medium">Ready to assist with medical queries.</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] md:max-w-[70%] p-4 rounded-2xl shadow-sm flex gap-3 ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-white text-slate-700 border border-slate-200 rounded-bl-none"
              }`}
            >
              {msg.role === "assistant" && <Bot className="w-5 h-5 mt-1 text-blue-600 shrink-0" />}
              <div className="leading-relaxed">{msg.content}</div>
              {msg.role === "user" && <User className="w-5 h-5 mt-1 text-blue-200 shrink-0" />}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white p-4 rounded-2xl rounded-bl-none border border-slate-200 flex items-center gap-2 text-slate-500 shadow-sm">
              <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
              <span className="text-sm font-medium">Analyzing medical database...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-slate-200">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Describe symptoms or ask a medical question..."
            className="flex-1 bg-slate-100 text-slate-900 border-transparent focus:bg-white border focus:border-blue-500 rounded-xl px-4 py-3 outline-none transition-all"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}