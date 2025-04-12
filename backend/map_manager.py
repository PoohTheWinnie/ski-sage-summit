from typing import Dict
import os
from anthropic import Anthropic
from openai import OpenAI
import base64
from dotenv import load_dotenv
from .data.config import SKI_MAPS

load_dotenv()

class MapManager:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.maps_data = {}
        self.initialize_maps()

    def initialize_maps(self):
        """Initialize map data by processing all maps once"""
        for resort_id, info in SKI_MAPS.items():
            with open(info['path'], "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Get initial analysis of the map
                response = self.openai.chat.completions.create(
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
                
                self.maps_data[resort_id] = {
                    "base64_image": base64_image,
                    "analysis": response.choices[0].message.content,
                    "metadata": info['metadata']
                }

    async def query_and_generate(self, query: str) -> str:
        """Query about maps and generate a response"""
        # Combine all map analyses
        all_analyses = "\n\n".join([
            f"Analysis of {data['metadata']['resort_name']}:\n{data['analysis']}"
            for data in self.maps_data.values()
        ])

        prompt = f"""You are a ski resort expert. Use the following analyses of ski resort maps to answer the question.
        
Available Maps and Analyses:
{all_analyses}

Question: {query}

Please provide a detailed response about the ski resorts and their features. If the question is about a specific resort,
focus on that resort's information. If comparing resorts or asking about general features, include relevant information
from multiple resorts."""

        response = self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text 