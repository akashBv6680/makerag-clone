from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Import routers
from app.routers import auth, projects, documents, retrieval, chat, settings, health

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("MakeRAG Backend Starting...")
    yield
    # Shutdown
    print("MakeRAG Backend Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="MakeRAG API",
    description="Retrieval-Augmented Generation Platform with Hybrid Search",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(retrieval.router, prefix="/api/retrieve", tags=["Retrieval"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(health.router, prefix="/api", tags=["Health"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "MakeRAG API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "makerag-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )
