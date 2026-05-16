import uuid
from pathlib import Path
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.config import settings


class DocumentProcessor:
    LOADER_MAP = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
        ".md": TextLoader,
    }
    SUPPORTED_EXTENSIONS = set(LOADER_MAP.keys())

    def __init__(self, chunk_size=None, chunk_overlap=None):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""],
        )

    def validate_file(self, filename):
        suffix = Path(filename).suffix.lower()
        if suffix not in self.SUPPORTED_EXTENSIONS:
            supported = ", ".join(self.SUPPORTED_EXTENSIONS)
            return False, f"Unsupported file type: {suffix}. Supported: {supported}"
        return True, None

    def process(self, file_path, filename):
        doc_id = "doc_" + uuid.uuid4().hex[:12]
        suffix = Path(filename).suffix.lower()
        loader_cls = self.LOADER_MAP[suffix]
        try:
            loader = loader_cls(file_path)
            raw_docs = loader.load()
        except Exception as e:
            raise ValueError(f"Failed to parse document '{filename}': {str(e)}")
        if not raw_docs:
            raise ValueError(f"Document '{filename}' is empty or could not be parsed")
        chunks = self.splitter.split_documents(raw_docs)
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "doc_id": doc_id,
                "filename": filename,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "source": file_path,
            })
            if "page" not in chunk.metadata:
                chunk.metadata["page"] = chunk.metadata.get("page_label", i)
        return doc_id, chunks