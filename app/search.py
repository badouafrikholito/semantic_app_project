from app.preprocessing import clean_text
from app.models.embedding_model import EmbeddingModel
from app.vector_db import VectorDB
from typing import Dict, Any, List

class SemanticSearch:
    def __init__(self, mode: str = "local"):
        self.mode = mode
        self.model = EmbeddingModel()
        self.db = VectorDB(mode)

    def index_documents(self):
        """
        Read app/data/sample_documents.txt and index each line as a document.
        """
        docs = []
        with open("app/data/sample_documents.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    docs.append(clean_text(line))

        if not docs:
            return {"status": "no_documents"}

        ids = [str(i) for i in range(len(docs))]
        embeddings = self.model.embed(docs)
        self.db.add(ids=ids, texts=docs, embeddings=embeddings)
        # If using local chroma with persist dir, commit/persist will be automatic
        return {"status": "indexed", "count": len(docs)}

    def search(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Clean query, compute embedding, run DB search, and return a friendly dict.
        """
        q = clean_text(query)
        emb = self.model.embed([q])[0]
        raw = self.db.search(emb, k)

        # raw is a dict; normalize into friendly structure
        results = {
            "ids": raw.get("ids", []),
            "documents": raw.get("documents", []),
            "distances": raw.get("distances", [])
        }
        return {"query": query, "results": results}