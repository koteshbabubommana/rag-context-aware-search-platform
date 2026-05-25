import time

from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.cache_service import CacheService
from app.services.monitoring_service import MonitoringService


class SearchService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.retrieval_service = RetrievalService()
        self.cache_service = CacheService()
        self.monitoring_service = MonitoringService()

    async def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        page: int = 1,
        page_size: int = 5,
        category: str | None = None
    ):
        start_time = time.time()

        cache_key = f"{query}:{top_k}:{page}:{page_size}:{category}"
        cached_result = self.cache_service.get(cache_key)

        if cached_result:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            cached_result["cached"] = True
            cached_result["latency_ms"] = latency_ms
            self.monitoring_service.record_request(latency_ms, cached=True)
            return cached_result

        query_embedding = self.embedding_service.generate_embedding(query)

        retrieved_results = self.retrieval_service.retrieve(
            query_embedding=query_embedding,
            top_k=top_k,
            category=category
        )

        total_results = len(retrieved_results)

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_results = retrieved_results[start_index:end_index]

        latency_ms = round((time.time() - start_time) * 1000, 2)

        response = {
            "query": query,
            "page": page,
            "page_size": page_size,
            "total_results": total_results,
            "cached": False,
            "latency_ms": latency_ms,
            "results": paginated_results
        }

        self.cache_service.set(
            cache_key,
            response.copy(),
            ttl_seconds=settings.CACHE_TTL_SECONDS
        )

        self.monitoring_service.record_request(latency_ms, cached=False)

        return response

    def get_metrics(self):
        return self.monitoring_service.get_metrics()