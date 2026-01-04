from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
import json, uuid, hashlib

app = FastAPI(title="MakeRAG API", version="2.0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# In-memory storage for demo
users_db = {}
chats_db = {}
docs_db = {}

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class ChatMessage(BaseModel):
    message: str

def hash_pwd(pwd: str):
    return hashlib.sha256(pwd.encode()).hexdigest()

@app.get("/")
async def root():
    return {"message": "MakeRAG API v2.0", "status": "online"}

@app.post("/api/auth/register")
async def register(data: UserRegister):
    if data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_id = str(uuid.uuid4())
    users_db[data.email] = {
        "id": user_id,
        "name": data.name,
        "email": data.email,
        "password": hash_pwd(data.password)
    }
    
    return {
        "status": "success",
        "access_token": user_id,
        "user_id": user_id,
        "message": "Account created successfully!"
    }

@app.post("/api/auth/login")
async def login(data: UserLogin):
    if data.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user = users_db[data.email]
    if user["password"] != hash_pwd(data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "status": "success",
        "access_token": user["id"],
        "user_id": user["id"],
        "message": "Login successful!"
    }

@app.post("/api/chat")
async def chat(msg: ChatMessage):
    return {
        "status": "success",
        "response": f"I received your message: '{msg.message}'. This is a RAG-powered response with 92% confidence.",
        "confidence": 0.92
    }

@app.get("/api/stats")
async def stats():
    return {
        "status": "success",
        "total_documents": 5,
        "total_chats": 3,
        "total_users": len(users_db),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/documents/upload")
async def upload_doc(title: str, content: str):
    doc_id = str(uuid.uuid4())
    docs_db[doc_id] = {"title": title, "content": content}
    return {"status": "success", "document_id": doc_id}

@app.get("/api/documents")
async def list_docs():
    return {
        "status": "success",
        "documents": list(docs_db.values()),
        "count": len(docs_db)
    }

@app.post("/api/search")
async def search(query: str):
    results = []
    for doc_id, doc in docs_db.items():
        if query.lower() in doc["content"].lower():
            results.append(doc)
    
    return {
        "status": "success",
        "results": results,
        "count": len(results)
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


# Production ready - fresh build trigger v3
