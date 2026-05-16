"""Tool: Summarize a document."""

from app.core.vectorstore import VectorStoreManager


def summarize_document(doc_id: str) -> str:
    """Get full document content for summarization."""
    store = VectorStoreManager()
    results = store.search("", k=20, doc_id=doc_id)
    if not results:
        return "Document not found or empty."
    # Sort by chunk order
    results.sort(key=lambda d: d.metadata.get("chunk_index", 0))
    return "\n\n".join(doc.page_content for doc in results)
