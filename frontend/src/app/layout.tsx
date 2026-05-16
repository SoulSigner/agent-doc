import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "智能文档分析",
  description: "基于 RAG 的智能文档问答助手，上传文档即可 AI 对话",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  );
}
