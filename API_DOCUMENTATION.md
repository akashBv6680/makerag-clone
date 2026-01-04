# MakeRAG API Documentation

## Base URL
```
Production: https://api.makerag.ai
Development: http://localhost:8000
```

## Authentication
All endpoints (except login/signup) require Bearer token in Authorization header:
```
Authorization: Bearer {access_token}
```

---

## Authentication Endpoints

### POST /api/auth/register
Register a new user account
```json
Request:
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}

Response (201):
{
  "id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-04T21:00:00Z"
}
```

### POST /api/auth/login
Login with email and password
```json
Request:
{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### POST /api/auth/refresh
Refresh access token
```json
Request:
{
  "refresh_token": "eyJhbGc..."
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

## Document Endpoints

### POST /api/documents
Upload a document
```
Request: multipart/form-data
- file: binary file
- title: string (optional)
- description: string (optional)

Response (201):
{
  "id": "doc_123",
  "title": "My Document",
  "status": "processing",
  "size": 1024000,
  "created_at": "2024-01-04T21:00:00Z"
}
```

### GET /api/documents
List all user documents
```json
Query Parameters:
- skip: integer (default: 0)
- limit: integer (default: 10)
- sort: string (created_at, name)

Response (200):
{
  "total": 25,
  "items": [
    {
      "id": "doc_123",
      "title": "My Document",
      "size": 1024000,
      "status": "completed",
      "created_at": "2024-01-04T21:00:00Z"
    }
  ]
}
```

### GET /api/documents/{id}
Get document details
```json
Response (200):
{
  "id": "doc_123",
  "title": "My Document",
  "content_preview": "Document content excerpt...",
  "chunks_count": 15,
  "embeddings_count": 15,
  "metadata": {}
}
```

### DELETE /api/documents/{id}
Delete a document
```
Response (204): No Content
```

---

## Search Endpoints

### POST /api/search
Hybrid search (vector + knowledge graph)
```json
Request:
{
  "query": "How to implement RAG?",
  "document_ids": ["doc_123", "doc_456"],
  "top_k": 5,
  "threshold": 0.3
}

Response (200):
{
  "results": [
    {
      "id": "chunk_123",
      "document_id": "doc_123",
      "content": "RAG implementation steps...",
      "score": 0.92,
      "metadata": {}
    }
  ],
  "total": 5
}
```

### POST /api/search/vector
Vector search only
```json
Request:
{
  "query": "Search query",
  "top_k": 5,
  "filter": {}
}

Response: Same as hybrid search
```

---

## Chat Endpoints

### POST /api/chat/conversations
Create new conversation
```json
Request:
{
  "title": "My Conversation",
  "document_ids": ["doc_123"]
}

Response (201):
{
  "id": "conv_123",
  "title": "My Conversation",
  "created_at": "2024-01-04T21:00:00Z"
}
```

### POST /api/chat/conversations/{id}/messages
Send message in conversation
```json
Request:
{
  "content": "What is RAG?",
  "include_sources": true
}

Response (201):
{
  "id": "msg_123",
  "role": "user",
  "content": "What is RAG?",
  "created_at": "2024-01-04T21:00:00Z"
}
```

### GET /api/chat/conversations/{id}/messages
Get conversation messages
```json
Response (200):
{
  "messages": [
    {
      "id": "msg_123",
      "role": "user",
      "content": "Question",
      "created_at": "2024-01-04T21:00:00Z"
    },
    {
      "id": "msg_124",
      "role": "assistant",
      "content": "Answer with sources...",
      "sources": [{"id": "chunk_123", "score": 0.92}],
      "created_at": "2024-01-04T21:01:00Z"
    }
  ]
}
```

---

## WebSocket Endpoints

### WS /ws/chat/{conversation_id}
Real-time chat connection

**Message Format (Send):**
```json
{
  "type": "message",
  "content": "Your message here"
}
```

**Message Format (Receive):**
```json
{
  "type": "message",
  "content": "Response from assistant",
  "sources": []
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters",
  "errors": [
    {"field": "email", "message": "Invalid email format"}
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "request_id": "uuid"
}
```

---

## Rate Limiting
- 100 requests per minute for authenticated users
- 10 requests per minute for public endpoints
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Pagination
Use `skip` and `limit` query parameters for paginated responses
