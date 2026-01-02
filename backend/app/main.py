from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import json
import uuid
from typing import List, Optional
import hashlib

app = FastAPI(title="MakeRAG API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
documents_db = {}
chat_sessions = {}
projects_db = {
    "demo_project_1": {
        "id": "demo_project_1",
        "name": "DEMO APP",
        "created_at": datetime.now().isoformat(),
        "documents": 0,
        "vectors": 0
    }
}
api_keys_db = {}
settings_db = {
    "retrieval_mode": "hybrid",
    "top_k": 5,
    "temperature": 0.7
}

@app.get("/")
async def root():
    return {"message": "MakeRAG Backend API", "status": "running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/projects/create")
async def create_project(data: dict):
    project_id = str(uuid.uuid4())
    projects_db[project_id] = {
        "id": project_id,
        "name": data.get("name", "Untitled Project"),
        "created_at": datetime.now().isoformat(),
        "documents": 0,
        "vectors": 0
    }
    return {"status": "success", "project_id": project_id, "project": projects_db[project_id]}

@app.get("/api/projects")
async def list_projects():
    return {"projects": list(projects_db.values()), "count": len(projects_db)}

@app.post("/api/documents/upload")
async def upload_document(project_id: str = "demo_project_1", file: UploadFile = File(...)):
    try:
        doc_id = str(uuid.uuid4())
        content = await file.read()
        
        documents_db[doc_id] = {
            "id": doc_id,
            "project_id": project_id,
            "filename": file.filename,
            "size": len(content),
            "content_type": file.content_type,
            "created_at": datetime.now().isoformat(),
            "chunks": 5,
            "vectors": 10
        }
        
        if project_id in projects_db:
            projects_db[project_id]["documents"] += 1
            projects_db[project_id]["vectors"] += 10
        
        return {
            "status": "success",
            "message": f"Document {file.filename} uploaded successfully",
            "document_id": doc_id,
            "document": documents_db[doc_id]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/documents/paste")
async def paste_document(data: dict):
    try:
        doc_id = str(uuid.uuid4())
        text_content = data.get("text", "")
        project_id = data.get("project_id", "demo_project_1")
        
        documents_db[doc_id] = {
            "id": doc_id,
            "project_id": project_id,
            "filename": f"pasted_text_{doc_id[:8]}.txt",
            "size": len(text_content),
            "content_type": "text/plain",
            "content": text_content,
            "created_at": datetime.now().isoformat(),
            "chunks": max(1, len(text_content) // 500),
            "vectors": max(5, len(text_content) // 100)
        }
        
        if project_id in projects_db:
            projects_db[project_id]["documents"] += 1
            projects_db[project_id]["vectors"] += documents_db[doc_id]["vectors"]
        
        return {
            "status": "success",
            "message": "Text pasted and ingested successfully",
            "document_id": doc_id,
            "document": documents_db[doc_id]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/documents")
async def list_documents(project_id: str = None):
    if project_id:
        docs = [doc for doc in documents_db.values() if doc.get("project_id") == project_id]
    else:
        docs = list(documents_db.values())
    return {"documents": docs, "count": len(docs)}

@app.post("/api/search")
async def search_documents(query_data: dict):
    search_query = query_data.get("query", "")
    retrieval_mode = query_data.get("retrieval_mode", settings_db["retrieval_mode"])
    top_k = query_data.get("top_k", settings_db["top_k"])
    
    mock_results = [
        {
            "id": f"result_{i}",
            "document_id": list(documents_db.keys())[0] if documents_db else "doc_1",
            "content": f"Relevant chunk {i+1} matching '{search_query}'",
            "score": 0.95 - (i * 0.1),
            "retrieval_type": retrieval_mode,
            "metadata": {"chunk_id": i, "source": "document"}
        }
        for i in range(min(top_k, 3))
    ]
    
    return {
        "query": search_query,
        "retrieval_mode": retrieval_mode,
        "results": mock_results,
        "total_results": len(mock_results),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat")
async def chat(message_data: dict):
    user_message = message_data.get("message", "")
    project_id = message_data.get("project_id", "demo_project_1")
    session_id = message_data.get("session_id", str(uuid.uuid4()))
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {"id": session_id, "messages": [], "created_at": datetime.now().isoformat()}
    
    ai_response = f"Based on your documents: I found relevant information about '{user_message}'. "
    ai_response += "This is a response powered by RAG (Retrieval-Augmented Generation). "
    ai_response += "Sources: Document 1 (95% match), Document 2 (87% match)."
    
    chat_sessions[session_id]["messages"].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    chat_sessions[session_id]["messages"].append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "user_message": user_message,
        "ai_response": ai_response,
        "session_id": session_id,
        "sources": ["Document 1", "Document 2"],
        "confidence": 0.91,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/chat/{session_id}")
async def get_chat_history(session_id: str):
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"session_id": session_id, "messages": chat_sessions[session_id]["messages"]}

@app.post("/api/settings")
async def update_settings(settings_data: dict):
    global settings_db
    settings_db.update(settings_data)
    return {"status": "success", "settings": settings_db}

@app.get("/api/settings")
async def get_settings():
    return {"settings": settings_db}

@app.post("/api/keys/create")
async def create_api_key(data: dict):
    key_name = data.get("name", "API Key")
    key_id = str(uuid.uuid4())
    api_key = f"mk_{hashlib.sha256(key_id.encode()).hexdigest()[:32]}"
    
    api_keys_db[key_id] = {
        "id": key_id,
        "name": key_name,
        "key": api_key,
        "created_at": datetime.now().isoformat(),
        "last_used": None,
        "status": "active"
    }
    
    return {
        "status": "success",
        "key_id": key_id,
        "api_key": api_key,
        "message": "Store this key securely. It won't be shown again."
    }

@app.get("/api/keys")
async def list_api_keys():
    keys = [{"id": k["id"], "name": k["name"], "created_at": k["created_at"], "last_used": k["last_used"], "status": k["status"]} for k in api_keys_db.values()]
    return {"keys": keys, "count": len(keys)}

@app.get("/api/stats")
async def get_stats():
    return {
        "total_projects": len(projects_db),
        "total_documents": len(documents_db),
        "total_chats": len(chat_sessions),
        "total_vectors": sum(d.get("vectors", 0) for d in documents_db.values()),
        "api_keys": len(api_keys_db),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
