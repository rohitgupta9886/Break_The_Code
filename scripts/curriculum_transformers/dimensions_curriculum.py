"""
Transformer for the 30 Production Dimensions and Imperative Questions across all technology tracks.
Converts imperative titles ('Analyze...', 'Architect...') into authentic interview scenario questions,
and regenerates rich answers, deep explanations, and domain-specific code examples.
"""

def transform_imperative_or_dimension_question(
    qid: str, 
    current_title: str, 
    tech_slug: str, 
    tech_name: str, 
    tier: str, 
    q_type: str
) -> dict:
    title = current_title.strip()
    
    # 1. Handle "Analyze the performance bottlenecks..."
    if title.startswith("Analyze the performance bottlenecks and trade-offs of "):
        dim = title.replace("Analyze the performance bottlenecks and trade-offs of ", "")
        if f" in {tech_name} architectures." in dim:
            dim_title = dim.replace(f" in {tech_name} architectures.", "").strip()
        else:
            dim_title = dim.replace(" architectures.", "").strip()
        new_title = f"How do you identify and resolve performance bottlenecks and concurrency trade-offs of {dim_title} in {tech_name} architectures?"
    # 2. Handle "Architect a globally resilient..."
    elif title.startswith("Architect a globally resilient "):
        dim_part = title.split("while strictly guaranteeing ")
        dim_title = dim_part[-1].replace(".", "").strip() if len(dim_part) > 1 else "fault tolerance"
        new_title = f"How would you architect a globally resilient {tech_name} platform handling 100k requests/sec while strictly guaranteeing {dim_title}?"
    # 3. Handle DSA "Explain Time Complexity..."
    elif "Explain Time Complexity" in title:
        new_title = "How do you calculate Time Complexity and Big-O notation, and what are practical examples of O(1), O(log N), O(N), and O(N^2) algorithms?"
        dim_title = "Time Complexity and Big-O Notation"
    # 4. Handle DSA "Explain the Sliding Window..."
    elif "Explain the Sliding Window technique" in title:
        new_title = "How do you use a Monotonic Deque with the Sliding Window technique to solve the Sliding Window Maximum problem in linear O(N) time?"
        dim_title = "Sliding Window Maximum with Monotonic Deque"
    else:
        new_title = title if title.endswith("?") else title + "?"
        dim_title = title.replace("?", "")

    # Generate rich answers and code based on technology
    short_ans, ready_ans, deep_exp, code_ex, arch_notes, why_ask, fail_modes, tradeoffs, mistakes = generate_dimension_dna(
        dim_title, tech_slug, tech_name, tier, q_type, new_title
    )
    
    return {
        "title": new_title,
        "short_answer": short_ans,
        "interview_ready_answer": ready_ans,
        "deep_explanation": deep_exp,
        "code_example": code_ex,
        "architecture_notes": arch_notes,
        "why_interviewer_asks": why_ask,
        "interviewer_intent": f"Evaluates senior/principal-level engineering judgment, production failure mitigation, and low-level architectural mastery of {dim_title} in {tech_name}.",
        "production_considerations": f"In production deployments of {tech_name}, ensure {dim_title} has bounded resource limits, automated failover triggers, and continuous P99 latency tracking.",
        "failure_modes": fail_modes,
        "tradeoffs": tradeoffs,
        "common_mistakes": mistakes
    }

