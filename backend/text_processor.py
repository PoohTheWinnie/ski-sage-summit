import os
import json
import PyPDF2
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

class TextProcessor:
    def __init__(self, data_dir: str = "data/texts"):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
        self.chunks_dir = self.data_dir / "chunks"
        self.index_name = "ski-sage-summit"
        
        # Create necessary directories
        self.processed_dir.mkdir(exist_ok=True)
        self.chunks_dir.mkdir(exist_ok=True)
        
        # Initialize Pinecone
        if not os.getenv("PINECONE_API_KEY"):
            raise ValueError("PINECONE_API_KEY environment variable is not set")
            
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
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
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def process_pdf(self, file_path: Path) -> str:
        """Extract text from PDF files"""
        text = ""
        with open(file_path, 'rb') as file:
            if file_path.suffix.lower() == '.pdf':
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
        return text
    
    def process_txt(self, file_path: Path) -> str:
        """Extract text from TXT files"""
        text = ""
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def process_files(self):
        """Process all files in the data directory"""
        processed_docs = []
        
        # Iterate through all files in the data directory
        for file_path in tqdm(list(self.data_dir.glob('*')), desc="Processing files"):
            # Skip directories and already processed files
            if file_path.is_dir() or file_path.parent == self.processed_dir:
                continue
            
            # Get file information
            file_name = file_path.stem
            file_type = file_path.suffix.lower()
            
            # Process based on file type
            if file_type == '.pdf':
                text = self.process_pdf(file_path)
            elif file_type == '.txt':
                text = self.process_txt(file_path)
            else:
                print(f"Warning: Unsupported file type {file_type} for {file_path}")
                continue
            
            if not text:
                print(f"Warning: No text extracted from {file_path}")
                continue
            
            # Create document data
            doc_data = {
                "title": file_name,
                "source": str(file_path),
                "text": text
            }
            
            # Save processed document
            processed_file = self.processed_dir / f"{file_name}_processed.json"
            with open(processed_file, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, indent=2)
            
            processed_docs.append(doc_data)
        
        return processed_docs

    def create_chunks(self, processed_docs: List[Dict[str, Any]]):
        """Create chunks from processed documents"""
        all_chunks = []
        
        for doc in tqdm(processed_docs, desc="Creating chunks"):
            text_chunks = self.text_splitter.split_text(doc["text"])
            
            chunks = []
            for i, chunk in enumerate(text_chunks):
                chunk_data = {
                    "text": chunk,
                    "metadata": {
                        "title": doc["title"],
                        "source": doc["source"],
                        "chunk_index": i,
                        "text": chunk  # Include text in metadata for retrieval
                    }
                }
                chunks.append(chunk_data)
            
            # Save chunks
            chunk_file = self.chunks_dir / f"{doc['title']}_chunks.json"
            with open(chunk_file, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2)
            
            all_chunks.extend(chunks)
        
        return all_chunks

    def add_to_pinecone(self, chunks: List[Dict]):
        """Add chunks to Pinecone"""
        # Clear existing index using the correct delete API
        # self.index.delete(deleteAll=True)
        
        # Prepare batches
        batch_size = 100
        for i in tqdm(range(0, len(chunks), batch_size), desc="Adding to Pinecone"):
            batch = chunks[i:i + batch_size]
            
            # Generate embeddings for the batch
            texts = [chunk["text"] for chunk in batch]
            embeddings = self.embedding_function(texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            for j, (chunk, embedding) in enumerate(zip(batch, embeddings)):
                vectors.append({
                    "id": f"chunk_{i + j}",
                    "values": embedding.tolist(),
                    "metadata": chunk["metadata"]
                })
            
            # Upsert to Pinecone
            self.index.upsert(vectors=vectors)

    def process_all(self):
        """Run the complete processing pipeline"""
        print("Starting text processing pipeline...")
        
        # Process files
        processed_docs = self.process_files()
        print(f"Processed {len(processed_docs)} documents")
        
        # Create chunks
        chunks = self.create_chunks(processed_docs)
        print(f"Created {len(chunks)} chunks")
        
        # Add to Pinecone
        self.add_to_pinecone(chunks)
        print("Documents added to Pinecone")


if __name__ == "__main__":
    text_processor = TextProcessor()
    text_processor.process_all()