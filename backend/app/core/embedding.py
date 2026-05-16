"""Embedding service using fastembed (ONNX-based, lightweight).

Uses BAAI/bge-small-zh-v1.5 via fastembed for local embedding generation.
Compatible with Python 3.13, no PyTorch dependency required.
"""

from typing import List
from langchain_core.embeddings import Embeddings
from fastembed import TextEmbedding


class FastEmbedWrapper(Embeddings):
    """LangChain-compatible wrapper for fastembed."""

    _model = None

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        self.model_name = model_name

    def _get_model(self) -> TextEmbedding:
        if self._model is None:
            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        model = self._get_model()
        embeddings = list(model.embed(texts))
        return [e.tolist() for e in embeddings]

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        model = self._get_model()
        embeddings = list(model.embed([text]))
        return embeddings[0].tolist()


class EmbeddingService:
    """Manages the local embedding model (singleton)."""

    _instance = None
    _embeddings = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_embeddings(self) -> FastEmbedWrapper:
        """Get or initialize the embedding model."""
        if self._embeddings is None:
            from app.config import settings
            self._embeddings = FastEmbedWrapper(
                model_name=settings.embedding_model_name
            )
        return self._embeddings

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query text."""
        return self.get_embeddings().embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple document texts."""
        return self.get_embeddings().embed_documents(texts)
