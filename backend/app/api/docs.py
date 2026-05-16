"""Document management API endpoints."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import DocumentInfo
from app.core.vectorstore import VectorStoreManager
from app.api.upload import get_document_registry

router = APIRouter(prefix="/api", tags=["docs"])


@router.get("/docs")
async def list_documents() -> list[DocumentInfo]:
    """List all uploaded documents."""
    registry = get_document_registry()
    return [
        DocumentInfo(
            doc_id=info["doc_id"],
            filename=info["filename"],
            chunks=info["chunks"],
            created_at=info["created_at"],
        )
        for info in registry.values()
    ]


@router.delete("/docs/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document and its vector store entries."""
    registry = get_document_registry()

    if doc_id not in registry:
        raise HTTPException(status_code=404, detail="Document not found")

    # Remove from vector store
    store = VectorStoreManager()
    store.delete_by_doc(doc_id)

    # Remove from registry
    del registry[doc_id]

    return {"status": "deleted", "doc_id": doc_id}
