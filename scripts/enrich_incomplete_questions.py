import sqlite3
import json

ENRICHMENTS = {
    "java-fresher-l1-equals-vs-double-equals": {
        "production_considerations": "In production Java applications, always use Objects.equals(a, b) to safeguard against NullPointerException when comparing potentially null references. For custom domain entities, ensure both equals() and hashCode() are consistently overridden to prevent silent failures when instances are used as keys in HashMaps or elements in HashSets.",
        "failure_modes": "Comparing two newly allocated Strings or boxed primitives with '==' instead of equals() causes subtle bugs where code passes unit tests with small interned values (e.g., Integer values between -128 and 127) but fails in production when larger numbers or dynamically created Strings from network payloads are compared.",
        "tradeoffs": "'==' is a single CPU instruction comparing memory addresses (extremely fast, zero allocation), whereas equals() requires method invocation, type-checking, and field-by-field comparisons. For performance-critical loops on primitive wrappers, prefer unboxing or identity checks only when guaranteed interned.",
        "common_mistakes": json.dumps([
            "Using '==' to compare Strings received from external API payloads or database queries.",
            "Overriding equals() without overriding hashCode(), breaking HashMap and HashSet lookup contracts.",
            "Calling str.equals(\"CONSTANT\") instead of \"CONSTANT\".equals(str), exposing the code to NullPointerExceptions."
        ])
    },
    "java-fresher-l1-arraylist-vs-linkedlist": {
        "production_considerations": "In modern production Java running on modern x86/ARM CPU architectures, ArrayList should almost always be preferred over LinkedList. CPU L1/L2 cache prefetching favors contiguous arrays heavily. LinkedList allocates a separate Node object per element (24-32 bytes overhead per node in 64-bit JVM), causing high memory fragmentation and poor cache locality.",
        "failure_modes": "Using LinkedList for random access by index (e.g. in a loop calling list.get(i)) converts an O(N) loop into an O(N^2) catastrophic performance degradation that can freeze production threads.",
        "tradeoffs": "ArrayList offers O(1) random access and minimal memory overhead with fast iteration, but incurs O(N) array copy cost during capacity expansion or insertions in the middle. LinkedList offers O(1) insertion/deletion once an iterator is positioned, but has severe pointer chasing and memory overhead.",
        "common_mistakes": json.dumps([
            "Assuming LinkedList is always faster for frequent insertions without measuring CPU cache-line misses.",
            "Iterating through a LinkedList using an indexed for-loop (list.get(i)) instead of an enhanced for-loop or Iterator.",
            "Failing to pre-size ArrayList when expected collection size is known, causing repeated array allocations and System.arraycopy calls."
        ])
    },
    "langgraph-fresher-l1-what-is-token-and-tokenization": {
        "production_considerations": "Production LLM applications must track token consumption per prompt and completion to prevent context window overflow (400 Bad Request) and runaway billing. Always use lightweight tokenizer libraries (like tiktoken for OpenAI or sentencepiece/byte-pair encoders) locally to measure token budgets before dispatching API calls.",
        "failure_modes": "Exceeding the model's maximum context length causes truncation or API rejection. Additionally, character-to-token ratio shifts dramatically across non-English scripts, code, and structured JSON, causing unexpected latency and latency budget spikes.",
        "tradeoffs": "Sub-word tokenizers (BPE, WordPiece) strike an optimal balance between vocabulary size (typically 32k-128k tokens) and sequence length. Smaller token vocabularies increase sequence lengths and inference latency, while huge vocabularies increase embedding table size.",
        "common_mistakes": json.dumps([
            "Estimating tokens simply as 1 word = 1 token (special characters, whitespace, and non-English text consume significantly more tokens).",
            "Failing to enforce max_tokens limit on user input before passing it to downstream agents.",
            "Neglecting system prompt and conversation history tokens in dynamic agent loops."
        ])
    },
    "rag-fresher-l1-what-is-vector-embedding": {
        "production_considerations": "In enterprise RAG, embedding model versioning is critical. Every document in the vector database and every search query must be embedded using the exact same model and dimension (e.g. text-embedding-3-small at 1536 dims). Upgrading an embedding model requires a full re-indexing of the entire corpus.",
        "failure_modes": "Querying a vector database with embeddings generated from a different model or tokenizer produces garbage similarity scores, leading to completely irrelevant context retrieval and subsequent LLM hallucinations.",
        "tradeoffs": "Higher-dimensional embeddings (e.g., 1536 or 3072 dims) capture nuanced semantic relationships but increase RAM requirements and distance calculation latency linearly. Dimension reduction (Matryoshka Representation Learning) allows truncation with minimal accuracy loss.",
        "common_mistakes": json.dumps([
            "Assuming vector similarity guarantees factual truth (vector search finds semantic relatedness, not factual accuracy).",
            "Using Euclidean distance when the index is built for Cosine similarity or inner product (Dot Product).",
            "Failing to normalize vectors before indexing when using dot-product similarity metrics."
        ])
    },
    "system-design-fresher-l1-client-server-and-http-basics": {
        "production_considerations": "Production client-server systems require HTTP/2 or HTTP/3 (QUIC) multiplexing, TLS 1.3 termination at reverse proxies/load balancers, keep-alive connection reuse, and comprehensive HTTP response headers (Cache-Control, Content-Security-Policy, HSTS) to ensure security and latency SLAs.",
        "failure_modes": "Connection starvation occurs when clients fail to reuse TCP/TLS connections or connection pools are misconfigured. Insecure plaintext HTTP endpoints risk man-in-the-middle attacks, credential snooping, and session hijacking.",
        "tradeoffs": "HTTPS adds a cryptographic handshake overhead (typically 1-2 RTTs on initial connect) and small CPU overhead for AES/ChaCha encryption compared to raw HTTP, but provides non-negotiable confidentiality, integrity, and client trust.",
        "common_mistakes": json.dumps([
            "Creating a new HTTP client connection for every request instead of utilizing a shared connection pool.",
            "Returning HTTP 200 OK with an error payload in the response body instead of standard 4xx/5xx HTTP status codes.",
            "Neglecting strict HSTS headers, leaving mobile/web clients vulnerable to protocol downgrade attacks."
        ])
    },
    "java-mid-l2-concurrenthashmap-internal-mechanics": {
        "production_considerations": "In high-throughput Java microservices, ConcurrentHashMap provides lock-free volatile reads and bin-level synchronization. For atomic updates, always use atomic methods like computeIfAbsent(), merge(), or getAndUpdate() rather than manual containsKey() followed by put(), which creates race conditions.",
        "failure_modes": "Calling size() or isEmpty() on ConcurrentHashMap provides an eventually consistent snapshot, not an atomic instantaneous count. Relying on size() in concurrency control logic leads to subtle race conditions.",
        "tradeoffs": "Java 8+ ConcurrentHashMap replaced the 16-segment lock design with lock-free CAS on the first node of each bin, falling back to synchronized on only the single head node. This minimizes lock contention from O(Segments) to O(Bins), while keeping memory footprint identical to standard HashMap.",
        "common_mistakes": json.dumps([
            "Writing check-then-act idioms like `if (!map.containsKey(k)) map.put(k, v);` instead of `map.computeIfAbsent(k, ...)`, introducing race conditions.",
            "Putting null keys or values into ConcurrentHashMap, which throws NullPointerException by design.",
            "Performing long-running IO or blocking tasks inside computeIfAbsent lambdas, blocking other threads accessing the same hash bucket."
        ])
    },
    "java-mid-l2-virtual-threads-vs-platform-threads": {
        "production_considerations": "Virtual Threads (Project Loom) in Java 21+ excel at synchronous, blocking I/O (HTTP calls, JDBC database queries, file access). Do NOT pool Virtual Threads; allocate them per task using Executors.newVirtualThreadPerTaskExecutor(). Beware of 'thread pinning' when blocking inside `synchronized` blocks or native methods.",
        "failure_modes": "Thread pinning occurs when a Virtual Thread executes a synchronized block or method and performs blocking I/O, preventing the carrier thread from being unmounted. This exhausts carrier worker threads in ForkJoinPool, causing application-wide starvation.",
        "tradeoffs": "Virtual Threads drastically simplify concurrency by preserving clean synchronous code styles while scaling to millions of threads, but they do NOT speed up CPU-bound operations and require replacing legacy `synchronized` with `ReentrantLock` for blocking code paths.",
        "common_mistakes": json.dumps([
            "Pooling Virtual Threads using thread pool executors instead of spawning them per request.",
            "Using Virtual Threads for compute-intensive tasks (e.g. cryptographic hashing, image processing), where they offer no throughput advantage over platform threads.",
            "Performing blocking socket I/O inside synchronized blocks or legacy libraries that cause carrier thread pinning."
        ])
    },
    "langgraph-mid-l2-stategraph-memory-checkpointer": {
        "production_considerations": "In production LangGraph agents, state persistence must use durable checkpointers (e.g. PostgresSaver or RedisSaver) keyed by `thread_id`. Ensure state schemas are versioned and serialize cleanly to JSON, and configure state TTLs to prevent unbounded database table growth.",
        "failure_modes": "Using the in-memory `MemorySaver` in a multi-pod Kubernetes deployment causes split-brain state where subsequent user interactions hit a pod without the conversation history, resulting in loss of agent context and repeated questions.",
        "tradeoffs": "Writing checkpoints on every node transition ensures fault tolerance, time-travel debugging, and human-in-the-loop resumption, but introduces write latency (5-20ms per step depending on DB latency). Batching or selective checkpointing can be tuned for high-speed flows.",
        "common_mistakes": json.dumps([
            "Using default in-memory checkpointer across distributed multi-instance container environments.",
            "Storing non-serializable objects (such as open network sockets or active file handles) directly in the AgentState.",
            "Forgetting to pass thread_id in runnable config, causing state to fail to persist across conversation turns."
        ])
    },
    "rag-mid-l2-hnsw-indexing-mechanics": {
        "production_considerations": "HNSW (Hierarchical Navigable Small World) provides logarithmic search complexity by constructing multi-layer graphs. In production, parameter tuning of `M` (max connections per node, typically 16-64) and `efConstruction` (size of candidate list during index build, 100-200) governs memory consumption and query recall. Index build requires significant RAM.",
        "failure_modes": "HNSW indexes reside primarily in memory; running out of RAM causes the vector engine (or container) to OOM crash. Dynamic deletions without vacuuming/compaction create 'tombstone' nodes that degrade recall and waste memory.",
        "tradeoffs": "HNSW achieves 95-99% recall with sub-millisecond query latency, outperforming IVF-PQ on raw speed, but has a 1.5x-2x higher memory overhead and slower insert/re-indexing times compared to inverted file approaches.",
        "common_mistakes": json.dumps([
            "Setting `efSearch` too low during query time, sacrificing recall to save a fraction of a millisecond.",
            "Underestimating the RAM requirements for high-dimension vectors (e.g., 1M vectors of 1536-dim floats require ~8-12GB RAM for HNSW).",
            "Failing to use quantization (Scalar or Product Quantization) when vector scale exceeds server memory budgets."
        ])
    },
    "system-design-mid-l2-cache-aside-pattern-redis": {
        "production_considerations": "Cache-Aside requires a robust dual-layer strategy: on cache miss, acquire a distributed mutex (or single-flight lock) before reading from the DB to prevent cache stampede. Apply jittered TTLs (e.g., base TTL ± 10% random offset) to prevent simultaneous bulk key expiration.",
        "failure_modes": "A sudden expiration of a hot key (or cache flush) causes hundreds of concurrent requests to hit the database simultaneously (Thundering Herd / Cache Stampede), spiking database CPU to 100% and triggering cascading service outages.",
        "tradeoffs": "Cache-Aside handles arbitrary data models gracefully and guarantees the database survives if Redis goes down, but introduces latency on cache misses and requires explicit cache invalidation logic on database writes.",
        "common_mistakes": json.dumps([
            "Updating the cache first and the database second, which risks silent data inconsistency if the DB write fails.",
            "Setting identical static TTLs for thousands of keys populated during batch runs, setting up future synchronized cache stampedes.",
            "Not handling Redis connection timeouts gracefully with a fallback circuit breaker, letting Redis latency drag down the entire service."
        ])
    }
}

def main():
    conn = sqlite3.connect('backend/breakthecode.db')
    cursor = conn.cursor()

    updated = 0
    for slug, data in ENRICHMENTS.items():
        cursor.execute("""
            UPDATE questions
            SET production_considerations = ?,
                failure_modes = ?,
                tradeoffs = ?,
                common_mistakes = ?
            WHERE slug = ?
        """, (
            data["production_considerations"],
            data["failure_modes"],
            data["tradeoffs"],
            data["common_mistakes"],
            slug
        ))
        if cursor.rowcount > 0:
            updated += 1
            print(f"Enriched: {slug}")

    conn.commit()
    conn.close()
    print(f"\nSuccessfully enriched {updated} questions!")

if __name__ == "__main__":
    main()
