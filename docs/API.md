# API Specification (API.md)
## Break The Code — REST Endpoints & Contracts

---

## 1. Authentication & Users (`/api/v1/auth`, `/api/v1/users`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new account with email & password | No |
| `POST` | `/api/v1/auth/login` | Authenticate and obtain JWT access token | No |
| `POST` | `/api/v1/auth/refresh` | Refresh expired access token | Refresh Token |
| `GET` | `/api/v1/users/me` | Fetch authenticated user profile & entitlements | Bearer Token |
| `PATCH` | `/api/v1/users/me` | Update display name, avatar, preferences | Bearer Token |

---

## 2. Questions & Taxonomy (`/api/v1/questions`, `/api/v1/technologies`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/technologies` | Get active tracks with question counts | No |
| `GET` | `/api/v1/technologies/{slug}` | Get technology details, topics, and roadmaps | No |
| `GET` | `/api/v1/questions` | Query questions with filters (tech, topic, difficulty, type, depth, page, limit) | No |
| `GET` | `/api/v1/questions/{slug}` | Get comprehensive question detail (Think mode data, code, architecture) | No |
| `GET` | `/api/v1/questions/{id}/hints` | Progressive hint retrieval by level (1, 2, 3) | No |
| `POST` | `/api/v1/questions/{id}/bookmark` | Toggle question bookmark | Bearer Token |
| `POST` | `/api/v1/questions/{id}/complete` | Mark question as practiced / completed | Bearer Token |

---

## 3. Search & Discovery (`/api/v1/search`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/search` | Hybrid keyword + semantic question search | No |
| `GET` | `/api/v1/search/autocomplete` | Fast typeahead for technologies, topics, questions | No |

---

## 4. AI & Answer Evaluation (`/api/v1/ai`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/ai/evaluate-answer` | Evaluates candidate answer via LangGraph pipeline | Bearer Token |
| `POST` | `/api/v1/ai/socratic-hint` | Generates guiding Socratic question for Think Mode | Bearer Token |

---

## 5. Administration CMS (`/api/v1/admin`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/admin/analytics` | High-level metrics (questions, users, reviews, AI usage) | Admin Role |
| `POST` | `/api/v1/admin/questions` | Create new question draft with full metadata | `questions:create` |
| `PUT` | `/api/v1/admin/questions/{id}` | Update question & record version snapshot | `questions:edit` |
| `POST` | `/api/v1/admin/questions/{id}/publish` | Transition question to `PUBLISHED` status | `questions:publish` |
| `POST` | `/api/v1/admin/questions/generate-ai` | Trigger AI question generation into `DRAFT` | `questions:create` |
| `GET` | `/api/v1/admin/questions/{id}/versions` | Inspect historical snapshots & diffs | Admin Role |
