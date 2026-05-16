"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # LLM Configuration
    mimo_api_key: str = "your_mimo_api_key_here"
    mimo_base_url: str = "https://api.mimo.com/v1"
    mimo_model_name: str = "mimo-v2.5-pro"

    # Embedding Configuration
    embedding_model_name: str = "BAAI/bge-small-zh-v1.5"
    embedding_device: str = "cpu"  # 'cpu' or 'cuda'

    # Vector Store
    chroma_persist_dir: str = "./chroma_db"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # Upload
    max_file_size_mb: int = 50
    upload_dir: str = "./uploads"

    # RAG Configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    retrieval_top_k: int = 4
    max_history_turns: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
