"""Tool: Extract structured information from documents."""

from app.core.vectorstore import VectorStoreManager


def extract_info(query: str, doc_id: str = None) -> str:
    """Extract specific information from documents."""
    store = VectorStoreManager()
    results = store.search(query, k=8, doc_id=doc_id)
    if not results:
        return "No relevant information found."
    results.sort(key=lambda d: d.metadata.get("chunk_index", 0))
    parts = []
    for doc in results:
        filename = doc.metadata.get("filename", "unknown")
        page = doc.metadata.get("page", "?")
        parts.append(f"[Source: {filename}, Page: {page}]\n{doc.page_content}")
    return "\n\n".join(parts)
