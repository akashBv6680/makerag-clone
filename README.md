# MakeRAG Clone - Comprehensive RAG Platform

A production-ready RAG (Retrieval-Augmented Generation) platform with hybrid search combining vector embeddings (FAISS) and knowledge graphs (Neo4j), AI-powered chat, document ingestion, and complete REST API.

## Features

### Core Features
- **Hybrid Search**: Combines vector search (semantic similarity) + graph search (entity relationships)
- **Multi-format Document Ingestion**: Supports PDF, DOCX, XLSX, TXT, MD files
- **AI Chat**: RAG-based conversational interface with source citations
- **Knowledge Graph**: Neo4j integration for entity and relationship extraction
- **Vector Database**: FAISS for efficient semantic search
- **REST API**: Complete API for all platform functionality
- **API Key Management**: Secure project-based API keys
- **Chatbot Embed**: Embedableshtml code for website integration
- **Configurable Search**: Adjustable top-k results, temperature, retrieval modes

### Technical Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **Graph DB**: Neo4j
- **LLM**: OpenAI GPT-3.5/GPT-4
- **Embeddings**: OpenAI Embeddings / HuggingFace Models
- **File Processing**: PyPDF2, python-docx, openpyxl
- **Deployment**: GitHub Pages (Frontend) + Railway/Render (Backend)

## Project Structure

```
makerag-clone/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration settings
│   │   ├── database.py             # Database connections
│   │   ├── dependencies.py         # Dependency injection
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── projects.py        # Project management
│   │   │   ├── documents.py       # Document upload/ingestion
│   │   │   ├── retrieval.py       # Search endpoints (vector/graph/hybrid)
│   │   │   ├── chat.py            # Chat endpoints
│   │   │   ├── settings.py        # Settings endpoints
│   │   │   └── health.py          # Health check
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py         # Pydantic models
│   │   │   ├── database.py        # SQLAlchemy models
│   │   │   └── rag.py             # RAG-specific models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py    # JWT auth, user management
│   │   │   ├── project_service.py # Project operations
│   │   │   ├── document_service.py# Document processing
│   │   │   ├── embedding_service.py# Embeddings generation
│   │   │   ├── vector_service.py  # FAISS operations
│   │   │   ├── graph_service.py   # Neo4j operations
│   │   │   ├── retrieval_service.py# Hybrid search
│   │   │   ├── chat_service.py    # LLM chat operations
│   │   │   └── file_service.py    # File parsing
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── security.py        # Password hashing, JWT
│   │   │   ├── logger.py          # Logging setup
│   │   │   └── validators.py      # Data validation
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── cors.py            # CORS configuration
│   │       └── error_handler.py   # Global error handling
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_documents.py
│   │   ├── test_retrieval.py
│   │   └── test_chat.py
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example               # Environment variables
│   ├── Dockerfile                 # Container setup
│   └── wsgi.py                    # WSGI entry point
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── index.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Navbar.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── Upload/
│   │   │   │   ├── UploadDocument.tsx
│   │   │   │   ├── FileUploader.tsx
│   │   │   │   └── UploadProgress.tsx
│   │   │   ├── Search/
│   │   │   │   ├── DocumentSearch.tsx
│   │   │   │   ├── SearchResults.tsx
│   │   │   │   └── SearchFilters.tsx
│   │   │   ├── Chat/
│   │   │   │   ├── AIChatInterface.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   ├── ChatInput.tsx
│   │   │   │   └── SourceCitations.tsx
│   │   │   ├── Chatbot/
│   │   │   │   ├── ChatbotEmbed.tsx
│   │   │   │   ├── ChatbotPreview.tsx
│   │   │   │   └── EmbedCodeGenerator.tsx
│   │   │   ├── APIKeys/
│   │   │   │   ├── APIKeysList.tsx
│   │   │   │   ├── CreateAPIKey.tsx
│   │   │   │   └── KeyManagement.tsx
│   │   │   ├── Settings/
│   │   │   │   ├── SearchSettings.tsx
│   │   │   │   ├── ModelSettings.tsx
│   │   │   │   └── ProjectSettings.tsx
│   │   │   └── Auth/
│   │   │       ├── Login.tsx
│   │   │       ├── Register.tsx
│   │   │       └── ProtectedRoute.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Upload.tsx
│   │   │   ├── Search.tsx
│   │   │   ├── Chat.tsx
│   │   │   ├── Chatbot.tsx
│   │   │   ├── APIKeys.tsx
│   │   │   ├── Settings.tsx
│   │   │   ├── Login.tsx
│   │   │   └── Register.tsx
│   │   ├── services/
│   │   │   ├── api.ts            # API client
│   │   │   ├── auth.ts           # Auth service
│   │   │   ├── storage.ts        # Local storage
│   │   │   └── formatters.ts     # Data formatting
│   │   ├── hooks/
│   │   │   ├── useAuth.ts        # Auth hook
│   │   │   ├── useAPI.ts         # API hook
│   │   │   ├── useLocalStorage.ts
│   │   │   └── useToast.ts       # Toast notifications
│   │   ├── types/
│   │   │   ├── index.ts          # Type definitions
│   │   │   ├── api.ts
│   │   │   └── rag.ts
│   │   ├── context/
│   │   │   ├── AuthContext.tsx
│   │   │   ├── AppContext.tsx
│   │   │   └── ProjectContext.tsx
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   ├── variables.css
│   │   │   └── animations.css
│   │   └── utils/
│   │       ├── constants.ts
│   │       ├── helpers.ts
│   │       └── validators.ts
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
├── .github/
│   └── workflows/
│       ├── backend-deploy.yml     # Backend CI/CD
│       ├── frontend-deploy.yml    # Frontend CI/CD
│       └── tests.yml              # Test pipeline
├── docs/
│   ├── API.md                     # API documentation
│   ├── ARCHITECTURE.md            # Architecture overview
│   ├── SETUP.md                   # Setup guide
│   └── DEPLOYMENT.md              # Deployment guide
├── docker-compose.yml             # Multi-container setup
├── .gitignore
├── LICENSE
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+ & npm/yarn
- Neo4j (local or cloud)
- OpenAI API key
- PostgreSQL (for user management)

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yourusername/makerag-clone.git
cd makerag-clone/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with API endpoint

# Start development server
npm start
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login & get token
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/logout` - Logout

