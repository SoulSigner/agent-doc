"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.docs import router as docs_router


app = FastAPI(
    title="Smart Doc Analysis Agent",
    description="RAG + Agent driven document analysis assistant",
    version="1.0.0",
)

# CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:2400",
        "http://127.0.0.1:2400",
        "http://localhost:3001",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(docs_router)


@app.get("/")
async def root():
    return {
        "name": "Smart Doc Analysis Agent",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
    )