# Technical Requirements Document (TRD)
## Break The Code — Technology Standards & Specifications

---

## 1. Stack Specifications

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend Framework** | Next.js | 15.x / React 19 | Server Component rendering, SEO, App Router |
| **Language (FE)** | TypeScript | 5.x | Strict type safety across client & schemas |
| **Styling** | Tailwind CSS | 3.4.x / 4.x | Utility-first design tokens, dark/light themes |
| **Icons** | Lucide React | Latest | Consistent developer icon set |
| **Backend Framework** | FastAPI | 0.115+ | High-performance asynchronous REST API |
| **Language (BE)** | Python | 3.12+ / 3.13 | Native async/await, modern type hints |
| **Validation** | Pydantic | v2.10+ | Request/response serialization and validation |
| **ORM** | SQLAlchemy | 2.0+ (async) | Async database session management |
| **Migrations** | Alembic | 1.14+ | Schema version control |
| **Database** | PostgreSQL | 16+ | ACID relational store |
| **Vector Search** | pgvector | 0.7+ | Dense embedding indexing (1536-dim) |
| **Cache & Queue** | Redis | 7.2+ | Key-value caching, rate-limiting, session state |
| **AI Framework** | LangGraph & LangChain | 0.2+ | Agentic graphs, workflow state persistence |
| **Observability** | LangSmith & OpenTelemetry | Latest | Trace LLM latency, token cost, failure modes |

---

## 2. API Conventions & Standards
- Base URL: `/api/v1`
- Content Type: `application/json`
- Standard Response Envelope:
  ```json
  {
    "success": true,
    "data": { ... },
    "meta": {
      "page": 1,
      "limit": 20,
      "total": 142
    },
    "error": null
  }
  ```
- Error Response Format:
  ```json
  {
    "success": false,
    "data": null,
    "error": {
      "code": "RESOURCE_NOT_FOUND",
      "message": "Question with slug 'rag-hybrid-search' does not exist",
      "details": []
    }
  }
  ```

---

## 3. Performance & Quality Benchmarks
- Web Vitals:
  - Largest Contentful Paint (LCP) < 2.5 seconds on simulated 4G.
  - Cumulative Layout Shift (CLS) < 0.1.
  - Interaction to Next Paint (INP) < 200 ms.
- Database: All filter columns (`technology_id`, `difficulty`, `status`, `slug`) indexed with compound B-Trees.
- Search queries execute in < 45 ms utilizing composite PostgreSQL GIN full-text indexes and vector HNSW indexes.
