from pydantic import BaseModel
from typing import List


class SearchResult(BaseModel):
    document_id: str
    title: str
    content: str
    category: str
    score: float


class SearchResponse(BaseModel):
    query: str
    page: int
    page_size: int
    total_results: int
    cached: bool
    latency_ms: float
    results: List[SearchResult]