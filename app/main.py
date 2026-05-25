from fastapi import FastAPI

from app.config import settings
from app.models.request_models import SearchRequest
from app.models.response_models import SearchResponse
from app.services.search_service import SearchService
from app.utils.logger import logger


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description=(
        "Production-style RAG context-aware search backend with semantic retrieval, "
        "embedding ranking, filtering, pagination, caching, and monitoring."
    )
)

search_service = SearchService()


@app.get("/")
async def home():
    return {
        "message": "RAG Context-Aware Search Platform Running",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "rag-context-aware-search-platform"
    }


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    logger.info(f"Running semantic search for query={request.query}")

    return await search_service.semantic_search(
        query=request.query,
        top_k=request.top_k,
        page=request.page,
        page_size=request.page_size,
        category=request.category
    )


@app.get("/metrics")
async def metrics():
    return search_service.get_metrics()


@app.get("/documents")
async def documents():
    from app.services.retrieval_service import DOCUMENTS

    return {
        "total_documents": len(DOCUMENTS),
        "documents": DOCUMENTS
    }