"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, Loader2 } from "lucide-react";
import { uploadDocument, DocumentInfo } from "@/lib/api";

interface FileUploadProps {
  onUpload: (doc: DocumentInfo) => void;
}

export default function FileUpload({ onUpload }: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      setError(null);
      for (const file of acceptedFiles) {
        setUploading(true);
        try {
          const doc = await uploadDocument(file);
          onUpload(doc);
        } catch (e: any) {
          setError(e.message || "上传失败");
        } finally {
          setUploading(false);
        }
      }
    },
    [onUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "text/plain": [".txt"],
      "text/markdown": [".md"],
    },
    maxSize: 50 * 1024 * 1024,
    disabled: uploading,
  });

  return (
    <div
      {...getRootProps()}
      className={`relative border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-all duration-200 ${
        isDragActive
          ? "border-accent-blue bg-accent-blue-soft scale-[1.02]"
          : "border-swiss-border hover:border-accent-blue/40 hover:bg-swiss-neutral"
      } ${uploading ? "opacity-60 pointer-events-none" : ""}`}
    >
      <input {...getInputProps()} />
      {uploading ? (
        <div className="flex flex-col items-center gap-2">
          <Loader2 className="h-7 w-7 text-accent-blue animate-spin" />
          <p className="text-sm text-swiss-muted">上传处理中...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-1.5">
          <div className="w-10 h-10 rounded-xl bg-accent-blue-soft flex items-center justify-center mb-0.5">
            <Upload className="h-5 w-5 text-accent-blue" />
          </div>
          <p className="text-sm font-medium text-swiss-ink">
            {isDragActive ? "释放以上传文件" : "点击或拖放文件上传"}
          </p>
          <p className="text-xs text-swiss-muted">
            PDF · DOCX · TXT · MD（最大 50MB）
          </p>
        </div>
      )}
      {error && (
        <p className="mt-2 text-xs text-red-500 animate-fade-in">{error}</p>
      )}
    </div>
  );
}
