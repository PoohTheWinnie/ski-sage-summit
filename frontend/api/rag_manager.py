from pathlib import Path
from typing import List
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from dotenv import load_dotenv
import os
from chromadb.utils import embedding_functions

load_dotenv()

class RAGManager:
    def __init__(self, data_dir: str = "data/texts"):
        self.data_dir = Path(data_dir)
        self.index_name = "ski-sage-summit"
        
        # Initialize Pinecone
        if not os.getenv("PINECONE_API_KEY"):
            raise ValueError("PINECONE_API_KEY environment variable is not set")
            
        # Create Pinecone instance with new API
        self.pc = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY")
        )
        
        # Get or create Pinecone index
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # Default dimension for all-MiniLM-L6-v2
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region='us-east-1'
                ) 
            )
        self.index = self.pc.Index(self.index_name)
        
        # Initialize ChromaDB embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo"
        
        # Define system prompt
        self.system_prompt = """You are an expert skiing instructor and guide. Use the following relevant information from skiing books and manuals to answer the user's question. Be specific and detailed in your response, citing techniques and concepts from the source material.

Context information:
{context}

Remember to:
1. Focus on practical, actionable advice
2. Explain techniques clearly and systematically
3. Include safety considerations when relevant
4. Use proper skiing terminology
"""

    def retrieve_relevant_chunks(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant chunks for a query"""
        # Generate embeddings for the query
        query_embedding = self.embedding_function([query])[0].tolist()  # Convert numpy array to list
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True
        )
        
        # Extract texts from results
        texts = [match.metadata['text'] for match in results.matches]
        return texts

    def generate_response(self, query: str) -> str:
        """Generate a response using RAG"""
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(query)
        
        # Combine chunks into context
        context = "\n\n".join(relevant_chunks)
        
        # Format system prompt with context
        formatted_system_prompt = self.system_prompt.format(context=context)
        
        # Generate response using OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": formatted_system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    

if __name__ == "__main__":
    rag_manager = RAGManager()
    response = rag_manager.generate_response("What is the best way to ski a black diamond?")
    print(response)