from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import json

app = FastAPI(title="MakeRAG API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
documents_db = {}
chat_history = []

@app.get("/")
async def root():
    return {"message": "MakeRAG Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/documents/upload")
async def upload_document():
    return {"status": "success", "message": "Document uploaded"}

@app.get("/api/documents")
async def list_documents():
    return {"documents": list(documents_db.values()), "count": len(documents_db)}

@app.post("/api/search")
async def search_documents(query: dict):
    search_query = query.get("query", "")
    return {"query": search_query, "results": [], "total_results": 0}

@app.post("/api/chat")
async def chat(message: dict):
    user_message = message.get("message", "")
    ai_response = f"Response to: {user_message}"
    return {"user_message": user_message, "ai_response": ai_response}

@app.get("/api/stats")
async def get_stats():
    return {"total_documents": len(documents_db), "total_chats": len(chat_history)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
