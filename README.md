# Break The Code

> **Break The Code. Crack The Interview.**  
> *Learn. Practice. Get Interview-Ready.*

Break The Code is an enterprise-grade AI-powered technical interview preparation platform designed for modern software engineers. It covers **AI/GenAI**, **Java/Backend**, **Python**, **DSA**, and **System Design** with multi-level interview depth (L1 Definition to L5 Production Scenario), real-time **Think Mode**, **Progressive Hints**, and **LangGraph-driven Answer Evaluation**.

---

## 🌟 Key Features

- **Dynamic Technology Tracks**: Dynamic database-backed taxonomy across AI/GenAI (LangGraph, Hybrid RAG, LoRA, Vector DBs), Java/Backend (JVM internals, Concurrency, Spring Boot), Python, DSA, and System Design.
- **Deep Interview Question DNA**: Every question provides short answers, interview-ready answers, deep architectural explanations, code examples, common pitfalls, and interviewer intent.
- **Think Mode with Timer**: Simulate real-time interview pressure with live timer and draft submission.
- **3-Level Progressive Hints**: Conceptual, Implementation, and Architecture hints.
- **AI Answer Evaluation**: Multi-rubric scoring (Correctness, Completeness, Depth, Clarity) and covered vs. missed points breakdown.
- **Admin CMS & Quality Engine**: Full question lifecycle (`DRAFT -> REVIEW -> PUBLISHED`), immutable version snapshots, and review queues.
- **Search & Filter Engine**: Fast faceted filtering and hybrid search.

---

## 🛠️ Tech Stack

- **Frontend**: Next.js 15+ (App Router, Server Components), React 19, TypeScript, Tailwind CSS, Lucide React.
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2.
- **Database & Cache**: PostgreSQL 16 + pgvector, Redis, SQLite fallback for rapid zero-dependency local runs.
- **AI Orchestration**: LangGraph, LangChain, multi-provider LLM abstraction.

---

## 🚀 Getting Started

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python ../scripts/seed_database.py
uvicorn app.main:app --reload --port 8000
```
API Documentation will be accessible at: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Web application will be accessible at: `http://localhost:3000`

### 3. Docker Compose (Full Stack)
```bash
docker-compose up --build
```
