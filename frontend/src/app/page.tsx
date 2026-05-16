"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Send, Sparkles, BookOpen } from "lucide-react";
import FileUpload from "@/components/FileUpload";
import DocList from "@/components/DocList";
import MessageBubble from "@/components/MessageBubble";
import useChat from "@/hooks/useChat";
import { fetchDocuments, DocumentInfo } from "@/lib/api";

export default function Home() {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<DocumentInfo | null>(null);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { messages, loading, error, sendMessage, clearMessages } = useChat({
    docId: selectedDoc?.doc_id,
  });

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await fetchDocuments();
      setDocuments(docs);
    } catch {
      // ignore
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleUpload = useCallback((doc: DocumentInfo) => {
    setDocuments((prev) => [...prev, doc]);
    setSelectedDoc(doc);
  }, []);

  const handleDelete = useCallback(
    (docId: string) => {
      setDocuments((prev) => prev.filter((d) => d.doc_id !== docId));
      if (selectedDoc?.doc_id === docId) {
        setSelectedDoc(null);
        clearMessages();
      }
    },
    [selectedDoc, clearMessages]
  );

  const handleSend = () => {
    if (input.trim() && !loading) {
      sendMessage(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-screen bg-swiss-neutral">
      {/* Sidebar */}
      <aside className="w-80 flex flex-col border-r border-swiss-border bg-white">
        {/* Brand Header */}
        <div className="px-5 pt-6 pb-5">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-accent-blue flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-swiss-ink">
                智能文档分析
              </h1>
              <p className="text-xs text-swiss-muted mt-0.5">
                上传文档，AI 智能问答
              </p>
            </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="px-4 pb-4">
          <FileUpload onUpload={handleUpload} />
        </div>

        {/* Divider */}
        <div className="mx-4 hairline bg-swiss-border" />

        {/* Document List */}
        <div className="flex-1 overflow-y-auto px-4 pt-4 pb-3">
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs font-semibold uppercase tracking-widest text-swiss-muted">
              我的文档
            </p>
            <span className="text-xs text-swiss-muted">
              {documents.length}
            </span>
          </div>
          <DocList
            documents={documents}
            selectedId={selectedDoc?.doc_id || null}
            onSelect={setSelectedDoc}
            onDelete={handleDelete}
          />
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Active Document Bar */}
        {selectedDoc && (
          <div className="px-6 py-3 bg-white border-b border-swiss-border flex items-center gap-3 animate-fade-in">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse-dot" />
            <span className="text-sm font-medium text-swiss-ink">
              {selectedDoc.filename}
            </span>
            <button
              onClick={() => {
                setSelectedDoc(null);
                clearMessages();
              }}
              className="ml-auto text-xs text-swiss-muted hover:text-swiss-ink transition-colors duration-200"
            >
              清除对话
            </button>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5">
          {messages.length === 0 && !selectedDoc && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center max-w-sm">
                <div className="w-16 h-16 rounded-2xl bg-accent-blue-soft flex items-center justify-center mx-auto mb-5">
                  <BookOpen className="h-8 w-8 text-accent-blue" />
                </div>
                <h2 className="text-lg font-semibold text-swiss-ink mb-1">
                  上传文档开始使用
                </h2>
                <p className="text-sm text-swiss-muted leading-relaxed">
                  将 PDF、Word、TXT 或 Markdown 文件拖入左侧区域，
                  即可使用 AI 对文档内容进行智能问答
                </p>
              </div>
            </div>
          )}
          {messages.length === 0 && selectedDoc && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center max-w-sm">
                <p className="text-lg font-medium text-swiss-ink mb-2">
                  向「{selectedDoc.filename}」提问
                </p>
                <p className="text-sm text-swiss-muted">
                  试试：总结此文档的核心内容
                </p>
              </div>
            </div>
          )}
          {messages.map((msg, i) => (
            <MessageBubble key={i} message={msg} />
          ))}
          {loading && (
            <div className="flex items-center gap-2 text-swiss-muted text-sm animate-fade-in">
              <span className="flex gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-accent-blue animate-pulse-dot" />
                <span className="w-1.5 h-1.5 rounded-full bg-accent-blue animate-pulse-dot" style={{ animationDelay: "0.2s" }} />
                <span className="w-1.5 h-1.5 rounded-full bg-accent-blue animate-pulse-dot" style={{ animationDelay: "0.4s" }} />
              </span>
              思考中...
            </div>
          )}
          {error && (
            <div className="text-center text-red-500 text-sm py-3 animate-fade-in">
              {error}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="px-6 py-4 bg-white border-t border-swiss-border">
          <div className="flex items-end gap-3 max-w-3xl">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                selectedDoc
                  ? "输入你的问题..."
                  : "请先在左侧选择或上传文档"
              }
              rows={2}
              className="flex-1 resize-none rounded-xl border border-swiss-border px-4 py-3 text-sm focus:outline-none focus:border-accent-blue focus:ring-1 focus:ring-accent-blue disabled:bg-swiss-neutral disabled:text-swiss-muted transition-all duration-200"
              disabled={!selectedDoc || loading}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="flex-shrink-0 w-10 h-10 rounded-xl bg-accent-blue text-white hover:bg-accent-blue-light disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-200 flex items-center justify-center"
            >
              <Send className="h-4.5 w-4.5" />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
