from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
import json
from fastapi.responses import StreamingResponse
from .map_manager import MapManager
from .encyclopedia_manager import EncyclopediaManager

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
map_manager = MapManager()
encyclopedia_manager = EncyclopediaManager()

class ChatRequest(BaseModel):
    message: str
    modelType: str

async def stream_response(message: str):
    """Stream the response word by word with slower speed"""
    words = message.split()
    for word in words:
        # Increased delay to 0.15 seconds between words
        await asyncio.sleep(0.15)  # Increased from 0.05 to 0.15
        
        # Add punctuation-based delays for more natural rhythm
        if word.endswith(('.', '!', '?')):
            await asyncio.sleep(0.3)  # Longer pause after sentences
        elif word.endswith((',', ';', ':')):
            await asyncio.sleep(0.2)  # Medium pause after clauses
            
        yield f"data: {json.dumps(word)}\n\n"
    
    # Add final delay before DONE signal
    await asyncio.sleep(0.3)
    yield "data: [DONE]\n\n"

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Handle chat requests with appropriate manager"""
    try:
        if request.modelType == 'map':
            response = await map_manager.query_and_generate(request.message)
        else:  # encyclopedia mode
            response = await encyclopedia_manager.query_and_generate(request.message)
        
        return StreamingResponse(
            stream_response(response),
            media_type="text/event-stream",
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'text/event-stream',
            }
        )
    except Exception as e:
        print(f"Error processing request: {e}")
        return {"error": "An error occurred processing your request"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)