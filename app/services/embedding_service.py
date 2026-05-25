import torch


class EmbeddingService:
    def __init__(self):
        self.embedding_size = 128

    def generate_embedding(self, text: str):
        text = text.lower().strip()
        seed = sum(ord(char) for char in text)
        torch.manual_seed(seed)

        embedding = torch.rand(self.embedding_size)
        embedding = embedding / torch.norm(embedding)

        return embedding