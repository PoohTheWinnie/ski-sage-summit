import os
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
import json
from transformers import CLIPProcessor, CLIPModel
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

class ImageProcessor:
    def __init__(self, maps_directory: str = "./data/maps"):
        """
        Initialize the Image Processor to encode images using CLIP and upload to Pinecone.
        
        Args:
            maps_directory (str): Path to directory containing map images
        """
        self.maps_directory = Path(maps_directory)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize CLIP model and processor
        print(f"Loading CLIP model on {self.device}...")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Initialize Pinecone
        self.pc = Pinecone(
            api_key=os.getenv('PINECONE_API_KEY'),
        )
        
        # Constants
        self.INDEX_NAME = "ski-map-embeddings"
        self.EMBEDDING_DIM = 512  # CLIP's embedding dimension
        
        # Create Pinecone index if it doesn't exist
        self._initialize_pinecone_index()
        
        # Connect to the index
        self.index = self.pc.Index(self.INDEX_NAME)
        
        # Store metadata
        self.metadata = {}
        
    def _initialize_pinecone_index(self):
        """Create Pinecone index if it doesn't exist."""
        if self.INDEX_NAME not in self.pc.list_indexes().names():
            print(f"Creating new Pinecone index: {self.INDEX_NAME}")
            self.pc.create_index(
                name=self.INDEX_NAME,
                dimension=self.EMBEDDING_DIM,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region='us-east-1'
                ) 
            )
            print(f"Created new Pinecone index: {self.INDEX_NAME}")
        else:
            print(f"Using existing Pinecone index: {self.INDEX_NAME}")
    
    def encode_and_upload_images(self):
        """Encode all images in the maps directory using CLIP and upload to Pinecone."""
        print(f"Processing images from {self.maps_directory}...")
        
        # Get existing vectors to avoid re-uploading
        try:
            stats = self.index.describe_index_stats()
            print(f"Current index has {stats['total_vector_count']} vectors")
            
            # Get list of vector IDs (if needed)
            # existing_ids = set()
            # You would need to implement pagination to get all IDs
            
        except Exception as e:
            print(f"Error checking index stats: {str(e)}")
        
        # Batch processing parameters
        batch_size = 10
        vectors_to_upsert = []
        processed_count = 0
        
        # Process all PNG images in the directory
        image_files = list(self.maps_directory.glob("*.png"))
        print(f"Found {len(image_files)} image files")
        
        for img_path in tqdm(image_files):
            try:
                vector_id = str(img_path.stem)
                
                # Load and process image
                image = Image.open(img_path)
                inputs = self.processor(images=image, return_tensors="pt", padding=True)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                # Generate image embedding
                with torch.no_grad():
                    image_features = self.model.get_image_features(**inputs)
                    image_embedding = image_features.cpu().numpy()[0]
                
                # Extract metadata
                metadata = self._extract_metadata(img_path)
                self.metadata[str(img_path)] = metadata
                
                # Prepare vector for upserting
                vector_data = {
                    'id': vector_id,
                    'values': image_embedding.tolist(),
                    'metadata': {
                        'filepath': str(img_path),
                        **metadata
                    }
                }
                vectors_to_upsert.append(vector_data)
                processed_count += 1
                
                # Batch upsert when batch is full
                if len(vectors_to_upsert) >= batch_size:
                    print(f"Upserting batch of {len(vectors_to_upsert)} vectors")
                    self.index.upsert(vectors=vectors_to_upsert)
                    vectors_to_upsert = []
                
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
        
        # Upsert any remaining vectors
        if vectors_to_upsert:
            print(f"Upserting final batch of {len(vectors_to_upsert)} vectors")
            self.index.upsert(vectors=vectors_to_upsert)
        
        # Save metadata
        self._save_metadata()
        
        print(f"Successfully processed {processed_count} images")
        print(f"Index now contains {self.index.describe_index_stats()['total_vector_count']} vectors")
    
    def _extract_metadata(self, image_path: Path) -> dict:
        """Extract metadata from image filename and any associated metadata files."""
        filename = image_path.stem
        metadata = {
            "name": filename,
            "features": [],
            "difficulty_levels": []
        }
        
        # Extract features based on filename
        if "back-side" in filename.lower():
            metadata["features"].append("back side trails")
        if "front-side" in filename.lower():
            metadata["features"].append("front side trails")
        if "goats-eye" in filename.lower():
            metadata["features"].append("expert terrain")
        if "louise" in filename.lower():
            metadata["features"].append("lake views")
        if "palisades" in filename.lower():
            metadata["features"].append("palisades resort")
        
        return metadata
    
    def _save_metadata(self):
        """Save metadata to a JSON file."""
        metadata_path = self.maps_directory / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

if __name__ == "__main__":
    processor = ImageProcessor()
    processor.encode_and_upload_images()
