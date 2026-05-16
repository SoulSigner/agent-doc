# 智能文档分析 Agent

RAG + Agent 驱动的智能文档分析助手，上传 PDF/DOCX/TXT/MD 文档，AI 自动解析、摘要、提取关键信息。

## 技术栈
- 后端: FastAPI + LangChain + ChromaDB + FastEmbed
- 前端: Next.js 14 + Tailwind CSS
- LLM: MIMO API
- Embedding: BAAI/bge-small-zh-v1.5 (ONNX)

## 快速启动

### 后端
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

打开 http://localhost:2400
