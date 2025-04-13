import os
import torch
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional, Dict
from transformers import CLIPProcessor, CLIPModel
from pathlib import Path
from dotenv import load_dotenv
import json
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
from openai import OpenAI

load_dotenv()

class TrailMapRAG:
    def __init__(self, maps_directory: str = "backend/data/maps"):
        """
        Initialize the Trail Map RAG system with Pinecone and DALL-E 2.
        
        Args:
            maps_directory (str): Path to directory containing trail map images
        """
        self.maps_directory = Path(maps_directory)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize CLIP model and processor
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
        
        # Build the index
        self._build_index()
    
    def _initialize_pinecone_index(self):
        """Create Pinecone index if it doesn't exist."""
        if self.INDEX_NAME not in self.pc.list_indexes().names():
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
    
    def _build_index(self):
        """Build the Pinecone index from all images in the maps directory."""
        print("Building image index...")
        
        # Get existing vectors
        existing_ids = set()
        
        # Batch processing parameters
        batch_size = 10
        vectors_to_upsert = []
        
        for img_path in tqdm(list(self.maps_directory.glob("*.png"))):
            try:
                vector_id = str(img_path.stem)
                
                # Skip if already indexed
                if vector_id in existing_ids:
                    print(f"Skipping already indexed: {img_path.name}")
                    continue
                
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
                
                # Batch upsert when batch is full
                if len(vectors_to_upsert) >= batch_size:
                    self.index.upsert(vectors=vectors_to_upsert)
                    vectors_to_upsert = []
                
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
        
        # Upsert any remaining vectors
        if vectors_to_upsert:
            self.index.upsert(vectors=vectors_to_upsert)
        
        # Save metadata
        self._save_metadata()
        
        print(f"Indexed {self.index.describe_index_stats()['total_vector_count']} images")
    
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
        
        return metadata
    
    def _save_metadata(self):
        """Save metadata to a JSON file."""
        metadata_path = self.maps_directory / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)
    
    def query(self, text_query: str, k: int = 3) -> List[Tuple[str, float]]:
        """
        Query the Pinecone index with a text description and return the most similar images.
        
        Args:
            text_query (str): Text description of desired trail map
            k (int): Number of results to return
            
        Returns:
            List[Tuple[str, float]]: List of (image_path, similarity_score) pairs
        """
        # Process text query
        inputs = self.processor(text=text_query, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate text embedding
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
            text_embedding = text_features.cpu().numpy()[0]
        
        # Query Pinecone
        query_results = self.index.query(
            vector=text_embedding.tolist(),
            top_k=k,
            include_metadata=True
        )
        
        # Format results
        results = []
        for match in query_results['matches']:
            image_path = match['metadata']['filepath']
            score = match['score']
            results.append((image_path, score))
        
        return results
    
    def get_metadata(self, image_path: str) -> dict:
        """Get metadata for a specific image."""
        return self.metadata.get(image_path, {})

    def generate_enhanced_map(self, 
                            query: str,
                            difficulty_level: str = "intermediate",
                            size: str = "512x512",
                            num_references: int = 3) -> Dict:
        """
        Generate a new trail map using DALL-E 2 with RAG enhancement.
        
        Args:
            query (str): User's description of desired trail map
            difficulty_level (str): Difficulty level of trails
            size (str): Image size for DALL-E 2
            num_references (int): Number of reference maps to use
            
        Returns:
            Dict: Contains generated image URL, reference maps, and generation details
        """
        # Get similar maps
        similar_maps = self.query(query, k=num_references)
        
        # Extract features and characteristics from similar maps
        features = []
        characteristics = []
        reference_paths = []
        
        for map_path, score in similar_maps:
            metadata = self.get_metadata(map_path)
            features.extend(metadata.get("features", []))
            reference_paths.append(map_path)
            
            # Extract map characteristics
            map_name = metadata.get("name", "").replace("-", " ")
            if map_name:
                characteristics.append(f"style elements from {map_name}")
        
        # Construct enhanced prompt
        base_prompt = f"Create a ski trail map with {difficulty_level} difficulty trails"
        
        # Add unique features from reference maps
        unique_features = list(set(features))
        if unique_features:
            feature_text = ", ".join(unique_features)
            base_prompt += f", incorporating {feature_text}"
        
        # Add style characteristics
        if characteristics:
            style_text = " and ".join(characteristics[:2])  # Limit to top 2 references
            base_prompt += f". Reference {style_text}"
        
        # Add specific requirements from user query
        base_prompt += f". {query}"
        
        # Add professional styling
        base_prompt += ". Create in a professional ski resort map style with clear trail markers, lifts, and legend"
        
        try:
            # Generate image with DALL-E 2
            response = self.openai_client.images.generate(
                model="dall-e-2",
                prompt=base_prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            # Prepare result
            result = {
                "generated_image_url": response.data[0].url,
                "reference_maps": reference_paths,
                "prompt_used": base_prompt,
                "features_incorporated": unique_features,
                "reference_characteristics": characteristics
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")

    def analyze_map_style(self, image_path: str) -> List[str]:
        """
        Analyze the style characteristics of a given map.
        
        Args:
            image_path (str): Path to the map image
            
        Returns:
            List[str]: List of style characteristics
        """
        try:
            metadata = self.get_metadata(image_path)
            characteristics = []
            
            # Extract style characteristics based on metadata
            if "back side" in str(image_path).lower():
                characteristics.append("back side trail layout")
            if "front side" in str(image_path).lower():
                characteristics.append("front side trail layout")
            if metadata.get("features"):
                characteristics.extend(metadata["features"])
                
            return characteristics
            
        except Exception as e:
            print(f"Error analyzing map style: {str(e)}")
            return [] 