"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel
from typing import Optional


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    chunks: int
    status: str


class DocumentInfo(BaseModel):
    doc_id: str
    filename: str
    chunks: int
    created_at: str


class SourceReference(BaseModel):
    filename: str
    page: int | str
    excerpt: str


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    sources: Optional[list[SourceReference]] = None


class ChatRequest(BaseModel):
    message: str
    doc_id: Optional[str] = None
    history: Optional[list[dict]] = None


class ChatResponse(BaseModel):
    message: str
    sources: list[SourceReference] = []
