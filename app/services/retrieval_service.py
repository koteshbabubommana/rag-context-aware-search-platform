import torch.nn.functional as F

from app.services.embedding_service import EmbeddingService


DOCUMENTS = [
    {
        "document_id": "doc_001",
        "title": "FastAPI Backend Optimization",
        "content": "Techniques for reducing API latency using async processing, caching, and efficient request handling.",
        "category": "backend"
    },
    {
        "document_id": "doc_002",
        "title": "RAG Retrieval Workflow",
        "content": "Retrieval augmented generation systems use embeddings, semantic search, and context ranking to improve answer quality.",
        "category": "rag"
    },
    {
        "document_id": "doc_003",
        "title": "Redis Caching for Search APIs",
        "content": "Redis caching improves low-latency API responses by storing frequent search results and reducing repeated computation.",
        "category": "cache"
    },
    {
        "document_id": "doc_004",
        "title": "Vector Similarity Search",
        "content": "Semantic search platforms use vector embeddings and cosine similarity to retrieve contextually relevant documents.",
        "category": "search"
    },
    {
        "document_id": "doc_005",
        "title": "AI Recommendation Ranking",
        "content": "Ranking pipelines use similarity scores, metadata filters, and relevance scoring to return high quality recommendations.",
        "category": "ai"
    },
    {
        "document_id": "doc_006",
        "title": "Monitoring Search Platforms",
        "content": "Production search platforms track latency, throughput, cache hit rates, and retrieval quality metrics.",
        "category": "monitoring"
    },
    {
        "document_id": "doc_007",
        "title": "Context-Aware Search Systems",
        "content": "Context-aware search improves retrieval by combining query intent, document metadata, and semantic embeddings.",
        "category": "search"
    },
    {
        "document_id": "doc_008",
        "title": "PostgreSQL Search Backend",
        "content": "Search backends often use PostgreSQL for metadata persistence and vector extensions for similarity retrieval.",
        "category": "database"
    }
]


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.document_embeddings = {
            document["document_id"]: self.embedding_service.generate_embedding(
                document["title"] + " " + document["content"]
            )
            for document in DOCUMENTS
        }

    def retrieve(self, query_embedding, top_k=5, category=None):
        results = []

        for document in DOCUMENTS:
            if category and document["category"] != category:
                continue

            document_embedding = self.document_embeddings[document["document_id"]]

            score = F.cosine_similarity(
                query_embedding.unsqueeze(0),
                document_embedding.unsqueeze(0)
            ).item()

            results.append({
                "document_id": document["document_id"],
                "title": document["title"],
                "content": document["content"],
                "category": document["category"],
                "score": round(float(score), 4)
            })

        results = sorted(results, key=lambda item: item["score"], reverse=True)

        return results[:top_k]