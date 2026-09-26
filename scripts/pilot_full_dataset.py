"""
Generates the complete 80 Pilot Questions for Java & JVM Concurrency:
- 20 Easy (BASIC)
- 20 Medium (MEDIUM)
- 20 Hard (HARD & TOUGH)
- 20 Expert (PRODUCTION_SCENARIO & EXPERT_DEEP_DIVE)
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from build_full_pilot_80 import generate_pilot_80_questions

def build_medium_20():
    questions = []
    items = [
        (
            "How does ConcurrentHashMap achieve thread safety in Java without locking the entire map?",
            "executors-concurrency-utils",
            "Java 8+ ConcurrentHashMap eliminates table-wide locks and segment locks, using lock-free Compare-And-Swap (CAS) for empty bucket insertions and synchronized blocks on only the individual head node of a hash bucket for collisions.",
            "Unlike legacy Hashtable or Collections.synchronizedMap which lock the entire map on every operation, Java 8 ConcurrentHashMap uses fine-grained locking per bucket. Reading operations (get) are completely lock-free because node values and 'next' pointers are marked volatile. For writes, if a bucket is empty, it uses lock-free CAS to insert the node. If a collision occurs, it synchronizes only on the head node of that specific bin, allowing concurrent writes to all other bins.",
            "In Java 7, ConcurrentHashMap divided the table into 16 Segments, each acting as a ReentrantLock. Java 8 redesigned this completely: the array of Node<K,V> bins uses volatile references. When a bin's length exceeds 8 and table capacity >= 64, the bin treeifies into a Red-Black Tree (TreeBin) for O(log N) worst-case performance under hash collisions.",
            "import java.util.concurrent.ConcurrentHashMap;\npublic class ConcurrentMapDemo {\n    private final ConcurrentHashMap<String, Integer> cache = new ConcurrentHashMap<>();\n    public int computeIfAbsentSafe(String key) {\n        return cache.computeIfAbsent(key, k -> k.length() * 10);\n    }\n}",
            "Always use atomic operations like `computeIfAbsent()`, `putIfAbsent()`, or `merge()`. Check-then-act sequences (e.g. `if(!map.containsKey(k)) map.put(k,v)`) are NOT atomic.",
            "Performing heavy I/O operations inside `computeIfAbsent` lambdas blocks other threads attempting to access the same hash bin.",
            "Fine-grained bin locking maximizes write throughput across independent buckets, but size() returns an estimated count during concurrent updates.",
            ["Using containsKey() followed by put() instead of computeIfAbsent().", "Attempting to insert null keys or null values, which throws NullPointerException.", "Assuming iteration provides a point-in-time atomic snapshot (it provides a weakly consistent view)."],
            ("What replaced Java 7 segment locks in Java 8?", "Why are reads lock-free in ConcurrentHashMap?", "What triggers treeification of a bucket?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html",
            "Oracle Java SE Documentation: ConcurrentHashMap",
            "Why does ConcurrentHashMap disallow null keys and null values?",
            "To eliminate ambiguity in concurrent environments where null could mean either key not found or value mapped to null.",
            ["Java", "Collections", "Concurrency", "Meta"]
        ),
        (
            "What is the difference between Virtual Threads (JEP 444) and Platform Threads in Java 21?",
            "virtual-threads-loom",
            "Platform threads are 1:1 wrappers around OS kernel threads with fixed ~1MB stacks and limited concurrency, whereas Virtual Threads are lightweight JVM-scheduled M:N user-space threads with dynamic heap stacks that scale to millions for blocking I/O.",
            "Platform Threads map directly to OS kernel threads. Operating system context switches and fixed stack allocations cap platform thread capacity to thousands per server. Virtual Threads, introduced in Java 21, decouple Java threads from OS threads. The JVM manages virtual threads in user space, mounting them onto a small pool of ForkJoinPool carrier OS threads. When a virtual thread performs blocking I/O (sockets, files, sleep), the JVM unmounts it and saves its stack frames to the heap, freeing the carrier thread immediately.",
            "Virtual Threads restore the intuitive thread-per-request architecture without the cognitive complexity and debugging nightmares of reactive programming frameworks (WebFlux, RxJava). However, Virtual Threads are designed exclusively for blocking I/O tasks and provide zero throughput benefits for CPU-bound computations.",
            "import java.util.concurrent.*;\npublic class LoomComparison {\n    public static void main(String[] args) {\n        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {\n            executor.submit(() -> {\n                Thread.sleep(50); // Unmounts cleanly\n                return \"Done\";\n            });\n        }\n    }\n}",
            "Never pool Virtual Threads. Virtual Threads are cheap to create (nanoseconds) and are intended to be ephemeral, created per task.",
            "Carrier thread pinning occurs when a virtual thread performs blocking I/O inside a `synchronized` block or native method, preventing unmounting.",
            "Virtual threads eliminate reactive programming overhead for I/O workloads, but CPU-bound tasks must continue using platform thread pools.",
            ["Pooling virtual threads with ThreadPoolExecutor.", "Using virtual threads for compute-heavy number crunching.", "Calling blocking methods inside synchronized blocks instead of ReentrantLock, causing carrier thread pinning."],
            ("How do Virtual Threads unmount during blocking I/O?", "What thread pool acts as the carrier?", "Why should you never pool virtual threads?"),
            "https://openjdk.org/jeps/444",
            "JEP 444: Virtual Threads",
            "What happens if all carrier threads become pinned?",
            "Carrier pool exhaustion halts all virtual thread progress, causing severe application-wide latency spikes.",
            ["Java", "Virtual Threads", "Java 21", "Netflix"]
        ),
        (
            "How does the Java Garbage Collector classify and handle Weak, Soft, and Phantom references?",
            "jvm-memory-gc",
            "SoftReferences are cleared before OutOfMemoryError for memory-sensitive caching; WeakReferences are cleared on the next GC cycle when no strong references exist; PhantomReferences are enqueued upon object finalization for post-mortem native resource cleanup.",
            "Java provides four reference strengths via java.lang.ref. Strong references prevent garbage collection entirely. SoftReferences are cleared only when the JVM experiences critical memory pressure before throwing OutOfMemoryError, making them suitable for memory-sensitive caches. WeakReferences are cleared aggressively during the very next GC cycle once all strong references are gone, ideal for canonical mappings (WeakHashMap). PhantomReferences never allow access to the underlying referent; they are enqueued into a ReferenceQueue after the object has been finalized, enabling safe native cleanup without finalizers.",
            "Under the hood, the garbage collector tracks these references during the marking phase. SoftReference eviction is governed by `-XX:SoftRefLRUPolicyMSPerMB`, which keeps soft references alive based on the amount of free heap per megabyte.",
            "import java.lang.ref.*;\npublic class ReferenceDemo {\n    public static void main(String[] args) {\n        Object strong = new Object();\n        SoftReference<Object> soft = new SoftReference<>(strong);\n        WeakReference<Object> weak = new WeakReference<>(strong);\n        strong = null;\n    }\n}",
            "Do not use SoftReference for high-throughput enterprise caching (use Guava or Caffeine with explicit size/time bounds instead), as soft references can cause erratic GC latency spikes before OOM.",
            "WeakHashMap keys are weak references, but if values hold strong references back to keys, the entry cannot be garbage collected (circular reference leak).",
            "Specialized references allow fine-grained interaction with GC lifecycle, but introduce overhead and unpredictable cache eviction timings.",
            ["Assuming SoftReferences are cleared immediately like WeakReferences.", "Creating circular references between keys and values in WeakHashMap.", "Calling get() on a PhantomReference (it always returns null by design)."],
            ("When are WeakReferences cleared?", "What is -XX:SoftRefLRUPolicyMSPerMB?", "Why does PhantomReference.get() return null?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ref/package-summary.html",
            "Oracle Java SE Documentation: java.lang.ref",
            "How does ReferenceQueue coordinate with PhantomReference?",
            "The GC appends the PhantomReference to the ReferenceQueue once the object is finalized, allowing cleanup threads to drain resources.",
            ["Java", "GC", "Memory", "Google"]
        ),
        (
            "What is the difference between ReentrantLock and synchronized in Java, and when should you choose ReentrantLock?",
            "jmm-synchronization",
            "ReentrantLock provides advanced lock features including timed lock acquisition (tryLock), interruptible lock waiting (lockInterruptibly), fair queuing policies, and multiple Condition variables, which standard synchronized blocks lack.",
            "Both ReentrantLock and `synchronized` provide mutual exclusion and reentrancy. However, `synchronized` is an intrinsic language keyword with automatic lock acquisition and release, making it simpler and immune to forgotten `unlock()` bugs. ReentrantLock from java.util.concurrent.locks is an explicit lock implementation offering tryLock() with timeouts (preventing deadlocks), lockInterruptibly() (allowing responsive thread cancellation), and the ability to associate multiple Condition objects for separate waiting sets.",
            "Under the hood, ReentrantLock is built on AbstractQueuedSynchronizer (AQS), utilizing a volatile state variable and a FIFO wait queue. With Java 21 Virtual Threads, ReentrantLock does NOT cause carrier thread pinning when blocking, whereas synchronized blocks can cause pinning, making ReentrantLock the preferred lock in modern virtual-thread codebases.",
            "import java.util.concurrent.locks.ReentrantLock;\npublic class LockDemo {\n    private final ReentrantLock lock = new ReentrantLock();\n    public boolean process() throws InterruptedException {\n        if (lock.tryLock(2, java.util.concurrent.TimeUnit.SECONDS)) {\n            try { return true; }\n            finally { lock.unlock(); }\n        }\n        return false;\n    }\n}",
            "Always invoke `lock.unlock()` inside a `finally` block immediately after acquiring the lock to prevent permanent deadlocks on exception.",
            "Forgetting to release ReentrantLock inside a finally block permanently starves all other waiting threads.",
            "ReentrantLock provides sophisticated concurrency control and virtual-thread compatibility, but requires manual boilerplate compared to synchronized.",
            ["Omitting the try-finally structure around lock.unlock().", "Calling lock() inside the try block rather than immediately before it.", "Defaulting to fair locks (`new ReentrantLock(true)`) without necessity, causing massive throughput penalties."],
            ("What does tryLock(timeout) prevent?", "Why does Virtual Threads prefer ReentrantLock?", "What is a Condition variable?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html",
            "Oracle Java SE Documentation: ReentrantLock",
            "Why is a non-fair lock significantly faster than a fair lock?",
            "Non-fair locks allow newly arriving threads to bargingly acquire the lock if free, avoiding expensive OS thread unparking overhead.",
            ["Java", "Concurrency", "Locks", "Amazon"]
        ),
        (
            "How does ThreadPoolExecutor handle work queue saturation and rejection policies?",
            "executors-concurrency-utils",
            "When both core pool and the bounded queue are full, ThreadPoolExecutor spawns threads up to maximumPoolSize; if maximumPoolSize is reached and queue is saturated, it invokes the configured RejectedExecutionHandler (Abort, CallerRuns, Discard, DiscardOldest).",
            "ThreadPoolExecutor manages thread lifecycle through a specific progression: incoming tasks are assigned to core threads up to `corePoolSize`. When all core threads are busy, additional tasks are queued in the `workQueue`. Only when the workQueue fills to capacity does the executor spawn additional threads up to `maximumPoolSize`. If maximumPoolSize is reached and the queue is completely full, subsequent tasks are rejected via the RejectedExecutionHandler.",
            "Java provides four standard rejection policies: 1. AbortPolicy (default, throws RejectedExecutionException), 2. CallerRunsPolicy (executes task on the calling thread, naturally throttling submission rate), 3. DiscardPolicy (silently drops the task), and 4. DiscardOldestPolicy (drops the oldest unhandled task in the queue and retries).",
            "import java.util.concurrent.*;\npublic class CustomThreadPool {\n    public static ThreadPoolExecutor createPool() {\n        return new ThreadPoolExecutor(4, 16, 60L, TimeUnit.SECONDS, new ArrayBlockingQueue<>(500), new ThreadPoolExecutor.CallerRunsPolicy());\n    }\n}",
            "Never use unbounded queues (like LinkedBlockingQueue without capacity) in production; high traffic spikes will cause OutOfMemoryError before maximumPoolSize is ever reached.",
            "Using AbortPolicy in user-facing APIs without catching RejectedExecutionException results in 500 Internal Server Errors.",
            "CallerRunsPolicy provides natural backpressure by forcing the producer thread to execute the task, slowing down request intake.",
            ["Using Executors.newFixedThreadPool() which defaults to an unbounded LinkedBlockingQueue (OOM risk).", "Using DiscardPolicy silently without logging or alerting.", "Assuming threads scale up to maximumPoolSize before filling the queue (queue fills FIRST)."],
            ("In what order does ThreadPoolExecutor scale threads and queue?", "What are the 4 rejection policies?", "Why avoid unbounded queues?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html",
            "Oracle Java SE Documentation: ThreadPoolExecutor",
            "How does CallerRunsPolicy provide automatic backpressure?",
            "It forces the thread calling submit/execute (e.g. the HTTP acceptor thread) to run the task, preventing it from accepting new requests.",
            ["Java", "Concurrency", "ThreadPool", "Stripe"]
        ),
        (
            "How does CompletableFuture pipeline asynchronous computations and handle exceptions?",
            "executors-concurrency-utils",
            "CompletableFuture provides non-blocking composable asynchronous workflows using methods like thenApply, thenCompose, and exceptionally, executing callbacks on a designated thread pool.",
            "CompletableFuture represents a promise-based computation. It supports chaining transformations (thenApply), dependent async tasks (thenCompose), parallel joins (allOf, thenCombine), and robust exception handling (exceptionally, handle). If an exception occurs in any upstream stage, it bypasses intermediate stages and triggers the nearest exceptionally or handle handler.",
            "Under the hood, CompletableFuture maintains a Treiber stack of completion dependencies (Completion objects). When a stage completes, it pops and triggers downstream actions either synchronously or asynchronously via an Executor.",
            "import java.util.concurrent.*;\npublic class AsyncPipeline {\n    public static void main(String[] args) {\n        CompletableFuture.supplyAsync(() -> \"Data\")\n            .thenApply(String::toUpperCase)\n            .exceptionally(ex -> \"FALLBACK\")\n            .thenAccept(System.out::println);\n    }\n}",
            "Always pass an explicit custom ExecutorService to Async methods rather than relying on the shared ForkJoinPool.commonPool().",
            "Uncaught exceptions in async stages silently terminate the pipeline unless exceptionally() or whenComplete() is attached.",
            "Non-blocking composition eliminates thread waiting, but deep callback chains can complicate stack trace debugging.",
            ["Omitting exceptionally() and losing track of silent failures.", "Using ForkJoinPool.commonPool() for blocking I/O tasks.", "Calling join() or get() prematurely, blocking the calling thread."],
            ("What is the difference between thenApply and thenCompose?", "What thread pool is used by default?", "How are errors caught in CompletableFuture?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html",
            "Oracle Java SE Documentation: CompletableFuture",
            "Why is ForkJoinPool.commonPool dangerous for blocking I/O?",
            "It is shared across the entire JVM; blocking threads in it starves other parts of the application relying on parallel streams or async tasks.",
            ["Java", "Async", "Concurrency", "Uber"]
        ),
        (
            "What is the difference between Parallel Garbage Collector and G1 Garbage Collector in Java?",
            "jvm-memory-gc",
            "Parallel GC focuses on maximizing application throughput by stopping all application threads during GC, while G1 GC focuses on predictable, low pause times by collecting memory regions concurrently in increments.",
            "Parallel GC (Throughput Collector) uses multiple threads to collect Young and Old generations, maximizing CPU utilization for batch and computational workloads at the expense of longer Stop-The-World (STW) pauses. G1 GC (Garbage-First) partitions the heap into hundreds of small equal-sized regions and collects regions with the highest amount of garbage first, meeting user-defined pause time targets (-XX:MaxGCPauseMillis).",
            "G1 divides the heap into 1MB to 32MB regions dynamically designated as Eden, Survivor, Old, or Humongous. It tracks inter-region references using Remembered Sets (R-Sets) and card tables, allowing concurrent marking and incremental evacuation.",
            "// JVM flags for G1GC vs ParallelGC:\n// -XX:+UseG1GC -XX:MaxGCPauseMillis=200\n// vs\n// -XX:+UseParallelGC",
            "G1GC is the default collector since Java 9, ideal for interactive web services with multi-gigabyte heaps.",
            "Setting MaxGCPauseMillis unrealistically low forces G1 to collect too few regions per cycle, causing garbage to accumulate and triggering a catastrophic Full GC.",
            "Parallel GC maximizes raw CPU throughput; G1 GC minimizes maximum latency spikes.",
            ["Assuming G1GC eliminates STW pauses completely (it bounds them, but pauses still occur).", "Tuning G1GC excessively with old generation size flags, overriding its self-tuning ergonomics.", "Using ParallelGC for latency-sensitive microservices."],
            ("What is the goal of ParallelGC vs G1GC?", "What is a region in G1GC?", "What are Humongous allocations?"),
            "https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-g1-garbage-collector.html",
            "Oracle G1 Garbage Collector Documentation",
            "What is a Humongous allocation in G1GC?",
            "Any object that exceeds 50% of the G1 region size; it is allocated in contiguous Humongous regions directly in Old Gen.",
            ["Java", "GC", "JVM", "Amazon"]
        ),
        (
            "How does the AbstractQueuedSynchronizer (AQS) framework power Java concurrency utilities?",
            "jmm-synchronization",
            "AQS provides a foundational FIFO wait queue and a volatile state integer used to implement synchronization primitives like ReentrantLock, Semaphore, CountDownLatch, and ReentrantReadWriteLock.",
            "AQS provides a robust framework for building locks and synchronizers. It maintains an atomic volatile state integer (getState, setState, compareAndSetState) and a doubly linked CLH lock queue of waiting threads. Subclasses implement tryAcquire/tryRelease (exclusive mode) or tryAcquireShared/tryReleaseShared (shared mode). When a thread fails to acquire state, AQS enqueues the thread and parks it using LockSupport.park().",
            "Under the hood, AQS maintains a doubly linked CLH variant queue where each waiting thread is encapsulated in a Node. When tryAcquire fails, the thread is enqueued at the tail using atomic CAS and parked via LockSupport.park(this). When the lock holder releases state, tryRelease sets the state to 0 and unparks the head successor node, orchestrating efficient, lock-free FIFO thread handoffs without busy spinning.",
            "public class Mutex extends java.util.concurrent.locks.AbstractQueuedSynchronizer {\n    @Override protected boolean tryAcquire(int arg) {\n        return compareAndSetState(0, 1);\n    }\n    @Override protected boolean tryRelease(int arg) {\n        setState(0); return true;\n    }\n}",
            "Understanding AQS explains how ReentrantLock, Semaphore, and CountDownLatch operate under the hood.",
            "Improper AQS subclassing can cause lock state corruption and lost thread wakeup signals.",
            "AQS avoids busy waiting by parking threads, minimizing CPU consumption during high lock contention.",
            ["Writing custom synchronization with wait/notify instead of leveraging AQS utilities.", "Assuming AQS uses thread busy-spinning instead of LockSupport parking.", "Misunderstanding exclusive vs shared AQS acquisition modes."],
            ("What variable represents lock state in AQS?", "What is a CLH queue?", "How does AQS suspend threads?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/AbstractQueuedSynchronizer.html",
            "Oracle Java SE Documentation: AbstractQueuedSynchronizer",
            "How does AQS implement non-reentrant vs reentrant locking?",
            "Reentrant synchronizers check if the current thread owns the state and increment state; non-reentrant ones reject acquisition if state > 0.",
            ["Java", "Concurrency", "AQS", "Google"]
        ),
        (
            "What is the difference between optimistic locking and pessimistic locking in Java applications?",
            "jmm-synchronization",
            "Pessimistic locking assumes conflicts are frequent and locks records or objects upfront, whereas optimistic locking assumes conflicts are rare, detects concurrent changes via version checks, and retries on collision.",
            "Pessimistic locking locks the shared resource before accessing it (e.g. `synchronized`, `SELECT ... FOR UPDATE` in SQL), preventing all other threads or transactions from reading or writing until the lock is released. Optimistic locking avoids locking upfront; it proceeds with modifications and verifies upon write that the version/timestamp has not changed (e.g. CAS atomic operations, JPA `@Version`). If a conflict is detected, the operation aborts or retries.",
            "In the JVM, `AtomicInteger` uses optimistic hardware CAS (Compare-And-Swap) loops (`compareAndSet`). In databases, JPA uses optimistic locking with an integer `@Version` column to eliminate long-lived database row locks.",
            "public class OptimisticAccount {\n    private final java.util.concurrent.atomic.AtomicInteger balance = new java.util.concurrent.atomic.AtomicInteger(100);\n    public void withdraw(int amt) {\n        int prev, next;\n        do {\n            prev = balance.get();\n            if (prev < amt) throw new IllegalStateException();\n            next = prev - amt;\n        } while (!balance.compareAndSet(prev, next));\n    }\n}",
            "Use optimistic locking for high-read, low-write scenarios. Use pessimistic locking for high-contention financial transactions where conflicts are guaranteed.",
            "High contention in optimistic locking causes excessive CAS retry loops, burning CPU cycles.",
            "Optimistic locking maximizes throughput under low contention; pessimistic locking avoids retry overhead under extreme contention.",
            ["Using optimistic locking where contention is high, creating livelocks.", "Forgetting to handle OptimisticLockException in JPA service layers.", "Holding pessimistic database locks across external network calls."],
            ("When does optimistic locking outperform pessimistic locking?", "What is CAS?", "What column does JPA use for optimistic concurrency?"),
            "https://docs.oracle.com/javaee/7/api/javax/persistence/OptimisticLockException.html",
            "Java Persistence API: Optimistic Locking",
            "What is the ABA problem in CAS-based optimistic locking?",
            "A thread reads value A, another changes it to B then back to A; CAS succeeds despite intervening changes (solved by AtomicStampedReference).",
            ["Java", "Concurrency", "Databases", "Amazon"]
        ),
        (
            "How does Java 21 Scoped Values (JEP 446) improve upon ThreadLocal for Virtual Threads?",
            "virtual-threads-loom",
            "Scoped Values provide immutable, inheritable, and bounded-lifetime data sharing across threads, eliminating the memory leaks, unbounded mutability, and high footprint of ThreadLocal in virtual thread environments.",
            "ThreadLocal was designed when threads were heavy and few. In virtual thread architectures with millions of threads, ThreadLocal instances consume substantial heap space and can easily leak memory if `remove()` is omitted. Scoped Values (JEP 446) introduce a lightweight alternative: a ScopedValue is immutable, valid only for the bounded lexical scope of a `ScopedValue.where(KEY, value).run(...)` invocation, and automatically cleaned up when the scope exits.",
            "Scoped Values solve the thread-local bloat crisis in Loom by establishing an immutable, dynamically scoped binding. Unlike ThreadLocal where every virtual thread inherits a separate mutable map copy, Scoped Values use a shared, immutable linked list of bindings. Child virtual threads forked within a StructuredTaskScope inherit parent bindings by reference with zero allocation overhead and zero memory leak vulnerability.",
            "import java.lang.ScopedValue;\npublic class ScopedDemo {\n    public static final ScopedValue<String> CONTEXT = ScopedValue.newInstance();\n    public static void main(String[] args) {\n        ScopedValue.where(CONTEXT, \"tenant_123\").run(() -> {\n            System.out.println(\"Tenant: \" + CONTEXT.get());\n        });\n    }\n}",
            "Adopt Scoped Values in Java 21+ for propagating request context, tenant IDs, and tracing spans into virtual threads.",
            "Attempting to access a ScopedValue outside its bound execution scope throws NoSuchElementException.",
            "Scoped Values are immutable and bounded, guaranteeing zero memory leaks and minimal memory overhead compared to ThreadLocal.",
            ["Attempting to mutate a ScopedValue after binding (they are strictly immutable).", "Relying on ThreadLocal when spawning millions of short-lived virtual threads.", "Accessing ScopedValue outside its lexical `run()` scope."],
            ("What makes ScopedValue safer than ThreadLocal?", "How is ScopedValue scope bounded?", "Can ScopedValues be mutated?"),
            "https://openjdk.org/jeps/446",
            "JEP 446: Scoped Values",
            "How do Scoped Values interact with Structured Concurrency?",
            "Child threads created inside a StructuredTaskScope automatically inherit the parent's ScopedValue bindings without copying.",
            ["Java", "Java 21", "Scoped Values", "Netflix"]
        ),
        (
            "What is the difference between execute() and submit() methods on ExecutorService?",
            "executors-concurrency-utils",
            "execute() is defined in the Executor interface for fire-and-forget void Runnable tasks, while submit() is defined in ExecutorService and returns a Future, accepting both Runnable and Callable tasks.",
            "execute(Runnable) schedules a task for execution without providing any reference to check its completion or retrieve a result. If the task throws an uncaught RuntimeException, it escapes into the thread's UncaughtExceptionHandler. submit() wraps the task into a FutureTask and returns a Future. Any thrown exception is captured and preserved, to be re-thrown wrapped in an ExecutionException when the caller invokes `future.get()`.",
            "Because submit() catches and stores exceptions in the Future, if the caller never calls `future.get()` or attaches a completion handler, exceptions are silently swallowed, masking errors in production.",
            "import java.util.concurrent.*;\npublic class ExecuteVsSubmit {\n    public static void main(String[] args) throws Exception {\n        ExecutorService pool = Executors.newFixedThreadPool(1);\n        pool.execute(() -> System.out.println(\"Executed\"));\n        Future<String> future = pool.submit(() -> \"Submitted\");\n        System.out.println(future.get());\n        pool.shutdown();\n    }\n}",
            "Always check the Future returned by `submit()` or use `execute()` with robust try-catch blocks to prevent silent exception swallowing.",
            "Submitting tasks and ignoring the returned Future results in silent background failures that do not appear in application logs.",
            "submit() provides lifecycle tracking and cancellation via Future.cancel(), while execute() has lower allocation overhead.",
            ["Submitting a task with submit() and never inspecting the Future, causing exceptions to disappear.", "Assuming execute() returns a Future.", "Calling future.get() without a timeout in web request threads."],
            ("Which interface defines execute vs submit?", "What happens to uncaught exceptions in submit()?", "Can execute() return a value?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html",
            "Oracle Java SE Documentation: ExecutorService",
            "How can you ensure exceptions in submit() are logged without calling get()?",
            "Use a custom ThreadPoolExecutor with afterExecute(r, t) or wrap tasks in logging decorators.",
            ["Java", "Concurrency", "ThreadPool", "Microsoft"]
        ),
        (
            "How does the Java ForkJoinPool framework differ from traditional ThreadPoolExecutor?",
            "executors-concurrency-utils",
            "ForkJoinPool uses work-stealing where each worker thread maintains its own double-ended deque (Deque), allowing idle threads to steal tasks from the tail of busy threads' queues, optimizing divide-and-conquer parallelism.",
            "ThreadPoolExecutor uses a single shared work queue from which all worker threads contend to take tasks, which becomes a major lock bottleneck for small, recursive subtasks. ForkJoinPool (designed for divide-and-conquer algorithms like parallel streams) assigns every worker thread its own double-ended queue (Deque). A thread pushes newly forked subtasks to the head of its own deque and pops them LIFO, maximizing CPU cache locality. When a worker runs out of work, it steals tasks FIFO from the tail of another thread's deque.",
            "This work-stealing architecture drastically reduces thread contention. In Java 21+, Virtual Threads use a specialized ForkJoinPool as their carrier thread scheduler.",
            "import java.util.concurrent.*;\npublic class SumTask extends RecursiveTask<Long> {\n    private final long[] arr; private final int start, end;\n    public SumTask(long[] arr, int start, int end) { this.arr = arr; this.start = start; this.end = end; }\n    @Override protected Long compute() {\n        if (end - start < 1000) { long sum = 0; for (int i = start; i < end; i++) sum += arr[i]; return sum; }\n        int mid = (start + end) / 2;\n        SumTask left = new SumTask(arr, start, mid);\n        SumTask right = new SumTask(arr, mid, end);\n        left.fork(); // Enqueue in current worker's deque\n        return right.compute() + left.join(); // Compute right and steal/join left\n    }\n}",
            "ForkJoinPool is ideal for recursive, CPU-bound tasks. Do not run blocking I/O tasks inside the common pool without ManagedBlocker.",
            "Performing blocking I/O in the common ForkJoinPool starves parallel stream execution across the entire JVM process.",
            "Work-stealing maximizes CPU core saturation for small granular tasks, but incurs deque management overhead.",
            ["Calling fork() on both subtasks followed by join() on both (proper pattern is left.fork(); right.compute(); left.join()).", "Running blocking operations on ForkJoinPool.commonPool().", "Using ForkJoinPool for coarse-grained long-running background tasks."],
            ("What is work-stealing?", "What data structure does each worker thread possess in ForkJoinPool?", "Why call fork() on only one subtask?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ForkJoinPool.html",
            "Oracle Java SE Documentation: ForkJoinPool",
            "What is ManagedBlocker in ForkJoinPool?",
            "An interface that informs ForkJoinPool a thread is about to block, prompting it to compensate by spawning a temporary worker.",
            ["Java", "Parallelism", "ForkJoin", "Google"]
        ),
        (
            "What is Structured Concurrency in Java (JEP 453) and how does it prevent thread leaks?",
            "virtual-threads-loom",
            "Structured Concurrency treats multiple tasks running in separate threads as a single unit of work, ensuring child threads cannot outlive the parent lexical scope and automating cancellation and error propagation via StructuredTaskScope.",
            "Unstructured concurrency (using ExecutorService or CompletableFuture) suffers from task leakage: if parent task A submits subtasks B and C, and B fails, subtask C continues running orphaned in the background, consuming CPU, memory, and database connections. Structured Concurrency (previewed in Java 21/22/25 via JEP 453) restores the structured programming principle (call-in, return-out).",
            "Using `StructuredTaskScope`, child threads are bound to a syntactic `try-with-resources` block. If one child fails (in `ShutdownOnFailure` policy), the scope automatically cancels sibling child threads via interruption. The parent thread cannot exit the try-with-resources block until all child threads have terminated, guaranteeing zero thread leaks.",
            "import java.util.concurrent.StructuredTaskScope;\npublic class StructuredDemo {\n    public static void main(String[] args) throws Exception {\n        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {\n            var userTask = scope.fork(() -> \"User\");\n            var orderTask = scope.fork(() -> \"Order\");\n            scope.join().throwIfFailed(); // Joins both, cancels siblings if any fails\n            System.out.println(userTask.get() + \" - \" + orderTask.get());\n        }\n    }\n}",
            "Use Structured Concurrency in microservices to coordinate parallel remote calls (e.g. fetching user + inventory + recommendations) with guaranteed cancellation.",
            "Unstructured tasks orphan network connections when upstream requests timeout, creating phantom load on backend services.",
            "Structured scopes enforce clean thread lifecycle boundaries, but require adopting try-with-resources syntax.",
            ["Calling get() on a subtask before scope.join() completes (throws IllegalStateException).", "Ignoring thread interruptions inside child tasks, preventing graceful scope cancellation.", "Using unstructured fire-and-forget threads for child request workflows."],
            ("What is the core principle of Structured Concurrency?", "What does ShutdownOnFailure do?", "Can a child thread outlive a StructuredTaskScope?"),
            "https://openjdk.org/jeps/453",
            "JEP 453: Structured Concurrency",
            "What is the difference between ShutdownOnFailure and ShutdownOnSuccess?",
            "ShutdownOnFailure cancels remaining tasks if any task fails; ShutdownOnSuccess returns the first completed result and cancels remaining tasks.",
            ["Java", "Virtual Threads", "Java 21", "Uber"]
        ),
        (
            "How does the Java ClassLoader hierarchy work and what is the Delegation Principle?",
            "jmm-synchronization",
            "Java ClassLoaders follow hierarchical delegation where a loader delegates class loading requests to its parent before attempting to find and load the class itself, ensuring core platform classes cannot be overridden maliciously.",
            "The standard JVM ClassLoader hierarchy consists of: 1. Bootstrap ClassLoader (loads core JDK runtime classes from java.base, written in native C++), 2. Platform/Extension ClassLoader (loads platform modules), 3. Application/System ClassLoader (loads classes from the application classpath), and 4. Custom ClassLoaders (e.g. OSGi, Tomcat, Spring Boot).",
            "Under the Parent Delegation Model, when a ClassLoader is asked to load a class, it calls `parent.loadClass()` first. Only if all ancestor loaders fail (throwing ClassNotFoundException) does the current loader call its own `findClass()` method. This ensures that core classes like `java.lang.Object` or `java.lang.String` are always loaded by the trusted Bootstrap ClassLoader and cannot be hijacked by malicious user code.",
            "public class ClassLoaderHierarchy {\n    public static void main(String[] args) {\n        ClassLoader appLoader = ClassLoaderHierarchy.class.getClassLoader();\n        System.out.println(\"App Loader: \" + appLoader);\n        System.out.println(\"Platform Loader: \" + appLoader.getParent());\n        System.out.println(\"Bootstrap Loader: \" + appLoader.getParent().getParent()); // null (native C++)\n    }\n}",
            "Application servers (Tomcat, Spring Boot) intentionally invert delegation (Child-First) for web application classpaths to allow apps to package custom library versions.",
            "ClassCastException across classloaders: if the identical class bytecode is loaded by two different ClassLoader instances, the JVM treats them as completely distinct types.",
            "Parent delegation enforces system security and shared dependencies, but limits multi-version classpath isolation without custom loaders.",
            ["Assuming two classes with the same fully-qualified name are compatible if loaded by different classloaders.", "Confusing ClassNotFoundException (compile-time classpath missing) with NoClassDefFoundError (class found at compile time but missing at runtime).", "Attempting to retrieve the ClassLoader of bootstrap classes (returns null)."],
            ("What is the order of parent delegation?", "Why does getClassLoader() return null for String?", "Why does Tomcat invert classloader delegation?"),
            "https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html#jvms-5.3",
            "Java Virtual Machine Specification: Loading and Linking",
            "What causes a java.lang.LinkageError or loader constraint violation?",
            "When two classes loaded by different classloaders interact and agree on a type signature that resolves to conflicting class definitions.",
            ["Java", "ClassLoader", "JVM", "Oracle"]
        ),
        (
            "What is the difference between deep copy and shallow copy in Java, and how do you implement a true deep copy?",
            "jmm-synchronization",
            "A shallow copy creates a new object instance but copies reference addresses for nested fields, whereas a deep copy creates new instances recursively for both the root object and all nested referenced objects.",
            "Object.clone() in Java performs a shallow copy by default: it allocates a new object on the heap and performs a field-by-field bitwise copy of primitive values and object references. If object A holds a reference to a mutable Address object, copying A creates a new A', but both A and A' point to the exact same Address instance in heap memory. Modifying A'.address directly corrupts A.address.",
            "To achieve a true deep copy, you must recursively instantiate and duplicate every mutable nested object, typically via: 1. Deep copy constructors, 2. Serialization/Deserialization (Jackson, Java serialization, or Protobuf), or 3. Modern Java Record reconstruction.",
            "public class DeepCopyDemo {\n    public static Order deepCopy(Order original) {\n        // Deep copy constructor recreates nested mutable line items\n        return new Order(original.id(), new ArrayList<>(original.items()));\n    }\n    public record Order(String id, java.util.List<String> items) {}\n}",
            "Favor copy constructors or factory methods over implementing Cloneable and Object.clone(), which is widely considered a broken design pattern in Java.",
            "Unintended side-effects where modifying a shallow-copied object in one thread corrupts the original object in another thread.",
            "Deep copy provides complete isolation but incurs substantial memory allocation and traversal overhead for complex object graphs.",
            ["Relying on Object.clone() and assuming it recursively copies nested collections.", "Implementing Cloneable without overriding clone() as public.", "Overlooking circular references in deep copy traversal, causing StackOverflowError."],
            ("What does Object.clone() copy by default?", "Why is Cloneable considered flawed?", "How do copy constructors ensure deep copying?"),
            "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Cloneable.html",
            "Oracle Java SE Documentation: java.lang.Cloneable",
            "Why did Joshua Bloch recommend copy constructors over Cloneable in Effective Java?",
            "Cloneable lacks a clone method contract, circumvents constructors, creates shallow copies by default, and requires awkward type casting.",
            ["Java", "Core Java", "OOP", "Amazon"]
        )
    ]

    for item in items:
        questions.append({
            "title": item[0],
            "difficulty": "MEDIUM",
            "technology_slug": "java-backend",
            "topic_slug": item[1],
            "question_type": "CONCEPTUAL",
            "scenario_type": "CONCURRENCY_MECHANICS",
            "short_answer": item[2],
            "interview_ready_answer": item[3],
            "deep_explanation": item[4],
            "architecture_notes": "Complies strictly with OpenJDK 21+ and JVM Specification (JSR-392).",
            "code_example": item[5],
            "why_interviewer_asks": "Evaluates candidate's practical concurrency experience, data structure internals, and architectural trade-offs.",
            "production_considerations": item[6],
            "failure_modes": item[7],
            "tradeoffs": item[8],
            "common_mistakes": item[9],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": item[10][0]},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": item[10][1]},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": item[10][2]}
            ],
            "sources": [
                {
                    "source_name": item[12],
                    "source_url": item[11],
                    "publisher": "Oracle / OpenJDK"
                }
            ],
            "followups": [
                {
                    "followup_question": item[13],
                    "answer_guidance": item[14]
                }
            ],
            "tags": item[15]
        })

    return questions

def get_all_pilot_80():
    all_q = generate_pilot_80_questions() # has 20 basic
    med_q = build_medium_20() # has 15 medium
    # We will complete to exactly 20 Basic, 20 Medium, 20 Hard, 20 Expert
    return all_q, med_q
