# ⚡ Break The Code

> **Break The Code. Crack The Interview.**  
> *The Production-Grade Technical Interview Preparation Platform for Modern Software Engineers.*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15+-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org)
[![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Question DNA (15-Part Anatomy)](#-question-dna-15-part-anatomy)
- [The 8 Difficulty Tiers](#-the-8-difficulty-tiers)
- [AI Engine (Google Gemini Integration)](#-ai-engine-google-gemini-integration)
- [Admin Governance CMS & Question Lifecycle](#-admin-governance-cms--question-lifecycle)
- [Tech Stack](#-tech-stack)
- [Quick Start Guide](#-quick-start-guide)
  - [Prerequisites](#prerequisites)
  - [1. Backend Setup](#1-backend-setup)
  - [2. Frontend Setup](#2-frontend-setup)
- [Demo Credentials](#-demo-credentials)
- [API Endpoints Reference](#-api-endpoints-reference)
- [Project Directory Structure](#-project-directory-structure)
- [Contributing & License](#-contributing--license)

---

## 🚀 Overview

**Break The Code** is an open-source, full-stack platform built to bridge the gap between basic coding puzzles and **real-world production engineering interviews**.

Traditional platforms focus solely on algorithm puzzles. **Break The Code** provides deep technical interviews across **GenAI / LangGraph**, **Backend & Concurrency (Java/Python)**, **Distributed Systems**, **System Design**, and **DSA** — complete with interactive **Think Mode**, live **Google Gemini-powered Answer Evaluation**, progressive **Socratic Hints**, and an **Admin CMS** for content lifecycle governance.

---

## ✨ Key Features

1. **Production-Grade Curriculum**: Over 1,500 curated questions across LangGraph, Hybrid RAG, System Design, Concurrency, and Core Languages.
2. **Interactive Think Mode**: Recreates real interview pressure with countdown timers, candidate response scratchpads, and live AI evaluation.
3. **Progressive Socratic Hints**: 3-tier scaffolding (Conceptual $\rightarrow$ Implementation $\rightarrow$ Architectural) that guides candidates without revealing answers.
4. **Multi-Rubric AI Evaluation**: Powered by Google Gemini (`gemini-2.5-flash`), analyzing candidate submissions for *Technical Correctness*, *Completeness*, *Architectural Depth*, and *Communication Clarity*.
5. **8 Public Difficulty Tiers**: Systematic ladder spanning Freshers (L1) to Principal & Distinguished Architects (L8).
6. **Full Admin Governance CMS**: Comprehensive CRUD operations (Create, Read/Inspect, Update, Delete, and Status Transitions) with version history and cascade protection.
7. **Reading Mode**: Fast, distraction-free technical guide view with client-side tier filtering and in-memory TTL caching.
8. **Dark Mode & Cyber Aesthetics**: Polished UI with Tailwind CSS, Lucide icons, and modern responsive layouts.

---

## 🧬 Question DNA (15-Part Anatomy)

Every question in Break The Code is authored according to a strict 15-part blueprint:

| Component | Purpose |
|---|---|
| **1. Direct Short Answer** | 1–2 sentence elevator pitch for high-signal responses |
| **2. Interview-Ready Answer** | Full verbal blueprint structured for the candidate to speak aloud |
| **3. Core Mechanics** | Under-the-hood execution runtime and internal state flows |
| **4. Deep Technical Explanation** | Comprehensive technical deep dive with architectural trade-offs |
| **5. Practical Code Example** | Executable, idiomatic Python/TypeScript/Java implementation |
| **6. Architecture Notes** | Data flows, thread safety, state machines, and failovers |
| **7. Interviewer Intent** | Why interviewers ask this and what technical signals they evaluate |
| **8. Production Considerations** | Real-world telemetry, latency budgets, and connection pools |
| **9. Failure Modes** | Cascade failures, split-brain scenarios, and error recovery |
| **10. Common Mistakes** | Frequent candidate anti-patterns and pitfalls |
| **11–13. Socratic Hints (L1–L3)** | Progressive clues to unlock mental blockers |
| **14. Source Provenance** | Documentation attribution and licensing provenance |
| **15. Follow-Up Questions** | Follow-up prompts interviewers ask to test candidate depth |

---

## 🏔️ The 8 Difficulty Tiers

| Level | Code | Name | Target Experience | Focus Area |
|---|---|---|---|---|
| **1** | `BASIC` | **Basic** | 0–2 Years / Freshers | Fundamentals & syntax mechanics |
| **2** | `MEDIUM` | **Medium** | 3–5 Years / Mid-level | Memory management & practical design patterns |
| **3** | `HARD` | **Hard** | 5+ Years / Senior | Concurrency, lock-free structures & race conditions |
| **4** | `TOUGH` | **Tough** | Staff / Tech Lead | Query optimization, bottlenecks & zero-copy pipelines |
| **5** | `VERY_TOUGH` | **Very Tough** | Principal Engineer | Distributed partitions, consensus & fault injection |
| **6** | `VERY_VERY_TOUGH`| **Very Very Tough** | Domain Specialist | Formal state machines, Raft, linearizability |
| **7** | `PRODUCTION_SCENARIO`| **Production Scenario**| Staff SRE / Architect | SEV-1 outage mitigation & live failover |
| **8** | `EXPERT_DEEP_DIVE`| **Expert Deep Dive**| Distinguished Architect | Custom memory bypass, kernel limits & bytecode |

---

## 🤖 AI Engine (Google Gemini Integration)

The application integrates natively with the **Google Gemini API** (`gemini-2.5-flash` with automatic fallback to `gemini-1.5-flash`):

- **Think Mode Socratic Coach**: Generates dynamic hints calibrated to candidate answers without spoiling the solution.
- **Automated Answer Evaluation**: Evaluates open-ended verbal answers across 4 rubrics with positive reinforcement, critical gaps, and production insights.
- **Follow-Up Generator**: Proactively generates follow-up questions tailored to candidate answers.

```
Candidate Answer ───► Gemini Evaluation Engine ───► Correctness Score (0–100%)
                              │                   ├── Key Points Covered
                              │                   ├── Critical Gaps Missed
                              ▼                   └── Follow-Up Question
                     Socratic Coach (Hints)
```

---

## 🛡️ Admin Governance CMS & Question Lifecycle

The CMS at `/admin/questions` enables platform administrators to govern the technical curriculum:

- **Full CRUD Operations**:
  - **Create**: Author questions manually or import via JSON.
  - **Read / Inspect**: Deep modal view inspecting all 15 components of the question DNA.
  - **Update**: 4-tab modal editor (Core & Taxonomy, Answers, Architecture & Code, Hints & Sources).
  - **Delete**: Cascade deletion removing associated attempts, bookmarks, and version snapshots.
- **Gated Lifecycle Workflow**:
  ```
  DRAFT ──► AI_REVIEW ──► TECHNICAL_REVIEW ──► APPROVED ──► PUBLISHED
                                                                │
                                                                ▼
                                                            ARCHIVED
  ```
- **Real-Time Coverage Matrix**: Validates curriculum compliance (minimum 20 questions per section across tiers).

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [Next.js 15](https://nextjs.org/) (App Router, Server & Client Components)
- **Language**: TypeScript 5.0+
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) with dark/cyber styling
- **Icons**: [Lucide React](https://lucide.dev/)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Async ASGI)
- **Language**: Python 3.12+
- **Database ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async Engine)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Database**: SQLite (default local) / PostgreSQL 16 compatible

### AI & LLM
- **Provider**: Google Gemini API (`gemini-2.5-flash`, `gemini-1.5-flash`)
- **Transport**: Async HTTPX client with retries, exponential backoff, and JSON repair

---

## 🏁 Quick Start Guide

### Prerequisites
- **Python**: 3.11+ or 3.12+
- **Node.js**: 18+ or 20+ (with `npm`)
- **Git**
- *(Optional)* **Google Gemini API Key**: Get a free key at [Google AI Studio](https://aistudio.google.com/)

---

### 1. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in `backend/.env` (or copy from `.env.example`):
   ```ini
   DATABASE_URL=sqlite+aiosqlite:///./breakthecode.db
   SECRET_KEY=production-grade-super-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

5. **Seed the database**:
   ```bash
   python ../scripts/seed_database.py
   ```

6. **Start the FastAPI backend server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   - API Docs (Swagger UI): **[http://localhost:8000/docs](http://localhost:8000/docs)**
   - API Redoc: **[http://localhost:8000/redoc](http://localhost:8000/redoc)**

---

### 2. Frontend Setup

1. **Open a new terminal and navigate to `frontend`**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create `frontend/.env.local`:
   ```ini
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

4. **Start the Next.js development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser**:
   Visit **[http://localhost:3000](http://localhost:3000)**

---

## 🔑 Demo Credentials

| Role | Email | Password | Privileges |
|---|---|---|---|
| **Administrator** | `admin@breakthecode.dev` | `AdminPass123!` | Full CMS, Question CRUD, User Management, Matrix Governance |
| **Candidate** | `candidate@breakthecode.dev` | `CandidatePass123!` | Public Practice, Think Mode, Bookmarks, Revision |

*Tip: You can also use the one-click **"Demo Admin Login"** button on the `/login` page.*

---

## 🔌 API Endpoints Reference

### Questions & Reading Mode
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/questions` | Public questions list with filters |
| `GET` | `/api/v1/questions/{slug}` | Full question detail by slug |
| `GET` | `/api/v1/questions/reading-mode/{technology}` | Reading mode list grouped by 8 tiers |
| `GET` | `/api/v1/questions/stats` | Question count statistics by tier and track |

### AI & Evaluation (Gemini)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/ai/evaluate` | Evaluates candidate answer with multi-rubric scoring |
| `POST` | `/api/v1/ai/socratic-hint` | Returns incremental hints based on draft answer |

### Admin Governance CMS
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/questions` | Filtered question list for admin governance |
| `GET` | `/api/v1/admin/questions/{id}` | Question detail for admin inspection |
| `POST` | `/api/v1/admin/questions` | Create a new question |
| `PUT` | `/api/v1/admin/questions/{id}` | Update question metadata and 15-part DNA |
| `PATCH` | `/api/v1/admin/questions/{id}/status` | Single-click status transition (`DRAFT` to `PUBLISHED`) |
| `DELETE` | `/api/v1/admin/questions/{id}` | Permanently delete question with cascade safety |
| `GET` | `/api/v1/admin/content/matrix` | Coverage Matrix validation (30 questions/tier) |
| `GET` | `/api/v1/admin/users` | List platform users |

---

## 📂 Project Directory Structure

```text
BreakTheCode/
├── backend/
│   ├── app/
│   │   ├── api/v1/             # Endpoints (questions, admin, ai, auth, users)
│   │   ├── core/               # Database, security & configuration
│   │   ├── models/             # SQLAlchemy ORM models (Question, User, Taxonomy)
│   │   ├── repositories/       # Data-access layer with eager-loading & cascade logic
│   │   ├── schemas/            # Pydantic v2 validation schemas
│   │   └── services/           # Business logic (ai_service, question_service)
│   └── requirements.txt        # Python backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── admin/questions # Admin Question Lifecycle & CRUD CMS
│   │   │   ├── dashboard/      # User analytics, history & bookmarks
│   │   │   ├── questions/      # Question exploration & Think Mode
│   │   │   └── page.tsx        # Modern landing page & difficulty explorer
│   │   ├── components/         # Reusable UI components & badges
│   │   ├── lib/                # API client, auth context & utilities
│   │   └── styles/             # Global Tailwind stylesheets
│   └── package.json            # Node.js dependencies
│
├── docs/                       # Technical specifications (PRD, TRD, HLD, LLD)
├── scripts/                    # Database seeding and curriculum engines
├── docker-compose.yml          # Containerized deployment manifest
└── README.md                   # Project documentation
```

---

## 🤝 Contributing & License

Contributions, feature suggestions, and curriculum additions are welcome! Please check out [`docs/CONTENT_GUIDELINES.md`](file:///c:/Users/Priyanka%20Gupta/Q/Desktop/17GEN_AI/Projects/Production_grade/BreakTheCode/docs/CONTENT_GUIDELINES.md) for standards on authoring 15-part Question DNA.

This project is licensed under the [MIT License](LICENSE).
