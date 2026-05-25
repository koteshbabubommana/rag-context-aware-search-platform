from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    page: int = 1
    page_size: int = 5
    category: str | None = None