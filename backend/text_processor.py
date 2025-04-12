from typing import List, Dict
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

class TextProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))

    def process_book(self, text: str, metadata: Dict) -> List[Dict]:
        """Process a book and return chunks with embeddings"""
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                'content': chunk,
                'metadata': {
                    **metadata,
                    'chunk_id': i,
                }
            }
            documents.append(doc)
            
        return documents 