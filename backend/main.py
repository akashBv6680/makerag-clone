from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import logging
from typing import List, Optional
import json
from datetime import datetime
import aiofiles
import shutil
from pathlib import Path

# Import our custom modules
from config import settings
from models import ChatMessage, Document, SearchQuery
from rag_engine import RAGEngine
from database import init_db, get_db

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MakeRAG Clone API",
    description="AI-powered RAG platform with document management and chat",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = RAGEngine()

# Initialize database
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up MakeRAG Clone API")
    init_db()
    await rag_engine.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down MakeRAG Clone API")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "MakeRAG Clone API", "timestamp": datetime.now().isoformat()}

# Document management endpoints
@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Upload a document for RAG processing
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file type
        allowed_types = [".pdf", ".txt", ".docx", ".md"]
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_types:
            raise HTTPException(status_code=400, detail=f"File type {file_ext} not allowed")
        
        # Save file
        file_path = await save_uploaded_file(file)
        
        # Process document in background
        if background_tasks:
            background_tasks.add_task(rag_engine.process_document, file_path, file.filename)
        
        return {
            "status": "success",
            "message": "Document uploaded and queued for processing",
            "filename": file.filename,
            "file_path": str(file_path)
        }
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
async def list_documents():
    """
    List all uploaded documents
    """
    try:
        documents = await rag_engine.get_documents_list()
        return {"status": "success", "documents": documents}
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str):
    """
    Delete a document and its embeddings
    """
    try:
        await rag_engine.delete_document(doc_id)
        return {"status": "success", "message": f"Document {doc_id} deleted"}
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoints
@app.post("/api/chat")
async def chat(message: ChatMessage):
    """
    Process a chat message with RAG context
    """
    try:
        if not message.content or len(message.content.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message content cannot be empty")
        
        # Get RAG context and generate response
        response = await rag_engine.process_query(message.content)
        
        return {
            "status": "success",
            "message": response["answer"],
            "sources": response["sources"],
            "confidence": response["confidence"]
        }
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search(query: SearchQuery):
    """
    Search documents using RAG
    """
    try:
        if not query.query or len(query.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        results = await rag_engine.search_documents(query.query, top_k=query.top_k)
        
        return {
            "status": "success",
            "query": query.query,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoints
@app.get("/api/stats")
async def get_stats():
    """
    Get platform statistics
    """
    try:
        stats = await rag_engine.get_stats()
        return {"status": "success", "stats": stats}
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper function
async def save_uploaded_file(file: UploadFile) -> Path:
    """
    Save uploaded file to disk
    """
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / file.filename
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return file_path

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
