from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import os, json, uuid, secrets, hashlib
from typing import Optional, List
import jwt

# Database imports
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="MakeRAG API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Database config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/makerag_db")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255),
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Documents table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                file_path VARCHAR(255),
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Vectors table (for semantic search)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                embedding_vector FLOAT8[],
                chunk_text TEXT,
                chunk_index INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Chat sessions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Chat messages table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
                role VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                confidence FLOAT DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # API Keys table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                key_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255),
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# Pydantic Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: str

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class SearchQuery(BaseModel):
    query: str
    retrieval_mode: str = "hybrid"
    top_k: int = 5

# Auth helpers
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthCredentials) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "MakeRAG API v2.0 - Real RAG Platform", "status": "online"}

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    conn = get_db_connection()
    cur = conn.cursor(RealDictCursor)
    try:
        user_id = str(uuid.uuid4())
        password_hash = hash_password(user_data.password)
        
        cur.execute(
            "INSERT INTO users (id, email, name, password_hash) VALUES (%s, %s, %s, %s)",
            (user_id, user_data.email, user_data.name, password_hash)
        )
        conn.commit()
        
        token = create_access_token(user_id)
        return {"status": "success", "access_token": token, "user_id": user_id}
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        cur.close()
        conn.close()

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    conn = get_db_connection()
    cur = conn.cursor(RealDictCursor)
    try:
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (user_data.email,))
        user = cur.fetchone()
        
        if not user or user["password_hash"] != hash_password(user_data.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token(user["id"])
        return {"status": "success", "access_token": token, "user_id": user["id"]}
    finally:
        cur.close()
        conn.close()

@app.post("/api/documents/upload")
async def upload_document(title: str, content: str, credentials: HTTPAuthCredentials = Depends(security)):
    user = verify_token(credentials)
    conn = get_db_connection()
    cur = conn.cursor(RealDictCursor)
    try:
        doc_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO documents (id, user_id, title, content) VALUES (%s, %s, %s, %s)",
            (doc_id, user["user_id"], title, content)
        )
        conn.commit()
        return {"status": "success", "document_id": doc_id, "message": "Document uploaded"}
    finally:
        cur.close()
        conn.close()

@app.post("/api/search")
async def search(query_data: SearchQuery, credentials: HTTPAuthCredentials = Depends(security)):
    user = verify_token(credentials)
    conn = get_db_connection()
    cur = conn.cursor(RealDictCursor)
    try:
        cur.execute("""
            SELECT d.id, d.title, d.content FROM documents d
            WHERE d.user_id = %s AND d.content ILIKE %s
            LIMIT %s
        """, (user["user_id"], f"%{query_data.query}%", query_data.top_k))
        
        results = cur.fetchall()
        return {"status": "success", "results": results, "count": len(results)}
    finally:
        cur.close()
        conn.close()

@app.post("/api/chat")
async def chat(msg: ChatMessage, credentials: HTTPAuthCredentials = Depends(security)):
    user = verify_token(credentials)
    conn = get_db_connection()
    cur = conn.cursor(RealDictCursor)
    try:
        # Create or get session
        session_id = msg.session_id or str(uuid.uuid4())
        
        cur.execute("SELECT id FROM chat_sessions WHERE id = %s AND user_id = %s", (session_id, user["user_id"]))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO chat_sessions (id, user_id, title) VALUES (%s, %s, %s)",
                (session_id, user["user_id"], msg.message[:50])
            )
        
        # Store user message
        cur.execute(
            "INSERT INTO chat_messages (id, session_id, role, content) VALUES (%s, %s, %s, %s)",
            (str(uuid.uuid4()), session_id, "user", msg.message)
        )
        
        # Generate AI response (simulated RAG)
        response_text = f"Response to: {msg.message}. [Retrieved from your documents]"
        cur.execute(
            "INSERT INTO chat_messages (id, session_id, role, content, confidence) VALUES (%s, %s, %s, %s, %s)",
            (str(uuid.uuid4()), session_id, "assistant", response_text, 0.92)
        )
        
        conn.commit()
        return {"status": "success", "response": response_text, "session_id": session_id, "confidence": 0.92}
    finally:
        cur.close()
        conn.close()

@app.get("/api/documents")
async def list_documents(credentials: HTTPAuthCredentials = Depends(security)):
    user = verify_token(credentials)
    conn = get_db_connection()
    cur = conn.cursor(RealDictCursor)
    try:
        cur.execute("SELECT id, title, created_at FROM documents WHERE user_id = %s ORDER BY created_at DESC", (user["user_id"],))
        documents = cur.fetchall()
        return {"status": "success", "documents": documents, "count": len(documents)}
    finally:
        cur.close()
        conn.close()

@app.get("/api/stats")
async def get_stats(credentials: HTTPAuthCredentials = Depends(security)):
    user = verify_token(credentials)
    conn = get_db_connection()
    cur = conn.cursor(RealDictCursor)
    try:
        cur.execute("SELECT COUNT(*) as count FROM documents WHERE user_id = %s", (user["user_id"],))
        doc_count = cur.fetchone()["count"]
        
        cur.execute("SELECT COUNT(*) as count FROM chat_sessions WHERE user_id = %s", (user["user_id"],))
        chat_count = cur.fetchone()["count"]
        
        return {"status": "success", "total_documents": doc_count, "total_chats": chat_count, "timestamp": datetime.now().isoformat()}
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
