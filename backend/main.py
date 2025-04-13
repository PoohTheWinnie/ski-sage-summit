from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_manager import RAGManager
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG manager
rag_manager = RAGManager()

class ChatRequest(BaseModel):
    message: str
    modelType: str  # Keeping this for backward compatibility

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Handle chat requests using RAG system"""
    print('request', request)
    try:
        # Using RAG system regardless of model type
        response = rag_manager.generate_response(request.message)
        print('response', response)
        return {"response": response}
    except Exception as e:
        print(f"Error processing request: {e}")
        return {"error": "An error occurred processing your request"}

if __name__ == "__main__":
    # First-time setup
    uvicorn.run(app, host="0.0.0.0", port=8000)