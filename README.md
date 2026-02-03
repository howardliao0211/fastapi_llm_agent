# 🚀 fastapi_llm_agent

A full-stack **LLM agent platform** built with **FastAPI** and **React**, designed for building, experimenting with, and deploying **LLM-powered agents** using a modern, production-ready architecture.

This project integrates a FastAPI backend, a React + Tailwind frontend, secure JWT authentication, database migrations, and **vLLM** for high-performance local or self-hosted LLM inference.

---

### Backend

* **FastAPI** – High-performance async REST API
* **SQLAlchemy** – ORM for database interaction
* **Alembic** – Database migrations & schema versioning
* **JWT (JSON Web Tokens)** – Authentication & authorization
* **vLLM** – High-throughput LLM inference engine (OpenAI-compatible API)

### Frontend

* **React** – Component-based UI framework
* **Tailwind CSS** – Utility-first styling for rapid UI development

### Infrastructure & Tooling

* **Docker & Docker Compose** – Containerized development & deployment
* **Pipenv** – Python dependency management
* **pytest** – Backend testing framework

---

## 🧱 Project Overview

**fastapi_llm_agent** provides:

* 🔥 A FastAPI backend for LLM-powered agent APIs
* 🧠 Integration with **vLLM** for local or self-hosted large models
* 🔐 Secure authentication using JWT
* 🗄️ Persistent storage with SQLAlchemy + Alembic
* 🌐 A modern React + Tailwind chat UI
* 🐳 Dockerized full-stack setup for local development
* 🧪 Testing infrastructure for backend services

---

## 📁 Repository Structure

```
fastapi_llm_agent/
├── backend/                # FastAPI backend & agent logic
│   └── alembic/            # Alembic migration files
│   ├── apis/               # API routers
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── core/               # Auth, config, security
│   ├── db/                 # Database session & migrations
│   └── main.py             # FastAPI entrypoint
│
├── frontend/               # React + Tailwind frontend
│
├── docker-compose.yaml     # Multi-service stack
├── Dockerfile              # Backend image
├── .env.example            # Environment variables template
├── Pipfile                 # Python dependencies
├── Pipfile.lock
├── pytest.ini              # Test configuration
└── .github/                # CI / workflows
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/howardliao0211/fastapi_llm_agent.git
cd fastapi_llm_agent
```

---

### 2. Install Dependencies

```bash
pipenv install
pipenv shell
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and configure:

---

## 4. Database Migrations (Alembic)

Apply migrations:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "migration message"
```

---

### 5. Run Docker

```bash
docker compose up --build
```
Open in browser:

```
http://localhost:3000
```

---

## 🧠 vLLM Integration

This project is designed to work with **vLLM** as an OpenAI-compatible inference server.
The backend communicates with vLLM using the OpenAI-compatible API interface.

---

## 🐳 Docker (Recommended)

Run the full stack using Docker Compose:

```bash
docker-compose up --build
```

This starts:

* FastAPI backend
* React frontend
* Database
* vLLM service (if configured)

---

## 🧪 Testing

Run backend tests:

```bash
pipenv run pytest
```

---

## 📌 Key Features

* ✅ JWT-based authentication
* ✅ Database-backed users, chats, and messages
* ✅ LLM agent abstraction layer
* ✅ OpenAI-compatible inference via vLLM
* ✅ Modern chat UI with React + Tailwind
* ✅ Fully dockerized workflow
* ✅ Production-ready backend architecture

---

## 🛠 Future Improvements

* Retrieval-Augmented Generation (RAG)
* Multi-agent orchestration
* LangChain integration
---

## 📜 License

MIT License

---

If you find this project useful, feel free to ⭐ the repository or open an issue with suggestions or improvements.