### Projects
- `GET /projects` - List user projects
- `POST /projects` - Create new project
- `GET /projects/{project_id}` - Get project details
- `PUT /projects/{project_id}` - Update project
- `DELETE /projects/{project_id}` - Delete project

### Documents
- `POST /ingest` - Ingest text document
- `POST /ingest/file` - Upload and ingest file
- `GET /documents` - List documents
- `GET /ingest/status/{job_id}` - Check ingestion status
- `DELETE /documents/{doc_id}` - Delete document

### Retrieval (Search)
- `POST /retrieve/vector` - Vector search only
- `POST /retrieve/graph` - Graph search only
- `POST /retrieve/hybrid` - Hybrid search (recommended)

### Chat
- `POST /chat` - Chat with RAG
- `GET /chat/history` - Get chat history
- `DELETE /chat/{chat_id}` - Delete chat

### Settings
- `GET /settings` - Get search settings
- `PUT /settings` - Update search settings
- `GET /health` - Health check

### API Keys
- `GET /api-keys` - List API keys
- `POST /api-keys` - Create new key
- `DELETE /api-keys/{key_id}` - Revoke key

## Database Schema

### PostgreSQL
- Users table
- Projects table
- Documents table
- Chat history table
- API keys table

### Neo4j
- Entity nodes
- Relationship edges
- Document references

### FAISS
- Vector index for document chunks

## Deployment

### Deploy Backend to Railway/Render

```bash
# Set environment variables on platform
# Deploy using git push
git push origin main
```

### Deploy Frontend to GitHub Pages/Vercel

```bash
cd frontend
npm run build
npm run deploy
```

## Performance Optimizations

1. **Vector Search**: FAISS with GPU acceleration
2. **Batch Processing**: Async document processing
3. **Caching**: Redis for frequent queries
4. **Indexing**: Neo4j graph indexing
5. **Pagination**: Limit results per query
6. **Async Operations**: FastAPI async/await

## Security

- JWT token-based auth
- Password hashing with bcrypt
- Rate limiting
- CORS configuration
- Input validation
- SQL injection prevention
- XSS protection

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