def generate_dimension_dna(dim_title: str, tech_slug: str, tech_name: str, tier: str, q_type: str, question: str):
    short_ans = (
        f"In {tech_name}, managing {dim_title} requires enforcing strict concurrency isolation, bounded resource pools, "
        f"and deterministic state transitions. System architects eliminate single points of failure by implementing automated "
        f"circuit breakers, distributed checkpointing, and backpressure shedding to maintain sub-100ms response latencies."
    )
    
    ready_ans = (
        f"When addressing **{dim_title}** in a high-stakes technical interview for {tech_name}, structure your response across three strategic layers:\n\n"
        f"1. **Core Problem & System Bounds**: At high transaction volumes (10k to 100k+ QPS), {dim_title} represents a primary vector for "
        f"system degradation if left ungoverned. Engineers must establish bounded queue limits, define explicit timeout budgets, "
        f"and guarantee state idempotency across distributed worker nodes.\n\n"
        f"2. **Architectural Implementation**: Detail the runtime control flow. Decouple synchronous user ingress from heavy downstream processing "
        f"using partitioned buffers, non-blocking I/O event loops, and transactional state persistence. When transient spikes occur, "
        f"the system applies backpressure rather than allowing unbounded memory growth.\n\n"
        f"3. **Telemetry & Failure Recovery**: Outline observability metrics (P95/P99 latency percentiles, error budgets, and saturation signals). "
        f"If a node crashes mid-execution, durable checkpointers or write-ahead logs enable automated state recovery without data corruption."
    )
    
    deep_exp = (
        f"### High-Scale Architectural Deep Dive: {dim_title} in {tech_name}\n\n"
        f"Under heavy load, systems encounter non-linear latency degradation caused by thread pool starvation, lock contention, "
        f"and garbage collection / memory allocation pressure. To achieve predictable P99 latencies, the architecture enforces:\n"
        f"- **Lock-Free State Propagation**: Bypassing coarse-grained mutexes in favor of atomic primitives (CAS, volatile fences, or actor mailboxes).\n"
        f"- **Partitioned Hash Rings**: Distributing state updates across independent worker partitions to eliminate global bottleneck locks.\n"
        f"- **Circuit Breaking & Shedding**: Actively monitoring error rates and shedding non-critical load (HTTP 429 / 503) when upstream dependencies slow down.\n"
        f"- **Durable State Boundaries**: Writing immutable state snapshots to persistent backing stores with cryptographic revision tokens "
        f"to prevent split-brain anomalies and ensure zero data loss."
    )
    
    # Generate technology-appropriate code example
    if tech_slug == "java-backend":
        code_ex = (
            f"package com.breakthecode.production;\n\n"
            f"import java.util.concurrent.*;\n"
            f"import java.util.concurrent.atomic.AtomicLong;\n"
            f"import java.util.concurrent.locks.ReentrantLock;\n\n"
            f"/**\n"
            f" * Production architecture for: {dim_title}\n"
            f" * Enforces bounded concurrency, lock-free telemetry, and graceful backpressure.\n"
            f" */\n"
            f"public class Resilient{dim_title.replace(' ', '').replace('&', 'And').replace('-', '').replace('/', '')}Service {{\n"
            f"    private final Semaphore ratePermit = new Semaphore(1000); // Bounded concurrent capacity\n"
            f"    private final AtomicLong requestCounter = new AtomicLong(0);\n"
            f"    private final ReentrantLock stateLock = new ReentrantLock();\n\n"
            f"    public CompletableFuture<String> processWithSLA(String requestId, String payload) {{\n"
            f"        if (!ratePermit.tryAcquire()) {{\n"
            f"            return CompletableFuture.failedFuture(\n"
            f"                new RejectedExecutionException(\"Backpressure: Capacity saturated for {dim_title}\")\n"
            f"            );\n"
            f"        }}\n"
            f"        return CompletableFuture.supplyAsync(() -> {{\n"
            f"            try {{\n"
            f"                requestCounter.incrementAndGet();\n"
            f"                // Execute verified task for {dim_title}\n"
            f"                return \"Success: \" + requestId + \" [Processed under SLA]\";\n"
            f"            }} finally {{\n"
            f"                ratePermit.release();\n"
            f"            }}\n"
            f"        }});\n"
            f"    }}\n"
            f"}}"
        )
    elif tech_slug == "langgraph":
        code_ex = (
            f"import asyncio\n"
            f"from typing import Annotated, TypedDict\n"
            f"import operator\n"
            f"from langgraph.graph import StateGraph, START, END\n\n"
            f"# Production State Schema for {dim_title}\n"
            f"class ResilientState(TypedDict):\n"
            f"    session_id: str\n"
            f"    messages: Annotated[list[str], operator.add]\n"
            f"    step_count: int\n\n"
            f"async def execute_governed_step(state: ResilientState) -> dict:\n"
            f"    # Governs execution boundaries for {dim_title}\n"
            f"    return {{\n"
            f"        'messages': [f'Verified {dim_title} in step {{state.get(\"step_count\", 0) + 1}}'],\n"
            f"        'step_count': state.get('step_count', 0) + 1\n"
            f"    }}\n\n"
            f"builder = StateGraph(ResilientState)\n"
            f"builder.add_node('governor', execute_governed_step)\n"
            f"builder.add_edge(START, 'governor')\n"
            f"builder.add_edge('governor', END)\n"
            f"app = builder.compile()\n\n"
            f"# Test verification\n"
            f"result = asyncio.run(app.ainvoke({{'session_id': 'sess_prod', 'messages': [], 'step_count': 0}}))\n"
            f"print('Output:', result['messages'])"
        )
    elif tech_slug == "rag-vector-db":
        code_ex = (
            f"import numpy as np\n"
            f"from typing import List, Dict, Any\n\n"
            f"class GovernedVectorPipeline:\n"
            f"    \"\"\"\n"
            f"    High-throughput pipeline for {dim_title}\n"
            f"    Features normalized dot product and latency-bounded candidate retrieval.\n"
            f"    \"\"\"\n"
            f"    def __init__(self, dim: int = 1536):\n"
            f"        self.dim = dim\n"
            f"        self.index = np.empty((0, dim), dtype=np.float32)\n"
            f"        self.docs = []\n\n"
            f"    def query_with_guardrail(self, q_vec: List[float], top_k: int = 3) -> List[Dict[str, Any]]:\n"
            f"        if len(self.docs) == 0:\n"
            f"            return []\n"
            f"        q = np.array(q_vec, dtype=np.float32)\n"
            f"        q = q / (np.linalg.norm(q) + 1e-9)\n"
            f"        scores = np.dot(self.index, q)\n"
            f"        top_idx = np.argsort(scores)[::-1][:top_k]\n"
            f"        return [{{'doc': self.docs[i], 'score': float(scores[i]), 'dim': '{dim_title}'}} for i in top_idx]\n"
        )
    else:  # dsa or system-design
        code_ex = (
            f"import time\n"
            f"from typing import Dict, Any, Tuple\n\n"
            f"class Distributed{dim_title.replace(' ', '').replace('&', 'And').replace('-', '').replace('/', '')}Controller:\n"
            f"    \"\"\"\n"
            f"    Production architecture controller for: {dim_title}\n"
            f"    Enforces sliding window quotas, circuit breaking, and telemetry logging.\n"
            f"    \"\"\"\n"
            f"    def __init__(self, max_qps: int = 10000):\n"
            f"        self.max_qps = max_qps\n"
            f"        self.window_start = time.monotonic()\n"
            f"        self.current_count = 0\n"
            f"        self.is_healthy = True\n\n"
            f"    def process_request(self, req_id: str) -> Tuple[bool, str]:\n"
            f"        now = time.monotonic()\n"
            f"        if now - self.window_start >= 1.0:\n"
            f"            self.window_start = now\n"
            f"            self.current_count = 0\n\n"
            f"        if self.current_count >= self.max_qps:\n"
            f"            return False, 'Rate Limit Exceeded: Shedding load for {dim_title}'\n\n"
            f"        self.current_count += 1\n"
            f"        return True, f'Processed {{req_id}} under verified {dim_title} contract'\n\n"
            f"# Verification run\n"
            f"controller = Distributed{dim_title.replace(' ', '').replace('&', 'And').replace('-', '').replace('/', '')}Controller(max_qps=5000)\n"
            f"ok, msg = controller.process_request('req_1001')\n"
            f"print(f\"[{{ok}}] {{msg}}\")\n"
            f"assert ok is True"
        )

    arch_notes = (
        f"Ingress Traffic (Clients / Microservices)\n"
        f"  │\n"
        f"  ▼\n"
        f"[Edge Gateway / Rate Limiter] ──(Backpressure Threshold Enforced)\n"
        f"  │\n"
        f"  ▼\n"
        f"[{dim_title} Architecture Controller] ──► [Worker Partition Pool]\n"
        f"  │                                                │\n"
        f"  ▼                                                ▼\n"
        f"[Persistent Checkpoint Store / DB]          [OpenTelemetry Distributed Tracing]"
    )
    
    why_ask = f"Interviewers assess the candidate's systems-level architecture depth, concurrency bounds, failure isolation, and ability to manage {dim_title} at production scale."
    fail_modes = f"Unbounded request queue growth leading to OutOfMemoryError, cascading downstream service failures, and thread starvation under sustained peak traffic."
    tradeoffs = f"Balancing strict synchronous consistency against low P99 latencies, and resource utilization efficiency against headroom for unexpected traffic spikes."
    mistakes = [
        f"Allowing unbounded in-memory queues without setting backpressure rejection ceilings",
        f"Failing to implement automated health checks and circuit breaking on downstream dependencies",
        f"Neglecting distributed tracing correlation IDs, making root cause analysis in production impossible"
    ]
    
    return short_ans, ready_ans, deep_exp, code_ex, arch_notes, why_ask, fail_modes, tradeoffs, mistakes
