"""Chat API endpoint with streaming RAG responses."""

import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest
from app.core.agent import AgentService
from app.api.upload import get_document_registry

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat")
async def chat(request: ChatRequest):
    """Stream chat response with RAG context."""
    agent = AgentService()

    # Validate doc_id if provided
    if request.doc_id:
        registry = get_document_registry()
        if request.doc_id not in registry:
            raise HTTPException(
                status_code=404,
                detail=f"Document not found: {request.doc_id}"
            )

    async def event_stream():
        async for chunk in agent.chat_stream(
            message=request.message,
            doc_id=request.doc_id,
            history=request.history or [],
        ):
            yield f"event: message\ndata: {json.dumps(chunk, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
