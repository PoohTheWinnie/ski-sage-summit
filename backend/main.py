from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from encyclopedia_rag import EncyclopediaRAG
from map_rag import MapRAG
import uvicorn
from typing import Optional

app = FastAPI()

# Add CORS middleware with production URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ski-sage-summit.vercel.app",  # Production
        "http://localhost:3000"  # Development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG manager
encyclopedia_rag = EncyclopediaRAG()
map_rag = MapRAG()
class ChatRequest(BaseModel):
    message: str
    modelType: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Handle chat requests using RAG system"""
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        if request.modelType == "encyclopedia":
            response = encyclopedia_rag.generate_response(request.message)
        elif request.modelType == "map":
            response = map_rag.generate_enhanced_map(request.message)
        else:
            raise HTTPException(status_code=400, detail="Invalid model type")
        
        # Validate response
        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate response")
            
        print(response)
        
        return {
            "response": response,
            "status": "success"
        }
        
    except Exception as e:
        # Log the full error
        print(f"Error processing request: {str(e)}")
        
        # Return a proper error response
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred processing your request: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)