import chromadb
from chromadb.config import Settings
import os

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory="db"
        ))
        self.collection = self.client.get_or_create_collection("ski_maps")

    def add_document(self, id: str, description: str, metadata: dict):
        """Add a document to the vector store"""
        self.collection.add(
            documents=[description],
            metadatas=[metadata],
            ids=[id]
        )

    def query(self, query_text: str, n_results: int = 3):
        """Query the vector store"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results 