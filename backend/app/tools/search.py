"""Tool: Search documents in vector store."""

from app.core.vectorstore import VectorStoreManager


def document_search(query: str, doc_id: str = None, k: int = 4) -> str:
    """Search for relevant document chunks."""
    store = VectorStoreManager()
    results = store.search(query, k=k, doc_id=doc_id)
    if not results:
        return "No relevant documents found."
    parts = []
    for doc in results:
        filename = doc.metadata.get("filename", "unknown")
        page = doc.metadata.get("page", "?")
        parts.append(f"[Source: {filename}, Page: {page}]\n{doc.page_content}")
    return "\n\n".join(parts)
