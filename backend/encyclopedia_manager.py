from typing import List, Dict
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .data.config import SKI_TEXTS

load_dotenv()

class EncyclopediaManager:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
        self.vector_store = None
        self.initialize_vector_store()

    def initialize_vector_store(self):
        """Initialize the vector store with all ski texts"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        documents = []
        for category, info in SKI_TEXTS.items():
            with open(info['path'], 'r') as f:
                text = f.read()
                chunks = text_splitter.split_text(text)
                
                for chunk in chunks:
                    documents.append({
                        'content': chunk,
                        'metadata': {
                            'category': category,
                            **info['metadata']
                        }
                    })

        texts = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        self.vector_store = Chroma(
            collection_name="ski_encyclopedia",
            embedding_function=self.embeddings,
            persist_directory="encyclopedia_db"
        )
        
        # Only add documents if the collection is empty
        if self.vector_store.get()['ids'] == []:
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            self.vector_store.persist()

    async def query_and_generate(self, query: str) -> str:
        """Query the vector store and generate a response"""
        results = self.vector_store.similarity_search_with_relevance_scores(
            query,
            k=5
        )
        
        contexts = []
        for doc, score in results:
            if score > 0.7:
                contexts.append(f"From {doc.metadata['category']} section:\n{doc.page_content}")

        context_text = "\n\n".join(contexts)
        
        prompt = f"""You are a ski encyclopedia expert. Use the following information to answer the question.
        If the context doesn't contain relevant information, use your general knowledge about skiing but mention this fact.
        
Context:
{context_text}

Question: {query}

Please provide a detailed, well-structured response about skiing. If you're citing specific information from the knowledge base,
mention the category it came from. Format the response in a clear, easy-to-read manner."""

        response = self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text 