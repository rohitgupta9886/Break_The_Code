"""
System Design Batch Expansion
Focuses on under-represented topics:
- sharding-consensus (Database Sharding, Replication & Distributed Consensus)
- api-gateway-resilience (API Gateway, Rate Limiting & System Reliability)
Tiers: HARD, TOUGH, PRODUCTION_SCENARIO, EXPERT_DEEP_DIVE
All compliant with the strict 10-point Content Quality Gatekeeper.
"""

def get_system_design_expansion_batch():
    return [
        {
            "title": "How does consistent hashing with virtual nodes prevent hot spots and data cascades during cluster scaling in distributed caches?",
            "difficulty": "HARD",
            "technology_slug": "system-design",
            "topic_slug": "sharding-consensus",
            "question_type": "CONCEPTUAL",
            "scenario_type": "SYSTEM_ARCHITECTURE",
            "short_answer": "Consistent hashing maps both node identifiers and cache keys onto a shared 32-bit or 64-bit circular ring; introducing multiple virtual nodes per physical machine uniformly distributes key ownership and limits data migration to 1/N of keys during node additions or removals.",
            "interview_ready_answer": "Standard modulo hashing (hash(key) % N) causes a complete cache thrash (nearly 100% key remap) whenever a server node joins or leaves. Consistent hashing solves this by arranging hash values on a logical circular ring (0 to 2^32 - 1). A key is assigned to the first server encountered moving clockwise. To prevent non-uniform distribution (hot spots), each physical server is represented by 100 to 200 'virtual nodes' positioned randomly along the ring. When a server fails, its keys are evenly distributed across all remaining physical servers rather than cascading onto a single neighbor.",
            "deep_explanation": "Under the hood, consistent hashing algorithms (like MurmurHash3 or Ketama) hash each physical node's name with an index (e.g. 'nodeA#1', 'nodeA#2') and store their positions in a sorted array or red-black tree (TreeMap in Java). Key lookup executes binary search (O(log(V*N))) to locate the ceiling entry on the ring. Without virtual nodes, standard deviation of assigned keys is high, causing memory skew. Virtual nodes leverage the Law of Large Numbers to smooth variance across the ring.",
            "architecture_notes": "Utilized in Amazon Dynamo, Apache Cassandra, and Discord's distributed caching infrastructure to achieve predictable O(1/N) redistribution.",
            "code_example": """import java.util.*;
public class ConsistentHashRing<T> {
    private final SortedMap<Integer, T> ring = new TreeMap<>();
    private final int virtualNodes;
    public ConsistentHashRing(int virtualNodes, Collection<T> nodes) {
        this.virtualNodes = virtualNodes;
        for (T node : nodes) addNode(node);
    }
    public void addNode(T node) {
        for (int i = 0; i < virtualNodes; i++) {
            ring.put((node.toString() + "#" + i).hashCode(), node);
        }
    }
    public T getNode(String key) {
        if (ring.isEmpty()) return null;
        int hash = key.hashCode();
        SortedMap<Integer, T> tail = ring.tailMap(hash);
        int target = tail.isEmpty() ? ring.firstKey() : tail.firstKey();
        return ring.get(target);
    }
}""",
            "why_interviewer_asks": "Evaluates candidate's understanding of horizontal scaling, partition tolerance, and load distribution mechanics under dynamic cluster membership.",
            "production_considerations": "Calibrate virtual node count (typically 150-250) based on memory overhead in client ring metadata vs key balance variance.",
            "failure_modes": "Inadequate virtual nodes cause severe storage imbalance where one physical machine runs out of memory while others remain 30% utilized.",
            "tradeoffs": "Provides minimal rebalancing churn (1/N keys remapped) at the cost of O(log K) routing lookup complexity and client-side ring topology synchronization.",
            "common_mistakes": [
                "Using standard modulo hashing (hash % N) for elastic distributed caches.",
                "Using too few virtual nodes (< 20), resulting in severe key clustering.",
                "Failing to replicate key ranges onto successor nodes when high availability is required."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "What happens to `hash(key) % N` when N changes from 10 to 9?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "How do virtual nodes spread a single physical server across multiple ring positions?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "What data structure allows finding the next clockwise node in O(log M) time?"}
            ],
            "sources": [
                {
                    "source_name": "Dynamo: Amazon's Highly Available Key-value Store",
                    "source_url": "https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf",
                    "publisher": "Amazon / ACM"
                }
            ],
            "followups": [
                {
                    "followup_question": "How does Google's Maglev hashing improve upon Ketama consistent hashing?",
                    "answer_guidance": "Maglev uses lookup tables generated via permutation arrays, achieving O(1) lookup time and uniform distribution without binary search on a ring."
                }
            ],
            "tags": ["System Design", "Distributed Systems", "Consistent Hashing", "Amazon", "Cassandra"]
        },
        {
            "title": "How does the Raft consensus algorithm guarantee log matching and leader completeness during network partitions?",
            "difficulty": "HARD",
            "technology_slug": "system-design",
            "topic_slug": "sharding-consensus",
            "question_type": "CONCEPTUAL",
            "scenario_type": "DISTRIBUTED_CONSENSUS",
            "short_answer": "Raft guarantees consistency through strict election rules where a candidate must possess all committed entries to win an election, combined with a leader-driven Log Matching Property that forces followers to overwrite uncommitted conflicting entries with the leader's log.",
            "interview_ready_answer": "Raft decomposes distributed consensus into Leader Election, Log Replication, and Safety. To guarantee Safety, Raft enforces the 'Leader Completeness Property': during an election, a follower votes for a candidate only if the candidate's log is at least as up-to-date as its own (measured by term first, then log length). Because any committed entry must reside on a majority (quorum) of nodes, and any winning leader must also receive votes from a majority, at least one node in the voting majority must contain all committed entries. Once elected, the leader dictates the log; if a follower's log diverges, the leader decrements `nextIndex` until a match is found and overwrites any conflicting follower entries.",
            "deep_explanation": "The Raft Log Matching Property establishes two invariants: 1. If two logs contain an entry with the same index and term, they store the same command. 2. If two logs contain an entry with the same index and term, then their logs are identical in all preceding entries. Leaders maintain `nextIndex[]` and `matchIndex[]` for every follower. During AppendEntries RPC, the leader includes `prevLogIndex` and `prevLogTerm`. If the follower finds no matching entry at `prevLogIndex`, it rejects the RPC. The leader decrements `nextIndex` and retries until consistency is restored, ensuring uncommitted entries from isolated terms are cleanly discarded.",
            "architecture_notes": "Raft powers etcd, HashiCorp Consul, and TiKV, underpinning the control plane of Kubernetes clusters worldwide.",
            "code_example": """# Raft AppendEntries RPC verification logic on follower:
def process_append_entries_rpc(term, leader_id, prev_log_index, prev_log_term, entries, leader_commit):
    if term < current_term:
        return False, current_term  # Reject stale leader
    reset_election_timer()
    # Log matching check:
    if len(log) <= prev_log_index or log[prev_log_index].term != prev_log_term:
        return False, current_term  # Reject mismatched log; leader will decrement nextIndex
    # Overwrite conflicts and append new entries:
    log = log[:prev_log_index + 1] + entries
    if leader_commit > commit_index:
        commit_index = min(leader_commit, len(log) - 1)
    return True, current_term""",
            "why_interviewer_asks": "Tests deep understanding of quorum intersections, split-brain prevention, and state machine replication mechanics in modern distributed databases.",
            "production_considerations": "Tune election timeouts (typically 150ms-300ms) with randomized jitter to prevent split votes, ensuring timeouts exceed network round-trip time.",
            "failure_modes": "In symmetric network partitions where no side achieves a quorum (e.g., 2 nodes vs 2 nodes in a 5-node cluster), the cluster becomes completely unavailable for writes.",
            "tradeoffs": "Raft delivers strict linearizability and high clarity over Multi-Paxos, but requires an odd number of nodes (2F+1) and incurs leader write bottlenecking.",
            "common_mistakes": [
                "Assuming Raft allows writes to commit when only a minority partition is active.",
                "Believing that an entry is safely committed before a majority of nodes have acknowledged disk persistence.",
                "Failing to randomize election timeouts, causing endless split-vote election loops."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How does the intersection of two majorities guarantee that at least one node knows all committed logs?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "What parameters in AppendEntries RPC allow a follower to detect log divergences?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Why does a candidate's log need to be compared before a peer casts its vote?"}
            ],
            "sources": [
                {
                    "source_name": "In Search of an Understandable Consensus Algorithm (Ongaro & Ousterhout)",
                    "source_url": "https://raft.github.io/raft.pdf",
                    "publisher": "Stanford University / USENIX"
                }
            ],
            "followups": [
                {
                    "followup_question": "What is the Joint Consensus mechanism in Raft used for?",
                    "answer_guidance": "Joint Consensus enables dynamic cluster membership reconfiguration (adding or removing nodes) without halting the cluster or risking dual-quorum split brains."
                }
            ],
            "tags": ["System Design", "Distributed Systems", "Raft", "Consensus", "Kubernetes", "etcd"]
        },
        {
            "title": "How does the Token Bucket rate limiting algorithm compare to the Leaky Bucket algorithm under bursty API traffic?",
            "difficulty": "HARD",
            "technology_slug": "system-design",
            "topic_slug": "api-gateway-resilience",
            "question_type": "CONCEPTUAL",
            "scenario_type": "API_GATEWAY",
            "short_answer": "Token Bucket allows traffic bursts up to bucket capacity while enforcing a long-term average rate, whereas Leaky Bucket smooths outgoing traffic at a strictly constant rate regardless of incoming burst volume.",
            "interview_ready_answer": "Both Token Bucket and Leaky Bucket are core rate limiting algorithms, but they serve fundamentally different egress requirements. Token Bucket holds tokens generated at a fixed rate `r` up to capacity `C`. A burst of up to `C` requests can be processed immediately without delay if sufficient tokens exist. Leaky Bucket queues incoming requests in a FIFO buffer and releases them at a strictly constant rate (like water dripping from a punctured bucket). For user-facing Web APIs, Token Bucket is preferred because users expect rapid page loads during momentary bursts. For downstream rate-limited third-party APIs (like payment gateways), Leaky Bucket is optimal to prevent downstream queue saturation.",
            "deep_explanation": "Under the hood, Token Bucket does not require background timer threads to replenish tokens. In high-performance implementations (like Envoy or Redis Lua scripts), it calculates token replenishment lazily upon request arrival: `tokens = min(capacity, current_tokens + (now - last_refill_time) * refill_rate)`. This requires only two numeric state variables per user: `tokens` and `last_updated`, enabling microsecond latency in distributed Redis clusters. Leaky Bucket, conversely, requires a physical queue data structure; if the queue fills, incoming requests are dropped or rejected with HTTP 429.",
            "architecture_notes": "Implemented in Envoy Proxy, Kong Gateway, AWS API Gateway, and Cloudflare Edge Workers.",
            "code_example": """import time
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill = time.time()
    def allow_request(self, tokens_needed: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True
        return False""",
            "why_interviewer_asks": "Evaluates candidate's knowledge of traffic shaping, edge resilience, and memory-efficient algorithm design for distributed gateways.",
            "production_considerations": "When implementing in Redis for distributed clusters, execute the check-and-decrement logic within an atomic Lua script to prevent race conditions across gateway nodes.",
            "failure_modes": "In distributed environments without atomic Lua scripts, concurrent requests from multiple gateway nodes observe stale token counts, allowing 2x-5x burst volume past rate limits.",
            "tradeoffs": "Token Bucket provides low latency and accommodates natural user bursts, but can stress backend services during sudden full-bucket spikes.",
            "common_mistakes": [
                "Using background tick threads to update millions of user buckets instead of lazy timestamp delta math.",
                "Using Leaky Bucket for interactive web users, causing artificial latency delays on legitimate bursty page navigations.",
                "Failing to execute Redis read-modify-write operations inside atomic Lua scripts."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How do the two algorithms treat a sudden spike of 50 requests coming in the same millisecond?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Why is lazy mathematical replenishment far more scalable than background timer tasks?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "How do you synchronize token counts across 20 API gateway instances sharing Redis?"}
            ],
            "sources": [
                {
                    "source_name": "Envoy Proxy: Rate Limit Architecture",
                    "source_url": "https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_features/global_rate_limiting",
                    "publisher": "Envoy / CNCF"
                }
            ],
            "followups": [
                {
                    "followup_question": "What is the Sliding Window Counter algorithm and why is it used over Fixed Window Counter?",
                    "answer_guidance": "Fixed Window counters allow 2x the rate limit at window boundaries (e.g. at 00:59 and 01:01); Sliding Window Counter calculates an estimate based on the overlap percentage of the previous and current window, eliminating boundary bursts with minimal memory."
                }
            ],
            "tags": ["System Design", "API Gateway", "Rate Limiting", "Envoy", "Redis", "Cloudflare"]
        },
        {
            "title": "How do you design a Distributed Tracing architecture across 500 microservices using OpenTelemetry and W3C TraceContext?",
            "difficulty": "TOUGH",
            "technology_slug": "system-design",
            "topic_slug": "api-gateway-resilience",
            "question_type": "CONCEPTUAL",
            "scenario_type": "SYSTEM_ARCHITECTURE",
            "short_answer": "Distributed tracing injects W3C TraceContext headers (`traceparent`, `tracestate`) at the API Gateway and propagates them across HTTP, gRPC, and messaging boundaries, transmitting sampled spans via OpenTelemetry collectors to a distributed storage backend like Jaeger or ClickHouse.",
            "interview_ready_answer": "In large-scale microservice architectures, diagnosing high-latency requests requires distributed context propagation. When an external request hits the API Gateway, the gateway generates a 128-bit `trace_id` and a 64-bit `span_id`. These are encoded into standard W3C `traceparent` headers (`00-{trace_id}-{parent_id}-{trace_flags}`). As requests traverse service boundaries via HTTP headers, gRPC metadata, or Kafka message headers, each service reads the parent span, generates its own child span, and asynchronously exports span telemetry via OpenTelemetry Collector agents over OTLP/gRPC. To handle billions of daily spans without overwhelming storage, adaptive head-based or tail-based sampling is applied.",
            "deep_explanation": "Head-based sampling makes sampling decisions at the ingress gateway based on consistent hashing of the `trace_id` (e.g. sample 1% of traffic). While computationally cheap, it frequently misses rare errors and high-latency anomalies occurring deep in the call graph. Tail-based sampling routes all spans through an OpenTelemetry Collector cluster that buffers complete traces in memory. If any span within the trace records an HTTP 5xx error or latency exceeding SLA (e.g., > 1000ms), the collector retains 100% of the trace and discards nominal traces, maximizing diagnostic value per byte stored.",
            "architecture_notes": "Complies strictly with W3C Trace Context specification and OpenTelemetry standards (OTel v1.30+).",
            "code_example": """# W3C TraceParent Header Format:
# version-trace_id-parent_span_id-trace_flags
# 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01

from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = trace.get_tracer(__name__)

def make_downstream_call(headers: dict):
    with tracer.start_as_current_span("order-processing") as span:
        # Inject current span context into outgoing HTTP headers:
        TraceContextTextMapPropagator().inject(headers)
        span.set_attribute("http.status_code", 200)
        # Outgoing request now carries traceparent header downstream""",
            "why_interviewer_asks": "Evaluates candidate's experience with large-scale observability, protocol headers, asynchronous telemetry pipelines, and trace sampling trade-offs.",
            "production_considerations": "Deploy OpenTelemetry Collector as a local daemonset or sidecar to avoid application thread blocking during telemetry flushing.",
            "failure_modes": "Unsampled tracing in high-throughput systems generates terabytes of telemetry per hour, exhausting network bandwidth and causing Jaeger/Elasticsearch cluster crashes.",
            "tradeoffs": "Delivers end-to-end visibility and bottleneck localization across polyglot microservices, but adds 1-2ms serialization overhead and network transport bandwidth.",
            "common_mistakes": [
                "Dropping trace headers when forwarding messages through asynchronous message brokers like Kafka or RabbitMQ.",
                "Using 100% head-based sampling in high-throughput production clusters.",
                "Failing to scrub PII (passwords, credit cards) from span attributes and tags."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How do downstream microservices know they belong to the same originating user request?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "What is the standard W3C header used to propagate trace and span identifiers?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "What is the difference between head-based sampling and tail-based sampling?"}
            ],
            "sources": [
                {
                    "source_name": "W3C Recommendation: Trace Context",
                    "source_url": "https://www.w3.org/TR/trace-context/",
                    "publisher": "World Wide Web Consortium (W3C)"
                }
            ],
            "followups": [
                {
                    "followup_question": "How does tail-based sampling handle spans arriving out-of-order or delayed from asynchronous background workers?",
                    "answer_guidance": "Tail-based collectors use sliding time windows (e.g. 30 seconds) grouped by trace_id before evaluating sampling rules and committing to storage."
                }
            ],
            "tags": ["System Design", "Observability", "OpenTelemetry", "Distributed Tracing", "Microservices"]
        },
        {
            "title": "Production Incident: A database partition rebalancing operation causes cascading timeouts and connection pool exhaustion across 40 microservices. How do you mitigate and architect graceful rebalancing?",
            "difficulty": "PRODUCTION_SCENARIO",
            "technology_slug": "system-design",
            "topic_slug": "sharding-consensus",
            "question_type": "SCENARIO_BASED",
            "scenario_type": "PRODUCTION_INCIDENT",
            "short_answer": "Mitigate by applying client-side circuit breakers, throttling partition migration rates via token-bucket bandwidth limiters, and routing queries through an intelligent proxy layer that buffers requests for migrating partitions rather than exhausting database connections.",
            "interview_ready_answer": "During partition rebalancing (e.g. in Cassandra, Vitess, or MongoDB), data migration saturates server I/O and network bandwidth. When database query latencies spike from 5ms to 10s, client microservices hold connection pool slots waiting for responses. Within minutes, connection pools across all 40 microservices exhaust, causing cascading HTTP 504 gateway failures. Immediate mitigation: 1. Throttle or pause the rebalancing migration job. 2. Enable circuit breakers (Resilience4j/Envoy) to fast-fail non-essential queries. 3. Architectural fix: Enforce migration rate-limiting (e.g., max 20MB/s per node), use dual-writing with shadow reads during transitions, and deploy a connection-pooling proxy (like ProxySQL or PgBouncer) to absorb connection spikes.",
            "deep_explanation": "When partitions move between nodes, two major anti-patterns emerge: CPU/disk bandwidth saturation from bulk data transfers, and locking on shard routing tables. In distributed architectures, rebalancing must follow a multi-phase state machine: 1. Catch-Up Phase: Replicate existing partition data in background without locking. 2. Delta Catch-Up: Stream CDC change events to bring destination replica within milliseconds of source. 3. Cut-Over: Atomically flip routing metadata with a sub-second freeze. If the migration pipeline lacks rate limiting, disk queue depth explodes, causing read queries to queue behind multi-gigabyte file transfers.",
            "architecture_notes": "Implemented in Vitess VReplication, CockroachDB range splitting, and Apache Kafka partition reassignment throttle.",
            "code_example": """# Throttling migration bandwidth in distributed partition managers:
class PartitionRebalancer:
    def __init__(self, max_bytes_per_sec: int = 20 * 1024 * 1024):
        self.rate_limiter = TokenBucket(capacity=max_bytes_per_sec, refill_rate=max_bytes_per_sec)
    def migrate_chunk(self, chunk_data: bytes, dest_node):
        chunk_size = len(chunk_data)
        # Block until bandwidth token is available:
        while not self.rate_limiter.allow_request(chunk_size):
            time.sleep(0.05)
        dest_node.write_chunk(chunk_data)  # Safe, throttled migration!""",
            "why_interviewer_asks": "Evaluates candidate's real-world operational maturity, triage capabilities under severe production outages, and mastery of distributed data migration patterns.",
            "production_considerations": "Always configure partition rebalancing to execute during off-peak hours with automated pause triggers linked to P99 latency alerts.",
            "failure_modes": "Unbounded background migration consumes all storage IOPS, causing primary database heartbeat timeouts, false failover triggers, and split-brain scenarios.",
            "tradeoffs": "Throttling migration rate extends rebalance duration from hours to days, but guarantees zero degradation of customer-facing SLA.",
            "common_mistakes": [
                "Running partition reassignments at full speed during business hours without bandwidth throttling.",
                "Configuring microservice database connection pool timeouts to 30+ seconds instead of fast-failing in 2-3 seconds.",
                "Failing to provide backpressure metrics to the migration controller."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Why did query latency spikes cause connection pools to exhaust across all microservices?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "How can background data migration bandwidth be capped using token buckets?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "What is the three-phase state machine for safe partition cut-overs?"}
            ],
            "sources": [
                {
                    "source_name": "Vitess Documentation: VReplication Architecture",
                    "source_url": "https://vitess.io/docs/concepts/vreplication/",
                    "publisher": "Vitess Community / CNCF"
                }
            ],
            "followups": [
                {
                    "followup_question": "How does CockroachDB Range Leasing prevent read stale data during range splits and rebalancing?",
                    "answer_guidance": "CockroachDB uses single-leaseholders per range; all reads and writes route strictly through the leaseholder, which coordinates with Raft before transferring the lease."
                }
            ],
            "tags": ["System Design", "Production Incident", "Database Sharding", "Vitess", "Cassandra", "PostgreSQL"]
        }
    ]
