"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { copilotChat, type CopilotResponse } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  text: string;
  actions?: CopilotResponse["suggested_actions"];
}

export function TrademarkCopilot() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text: "Hi! I'm your trademark AI assistant. Ask me about clearance searches, Nice classes, renewal deadlines, or portfolio management.",
    },
  ]);
  const [loading, setLoading] = useState(false);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setLoading(true);
    try {
      const resp = await copilotChat(text);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: resp.reply,
          actions: resp.suggested_actions,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Sorry, I couldn't connect to the AI service right now. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* Floating trigger */}
      <button
        onClick={() => setOpen((o) => !o)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-indigo-600 text-white shadow-lg hover:bg-indigo-700 flex items-center justify-center text-2xl"
        aria-label="Open AI Copilot"
      >
        {open ? "×" : "✦"}
      </button>

      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-80 md:w-96 bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col max-h-[32rem]">
          <div className="px-4 py-3 border-b border-gray-100 flex items-center gap-2">
            <span className="text-indigo-600 text-lg">✦</span>
            <span className="font-semibold text-gray-900">Trademark Copilot</span>
          </div>

          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[85%] rounded-xl px-3 py-2 text-sm ${
                    msg.role === "user"
                      ? "bg-indigo-600 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {msg.text}
                  {msg.actions && msg.actions.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {msg.actions.map((action, j) => (
                        <a
                          key={j}
                          href={action.action}
                          className="inline-block bg-white border border-indigo-200 text-indigo-600 text-xs rounded-full px-2 py-0.5 hover:bg-indigo-50"
                        >
                          {action.label}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-xl px-3 py-2 text-sm text-gray-500 animate-pulse">
                  Thinking…
                </div>
              </div>
            )}
          </div>

          <div className="p-3 border-t border-gray-100 flex gap-2">
            <Input
              className="flex-1 text-sm"
              placeholder="Ask about trademarks…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              disabled={loading}
            />
            <Button onClick={send} disabled={loading || !input.trim()} className="px-3">
              →
            </Button>
          </div>
        </div>
      )}
    </>
  );
}
