from chromadb.config import Settings
import chromadb
from typing import List, Any
from app.config import MODE

class VectorDB:
    def __init__(self, mode: str = "local"):
        """
        Two modes:
          - local: uses embedded persistent duckdb+parquet (no external service)
          - docker: connects to a chroma REST server running in the 'chroma' container
        """
        if mode == "local":
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="local_chroma"
            ))
        else:
            # Docker expects a chroma server container named "chroma"
            self.client = chromadb.Client(Settings(
                chroma_api_impl="rest",
                chroma_server_host="chroma",
                chroma_server_http_port="8000"
            ))

        # create or get collection
        self.collection = self.client.get_or_create_collection(name="documents")

    def add(self, ids: List[str], texts: List[str], embeddings: Any):
        """
        Add documents and embeddings to the collection.
        embeddings: numpy array or list
        """
        # ensure lists
        self.collection.add(ids=ids, documents=texts, embeddings=embeddings)

    def search(self, query_embedding, k: int = 5):
        """
        Query the DB by embedding. Returns the raw query result from chroma.
        Typically contains 'ids', 'documents', 'distances' or similar structure.
        """
        res = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        return res