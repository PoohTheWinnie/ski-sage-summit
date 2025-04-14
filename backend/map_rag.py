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
import base64
import io
import re

load_dotenv()

class MapRAG:
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
        
        # Load metadata if exists
        self.metadata = self._load_metadata()
    
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
    
    def _load_metadata(self) -> Dict:
        """Load metadata from JSON file if it exists."""
        metadata_path = self.maps_directory / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                return json.load(f)
        return {}
    
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
        for match in query_results.matches:
            image_path = match.metadata['filepath']
            score = match.score
            results.append((image_path, score))
        
        return results
    
    def get_metadata(self, image_path: str) -> dict:
        """Get metadata for a specific image."""
        return self.metadata.get(image_path, {})
    
    def extract_features_from_query(self, query: str) -> Dict[str, List[str]]:
        """
        Extract key features from the user query to enhance DALL-E prompt.
        
        Args:
            query (str): User text query
            
        Returns:
            Dict[str, List[str]]: Dictionary of extracted features
        """
        features = {
            "terrainTypes": [],
            "difficultyLevels": [],
            "landscapeFeatures": [],
            "amenities": []
        }
        
        # Extract terrain types
        terrain_patterns = ["steep", "descent", "alpine", "mogul", "powder", "groomed", 
                           "tree", "forest", "glade", "bowl", "chute", "cliff", "jump"]
        for pattern in terrain_patterns:
            if re.search(r'\b' + pattern, query, re.IGNORECASE):
                features["terrainTypes"].append(pattern)
        
        # Extract difficulty levels
        if re.search(r'\bgreen\b|\beasiest\b|\bbeginner\b', query, re.IGNORECASE):
            features["difficultyLevels"].append("green/beginner")
        if re.search(r'\bblue\b|\bintermediate\b', query, re.IGNORECASE):
            features["difficultyLevels"].append("blue/intermediate")
        if re.search(r'\bblack\b|\badvanced\b|\bdifficult\b', query, re.IGNORECASE):
            features["difficultyLevels"].append("black/advanced")
        if re.search(r'\bdouble\s*black\b|\bexpert\b|\bextreme\b', query, re.IGNORECASE):
            features["difficultyLevels"].append("double black/expert")
        
        # Extract landscape features
        landscape_patterns = ["mountain", "peak", "ridge", "lake", "valley", "view", "scenic"]
        for pattern in landscape_patterns:
            if re.search(r'\b' + pattern, query, re.IGNORECASE):
                features["landscapeFeatures"].append(pattern)
        
        # Extract amenities
        amenity_patterns = ["lodge", "lift", "chair", "gondola", "restaurant", "parking", "restroom"]
        for pattern in amenity_patterns:
            if re.search(r'\b' + pattern, query, re.IGNORECASE):
                features["amenities"].append(pattern)
        
        return features
        
    def _image_to_base64(self, image_path: str) -> str:
        """Convert an image file to base64 encoding."""
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
        
    def generate_enhanced_map(self, 
                             query: str,
                             difficulty_level: str = "intermediate",
                             size: str = "1024x1024",
                             num_references: int = 3) -> Dict:
        """
        Generate an enhanced ski trail map based on the query and reference images.
        
        Args:
            query (str): User text query describing the desired ski map
            difficulty_level (str): Desired difficulty level for the trails
            size (str): Size of the generated image
            num_references (int): Number of reference images to use
            
        Returns:
            Dict: Generation results including the generated image
        """
        # Step 1: Extract features from the query to enhance DALL-E prompt
        features = self.extract_features_from_query(query)
        
        # Step 2: Retrieve similar maps using RAG
        similar_maps = self.query(query, k=num_references)
        
        # Step 3: Create an enhanced prompt for DALL-E
        difficulty_colors = {
            "beginner": "green",
            "intermediate": "blue",
            "advanced": "black",
            "expert": "double black diamond"
        }
        
        # Add difficulty color to the prompt
        difficulty_color = difficulty_colors.get(difficulty_level.lower(), "blue")
        
        # Build the enhanced prompt
        prompt = f"Create a detailed ski trail map with the following features:\n"
        
        # Add terrain types
        if features["terrainTypes"]:
            prompt += f"- Terrain types: {', '.join(features['terrainTypes'])}\n"
        else:
            # Default terrain types based on difficulty
            if difficulty_level == "beginner":
                prompt += "- Gentle, wide slopes and minimal inclines\n"
            elif difficulty_level == "intermediate":
                prompt += "- Moderate slopes with some steeper sections\n" 
            elif difficulty_level == "advanced":
                prompt += "- Steep slopes, moguls, and some challenging terrain\n"
            elif difficulty_level == "expert":
                prompt += "- Very steep slopes, chutes, cliffs, and technical terrain\n"
        
        # Add difficulty levels if specified, otherwise use the provided difficulty level
        if features["difficultyLevels"]:
            prompt += f"- Trail difficulty markings: {', '.join(features['difficultyLevels'])}\n"
        else:
            prompt += f"- Primary trail difficulty: {difficulty_level} ({difficulty_color})\n"
        
        # Add landscape features
        if features["landscapeFeatures"]:
            prompt += f"- Landscape features: {', '.join(features['landscapeFeatures'])}\n"
        
        # Add amenities
        if features["amenities"]:
            prompt += f"- Amenities: {', '.join(features['amenities'])}\n"
        
        # Add standard elements of a ski map
        prompt += """
        - Show lifts as dotted lines
        - Use a realistic design for the map
        - Each trail should be labeled with its difficulty level with an icon and color
        - green for beginner, blue for intermediate, black for advanced, double black for expert
        """
        
        # Step 4: Prepare reference images if available
        reference_images = []
        if similar_maps:
            print(f"Using {len(similar_maps)} reference images for generation")
            for path, score in similar_maps:
                try:
                    # Add reference image
                    image_path = path
                    if not os.path.exists(image_path):
                        # Try to find the image using the filename if the path isn't correct
                        filename = os.path.basename(path)
                        possible_path = os.path.join(self.maps_directory, filename)
                        if os.path.exists(possible_path):
                            image_path = possible_path
                        else:
                            print(f"Warning: Reference image not found: {path}")
                            continue
                    
                    # Create image for reference
                    reference_images.append({
                        "image": self._image_to_base64(image_path),
                        "weight": min(1.0, 0.5 + score / 2)  # Convert score to a weight between 0.5 and 1.0
                    })
                except Exception as e:
                    print(f"Error processing reference image {path}: {str(e)}")
        
        # Step 5: Generate new image with DALL-E
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",  # Using DALL-E 3 for better quality
                prompt=prompt,
                size=size,
                quality="hd",
                n=1,
            )
            
            # Step 6: Return the results
            return response.data[0].url
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return str(e)
    
    def analyze_map_style(self, image_path: str) -> List[str]:
        """
        Analyze the style elements of a given map.
        
        Args:
            image_path (str): Path to the image to analyze
            
        Returns:
            List[str]: List of style elements detected
        """
        # This could be implemented using vision models to detect styles
        # For now we'll return based on metadata
        metadata = self.get_metadata(image_path)
        features = metadata.get("features", [])
        
        # Add some basic style analysis
        styles = []
        if "back side trails" in features:
            styles.append("back side orientation")
        if "front side trails" in features:
            styles.append("front side orientation")
        if "expert terrain" in features:
            styles.append("expert terrain focus")
        if "lake views" in features:
            styles.append("scenic lake views")
        
        # Default styles if none detected
        if not styles:
            styles = ["standard ski map layout", "color-coded trails", "mountain topography"]
            
        return styles


if __name__ == "__main__":
    # Example usage
    rag = MapRAG()
    result = rag.generate_enhanced_map(
        query="Generate a ski trail map with steep descents and alpine terrain for expert skiers",
        difficulty_level="expert"
    )
    print("\nGenerated map URL:", result["generated_image_url"])
    print("\nPrompt used:", result["prompt"])
