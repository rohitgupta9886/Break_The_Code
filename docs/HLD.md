# High-Level Design (HLD)
## Break The Code — System Architecture

---

## 1. System Context & Top-Level Architecture

Break The Code utilizes a decoupled, high-performance monorepo architecture with a Next.js (React 19, TypeScript, Tailwind CSS) frontend and a Python (FastAPI, SQLAlchemy 2.0, Pydantic v2) backend. Persistent state resides in PostgreSQL (with pgvector), high-speed caching and rate-limiting in Redis, and asynchronous workflows in LangGraph.

```mermaid
graph TD
    Client[Web & Mobile Clients]
    CDN[Cloudflare / CDN Edge]
    Frontend[Next.js App Server]
    API_GW[FastAPI Application Gateway]
    
    subgraph Core Services
        AuthSvc[Auth & RBAC Service]
        QuestionSvc[Question & CMS Service]
        SearchSvc[Hybrid Search Service]
        ProgressSvc[Progress & Analytics Service]
        InterviewSvc[Interview & AI Service]
        AdminSvc[Admin & Quality Service]
    end
    
    subgraph Storage & Intelligence Layer
        PG[(PostgreSQL + pgvector)]
        R[(Redis Cache & Rate Limit)]
        LangGraphEng[LangGraph Workflow Engine]
        LLM[LLM Provider Abstraction]
        Storage[Object Storage / S3 / Local]
    end

    Client -->|HTTPS| CDN
    CDN -->|SSR / Assets| Frontend
    Frontend -->|REST API / JSON| API_GW
    API_GW --> AuthSvc
    API_GW --> QuestionSvc
    API_GW --> SearchSvc
    API_GW --> ProgressSvc
    API_GW --> InterviewSvc
    API_GW --> AdminSvc

    QuestionSvc --> PG
    QuestionSvc --> R
    SearchSvc --> PG
    SearchSvc --> R
    ProgressSvc --> PG
    ProgressSvc --> R
    InterviewSvc --> LangGraphEng
    LangGraphEng --> LLM
    LangGraphEng --> PG
    InterviewSvc --> PG
```

---

## 2. Component Breakdown

### 2.1 Frontend Tier (Next.js 15+ App Router)
- **Rendering Strategy**:
  - Static Generation & ISR for high-volume SEO pages (`/`, `/questions/[slug]`, `/learn/[technology]`).
  - Client-Side Rendering with TanStack Query for authenticated, dynamic interaction surfaces (`/dashboard`, `/interview/session/[id]`, `/admin/*`).
- **Design System**: Centralized token architecture in Tailwind CSS with semantic tokens for dark and light modes, typography scales, glass effects, and micro-animations.

### 2.2 API & Business Logic Tier (FastAPI)
- Clean four-layer architecture:
  `Router -> Service -> Repository -> Database / Cache`
- Strict dependency injection for database sessions, caching clients, current user auth, and LLM instances.
- Zero business logic inside router handlers.

### 2.3 AI & Agentic Tier (LangGraph + LangSmith)
- State machine graphs manage interview setup, question routing, response ingestion, multi-rubric evaluation, follow-up generation, and final report generation.
- LLM Provider Abstraction layer (`LLMProviderBase -> OpenAIProvider, AnthropicProvider, GeminiProvider, LocalProvider`) completely decouples business logic from vendors.

### 2.4 Data Tier
- **PostgreSQL 16**: Relational source of truth for users, questions, versions, reviews, bookmarks, and attempts.
- **pgvector**: Cosine similarity indexing over question embeddings for semantic search and question recommendation.
- **Redis 7**: Session tokens, sliding-window rate limit counters, hot question cache, and real-time interview state.
- **Object Storage**: S3-compatible or secure local filesystem storage for resumes and diagrams.

---

## 3. High-Level Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor Candidate
    participant NextJS as Frontend (Next.js)
    participant API as FastAPI Backend
    participant QService as Question Service
    participant AIService as AI & LangGraph Service
    participant DB as PostgreSQL + pgvector
    participant Redis as Redis Cache

    Candidate->>NextJS: Opens Question /questions/langgraph-checkpointing
    NextJS->>API: GET /api/v1/questions/langgraph-checkpointing
    API->>Redis: Check cache for slug
    alt Cache Hit
        Redis-->>API: Return cached question data
    else Cache Miss
        API->>QService: Get question by slug
        QService->>DB: Query question with joins (hints, tags, sources)
        DB-->>QService: Entity record
        QService->>Redis: Cache question (TTL: 1 hour)
    end
    API-->>NextJS: Question Payload (JSON)
    NextJS-->>Candidate: Render Question Page (Think Mode Ready)

    Candidate->>NextJS: Clicks "Think", types answer, clicks "Submit Answer"
    NextJS->>API: POST /api/v1/ai/evaluate-answer
    API->>AIService: Evaluate(question_id, candidate_answer)
    AIService->>AIService: Run LangGraph Evaluator Node
    AIService-->>API: Evaluation (Scores, Covered, Missed, Improved Answer)
    API->>DB: Record user attempt & accuracy
    API-->>NextJS: Evaluation Results
    NextJS-->>Candidate: Displays Scorecard, Diff Checklist, and Improved Answer
```
