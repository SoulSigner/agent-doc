"use client";

import { useState, useCallback } from "react";
import { streamChat, ChatMessage, SourceReference } from "@/lib/api";

interface UseChatOptions {
  docId?: string;
}

export default function useChat({ docId }: UseChatOptions = {}) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || loading) return;

      const userMessage: ChatMessage = { role: "user", content };
      setMessages((prev) => [...prev, userMessage]);
      setLoading(true);
      setError(null);

      const history = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      let assistantContent = "";
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: "",
      };
      setMessages((prev) => [...prev, assistantMessage]);

      try {
        const stream = streamChat(content, docId, history);
        for await (const chunk of stream) {
          if (chunk.done) {
            setMessages((prev) => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last.role === "assistant") {
                last.sources = chunk.sources || [];
              }
              return updated;
            });
          } else {
            assistantContent += chunk.token;
            setMessages((prev) => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last.role === "assistant") {
                last.content = assistantContent;
              }
              return updated;
            });
          }
        }
      } catch (e: any) {
        setError(e.message || "对话失败");
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last.role === "assistant") {
            last.content = assistantContent || "[错误：未能获取回复]";
          }
          return updated;
        });
      } finally {
        setLoading(false);
      }
    },
    [messages, loading, docId]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return { messages, loading, error, sendMessage, clearMessages };
}
