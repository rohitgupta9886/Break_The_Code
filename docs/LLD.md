# Low-Level Design (LLD)
## Break The Code — Component & Module Specification

---

## 1. Backend Module Hierarchy

```
backend/app/
├── api/
│   ├── deps.py                 # Dependency injectors (get_db, get_current_user, require_permission)
│   └── v1/
│       ├── auth.py             # Login, register, refresh, logout
│       ├── users.py            # User profile, preferences, notes
│       ├── questions.py        # Public question search, browse, detail, hints, bookmarks
│       ├── technologies.py     # Technology tracks & topics list
│       ├── progress.py         # User completion stats, streaks, XP
│       ├── ai.py               # Answer evaluation, hint generation, socratic assistant
│       ├── interviews.py       # LangGraph mock interview session control
│       └── admin.py            # CMS question create/edit/publish, review workflows, analytics
├── core/
│   ├── config.py               # Pydantic BaseSettings loading from .env
│   ├── security.py             # Password hashing (bcrypt), JWT generation/verification
│   ├── database.py             # Async SQLAlchemy engine & session factory
│   └── redis.py                # Redis connection pool & caching helpers
├── models/
│   ├── base.py                 # Declarative Base with timestamp mixins
│   ├── user.py                 # User, Role, Permission, UserRole
│   ├── taxonomy.py             # Domain, Technology, Topic, Subtopic, Tag
│   ├── question.py             # Question, QuestionVersion, QuestionHint, QuestionFollowup, Source
│   ├── interaction.py          # UserProgress, UserAttempt, Bookmark, UserNote
│   └── interview.py            # MockInterview, InterviewQuestion, InterviewAnswer
├── schemas/
│   ├── user.py                 # UserCreate, UserRead, TokenSchema
│   ├── question.py             # QuestionCreate, QuestionUpdate, QuestionDetailResponse, QuestionListResponse
│   ├── taxonomy.py             # TechnologySchema, TopicSchema
│   └── ai.py                   # AnswerEvaluationRequest, AnswerEvaluationResponse
├── repositories/
│   ├── base.py                 # Generic CRUD Repository
│   ├── user_repo.py            # User & auth queries
│   ├── question_repo.py        # Question queries with faceted filters & full text search
│   └── taxonomy_repo.py        # Tech & topic queries with live counts
└── services/
    ├── auth_service.py         # Authentication logic, password verification
    ├── question_service.py     # Question business logic, version snapshotting, publish rules
    ├── search_service.py       # Hybrid ranking (FTS + vector search)
    └── ai_service.py           # LangGraph executor wrapper
```

---

## 2. Frontend Component Hierarchy

```
frontend/src/
├── components/
│   ├── ui/                     # Design System Atoms & Molecules
│   │   ├── button.tsx          # Variants: primary, secondary, outline, ghost, glass
│   │   ├── badge.tsx           # DifficultyBadge, TechnologyBadge, StatusBadge
│   │   ├── card.tsx            # GlassCard, InteractiveCard, MetricCard
│   │   ├── modal.tsx           # Accessible Dialog / Modal
│   │   ├── input.tsx           # SearchInput, FormInput with validation styles
│   │   ├── select.tsx          # Custom accessible dropdown
│   │   ├── tabs.tsx            # Animated pill & underline tabs
│   │   ├── progress.tsx        # Linear ProgressBar & ProgressRing
│   │   ├── code-block.tsx      # Syntax-highlighted code viewer with copy button
│   │   ├── skeleton.tsx        # Content placeholders
│   │   └── toast.tsx           # Interactive notifications
│   ├── landing/
│   │   ├── hero.tsx            # Hero with dynamic call-to-actions
│   │   ├── animated-demo.tsx   # Visual interactive AI interviewer simulation
│   │   ├── track-grid.tsx      # Dynamic technology tracks with live question counts
│   │   ├── question-preview.tsx# Live interactive question sample
│   │   ├── social-proof.tsx    # Technical community testimonials
│   │   ├── pricing-section.tsx # Free, Pro, Premium tiers
│   │   └── faq-section.tsx     # Accordion FAQ
│   ├── questions/
│   │   ├── question-card.tsx   # Grid/list card with badges, estimate, bookmark
│   │   ├── filter-sidebar.tsx  # Faceted filters (Desktop & Mobile bottom sheet)
│   │   ├── think-mode.tsx      # Live timer, candidate input, reveal controls
│   │   ├── hint-system.tsx     # Progressive 3-level hint drawer
│   │   └── answer-viewer.tsx   # Structured tabs (Answer, Explanation, Architecture, Mistakes)
│   └── layout/
│       ├── navbar.tsx          # Global top navigation with Search trigger & Profile
│       ├── mobile-nav.tsx      # Sticky bottom bar for mobile screens
│       ├── footer.tsx          # Structured footer with track links & metadata
│       └── theme-toggle.tsx    # Smooth Dark/Light mode switcher
```
