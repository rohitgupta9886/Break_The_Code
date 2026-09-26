"""
High-Caliber Expansion for Java & JVM Concurrency
Provides authentic, deep questions across:
- executors-concurrency-utils
- virtual-threads-loom
- jvm-memory-gc
- jmm-synchronization
All passing the strict 10-point gatekeeper and deduplication engine.
"""

def get_java_expansion_batch():
    return [
        {
            "title": "How does the CopyOnWriteArrayList collection achieve thread-safe iteration without locking, and what are its performance trade-offs?",
            "difficulty": "MEDIUM",
            "technology_slug": "java-backend",
            "topic_slug": "jmm-synchronization",
            "question_type": "CONCEPTUAL",
            "scenario_type": "CONCURRENCY_MECHANICS",
            "short_answer": "CopyOnWriteArrayList creates a fresh copy of the underlying array on every write operation (add, set, remove), allowing reader threads to iterate through an immutable array snapshot without locks or ConcurrentModificationException.",
            "interview_ready_answer": "CopyOnWriteArrayList is designed for read-heavy, write-rare scenarios like event listener registries. Whenever a write occurs, the collection acquires an internal ReentrantLock, copies the entire existing array to a new array of size N+1, performs the mutation, and atomically updates the volatile array reference. Readers access the volatile array directly without acquiring any lock, guaranteeing fast, lock-free iteration over an immutable snapshot.",
            "deep_explanation": "Under the hood, CopyOnWriteArrayList maintains a single `private transient volatile Object[] array`. Because the array reference is volatile and the array itself is never mutated in-place, reading operations require no synchronization and will never throw ConcurrentModificationException. The iterator operates on a point-in-time snapshot of the array taken when the iterator was constructed. The critical trade-off is write cost: every mutation performs an O(N) memory copy and array allocation.",
            "architecture_notes": "Implemented in java.util.concurrent with a volatile array reference and ReentrantLock for mutating operations.",
            "code_example": """import java.util.concurrent.CopyOnWriteArrayList;
public class ListenerRegistry {
    private final CopyOnWriteArrayList<String> listeners = new CopyOnWriteArrayList<>();
    public void register(String listener) {
        listeners.add(listener); // Synchronized copy of array
    }
    public void notifyAllListeners() {
        for (String l : listeners) { // 100% Lock-free snapshot iteration!
            System.out.println("Notifying: " + l);
        }
    }
}""",
            "why_interviewer_asks": "Evaluates candidate's understanding of copy-on-write semantics, lock-free read trade-offs, and memory implications.",
            "production_considerations": "Never use CopyOnWriteArrayList in write-intensive pathways (e.g. streaming ingest); use ConcurrentLinkedQueue or Collections.synchronizedList instead.",
            "failure_modes": "Calling add() in a loop with 100,000 items creates 100,000 array copies and gigabytes of garbage, triggering severe memory thrashing and GC storms.",
            "tradeoffs": "Delivers lock-free, zero-latency reads and snapshot consistency at the cost of O(N) array allocation overhead on every write.",
            "common_mistakes": [
                "Using CopyOnWriteArrayList for high-frequency write operations.",
                "Attempting to modify the list via Iterator.remove() (throws UnsupportedOperationException by design).",
                "Assuming modifications made after iterator creation will be visible in the current iteration."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How can reads be completely lock-free if writers never mutate the existing array in-place?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Notice how the internal array reference is declared volatile."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "What is the Big-O time and space complexity of adding 10,000 elements one-by-one?"}
            ],
            "sources": [
                {
                    "source_name": "Oracle Java SE 21: CopyOnWriteArrayList",
                    "source_url": "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CopyOnWriteArrayList.html",
                    "publisher": "Oracle Corporation"
                }
            ],
            "followups": [
                {
                    "followup_question": "Why does CopyOnWriteArrayList's iterator throw UnsupportedOperationException on remove()?",
                    "answer_guidance": "Because the iterator traverses a fixed immutable snapshot; mutating the snapshot would contradict the copy-on-write design."
                }
            ],
            "tags": ["Java", "Collections", "Concurrency", "Netflix", "Amazon"]
        },
        {
            "title": "How does the HotSpot JVM JIT compiler perform Escape Analysis and Scalar Replacement to eliminate heap allocations?",
            "difficulty": "HARD",
            "technology_slug": "java-backend",
            "topic_slug": "jvm-memory-gc",
            "question_type": "CONCEPTUAL",
            "scenario_type": "JVM_INTERNALS",
            "short_answer": "Escape Analysis determines if an allocated object escapes its creating method or thread; if an object does not escape, the C2 compiler applies Scalar Replacement, dismantling the object into primitive variables stored directly in CPU registers or on the stack.",
            "interview_ready_answer": "In the HotSpot JVM, the C2 JIT compiler analyzes bytecode data flow to determine an object's escape state: NoEscape, ArgEscape, or GlobalEscape. When an object has NoEscape (it is never returned, stored in a field, or passed to non-inlined methods), the compiler applies Scalar Replacement. Instead of allocating the object header and fields on the heap, the compiler treats the object's fields as independent scalar variables, mapping them directly to CPU registers or stack frames. This completely eliminates heap allocation and garbage collection overhead for temporary objects.",
            "deep_explanation": "Scalar replacement is one of the most powerful JVM performance optimizations. Beyond scalar replacement, Escape Analysis enables Lock Elision: if an object never escapes the allocating thread, synchronized blocks on that object are completely removed because no other thread could ever contend for the monitor. Furthermore, consecutive synchronized blocks on the same monitor are merged via Lock Coarsening to minimize monitor acquisition overhead. For escape analysis to succeed, method inlining is a prerequisite; if a method cannot be inlined due to exceeding the bytecode size threshold, escape analysis fails.",
            "architecture_notes": "Implemented in HotSpot C2 optimizer; inspectable via `-XX:+PrintEscapeAnalysis` and `-XX:+PrintEliminateAllocations`.",
            "code_example": """public class EscapeAnalysisDemo {
    public int calculateCoordinateDistance() {
        // Point does NOT escape this method!
        // C2 decomposes Point into two primitive ints (x and y) in CPU registers!
        Point p = new Point(15, 25);
        return p.x * 2 + p.y * 3;
    }
    private static class Point {
        int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}""",
            "why_interviewer_asks": "Evaluates candidate's understanding of JIT compilation, compiler optimizations, and JVM memory allocation mechanics.",
            "production_considerations": "Keep hot methods small and cohesive (< 325 bytes of bytecode) so the JIT inlines them, allowing escape analysis to dismantle temporary objects.",
            "failure_modes": "Assigning temporary objects to instance fields or returning them defeats escape analysis, forcing heap allocation and creating GC pressure.",
            "tradeoffs": "Escape analysis significantly accelerates execution and reduces heap pressure, but increases JIT compilation time during warmup.",
            "common_mistakes": [
                "Assuming every 'new' keyword in Java strictly allocates heap memory (scalar replacement eliminates heap allocation).",
                "Writing monolithic methods that exceed the JIT inlining threshold, disabling escape analysis.",
                "Believing that Escape Analysis moves objects to the stack (it actually breaks objects into scalar primitives)."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "What happens if an object is created, used, and discarded entirely within a single method?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "How does the JIT compiler represent object fields without instantiating the object header?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Why is method inlining necessary before escape analysis can occur?"}
            ],
            "sources": [
                {
                    "source_name": "HotSpot Virtual Machine JIT Compiler Architecture",
                    "source_url": "https://wiki.openjdk.org/display/HotSpot/EscapeAnalysis",
                    "publisher": "OpenJDK Community"
                }
            ],
            "followups": [
                {
                    "followup_question": "What is the difference between NoEscape, ArgEscape, and GlobalEscape?",
                    "answer_guidance": "NoEscape is method-confined; ArgEscape escapes the method as an argument but not the thread; GlobalEscape escapes to other threads or heap fields."
                }
            ],
            "tags": ["Java", "JIT", "JVM", "Performance", "Google", "Meta"]
        },
        {
            "title": "How does the LongAccumulator class generalize LongAdder with custom binary accumulation functions in Java concurrency?",
            "difficulty": "HARD",
            "technology_slug": "java-backend",
            "topic_slug": "executors-concurrency-utils",
            "question_type": "CONCEPTUAL",
            "scenario_type": "CONCURRENCY_MECHANICS",
            "short_answer": "LongAccumulator extends the Striped64 cell architecture of LongAdder to support arbitrary, commutative binary operations (e.g. max, min, multiplication) across concurrent threads without locks.",
            "interview_ready_answer": "While LongAdder is restricted strictly to addition, LongAccumulator generalizes the lock-free Striped64 architecture to any associative, commutative binary function via `LongBinaryOperator`. By supplying a lambda like `Long::max` or `(x, y) -> x * y`, multiple threads update distributed, cache-line padded cells concurrently. When `get()` is called, the accumulator combines the identity value with all cell values using the supplied binary operator, achieving tens of millions of ops/sec under contention.",
            "deep_explanation": "Under the hood, LongAccumulator inherits from `java.util.concurrent.atomic.Striped64`. It maintains a base value and an array of `Cell` objects padded with `@jdk.internal.vm.annotation.Contended` to prevent CPU cache-line false sharing. When a thread calls `accumulate(x)`, it first attempts CAS on the base value. If contention occurs, it hashes the thread probe to a cell in the array and applies the binary operator via CAS on that cell. Because the operation is mathematically associative and commutative, the order in which cells are aggregated during `get()` produces a deterministic final result.",
            "architecture_notes": "Implemented in java.util.concurrent.atomic, extending Striped64 with customizable LongBinaryOperator lambdas.",
            "code_example": """import java.util.concurrent.atomic.LongAccumulator;
public class ConcurrentMaxTracker {
    // Tracks maximum latency across threads lock-free!
    private final LongAccumulator maxLatency = 
        new LongAccumulator(Long::max, 0L);

    public void recordLatency(long latencyMs) {
        maxLatency.accumulate(latencyMs); // High-throughput lock-free update
    }

    public long getMaxLatency() {
        return maxLatency.get(); // Aggregates base and striped cells
    }
}""",
            "why_interviewer_asks": "Evaluates candidate's depth with advanced java.util.concurrent primitives beyond basic AtomicLong.",
            "production_considerations": "Ensure the supplied LongBinaryOperator is strictly associative and commutative (order of operations must not alter the mathematical result).",
            "failure_modes": "Supplying a non-associative operator (like subtraction or division) produces non-deterministic, corrupted results under concurrent execution.",
            "tradeoffs": "Provides extreme multi-core scalability for custom aggregations, but consumes more memory than single-variable atomics.",
            "common_mistakes": [
                "Supplying non-commutative binary functions like subtraction.",
                "Expecting LongAccumulator.get() to return an instantaneous linearizable snapshot during concurrent updates.",
                "Using synchronized blocks for maximum tracking when LongAccumulator is available."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How can you track the running maximum across 100 concurrent threads without lock contention?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Look at the Striped64 base class shared with LongAdder."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Why must the accumulation operator be associative and commutative?"}
            ],
            "sources": [
                {
                    "source_name": "Oracle Java SE 21: LongAccumulator",
                    "source_url": "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/LongAccumulator.html",
                    "publisher": "Oracle Corporation"
                }
            ],
            "followups": [
                {
                    "followup_question": "Why is subtraction an illegal operator for LongAccumulator?",
                    "answer_guidance": "Subtraction is neither associative nor commutative ((a - b) - c != a - (b - c)), making cell reduction order non-deterministic."
                }
            ],
            "tags": ["Java", "Concurrency", "Atomics", "Stripe", "Uber"]
        },
        {
            "title": "How does the HotSpot JVM implement Biased Locking and why was it deprecated and disabled in modern Java?",
            "difficulty": "TOUGH",
            "technology_slug": "java-backend",
            "topic_slug": "jmm-synchronization",
            "question_type": "CONCEPTUAL",
            "scenario_type": "JVM_INTERNALS",
            "short_answer": "Biased locking eliminated atomic CAS instructions for uncontended single-threaded locks by recording the thread ID in the object header, but was deprecated in Java 15 because revocations required expensive global Stop-The-World safepoints.",
            "interview_ready_answer": "Biased locking (introduced in Java 6) was optimized for legacy applications (like Vector and Hashtable) where a single thread repeatedly acquired the same lock. It recorded the thread ID in the object's Mark Word; subsequent locks by the same thread executed with zero CAS instructions. However, if another thread contended for the object, the lock had to be revoked. Revocation was notoriously expensive: the JVM had to force a global Stop-The-World safepoint, inspect thread stacks, and re-write the header. In modern reactive and thread-pool architectures, revocation costs vastly exceeded the savings, leading to its deprecation in Java 15 (JEP 374).",
            "deep_explanation": "The HotSpot Mark Word layout uses the lowest 3 bits to encode biased locking status (101). When biased, the upper bits store the native OS thread ID. To revoke a bias, the VM initiates a VM_Operation executed by the VMThread at a safepoint. The safepoint halts all application threads, walks the stacks of the bias-holding thread to see if the monitor is still locked, updates the mark word to lightweight locking (displaced mark word) or unlocked, and resumes execution. As enterprise applications shifted to thread pools, microservices, and asynchronous work-stealing executors, biased lock revocations became a leading cause of inexplicable 10ms-50ms latency spikes.",
            "architecture_notes": "Disabled by default since Java 15 via JEP 374; removed completely in subsequent JVM releases.",
            "code_example": """// Legacy flag (now obsolete): -XX:+UseBiasedLocking -XX:BiasedLockingStartupDelay=0
public class LockBiasingAnalysis {
    private final Object monitor = new Object();
    public void executeLoop() {
        // In legacy JVM: Biased to thread on first acquisition
        // When thread 2 touches monitor: Triggered global Stop-The-World revocation pause!
        synchronized (monitor) {
            // Work
        }
    }
}""",
            "why_interviewer_asks": "Deep test of JVM evolution, object header memory layout, and the hidden latency costs of JVM optimizations.",
            "production_considerations": "Modern JVMs use lightweight CAS locking by default, eliminating safepoint latency spikes caused by bias revocation.",
            "failure_modes": "In Java 8/11 systems, high lock migration across thread pools triggered thousands of biased lock revocations, manifesting as high Time-To-Safepoint (TTSP) pauses.",
            "tradeoffs": "Saved a single CAS instruction on single-threaded locks at the catastrophic cost of global Stop-The-World pauses upon multi-thread contention.",
            "common_mistakes": [
                "Assuming biased locking is active in modern Java 21+ runtimes.",
                "Thinking biased lock revocation only pauses the contending threads (it stopped the entire JVM globally).",
                "Enabling biased locking in modern thread-pooled web services."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "What did the JVM do when an object biased to thread A was locked by thread B?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Think about why Stop-The-World safepoints were required to inspect thread stacks."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "How do modern thread pools and work stealing interact with lock affinity?"}
            ],
            "sources": [
                {
                    "source_name": "JEP 374: Deprecate and Disable Biased Locking",
                    "source_url": "https://openjdk.org/jeps/374",
                    "publisher": "OpenJDK Community"
                }
            ],
            "followups": [
                {
                    "followup_question": "What locking mechanism replaced biased locking as the first acquisition step in modern HotSpot?",
                    "answer_guidance": "Lightweight locking using atomic Compare-And-Swap (CAS) on the thread's Displaced Mark Word stack frame."
                }
            ],
            "tags": ["Java", "JVM", "Locking", "HotSpot", "Google"]
        },
        {
            "title": "How does Java 21 StructuredTaskScope manage subtask cancellation and fault isolation in multi-agent workflows?",
            "difficulty": "TOUGH",
            "technology_slug": "java-backend",
            "topic_slug": "virtual-threads-loom",
            "question_type": "CONCEPTUAL",
            "scenario_type": "STRUCTURED_CONCURRENCY",
            "short_answer": "StructuredTaskScope binds parallel subtasks to a lexical code block, automatically propagating cancellation signals via thread interruption to remaining tasks when a failure policy (ShutdownOnFailure) triggers.",
            "interview_ready_answer": "In asynchronous systems, if subtask A fails, sibling subtasks B and C often continue running as orphaned background threads, wasting resources. StructuredTaskScope (JEP 453) solves this by enforcing syntactic nesting: subtasks are forked within a try-with-resources scope. With `ShutdownOnFailure`, the moment any subtask throws an exception, the scope triggers shutdown, immediately interrupting all unfinished sibling virtual threads and waiting for their termination before the parent scope exits, guaranteeing deterministic resource reclamation.",
            "deep_explanation": "Under the hood, `StructuredTaskScope` maintains an internal linked list of forked `Subtask` handles. Forked tasks run as virtual threads. When a subtask completes exceptionally, `handleComplete()` is invoked. In `ShutdownOnFailure`, this sets a failure state and calls `interrupt()` on all active virtual threads in the scope. When the parent thread calls `scope.join()`, it blocks until all forked threads terminate (either normally, exceptionally, or via cancellation). This enforces the structured programming invariant: control flow cannot exit the block while child concurrent operations remain in flight.",
            "architecture_notes": "Introduced as preview in Java 21 (JEP 453) and Java 22 (JEP 462), tightly coupled with Virtual Threads and Scoped Values.",
            "code_example": """import java.util.concurrent.StructuredTaskScope;
public class MultiAgentCoordinator {
    public record AgentResponse(String searchResult, String databaseResult) {}

    public AgentResponse queryInParallel() throws Exception {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            var searchTask = scope.fork(() -> callSearchEngine());
            var dbTask = scope.fork(() -> callDatabase());

            scope.join();           // Wait for all subtasks to complete or fail
            scope.throwIfFailed(); // Propagate exception if any task failed!

            return new AgentResponse(searchTask.get(), dbTask.get());
        } // All child threads guaranteed terminated before this line!
    }
    private String callSearchEngine() { return "SearchOk"; }
    private String callDatabase() { return "DbOk"; }
}""",
            "why_interviewer_asks": "Evaluates candidate's knowledge of Java 21+ concurrency evolution, error propagation, and architectural cleanliness.",
            "production_considerations": "Ensure forked virtual tasks handle `InterruptedException` cleanly and do not swallow interruptions, allowing rapid cancellation propagation.",
            "failure_modes": "Swallowing `InterruptedException` inside child tasks prevents `ShutdownOnFailure` from terminating sibling tasks promptly, delaying parent scope exit.",
            "tradeoffs": "Provides bulletproof lifecycle management and zero thread leaks, but requires cooperative thread cancellation via interruption.",
            "common_mistakes": [
                "Catching and ignoring InterruptedException inside subtasks, preventing graceful scope cancellation.",
                "Calling subtask.get() before calling scope.join().",
                "Using unstructured CompletableFuture.allOf() where a single failure does not cancel sibling network calls."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "What happens to sibling threads when one subtask throws an exception in unstructured code?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "How does StructuredTaskScope ensure the parent cannot return before children finish?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "How does cooperative cancellation interact with thread interruption in Virtual Threads?"}
            ],
            "sources": [
                {
                    "source_name": "JEP 453: Structured Concurrency (Preview)",
                    "source_url": "https://openjdk.org/jeps/453",
                    "publisher": "OpenJDK Community"
                }
            ],
            "followups": [
                {
                    "followup_question": "What is the difference between StructuredTaskScope.Subtask state SUCCESS and FAILED?",
                    "answer_guidance": "Subtask.get() returns the result if state is SUCCESS; it throws IllegalStateException if called when state is FAILED or UNAVAILABLE."
                }
            ],
            "tags": ["Java", "Java 21", "Structured Concurrency", "Virtual Threads", "Uber"]
        }
    ]
