// 与后端通信的 API 客户端

export interface DocumentInfo {
  doc_id: string;
  filename: string;
  chunks: number;
  created_at: string;
}

export interface SourceReference {
  filename: string;
  page: number | string;
  excerpt: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: SourceReference[];
}

const API_BASE = "/api";

/** 上传文档文件 */
export async function uploadDocument(file: File): Promise<DocumentInfo> {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "上传失败");
  }
  return response.json();
}

/** 获取所有已上传文档 */
export async function fetchDocuments(): Promise<DocumentInfo[]> {
  const response = await fetch(`${API_BASE}/docs`);
  if (!response.ok) throw new Error("获取文档列表失败");
  return response.json();
}

/** 删除文档 */
export async function deleteDocument(docId: string): Promise<void> {
  const response = await fetch(`${API_BASE}/docs/${docId}`, { method: "DELETE" });
  if (!response.ok) throw new Error("删除文档失败");
}

/** 通过 SSE 流式获取对话回复 */
export async function* streamChat(
  message: string,
  docId?: string,
  history?: { role: string; content: string }[]
): AsyncGenerator<{ token: string; done: boolean; sources: SourceReference[] | null }> {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, doc_id: docId, history: history || [] }),
  });

  if (!response.ok) throw new Error("对话请求失败");

  const reader = response.body?.getReader();
  if (!reader) throw new Error("无响应数据流");

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const data = line.slice(6);
        try {
          yield JSON.parse(data);
        } catch {
          // 跳过解析错误
        }
      }
    }
  }
}
