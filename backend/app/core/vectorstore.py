"""ChromaDB vector store management."""

from typing import Optional
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from app.config import settings
from app.core.embedding import EmbeddingService


class VectorStoreManager:
    """Manages ChromaDB operations: add, search, delete documents."""

    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_db(self) -> Chroma:
        """Get or initialize ChromaDB instance."""
        if self._db is None:
            embedding_service = EmbeddingService()
            self._db = Chroma(
                persist_directory=settings.chroma_persist_dir,
                embedding_function=embedding_service.get_embeddings(),
                collection_metadata={"hnsw:space": "cosine"},
            )
        return self._db

    def add_documents(self, documents: list[Document], doc_id: str) -> int:
        """Add document chunks to vector store.

        Returns:
            Number of chunks added.
        """
        db = self._get_db()
        db.add_documents(documents)
        return len(documents)

    def search(
        self,
        query: str,
        k: int = None,
        doc_id: Optional[str] = None,
    ) -> list[Document]:
        """Search for similar documents.

        Args:
            query: Search query text
            k: Number of results to return
            doc_id: Optional filter by document ID

        Returns:
            List of relevant Document chunks
        """
        db = self._get_db()
        k = k or settings.retrieval_top_k

        if doc_id:
            return db.similarity_search(
                query, k=k, filter={"doc_id": doc_id}
            )
        return db.similarity_search(query, k=k)

    def search_with_score(
        self,
        query: str,
        k: int = None,
        doc_id: Optional[str] = None,
    ) -> list[tuple[Document, float]]:
        """Search with relevance scores."""
        db = self._get_db()
        k = k or settings.retrieval_top_k

        if doc_id:
            return db.similarity_search_with_relevance_scores(
                query, k=k, filter={"doc_id": doc_id}
            )
        return db.similarity_search_with_relevance_scores(query, k=k)

    def delete_by_doc(self, doc_id: str) -> bool:
        """Delete all chunks belonging to a document."""
        try:
            db = self._get_db()
            db.delete(where={"doc_id": doc_id})
            return True
        except Exception:
            return False

    def get_all_doc_ids(self) -> list[str]:
        """Get all unique document IDs in the store."""
        db = self._get_db()
        try:
            collection = db._collection
            results = collection.get(include=["metadatas"])
            doc_ids = set()
            for meta in results["metadatas"]:
                if meta and "doc_id" in meta:
                    doc_ids.add(meta["doc_id"])
            return sorted(doc_ids)
        except Exception:
            return []
