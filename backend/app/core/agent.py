"""Agent service for intent routing and tool orchestration."""

from typing import AsyncGenerator, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.config import settings
from app.core.vectorstore import VectorStoreManager
from app.tools.search import document_search
from app.tools.summarize import summarize_document
from app.tools.extract import extract_info


SYSTEM_PROMPT = """You are an intelligent document analysis assistant. Your capabilities include:

1. **Document Q&A**: Answer questions based on user-uploaded documents, citing specific content.
2. **Document Summarization**: Generate structured summaries of documents.
3. **Information Extraction**: Extract key information, entities, dates, amounts from documents.

Response Rules:
- Answer based on document content, do not fabricate information.
- If the document does not contain relevant information, honestly inform the user.
- Cite specific sources (filename, page number).
- Respond in Chinese.
- For summarization and extraction tasks, use structured output."""


class AgentService:
    """Handles chat with RAG retrieval and tool-based responses."""

    _instance = None
    _llm = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_llm(self, stream: bool = False):
        """Get or initialize the LLM instance."""
        return ChatOpenAI(
            api_key=settings.mimo_api_key,
            base_url=settings.mimo_base_url,
            model=settings.mimo_model_name,
            temperature=0.3,
            streaming=stream,
            max_tokens=2048,
        )

    def _classify_intent(self, message: str) -> str:
        """Simple keyword-based intent classification.

        Returns: 'summary', 'extract', or 'qa'
        """
        summary_keywords = ["summary", "summarize", "tldr", "recap"]
        extract_keywords = ["extract", "find", "list", "entities", "dates", "amounts"]

        msg_lower = message.lower()

        for kw in summary_keywords:
            if kw in msg_lower:
                return "summary"

        for kw in extract_keywords:
            if kw in msg_lower:
                return "extract"

        return "qa"

    def _build_messages(
        self,
        message: str,
        context: str,
        history: list[dict],
    ) -> list:
        """Build message list for LLM call."""
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        # Add conversation history
        for msg in history[-settings.max_history_turns * 2:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        # Add current message with context
        if context:
            user_content = f"Reference document content:\n{context}\n\nUser question: {message}"
        else:
            user_content = message

        messages.append(HumanMessage(content=user_content))
        return messages

    async def chat_stream(
        self,
        message: str,
        doc_id: Optional[str] = None,
        history: list[dict] = None,
    ) -> AsyncGenerator[dict, None]:
        """Stream chat response with RAG context.

        Yields:
            {"token": str, "done": bool, "sources": list | None}
        """
        history = history or []
        store = VectorStoreManager()

        # Step 1: Classify intent
        intent = self._classify_intent(message)

        # Step 2: Retrieve context based on intent
        context = ""
        sources = []

        if intent == "summary":
            results = store.search(message, k=10, doc_id=doc_id)
            results.sort(key=lambda d: d.metadata.get("chunk_index", 0))
        elif intent == "extract":
            results = store.search(message, k=10, doc_id=doc_id)
            results.sort(key=lambda d: d.metadata.get("chunk_index", 0))
        else:
            results = store.search(message, k=settings.retrieval_top_k, doc_id=doc_id)

        if results:
            context_parts = []
            for doc in results:
                filename = doc.metadata.get("filename", "unknown")
                page = doc.metadata.get("page", "?")
                context_parts.append(
                    f"[Source: {filename}, Page: {page}]\n{doc.page_content}"
                )
                sources.append({
                    "filename": filename,
                    "page": page,
                    "excerpt": doc.page_content[:200],
                })
            context = "\n\n".join(context_parts)

        # Truncate context if too long
        max_context = 12000
        if len(context) > max_context:
            context = context[:max_context] + "\n\n[Context truncated]"

        # Step 3: Build messages and call LLM
        messages = self._build_messages(message, context, history)
        llm = self._get_llm(stream=True)

        try:
            full_response = ""
            async for chunk in llm.astream(messages):
                if chunk.content:
                    full_response += chunk.content
                    yield {
                        "token": chunk.content,
                        "done": False,
                        "sources": None,
                    }

            # Final message with sources
            yield {
                "token": "",
                "done": True,
                "sources": sources[:4] if sources else [],
            }

        except Exception as e:
            yield {
                "token": f"\n\n[Error] LLM call failed: {str(e)}",
                "done": True,
                "sources": [],
            }