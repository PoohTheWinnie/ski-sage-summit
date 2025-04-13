import os
import time
from openai import OpenAI
from typing import Optional, List, Tuple
from dotenv import load_dotenv
from .image_rag import TrailMapRAG

load_dotenv()

class ImageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ImageGenerator with OpenAI API key and RAG system.
        """
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.rag = TrailMapRAG()

    def generate_trail_map(self, 
                          difficulty_level: str = "intermediate",
                          terrain_features: str = "",
                          model: str = "dall-e-2",
                          size: str = "512x512",
                          num_reference_maps: int = 3) -> tuple[str, float, List[str]]:
        """
        Generate a ski trail map using DALL-E with RAG enhancement.
        
        Args:
            difficulty_level (str): Skill level (beginner, intermediate, advanced)
            terrain_features (str): Additional terrain details
            model (str): "dall-e-2" (cheaper) or "dall-e-3" (higher quality)
            size (str): Image size
            num_reference_maps (int): Number of reference maps to retrieve
            
        Returns:
            tuple[str, float, List[str]]: Tuple containing (image URL, execution time, reference maps used)
        """
        start_time = time.time()

        # Validate parameters
        valid_sizes = {
            "dall-e-2": ["256x256", "512x512", "1024x1024"],
            "dall-e-3": ["1024x1024", "1792x1024"]
        }
        
        if model not in ["dall-e-2", "dall-e-3"]:
            model = "dall-e-2"
        
        if size not in valid_sizes[model]:
            size = "512x512" if model == "dall-e-2" else "1024x1024"

        # Construct query for RAG
        rag_query = f"ski trail map with {difficulty_level} difficulty"
        if terrain_features:
            rag_query += f" featuring {terrain_features}"
        
        # Get similar maps from RAG system
        similar_maps = self.rag.query(rag_query, k=num_reference_maps)
        reference_maps = [path for path, _ in similar_maps]
        
        # Extract relevant features from similar maps
        features = []
        for map_path in reference_maps:
            metadata = self.rag.get_metadata(map_path)
            features.extend(metadata.get("features", []))
        
        # Construct enhanced prompt using RAG results
        prompt = f"Create a ski trail map with {difficulty_level} level trails"
        if terrain_features:
            prompt += f", including {terrain_features}"
        if features:
            unique_features = list(set(features))
            prompt += f". Reference features: {', '.join(unique_features)}"
        prompt += ". Style: Clean, professional ski resort map with clear trail markers and lifts."

        try:
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            execution_time = time.time() - start_time
            return response.data[0].url, execution_time, reference_maps
        
        except Exception as e:
            execution_time = time.time() - start_time
            raise Exception(f"Failed to generate image (took {execution_time:.2f}s): {str(e)}")

# Example usage
if __name__ == "__main__":
    generator = ImageGenerator()
    
    try:
        image_url, runtime, reference_maps = generator.generate_trail_map(
            difficulty_level="intermediate",
            terrain_features="terrain park, tree skiing",
            model="dall-e-2",
            size="512x512"
        )
        print(f"Generated image URL: {image_url}")
        print(f"Generation time: {runtime:.2f} seconds")
        print("Reference maps used:")
        for ref_map in reference_maps:
            print(f"- {ref_map}")
    except Exception as e:
        print(f"Error: {str(e)}")
