# Content Guidelines & Editorial Standards (CONTENT_GUIDELINES.md)
## Break The Code — Content Quality & Integrity Standards

---

## 1. Editorial Integrity & Copyright Protection
- **No Scraping**: Never copy verbatim proprietary questions and answers from commercial interview portals.
- **Original Authorship**: Formulate questions around official framework documentation (e.g. LangGraph documentation, Python PEPs, OpenJDK specs, Spring Boot Reference Guides).
- **Source Attribution**:
  - Every question tracks `source_name`, `source_url`, `source_author`, `license`, and `content_origin` (`ORIGINAL`, `ADAPTED`, `SYNTHESIZED`, `LICENSED`).
  - If adapted from an open-source educational repository, full attribution must be preserved.

---

## 2. Multi-Stage Review Pipeline
AI-generated or community-contributed questions must traverse the approval lifecycle:
1. `DRAFT`: Author or AI generates question structure.
2. `AI_REVIEW`: Automated Quality Engine runs linting, code validation, and duplicate detection.
3. `EDITOR_REVIEW`: Content editor reviews tone, grammar, and typography.
4. `TECHNICAL_REVIEW`: Domain expert verifies technical accuracy, architecture validity, and common mistake lists.
5. `APPROVED`: Staged for release.
6. `PUBLISHED`: Publicly indexable and accessible to candidates.

---

## 3. Question DNA Structure
Every question in Break The Code must provide:
- **Title**: Action-oriented and precise.
- **Interview Depth Level**: (L1 Definition to L5 Production Scenario).
- **Short Answer**: 2-3 sentence elevator pitch for rapid recall.
- **Interview-Ready Answer**: Structured 2-minute spoken response suitable for actual interviews.
- **Deep Explanation**: In-depth theoretical grounding and inner workings.
- **Architecture Notes**: Diagrams or data flow explanation.
- **Code Example**: Clean, runnable, commented code block.
- **Common Mistakes**: Array of mistakes candidates frequently make.
- **Interviewer Intent**: What the interviewer is evaluating (e.g. depth, edge cases, trade-offs).
- **3 Progressive Hints**: Conceptual, Implementation, and Architecture.
