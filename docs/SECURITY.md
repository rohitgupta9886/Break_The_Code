# Security & Compliance Specification (SECURITY.md)
## Break The Code — Enterprise Security Standards

---

## 1. Authentication & Session Security
- **Password Storage**: Hashed using **bcrypt** with work factor 12 (or Argon2id). Plaintext passwords never touch logs or databases.
- **JWT Tokens**:
  - Algorithm: `HS256` (or `RS256` in production cluster).
  - Short-lived Access Tokens (15–30 minutes) + Rotating Refresh Tokens (7 days).
  - HttpOnly, Secure, SameSite=Strict cookie storage for web clients.

---

## 2. Authorization & RBAC
- Granular permission matrix stored in PostgreSQL:
  - `SUPER_ADMIN`: All permissions.
  - `ADMIN`: User management, content management, analytics.
  - `CONTENT_EDITOR`: Create, edit, submit for review.
  - `TECHNICAL_REVIEWER`: Review, approve, reject questions.
  - `USER`: Read published questions, attempt, bookmark, take interviews.
- Server-side validation via FastAPI dependency injection on every protected endpoint.

---

## 3. Rate Limiting & Denial of Service Protection
- Redis Token Bucket / Sliding Window rate limiting:
  - Anonymous / Public: 60 requests/minute.
  - Authenticated Users: 200 requests/minute.
  - AI Evaluation & Generation: 10 requests/minute (Free), 50 requests/minute (Pro).
  - Auth Login / Register: 5 attempts/minute per IP (prevents credential stuffing).

---

## 4. AI & Content Security
- **Prompt Injection Defense**: Untrusted user inputs (resumes, answer submissions) are bounded inside explicit XML delimiters (`<candidate_answer>...</candidate_answer>`).
- **File Upload Protection**: Resumes restricted to PDF and DOCX, max 5MB, inspected by magic number (MIME validation), stored on private object storage with unguessable UUIDs.
- **Secrets Management**: Secrets loaded exclusively from environment variables; zero hardcoded credentials.
