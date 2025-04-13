from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_manager import RAGManager
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
rag_manager = RAGManager()

class ChatRequest(BaseModel):
    message: str
    modelType: Optional[str] = None  # Make modelType optional with default None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Handle chat requests using RAG system"""
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    try:
        # Log incoming request
        print(f"Processing chat request: {request.message[:100]}...")  # Log first 100 chars
        
        # Using RAG system regardless of model type
        response = rag_manager.generate_response(request.message)
        
        # Validate response
        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate response")
            
        # Log success
        print(f"Successfully generated response: {response[:100]}...")  # Log first 100 chars
        
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

# Add a health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}