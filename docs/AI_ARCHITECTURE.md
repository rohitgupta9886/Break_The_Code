# AI Architecture & LangGraph Workflows (AI_ARCHITECTURE.md)
## Break The Code — Agentic Intelligence Specification

---

## 1. Core Principles
1. **Provider Independence**: All AI invocation routes through an abstract `LLMProvider` interface (`OpenAIProvider`, `AnthropicProvider`, `GeminiProvider`, `MockProvider`). No single-vendor lock-in.
2. **State Machine Persistence**: Complex multi-turn interviews run as deterministic LangGraph state graphs with checkpointing to PostgreSQL.
3. **Guardrails & Quality Control**: AI outputs are strictly validated using Pydantic schemas before persistence or presentation.

---

## 2. Answer Evaluation Graph (Think Mode Submission)

```mermaid
graph TD
    A[START: Candidate Answer Submitted] --> B[Sanitize Input & Token Budget Check]
    B --> C[Retrieve Question Rubric & Ideal Answer]
    C --> D[Evaluator Node: Grade 4 Rubrics]
    
    subgraph Multi-Metric Grading
        D -->|Rubric 1| R1[Correctness: 0-10]
        D -->|Rubric 2| R2[Completeness: 0-10]
        D -->|Rubric 3| R3[Technical Depth: 0-10]
        D -->|Rubric 4| R4[Clarity: 0-10]
    end
    
    R1 --> E[Synthesizer Node: Extract Covered & Missed Points]
    R2 --> E
    R3 --> E
    R4 --> E
    
    E --> F[Generate Improved Answer]
    F --> G[Save Attempt to DB & Return Scorecard]
    G --> H[END]
```

---

## 3. Mock Interview Workflow Graph

```mermaid
graph TD
    Start[START] --> Setup[SETUP: Role, Experience, Topics, Duration]
    Setup --> QSelect[QUESTION_SELECTION: Filter question pool]
    QSelect --> Ask[ASK: Deliver question to candidate]
    Ask --> Wait[WAIT_FOR_ANSWER: Polling or WebSocket]
    Wait --> Eval[EVALUATE: Grade candidate answer]
    Eval --> Adapt{ADAPT_DIFFICULTY: Score >= 7.5?}
    
    Adapt -->|Yes| BumpDiff[Escalate: Basic -> Medium -> Tough]
    Adapt -->|No| LowerDiff[De-escalate or Focus on Fundamentals]
    
    BumpDiff --> FollowupCheck{Remaining Duration > 0?}
    LowerDiff --> FollowupCheck
    
    FollowupCheck -->|Yes & Needs Deep Dive| SelectFollowup[SELECT_FOLLOWUP]
    SelectFollowup --> AskFollowup[ASK_FOLLOWUP]
    AskFollowup --> Wait
    
    FollowupCheck -->|Yes & Next Topic| QSelect
    FollowupCheck -->|No| FinalReport[FINAL_EVALUATION: Scorecard & Recommendation]
    FinalReport --> End[END]
```

---

## 4. Observability & Cost Management
- **LangSmith Tracing**: Traces every run tree (`session_id`, prompt templates, token consumption, execution latency).
- **Prompt Injection Defense**: Input filters scan for control token exploits, delimiter injection, and jailbreak phrases before LLM dispatch.
- **Model Routing**: Cheaper lightweight models for Socratic hints and rapid grading; frontier reasoning models for full mock interviews and architecture defense.
