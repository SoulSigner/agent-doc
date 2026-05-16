"use client";

import ReactMarkdown from "react-markdown";
import { User, Bot } from "lucide-react";
import { ChatMessage } from "@/lib/api";
import SourceCard from "./SourceCard";

interface MessageBubbleProps {
  message: ChatMessage;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex gap-3 animate-slide-up ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-accent-blue-soft flex items-center justify-center">
          <Bot className="h-4 w-4 text-accent-blue" />
        </div>
      )}
      <div
        className={`max-w-[72%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "bg-accent-blue text-white rounded-br-lg"
            : "bg-white border border-swiss-border text-swiss-ink rounded-bl-lg shadow-sm"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="prose-chat">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-swiss-border space-y-1.5">
            <p className="text-xs font-medium text-swiss-muted mb-1">
              参考来源
            </p>
            {message.sources.map((s, i) => (
              <SourceCard key={i} source={s} />
            ))}
          </div>
        )}
      </div>
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-accent-blue flex items-center justify-center">
          <User className="h-4 w-4 text-white" />
        </div>
      )}
    </div>
  );
}
