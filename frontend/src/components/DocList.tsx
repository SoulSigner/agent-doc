"use client";

import { Trash2, FileText } from "lucide-react";
import { deleteDocument, DocumentInfo } from "@/lib/api";

interface DocListProps {
  documents: DocumentInfo[];
  selectedId: string | null;
  onSelect: (doc: DocumentInfo) => void;
  onDelete: (docId: string) => void;
}

export default function DocList({ documents, selectedId, onSelect, onDelete }: DocListProps) {
  if (documents.length === 0) {
    return (
      <div className="text-center py-8">
        <FileText className="h-8 w-8 mx-auto mb-3 text-swiss-border" />
        <p className="text-sm text-swiss-muted">暂无文档</p>
        <p className="text-xs text-swiss-border mt-1">
          上传文件即可开始
        </p>
      </div>
    );
  }

  const handleDelete = async (e: React.MouseEvent, docId: string) => {
    e.stopPropagation();
    try {
      await deleteDocument(docId);
      onDelete(docId);
    } catch {
      // ignore
    }
  };

  return (
    <div className="space-y-1">
      {documents.map((doc) => (
        <div
          key={doc.doc_id}
          onClick={() => onSelect(doc)}
          className={`group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all duration-200 ${
            selectedId === doc.doc_id
              ? "bg-accent-blue-soft border border-accent-blue/20"
              : "hover:bg-swiss-neutral border border-transparent"
          }`}
        >
          <div className="flex items-center gap-2.5 min-w-0">
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 transition-colors duration-200 ${
                selectedId === doc.doc_id
                  ? "bg-accent-blue text-white"
                  : "bg-swiss-neutral text-swiss-muted group-hover:bg-swiss-border"
              }`}
            >
              <FileText className="h-3.5 w-3.5" />
            </div>
            <div className="min-w-0">
              <p
                className={`text-sm font-medium truncate transition-colors duration-200 ${
                  selectedId === doc.doc_id
                    ? "text-accent-blue"
                    : "text-swiss-ink"
                }`}
              >
                {doc.filename}
              </p>
              <p className="text-xs text-swiss-muted">
                {doc.chunks} 个片段
              </p>
            </div>
          </div>
          <button
            onClick={(e) => handleDelete(e, doc.doc_id)}
            className="p-1.5 rounded-md opacity-0 group-hover:opacity-100 hover:bg-red-50 flex-shrink-0 transition-all duration-200"
          >
            <Trash2 className="h-3.5 w-3.5 text-swiss-muted hover:text-red-500" />
          </button>
        </div>
      ))}
    </div>
  );
}
