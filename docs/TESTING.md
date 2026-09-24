# Testing & Quality Assurance Plan (TESTING.md)
## Break The Code — Test Strategy & Verification

---

## 1. Test Levels & Coverage Goals
- **Unit Tests**: Coverage target >= 85% for core business services (`question_service`, `auth_service`, `ai_evaluator`).
- **Integration Tests**: End-to-end API test suites covering registration, login, question filtering, bookmarking, and answer evaluation.
- **Frontend Validation**: Automated Next.js compilation & TypeScript validation (`tsc --noEmit`).

---

## 2. Critical Test Scenarios
1. **Authentication & Security**:
   - Valid credentials return access token + user claims.
   - Malformed/expired token receives 401 Unauthorized.
   - Non-admin user accessing `/api/v1/admin/*` receives 403 Forbidden.
2. **Question Engine**:
   - Querying questions with `difficulty=TOUGH` & `technology=ai-genai` returns strictly filtered results.
   - Creating a question without required fields fails Pydantic schema validation with 422 Unprocessable Entity.
   - Publishing a question updates status and stores version snapshot in `question_versions`.
3. **AI Evaluation**:
   - Evaluation pipeline handles answers, calculates rubric scores (0-10), and extracts covered/missed points without crashing.
   - Graceful fallback when external LLM rate-limit or timeout occurs.
