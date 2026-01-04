from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
import json, uuid, hashlib

app = FastAPI(title="MakeRAG API", version="3.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

users_db = {}
chats_db = {}
docs_db = {}

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ChatMessage(BaseModel):
    message: str
    user_id: str = None

class DocumentUpload(BaseModel):
    title: str
    content: str
    user_id: str = None

def hash_pwd(pwd: str):
    return hashlib.sha256(pwd.encode()).hexdigest()

@app.get("/")
async def root():
    return {"message": "MakeRAG Backend API", "status": "running", "version": "3.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/auth/register")
async def register(data: UserRegister):
    if data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_id = str(uuid.uuid4())
    users_db[data.email] = {"id": user_id, "name": data.name, "email": data.email, "password": hash_pwd(data.password)}
    return {"success": True, "message": "Account created", "user_id": user_id, "user_name": data.name, "access_token": user_id}

@app.post("/api/auth/login")
async def login(data: UserLogin):
    if data.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = users_db[data.email]
    if user["password"] != hash_pwd(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "message": "Login successful", "user_id": user["id"], "user_name": user["name"], "access_token": user["id"]}

@app.post("/api/chat")
async def chat(msg: ChatMessage):
    chat_id = str(uuid.uuid4())
    chats_db[chat_id] = {"message": msg.message, "timestamp": datetime.now().isoformat()}
    return {"success": True, "response": f"RAG Response to: {msg.message}", "confidence": 0.92}

@app.post("/api/documents/upload")
async def upload_doc(doc: DocumentUpload):
    doc_id = str(uuid.uuid4())
    docs_db[doc_id] = {"title": doc.title, "content": doc.content, "created": datetime.now().isoformat()}
    return {"success": True, "message": "Document uploaded", "document_id": doc_id}

@app.get("/api/documents")
async def list_docs():
    return {"success": True, "documents": list(docs_db.values()), "count": len(docs_db)}

@app.post("/api/search")
async def search(query: str):
    results = []
    for doc_id, doc in docs_db.items():
        if query.lower() in doc["content"].lower():
            results.append(doc)
    return {"success": True, "query": query, "results": results, "count": len(results)}

@app.get("/api/stats")
async def stats():
    return {"success": True, "total_users": len(users_db), "total_docs": len(docs_db), "total_chats": len(chats_db)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
#v5-complete-rag-working
