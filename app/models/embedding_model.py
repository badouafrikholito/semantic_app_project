from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        # small, fast, good for semantic search in student projects
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)

    def embed(self, texts: List[str]):
        """
        Return embeddings as a Python list or numpy array.
        SentenceTransformer.encode returns numpy array by default.
        """
        return self.model.encode(texts, convert_to_numpy=True)