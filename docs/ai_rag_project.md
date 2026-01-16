# 🧠 AI-Assisted Knowledge Base Search + Chat (RAG + FastAPI + vLLM)

## 📌 Overview

This project provides an **AI-assisted document search and chat experience** using:

- **Retrieval-Augmented Generation (RAG)**
- **FastAPI backend**
- **Postgres + pgvector for semantic search**
- **vLLM for GPU-accelerated inference**
- **Token + latency analytics**

### 🎯 Real-World Use Cases

| Industry | Example Use |
|---|---|
| SaaS | Chatbot over API documentation |
| Enterprise | Search internal policies & knowledge bases |
| Finance | Compliance document Q&A |
| Legal | Contract summarization |
| Education | Chat with textbooks or lecture notes |

This mirrors modern platforms like **OpenAI RAG**, **LangChain RetrievalQA**, **LlamaIndex**, etc.

## 🏗️ High-Level Architecture

```
              ┌────────────────────────────────┐
              │           FastAPI API          │
              │  - File Upload                 │
              │  - Chat Sessions               │
              │  - RAG Search                  │
              │  - Analytics                   │
              └───────────┬────────────────────┘
                          │
                          ↓
                 ┌────────────────┐
                 │  Postgres DB   │
                 │ + pgvector     │
                 │ documents/chunks
                 │ embeddings      │
                 └───────┬────────┘
                         │
 embeddings              │ query vectors
                         ↓
              ┌──────────────────────┐
              │       Embeddings     │
              │ (local HF or OpenAI) │
              └───────────┬─────────┘
                          │ context
                          ↓
              ┌──────────────────────┐
              │         vLLM         │
              │ OpenAI-compatible API│
              └──────────────────────┘
```

## ✨ Key Features

- Document upload (PDF, TXT, Markdown)
- Automatic text extraction & chunking
- Semantic vector search with pgvector
- RAG-enhanced chat with citations
- Latency & token usage analytics
- Multi-turn conversation history
- Extendable: OCR, Auth, S3, UI frontend

## 🧩 Core Components

1. **FastAPI Backend**
2. **vLLM for LLM inference**
3. **Embedding Model** (BGE / E5 / nomic / OpenAI)
4. **Postgres + pgvector**
5. **pytest test suite**
6. **Docker Compose for deployment**

## 🗄️ Database Schema (pgvector)

### Entity Overview

```
Document ──< Chunk ──< ChatMessage
                     ↑
                  ChatSession
```

### Tables

#### `documents`

| Column | Type | Description |
|---|---|---|
| id | uuid (PK) | unique id |
| title | text | file name/title |
| file_type | text | pdf/txt/md |
| created_at | timestamp | upload time |

#### `chunks`

| Column | Type | Description |
|---|---|---|
| id | uuid (PK) |
| document_id | uuid (FK) |
| text | text |
| embedding | vector | pgvector |
| created_at | timestamp |

#### `chat_sessions`

| Column | Type |
|---|---|
| id | uuid (PK) |
| user_id | uuid / null |
| created_at | timestamp |

#### `chat_messages`

| Column | Type | Description |
|---|---|---|
| id | uuid (PK) |
| chat_id | uuid (FK) |
| role | enum(user, assistant) |
| content | text |
| created_at | timestamp |

#### `query_analytics`

| Column | Type |
|---|---|
| id | uuid |
| query | text |
| latency_ms | float |
| tokens_input | int |
| tokens_output | int |
| model_version | text |
| created_at | timestamp |

## 📦 API Endpoints

### 📁 Document Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/documents/upload` | Upload PDF/txt/md |
| GET | `/documents` | List documents |
| GET | `/documents/{id}` | Get document metadata |
| DELETE | `/documents/{id}` | Delete document |

### 🔍 Search (RAG)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/search` | Vector-based semantic retrieval |

Request:
```json
{ "query": "What is zero-knowledge proof?" }
```

Response:
```json
{ "results": [ { "text": "...", "score": 0.82, "document_id": "abc" } ] }
```

### 💬 Chat

| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat` | Create chat session |
| POST | `/chat/{chat_id}/message` | Chat with RAG context |
| GET | `/chat/{chat_id}` | Get full chat history |

### 📊 Analytics

| Method | Endpoint |
|---|---|
| GET | `/analytics/usage` |
| GET | `/analytics/recent-queries` |
| GET | `/analytics/models` |

## 🧠 RAG Workflow

1. User submits question.
2. Embed query.
3. Query pgvector via cosine similarity.
4. Build context prompt.
5. Call vLLM.
6. Store analytics & messages.

## 🐋 Docker Compose Configuration

```yaml
services:
  web:
    build: ./app
    depends_on:
      - db
      - vllm
    environment:
      - DATABASE_URL=postgresql://postgres:example@db:5432/postgres
      - VLLM_URL=http://vllm:8000/v1
    ports:
      - "8000:8000"

  vllm:
    image: vllm/vllm-openai:latest
    command: >
      --model Qwen/Qwen2.5-1.5B-Instruct
      --gpu-memory-utilization 0.7
    expose:
      - "8000"

  db:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=example
      - POSTGRES_DB=postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## 🔧 Embeddings

Recommended models:

| Model | Strength |
|---|---|
| BAAI/bge-small-en | Fast + good quality |
| intfloat/e5-base | Balanced |
| nomic-embed-text-v1 | OSS high-quality |
| OpenAI text-embedding-3-small | Strong but external |

Example:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-small-en")
vec = model.encode("hello world")
```

## 🤖 vLLM Integration

```python
import os, time
from openai import OpenAI

client = OpenAI(base_url=os.getenv("VLLM_URL", "http://vllm:8000/v1"), api_key="none")

def llm_chat(prompt, model):
    start = time.perf_counter()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    latency = (time.perf_counter() - start) * 1000
    return resp.choices[0].message.content, resp.usage, latency
```

## 🧪 Testing Strategy

### Unit Tests
- Chunking
- PDF extraction
- Embedding mock
- Ranking

### Integration Tests
- `/documents/upload`
- `/search`
- `/chat/{id}/message`

### Tools
- pytest
- httpx / TestClient
- pytest-mock

## 🏁 Roadmap

1. Backend skeleton
2. Document pipeline
3. RAG search
4. Chat integration
5. Analytics layer
6. Testing suite

## 🧩 Folder Structure

```
app/
  main.py
  api/
    routes/
      documents.py
      search.py
      chat.py
      analytics.py
  db/
    base.py
    session.py
    models/
  services/
    embeddings.py
    rag.py
    llm.py
    pdf.py
    chunking.py
  tests/
    unit/
    integration/
  core/
    config.py
    logging.py
```

## 📜 Deployment Notes

- Runs via Docker Compose
- Requires GPU for vLLM
- Works on RunPod/Vast.ai/Modal/AWS

---
