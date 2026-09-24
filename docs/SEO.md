# Search Engine Optimization & Discoverability (SEO.md)
## Break The Code — Indexing & Social Presence

---

## 1. URL Architecture & Taxonomy

- **Technology Landing Pages**:
  - `/ai/langgraph/interview-questions`
  - `/ai/rag/interview-questions`
  - `/java/spring-boot/interview-questions`
  - `/dsa/dynamic-programming/interview-questions`
- **Question Detail Pages**:
  - `/questions/{slug}` (e.g. `/questions/langgraph-checkpointing-state-persistence`)
- **Track Overviews**:
  - `/learn/{technology-slug}`

---

## 2. Meta Tags & OpenGraph Automation
- **Title Structure**: `{Question Title} | Break The Code`
- **Meta Description**: Concise 150-160 character summary highlighting key technical depth (L1-L5) and technology track.
- **OpenGraph Dynamic Images**: Previews rendered with title, technology badge, and difficulty badge.
- **Canonical URLs**: Strictly set to prevent duplicate content penalties across query param filters.

---

## 3. Structured Data (JSON-LD)
Every question page embeds schema.org `QAPage` or `TechArticle` microdata:
```json
{
  "@context": "https://schema.org",
  "@type": "QAPage",
  "mainEntity": {
    "@type": "Question",
    "name": "How does checkpointing work in LangGraph?",
    "text": "Explain state persistence and recovery mechanics...",
    "answerCount": 1,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Checkpointing saves the state snapshot at each superstep...",
      "url": "https://breakthecode.dev/questions/langgraph-checkpointing-state-persistence"
    }
  }
}
```

---

## 4. Robots & Sitemap Rules
- **Sitemap**: `/sitemap.xml` dynamically generated for published questions, technologies, topics, and roadmaps.
- **Robots**: Excludes `/admin/*`, `/dashboard/*`, `/interview/session/*`, `/api/*`.
