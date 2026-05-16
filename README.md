# 鏅鸿兘鏂囨。鍒嗘瀽 Agent

RAG + Agent 椹卞姩鐨勬櫤鑳芥枃妗ｅ垎鏋愬姪鎵?涓婁紶 PDF/DOCX/TXT/MD 鏂囨。锛孉I 鑷姩瑙ｆ瀽銆佹憳瑕併€佹彁鍙栧叧閿俊鎭€?

## 鎶€鏈爤
- 鍚庣: FastAPI + LangChain + ChromaDB + FastEmbed
- 鍓嶇: Next.js 14 + Tailwind CSS
- LLM: MIMO API
- Embedding: BAAI/bge-small-zh-v1.5 (ONNX)

## 蹇€熷惎鍔?

### 鍚庣
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 鍓嶇
```bash
cd frontend
npm install
npm run dev
```

鎵撳紑 http://localhost:2400
