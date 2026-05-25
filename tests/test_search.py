import asyncio

from app.services.search_service import SearchService


def test_semantic_search():
    async def run_test():
        service = SearchService()

        response = await service.semantic_search(
            query="FastAPI optimization",
            top_k=5,
            page=1,
            page_size=3
        )

        assert "results" in response
        assert response["total_results"] > 0
        assert len(response["results"]) <= 3

    asyncio.run(run_test())