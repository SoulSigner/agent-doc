"""Document upload API endpoint."""

import os
import json
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime

from app.config import settings
from app.models.schemas import UploadResponse
from app.core.document_processor import DocumentProcessor
from app.core.vectorstore import VectorStoreManager

router = APIRouter(prefix="/api", tags=["upload"])

# In-memory document registry (in production, use a database)
_document_registry: dict[str, dict] = {}


def get_document_registry() -> dict:
    """Get the in-memory document registry."""
    return _document_registry


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for processing and indexing.

    Supported formats: PDF, DOCX, TXT, MD
    Max file size: 50MB
    """
    # Validate file
    processor = DocumentProcessor()
    is_valid, error_msg = processor.validate_file(file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Check file size
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size_mb:.1f}MB. Max: {settings.max_file_size_mb}MB",
        )

    # Save file to upload directory
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(content)

    try:
        # Process document: parse, chunk, embed, store
        doc_id, chunks = processor.process(str(file_path), file.filename)

        # Add to vector store
        store = VectorStoreManager()
        num_added = store.add_documents(chunks, doc_id)

        # Register document
        _document_registry[doc_id] = {
            "doc_id": doc_id,
            "filename": file.filename,
            "chunks": num_added,
            "created_at": datetime.now().isoformat(),
            "file_path": str(file_path),
        }

        return UploadResponse(
            doc_id=doc_id,
            filename=file.filename,
            chunks=num_added,
            status="success",
        )

    except ValueError as e:
        # Clean up file on processing error
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )
