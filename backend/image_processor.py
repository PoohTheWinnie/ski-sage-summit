from PIL import Image
import io
from typing import List
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ImageProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def process_image(self, image_path: str) -> str:
        """Process image and return embeddings using OpenAI's API"""
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this ski mountain map. Describe the trails, lifts, and key features in detail."
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content 