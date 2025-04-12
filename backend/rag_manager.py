from typing import List, Dict
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from .image_processor import ImageProcessor
from .vector_store import VectorStore

load_dotenv()

class RAGManager:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.vector_store = VectorStore()
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def process_and_store_map(self, image_path: str, metadata: Dict):
        """Process a ski map and store its information"""
        # Generate description from image
        description = self.image_processor.process_image(image_path)
        
        # Store in vector database
        self.vector_store.add_document(
            id=metadata['name'],
            description=description,
            metadata=metadata
        )
        
        return {"status": "success", "description": description}

    async def query_and_generate(self, query: str) -> str:
        """Query the vector store and generate a response"""
        # Get relevant contexts
        results = self.vector_store.query(query)
        
        # Construct prompt with retrieved information
        context = "\n".join(results['documents'][0])
        
        prompt = f"""You are a ski resort expert assistant. Use the following context about ski maps to answer the question.
        
Context: {context}

Question: {query}

Please provide a detailed response about the ski trails and features mentioned in the question."""

        # Generate response using Claude
        response = self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text 