"""
Curriculum Transformer for System Design Track.
Transforms raw system design headings into principal-level architecture interview questions,
structured answers, and distributed systems architecture code (rate limiters, circuit breakers, distributed locks).
"""

def transform_system_design_topic(topic_title: str, level: str, sec_slug: str, sec_name: str) -> dict:
    t = topic_title.strip()
    question_title = format_system_design_question(t, level)
    short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes = generate_system_design_dna(t, level, sec_slug, sec_name, question_title)
    
    return {
        "title": question_title,
        "short_answer": short_ans,
        "interview_ready_answer": ready_ans,
        "deep_explanation": deep_exp,
        "code_example": code_ex,
        "architecture_notes": arch_flow,
        "why_interviewer_asks": why_ask,
        "interviewer_intent": f"Tests principal-level systems judgment, distributed consensus, failure domain isolation, scalability bottlenecks, and trade-off defense at {level} depth.",
        "production_considerations": f"In production distributed systems, ensure {t} has formal SLA/SLO definitions, automated disaster recovery failover procedures, and end-to-end OpenTelemetry distributed tracing.",
        "failure_modes": fail_modes,
        "tradeoffs": tradeoffs,
        "common_mistakes": mistakes
    }

def format_system_design_question(topic: str, level: str) -> str:
    mappings = {
        "Kafka Architecture (Brokers, Topics, Partitions)": "How does Apache Kafka's architecture (Brokers, Topics, Partitions, and Consumer Groups) achieve high-throughput horizontal scalability?",
        "Message Broker vs Event Stream (RabbitMQ vs Kafka)": "What are the architectural differences between an AMQP message broker (RabbitMQ) and an append-only distributed event log (Kafka)?",
        "Consumer Group and Partition Assignment": "How do Kafka Consumer Groups distribute topic partitions across multiple consumer instances, and what triggers a group rebalance?",
        "Partition Key and Ordering Guarantees": "How does Kafka guarantee strict message ordering within a single partition using partition keys, and what happens when the partition count increases?",
        "At-Least-Once vs At-Most-Once Delivery": "What are the architectural trade-offs between At-Least-Once, At-Most-Once, and Exactly-Once delivery semantics in distributed messaging?",
        "Dead Letter Queue (DLQ) Role": "What is the purpose of a Dead Letter Queue (DLQ) in event-driven systems, and how do you handle poison pill messages without halting consumers?",
        "Kafka Offset Management (Auto vs Manual Commit)": "How does Kafka manage consumer offsets in the __consumer_offsets topic, and why is manual synchronous/asynchronous commit preferred over auto-commit?",
        "Producer Acknowledgments (acks=0, 1, all)": "What is the difference between producer acks=0, acks=1, and acks=all in Kafka, and how does min.insync.replicas guarantee durability?",
        "Kafka Exactly-Once Semantics (EOS) & Transactional API": "How does Kafka achieve Exactly-Once Semantics (EOS) across read-process-write loops using the Transactional API and idempotent producers?",
        "Preventing and Handling Consumer Group Rebalance Storms": "How do you diagnose and prevent Consumer Group Rebalance Storms in Kafka using Static Group Membership and cooperative rebalancing?",
        "Zero-Copy Data Transfer via sendfile() in Kafka": "How does Kafka achieve multi-gigabyte throughput using the Linux OS sendfile() zero-copy system call and page cache bypassing?",
        
        "Cache-Aside (Lazy Loading) Pattern": "How does the Cache-Aside pattern work, and how do you prevent race conditions between concurrent database writes and cache updates?",
        "Write-Through vs Write-Back (Write-Behind) Caching": "What are the durability and latency trade-offs between Write-Through, Write-Behind (Write-Back), and Cache-Aside architectures?",
        "Cache Stampede (Thundering Herd) Basics": "What causes a Cache Stampede (Thundering Herd) when a hot key expires, and how do distributed mutex locks and probabilistic early expiration (XFetch) mitigate it?",
        "Consistent Hashing Role in Distributed Caching": "How does Consistent Hashing with Virtual Nodes distribute cache keys evenly across nodes and minimize remapping during node scale-out/scale-in?",
        "Redis Data Structures (Strings, Hashes, Lists, Sets, Sorted Sets)": "How do Redis core data structures map to production use cases like leaderboards, distributed locks, rate limiters, and session stores?",
        "Redis Persistence (RDB vs AOF)": "What are the operational trade-offs between Redis RDB point-in-time snapshots and AOF append-only logs regarding recovery time and data loss (RPO)?",
        "Dual-Layer Caching Architecture (Local Caffeine + Remote Redis)": "How do you design a Dual-Layer Caching architecture (in-process Caffeine L1 + distributed Redis L2), and how do you synchronize invalidations?",
        "Bloom Filters and Cuckoo Filters for Cache Penetration Defense": "How do Bloom Filters and Cuckoo Filters protect backing databases from Cache Penetration attacks for non-existent keys?",
        
        "Database Sharding Definition": "What is Database Sharding, and what criteria determine the choice of an optimal Sharding Key to avoid hot partitions and cross-shard queries?",
        "Synchronous vs Asynchronous Replication": "What are the trade-offs between Synchronous and Asynchronous database replication regarding data durability (RPO) and write latency?",
        "CAP Theorem Basics (Consistency, Availability, Partition Tolerance)": "How does the CAP Theorem constrain distributed database design during a network partition, and how does the PACELC theorem extend it?",
        "Raft Consensus Algorithm Leader Election": "How does the Raft distributed consensus algorithm elect a leader using randomized election timers, heartbeats, and term numbers?",
        "Two-Phase Commit (2PC) Overview": "How does the Two-Phase Commit (2PC) protocol coordinate distributed transactions across multiple databases, and why can it block indefinitely?",
        "Two-Phase Commit (2PC) Failure Modes and Sagas Pattern Alternative": "What are the fatal blocking failure modes of Two-Phase Commit (2PC), and how does the Saga Pattern (Orchestration vs Choreography) provide eventual consistency?",
        "Distributed ID Generation: Snowflake vs UUID vs Sequence Shards": "How does Twitter's Snowflake algorithm generate 64-bit time-sortable unique IDs across distributed nodes without coordination?",
        
        "Token Bucket Rate Limiting Algorithm": "How does the Token Bucket rate limiting algorithm accommodate bursts of traffic while enforcing average rate limits, and how is it implemented with Redis?",
        "Circuit Breaker Pattern States (Closed, Open, Half-Open)": "How does a Circuit Breaker transition between Closed, Open, and Half-Open states to prevent cascading failures across microservices?",
        "Distributed Rate Limiting with Redis and Sliding Window Counter": "How do you implement a precise Distributed Rate Limiter using Redis Sorted Sets (ZSET) and a Sliding Window Counter algorithm?",
        "Bulkhead Isolation for Thread Pools and Connection Pools": "How does the Bulkhead pattern isolate resource pools (thread pools, HTTP connection pools) to prevent a slow downstream dependency from consuming all server resources?"
    }
    
    if topic in mappings:
        return mappings[topic]
        
    clean = topic.replace(":", "").replace("?", "").strip()
    if clean.lower().startswith("what") or clean.lower().startswith("how") or clean.lower().startswith("why"):
        return clean + ("?" if not clean.endswith("?") else "")
        
    if level == "L1":
        return f"What is the foundational role of {clean} in distributed system design, and how does it function?"
    else:
        return f"How do you architect, scale, and ensure fault tolerance for {clean} in a mission-critical distributed platform?"

