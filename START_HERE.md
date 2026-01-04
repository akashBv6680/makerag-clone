# 🚀 MakeRAG Platform - Quick Start Guide

## Welcome to MakeRAG!

A comprehensive Retrieval-Augmented Generation (RAG) platform with hybrid search capabilities, AI chat, and document management. Built with modern tech stack for production deployments.

---

## ⚡ Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/akashBv6680/makerag-clone.git
cd makerag-clone
```

### 2. Setup with Docker (Recommended)
```bash
# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Swagger UI: http://localhost:8000/docs
```

### 3. Manual Setup (Alternative)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements_enhanced.txt
python app/main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```
makerag-clone/
├── frontend/              # React + Vite frontend
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
├── docs/                 # Documentation
├── docker-compose.yml    # Docker orchestration
├── .env.example          # Environment template
├── API_DOCUMENTATION.md  # Complete API reference
├── COMPLETE_PROJECT_SETUP.md
└── README.md
```

---

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and update:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/makerag_db

# LLM API Keys
OPENAI_API_KEY=sk-...
COHERE_API_KEY=...

# Vector Database
PINCONE_API_KEY=...
```

See `.env.example` for complete configuration options.

---

## 📚 Documentation

| Document | Purpose |
|----------|----------|
| **API_DOCUMENTATION.md** | Complete REST API reference |
| **COMPLETE_PROJECT_SETUP.md** | Full setup guide & architecture |
| **docker-compose.yml** | Docker services configuration |
| **.env.example** | Environment variable template |

---

## 🎯 Key Features

✅ **Vector Search** - Semantic search using embeddings  
✅ **Knowledge Graph** - Relationship-based retrieval  
✅ **Hybrid Search** - Combined vector + graph results  
✅ **AI Chat** - LLM-powered conversations  
✅ **Document Upload** - PDF, DOCX, TXT support  
✅ **Real-time Chat** - WebSocket-based messaging  
✅ **OAuth Authentication** - Google & GitHub login  
✅ **Production Ready** - Docker, Kubernetes-compatible  

---

## 🌐 Live Deployment

**Frontend:** https://akashbv6680.github.io/makerag-clone/  
**API:** Deploy to Render/Heroku using `docker-compose.yml`

---

## 📖 API Quick Reference

### Authentication
```bash
# Login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password"
}

# Returns: { "access_token": "...", "token_type": "bearer" }
```

### Document Upload
```bash
POST /api/documents
Content-Type: multipart/form-data
Authorization: Bearer {token}
File: document.pdf
```

### Search
```bash
POST /api/search
Authorization: Bearer {token}
{
  "query": "Your search query",
  "top_k": 5
}
```

### Chat
```bash
WS /ws/chat/{conversation_id}
# Send: { "type": "message", "content": "Hello" }
# Receive: { "type": "message", "content": "Response", "sources": [...] }
```

See **API_DOCUMENTATION.md** for complete endpoints.

---

## 🚀 Deployment Options

### Option 1: GitHub Pages + Render
1. Frontend deployed on GitHub Pages (free)
2. Backend on Render free tier or Heroku
3. Database: PostgreSQL (Render or Neon)

### Option 2: Docker on Cloud
```bash
# Deploy with: AWS ECS, Google Cloud Run, Azure Container Instances
docker build -f backend/Dockerfile -t makerag:latest .
docker push your-registry/makerag:latest
```

### Option 3: Kubernetes
```bash
kubectl apply -f kubernetes/deployment.yaml
```

---

## 🔐 Security

- ✅ JWT token-based authentication
- ✅ CORS properly configured
- ✅ Rate limiting enabled
- ✅ Password hashing with bcrypt
- ✅ Secure environment variables
- ✅ HTTPS recommended for production

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📞 Support & Resources

- **GitHub Issues:** Report bugs and request features
- **Documentation:** See `/docs` folder
- **API Docs:** Visit `/docs` endpoint when backend running
- **Community:** Discussions & Q&A in GitHub Discussions

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎉 Next Steps

1. ✅ Clone and setup (see Quick Start above)
2. ✅ Configure `.env` with API keys
3. ✅ Start services with Docker Compose
4. ✅ Visit http://localhost:3000 for frontend
5. ✅ Check http://localhost:8000/docs for API
6. ✅ Read API_DOCUMENTATION.md for full reference
7. ✅ Deploy to production!

---

**Happy building! 🚀**
