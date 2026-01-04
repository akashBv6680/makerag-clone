# MakeRAG - Complete Project Setup Guide

## Project Overview

MakeRAG is a comprehensive RAG (Retrieval-Augmented Generation) platform that combines:
- **Vector Search** - Using embeddings for semantic search
- **Knowledge Graph** - Graph-based retrieval for relationships
- **AI Chat** - LLM-powered conversational interface
- **Document Management** - Upload, process, and search documents
- **Hybrid Search** - Combines vector + knowledge graph results

## Architecture

### Frontend Stack
- React 18+ with TypeScript
- Vite for fast builds
- TailwindCSS for styling
- Zustand for state management
- React Query for data fetching
- Socket.io for real-time chat

### Backend Stack
- FastAPI (Python)
- PostgreSQL/MongoDB for storage
- Pinecone/Weaviate for vector DB
- Neo4j for knowledge graphs
- LangChain for LLM integration
- Celery for async tasks

## Installation & Setup

### Prerequisites
```bash
Node.js >= 16
Python >= 3.9
Docker & Docker Compose
Git
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Key Features

### 1. Authentication
- Email/Password login
- OAuth2 (Google, GitHub)
- JWT tokens
- Refresh token rotation

### 2. Document Management
- Upload PDFs, TXT, DOCX
- Automatic chunking
- Metadata extraction
- Vector embedding generation

### 3. Search Capabilities
- Semantic vector search
- Full-text search
- Metadata filtering
- Hybrid ranking

### 4. Chat Interface
- Real-time WebSocket chat
- Context-aware responses
- Citation tracking
- Conversation history

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  name VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Documents Table
```sql
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  title VARCHAR(255),
  content TEXT,
  metadata JSONB,
  embedding VECTOR(1536),
  created_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Conversations Table
```sql
CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  title VARCHAR(255),
  created_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Environment Configuration

### .env.example
```
# API Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/makerag
NEO4J_URI=bolt://localhost:7687
NEO4J_AUTH=neo4j:password

# Vector DB
PINCONE_API_KEY=your_key
PINCONE_ENVIRONMENT=production
PINCONE_INDEX_NAME=makerag

# LLM Configuration
OPENAI_API_KEY=your_key
COHERE_API_KEY=your_key

# Security
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Refresh token

### Documents
- `GET /api/documents` - List documents
- `POST /api/documents` - Upload document
- `DELETE /api/documents/{id}` - Delete document
- `GET /api/documents/{id}/search` - Search in document

### Chat
- `POST /api/chat/conversations` - Create conversation
- `POST /api/chat/conversations/{id}/messages` - Send message
- `GET /api/chat/conversations/{id}/messages` - Get chat history
- `WebSocket /ws/chat/{conversation_id}` - Real-time chat

### Search
- `POST /api/search` - Hybrid search
- `POST /api/search/vector` - Vector search only
- `POST /api/search/text` - Text search only

## Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Render Deployment
1. Connect GitHub repo
2. Set environment variables
3. Configure build command
4. Deploy

### GitHub Pages
- Frontend deployed on GitHub Pages
- API on Render/Heroku/AWS

## Performance Optimization

- Vector indexing with FAISS
- Query caching with Redis
- Async processing with Celery
- Database connection pooling
- CDN for static assets

## Security Best Practices

- JWT token validation
- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention
- HTTPS only

## Testing

```bash
# Frontend tests
npm run test

# Backend tests
pytest tests/

# E2E tests
npm run test:e2e
```

## Contributing

See CONTRIBUTING.md for guidelines

## License

MIT License