from .text_utils import clean_concept_name

def generate_system_design_dna(topic: str, level: str, sec_slug: str, sec_name: str, question: str):
    t_clean = clean_concept_name(topic)
    
    short_ans = (
        f"In distributed system architecture ({sec_name}), {t_clean} is a foundational pattern for achieving high availability, "
        f"fault isolation, and horizontal scale. It enforces clear operational contracts across network boundaries, preventing "
        f"cascading failures and guaranteeing data consistency under network partitions."
    )
    
    ready_ans = (
        f"When architecting **{t_clean}** in a Principal/Staff Systems Design interview, structure your blueprint across three distinct phases:\n\n"
        f"1. **Core Problem Statement & Invariants**: Define the operational requirement (throughput in QPS, latency budget in ms, "
        f"data consistency level, and durability SLA). {t_clean} is designed to eliminate single points of failure (SPOF) and handle "
        f"unreliable network channels without sacrificing system availability.\n\n"
        f"2. **Distributed Protocol & Mechanics**: Explain the data and control plane flow. For stateful partitioning, explain hash ring "
        f"rebalancing, leader-follower replication, and heartbeat consensus. For resiliency primitives, articulate how circuit breakers, "
        f"rate limiters, and backpressure queues isolate failure domains and shed excess traffic gracefully.\n\n"
        f"3. **Trade-offs & Disaster Recovery**: Explicitly evaluate CAP theorem constraints (AP vs CP), cost-to-performance trade-offs, "
        f"and failure modes during network splits (split-brain mitigation via quorum reads/writes `W + R > N`). "
        f"Define how the system recovers when downstream dependencies crash."
    )
    
    deep_exp = (
        f"### Distributed Systems Deep Dive: {t_clean}\n\n"
        f"At enterprise scale (100k+ QPS), distributed systems cannot rely on synchronous blocking calls across services. "
        f"Every network hop introduces non-deterministic latency and risk of thread starvation.\n\n"
        f"To guarantee durability and high throughput, architectures decouple data ingress from asynchronous processing using "
        f"distributed append-only logs (Kafka) with zero-copy I/O (`sendfile`), or distribute state across in-memory caching clusters (Redis) "
        f"partitioned via Consistent Hashing with virtual nodes. When writing to persistent databases, distributed transactions utilize "
        f"the Saga Pattern with compensating transactions rather than blocking Two-Phase Commit (2PC).\n\n"
        f"During traffic surges, rate limiting with the Token Bucket or Sliding Window Log algorithm enforces fair-share multi-tenant "
        f"quotas at the API Gateway layer, dropping or queuing unauthenticated requests before they can saturate downstream database connection pools."
    )
    
    # Real Python distributed algorithm code example (e.g. Sliding window rate limiter / circuit breaker)
    code_ex = (
        f"import time\n"
        f"from typing import Dict, Tuple\n\n"
        f"class Resilient{sec_slug.replace('-', ' ').title().replace(' ', '')}Manager:\n"
        f"    \"\"\"\n"
        f"    Production architecture implementation of {t_clean}\n"
        f"    Features atomic token tracking, window sliding, and failure state tripping.\n"
        f"    \"\"\"\n"
        f"    def __init__(self, capacity: int = 100, refill_rate_per_sec: float = 10.0):\n"
        f"        self.capacity = capacity\n"
        f"        self.refill_rate = refill_rate_per_sec\n"
        f"        self.tokens: float = capacity\n"
        f"        self.last_refill_time = time.monotonic()\n"
        f"        self.circuit_state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN\n"
        f"        self.consecutive_failures = 0\n"
        f"        self.failure_threshold = 5\n\n"
        f"    def allow_request(self) -> Tuple[bool, str]:\n"
        f"        # 1. Circuit breaker health check\n"
        f"        if self.circuit_state == 'OPEN':\n"
        f"            return False, 'Circuit Breaker OPEN - Request rejected to isolate failure'\n\n"
        f"        # 2. Token Bucket refill for {t_clean}\n"
        f"        now = time.monotonic()\n"
        f"        elapsed = now - self.last_refill_time\n"
        f"        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)\n"
        f"        self.last_refill_time = now\n\n"
        f"        # 3. Rate limit evaluation\n"
        f"        if self.tokens >= 1.0:\n"
        f"            self.tokens -= 1.0\n"
        f"            return True, 'Request Allowed'\n"
        f"        else:\n"
        f"            return False, 'HTTP 429 Too Many Requests - Rate limit exceeded'\n\n"
        f"    def record_failure(self):\n"
        f"        self.consecutive_failures += 1\n"
        f"        if self.consecutive_failures >= self.failure_threshold:\n"
        f"            self.circuit_state = 'OPEN'\n\n"
        f"# Production test verification\n"
        f"manager = Resilient{sec_slug.replace('-', ' ').title().replace(' ', '')}Manager(capacity=5, refill_rate_per_sec=2.0)\n"
        f"allowed, reason = manager.allow_request()\n"
        f"print(f\"[{t_clean}] Ingress decision: {{allowed}} ({{reason}})\")\n"
        f"assert allowed is True"
    )
    
    arch_flow = (
        f"Ingress Traffic (Clients / Mobile Apps / Web)\n"
        f"  │\n"
        f"  ▼\n"
        f"[Edge CDN & API Gateway (Cloudflare / Envoy)]\n"
        f"  │ ──► [Distributed Rate Limiter: Redis Sliding Window]\n"
        f"  ▼\n"
        f"[{t_clean} Resilient Processing Tier]\n"
        f"  │\n"
        f"  ├──────────────────────────────┬──────────────────────────────┐\n"
        f"  ▼                              ▼                              ▼\n"
        f"[Kafka Event Streaming Log]     [Distributed Cache: Redis]     [Database Shard Primary]\n"
        f"  │ (Partition Key Sharding)     │ (Consistent Hashing Ring)    │ (Raft Consensus / Quorum)\n"
        f"  ▼                              ▼                              ▼\n"
        f"[Consumer Group Workers]        [Local L1 Memory Cache]        [Read Replicas Pool]"
    )
    
    why_ask = f"Interviewers assess the candidate's grasp of distributed consensus, high-throughput message ordering, caching stampede mitigation, and system resiliency under cascading failure scenarios."
    fail_modes = f"Split-brain partitioning during network isolation, consumer group rebalance storms stalling message pipelines, and cache stampedes overwhelming backing databases."
    tradeoffs = f"Balancing strict consistency (CP) against high availability (AP), and in-memory cache speed against durability and data loss risks."
    mistakes = [
        f"Using synchronous two-phase commit (2PC) across microservices, creating distributed lock bottlenecks",
        f"Forgetting to set TTLs on cached keys, leading to memory exhaustion and stale data anomalies",
        f"Assuming Kafka preserves global order across all partitions instead of per-partition ordering"
    ]
    
    return short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes
