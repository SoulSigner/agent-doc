import { FileText } from "lucide-react";
import { SourceReference } from "@/lib/api";

interface SourceCardProps {
  source: SourceReference;
}

export default function SourceCard({ source }: SourceCardProps) {
  return (
    <div className="flex items-start gap-2 p-2 rounded-lg bg-swiss-neutral text-xs">
      <FileText className="h-3 w-3 text-swiss-muted mt-0.5 flex-shrink-0" />
      <div className="min-w-0">
        <span className="font-medium text-swiss-ink">
          {source.filename}
        </span>
        <span className="text-swiss-muted"> · 第 {source.page} 页</span>
        <p className="text-swiss-muted truncate mt-0.5">
          {source.excerpt}
        </p>
      </div>
    </div>
  );
}
