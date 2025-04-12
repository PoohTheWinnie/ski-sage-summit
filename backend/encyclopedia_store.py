import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

class EncyclopediaStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
        self.vector_store = Chroma(
            persist_directory="encyclopedia_db",
            embedding_function=self.embeddings
        )

    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store"""
        texts = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        self.vector_store.add_texts(
            texts=texts,
            metadatas=metadatas
        )
        self.vector_store.persist()

    def query(self, query_text: str, n_results: int = 5):
        """Query the vector store"""
        results = self.vector_store.similarity_search_with_relevance_scores(
            query_text,
            k=n_results
        )
        return results 