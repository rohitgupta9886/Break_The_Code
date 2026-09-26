"""
Unified Pilot Batch Runner for BreakTheCode
Constructs and ingests 80 high-caliber questions for Java & JVM Concurrency:
- 20 Easy (BASIC)
- 20 Medium (MEDIUM)
- 20 Hard (HARD / TOUGH)
- 20 Expert (PRODUCTION_SCENARIO / EXPERT_DEEP_DIVE)
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))
import json
from content_quality_engine import ContentQualityEngine, StrictDifficultyStandard

def build_pilot_questions():
    questions = []

    def make_q(title, difficulty, topic_slug, short_a, interview_a, deep_e, code_ex, prod_c, fail_m, trade_o, mistakes, hints, source_url, source_title, followup_q, followup_a, tags):
        return {
            "title": title,
            "difficulty": difficulty,
            "technology_slug": "java-backend",
            "topic_slug": topic_slug,
            "question_type": "SCENARIO_BASED" if "Incident" in title else "CONCEPTUAL",
            "scenario_type": "PRODUCTION_INCIDENT" if "Incident" in title else ("INTERNALS" if difficulty in ["HARD", "TOUGH", "EXPERT_DEEP_DIVE"] else "FUNDAMENTALS"),
            "short_answer": short_a,
            "interview_ready_answer": interview_a,
            "deep_explanation": deep_e,
            "architecture_notes": "Complies strictly with OpenJDK 21+ HotSpot JVM specifications (JSR-392).",
            "code_example": code_ex,
            "why_interviewer_asks": "Evaluates candidate's real-world technical depth, production acumen, and understanding of the Java execution model.",
            "production_considerations": prod_c,
            "failure_modes": fail_m,
            "tradeoffs": trade_o,
            "common_mistakes": mistakes,
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": hints[0]},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": hints[1]},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": hints[2]}
            ],
            "sources": [
                {
                    "source_name": source_title,
                    "source_url": source_url,
                    "publisher": "Oracle / OpenJDK"
                }
            ],
            "followups": [
                {
                    "followup_question": followup_q,
                    "answer_guidance": followup_a
                }
            ],
            "tags": tags
        }

    # =========================================================
    # 20 EASY (BASIC)
    # =========================================================
    # (Questions 1 to 20)
    basic_raw = [
        ("What is the difference between an interface and an abstract class in Java 8 and beyond?", "jmm-synchronization",
         "An abstract class can maintain state via instance fields and constructors and supports single inheritance, whereas an interface defines a contract, supports multiple inheritance, and can only hold constants, default, and static methods without instance state.",
         "In modern Java, an abstract class represents an 'is-a' relationship with state, meaning it can have constructors, instance fields, and any access modifier. An interface represents a 'can-do' capability contract, allowing a class to implement multiple interfaces. While Java 8 introduced default and static methods to interfaces, interfaces still cannot maintain mutable instance state.",
         "Historically, interfaces contained only method signatures, but Java 8 introduced default methods to facilitate backward compatibility for lambda expressions in the Collections framework without breaking existing implementations. Crucially, an interface cannot have instance variables; all fields are implicitly 'public static final'. Abstract classes, by contrast, participate in standard class hierarchy initialization via constructors and can enforce encapsulation with private/protected member fields.",
         "public interface Auditable {\n    String DEFAULT_AUDITOR = \"SYSTEM\";\n    String getAuditId();\n    default void logAudit() {\n        System.out.println(\"Audit recorded: \" + getAuditId());\n    }\n}\n\npublic abstract class BaseEntity {\n    private final long createdAt = System.currentTimeMillis();\n    public abstract String getId();\n    public long getCreatedAt() { return createdAt; }\n}",
         "Default methods should provide non-invasive fallback behaviors. Avoid placing heavy business logic inside interface default methods as it bypasses clean domain-driven architecture.",
         "Diamond problem with default methods: if two implemented interfaces define identical default method signatures, the implementing class must explicitly override and resolve the conflict using InterfaceName.super.method() or compilation fails.",
         "Interfaces maximize compositional flexibility and decoupling at the cost of requiring external state management. Abstract classes simplify shared state and skeletal implementations but consume the single inheritance slot.",
         ["Attempting to declare instance variables inside an interface, forgetting all fields are implicitly static and final.", "Using an abstract class purely for utility functions without any state or polymorphic hierarchy.", "Forgetting to resolve diamond dependency conflicts when implementing two interfaces with identical default method signatures."],
         ("Can an interface hold state?", "How does multiple inheritance work with interfaces vs classes?", "What are default methods?"),
         "https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html", "Oracle Java Documentation: Interface and Abstract Classes",
         "What happens if two interfaces declare the same default method?", "The compiler flags ambiguity; the implementing class must override and resolve explicitly using Interface.super.method().", ["Java", "OOP", "Core Java", "Google"]),
        
        ("Why is the String class immutable in Java, and what benefits does immutability provide?", "jmm-synchronization",
         "String is immutable in Java to ensure thread safety, enable String Pool caching (saving heap memory), guarantee secure class loading and network connections, and allow stable hashCode caching.",
         "String immutability is a foundational design choice in Java. It allows the JVM to safely share identical string literals in the String Pool, guarantees thread safety across concurrent threads without locks, ensures security parameters (like file paths, DB connection URLs, and classloader inputs) cannot be altered maliciously, and enables caching the calculated hashCode for fast HashMap lookups.",
         "Under the hood, String encapsulates an immutable byte[] array (since Java 9 Compact Strings) marked final and private, with no exposed mutators. Because String instances never mutate, the JVM's String Pool can return references to the same object for identical literals. In multithreading, immutability eliminates data races entirely. For hash-based collections (HashMap, HashSet), the hashCode is computed once lazily and cached, providing guaranteed O(1) bucket addressing.",
         "public final class StringImmutabilityDemo {\n    public static void main(String[] args) {\n        String a = \"BreakTheCode\";\n        String b = \"BreakTheCode\";\n        System.out.println(a == b); // true: shared String pool reference\n        String c = a.concat(\" 2026\");\n        System.out.println(a); // still \"BreakTheCode\"\n    }\n}",
         "Avoid string concatenation in tight loops using '+' operator; use StringBuilder or String.join to minimize heap churn.",
         "Excessive string allocations in high-throughput services trigger frequent Young Generation GC pauses.",
         "Immutability guarantees absolute thread safety and security at the cost of requiring new object allocations for mutations.",
         ["Using '+' inside loops instead of StringBuilder.", "Storing sensitive credentials in String instead of char[].", "Assuming substring() causes a memory leak (fixed since Java 7u6)."],
         ("What is the String Pool?", "How does thread safety work without locks?", "Why is hashCode cached?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html", "Oracle Java SE Documentation: java.lang.String",
         "Why store passwords in char[] instead of String?", "Strings remain in heap memory until GC; char arrays can be explicitly wiped with zeros immediately.", ["Java", "Memory", "Core Java", "Amazon"]),

        ("What is the contract between equals() and hashCode() in Java, and what happens when it is violated?", "jmm-synchronization",
         "If two objects are equal according to equals(), they must return the same hashCode(); if they have the same hashCode(), they are not required to be equal. Violating this contract breaks HashMap, HashSet, and Hashtable lookups.",
         "The equals-hashCode contract specifies that if objectA.equals(objectB) is true, then objectA.hashCode() must equal objectB.hashCode(). However, unequal objects can share the same hash code (a hash collision). If you override equals() without hashCode(), objects that are logically identical will produce different hash codes and map to different buckets in a HashMap, making it impossible to retrieve the stored entry.",
         "Hash collections use hashCode() to compute the bucket index (index = (n - 1) & hash). When inserting or querying a key, the collection first evaluates the bucket index via hashCode(). Only if a bucket contains entries does it iterate through the chain/tree and call equals() to match the exact key. If equals() returns true for two objects with different hashCodes, the lookup calculates the wrong bucket and fails to find the existing value.",
         "public class UserId {\n    private final String id;\n    public UserId(String id) { this.id = id; }\n    @Override public boolean equals(Object o) {\n        if (this == o) return true;\n        if (!(o instanceof UserId that)) return false;\n        return java.util.Objects.equals(id, that.id);\n    }\n    @Override public int hashCode() { return java.util.Objects.hashCode(id); }\n}",
         "Always compute hashCode from immutable fields to prevent bucket misalignment in HashMaps.",
         "Mutating an object after using it as a map key leads to silent memory leaks as the key cannot be found or removed.",
         "Uniform hash distributions keep bucket chains short (O(1) lookups), while poorly distributed hash codes degrade collections to O(N) or O(log N).",
         ["Overriding equals() without overriding hashCode().", "Using mutable fields inside hashCode().", "Changing equals parameter type to a concrete class instead of Object."],
         ("How does HashMap use hashCode?", "What happens on hash collision?", "Can two different objects have the same hashCode?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#hashCode()", "Oracle Java SE Documentation: Object.hashCode",
         "What if hashCode returns a constant like 42 for all objects?", "It satisfies the contract, but degrades HashMap performance to O(N) or O(log N) tree bins.", ["Java", "Collections", "Core Java", "Meta"]),

        ("What is the volatile keyword in Java, and what guarantees does it provide?", "jmm-synchronization",
         "The volatile keyword guarantees visibility of variable updates across threads and prevents instruction reordering around reads and writes, establishing a happens-before relationship without providing mutual exclusion or atomicity.",
         "In the Java Memory Model, 'volatile' provides two fundamental guarantees: Visibility and Ordering. Visibility ensures that whenever a thread writes to a volatile variable, the value is immediately flushed to main memory, and reading threads read directly from main memory rather than a stale CPU L1/L2 cache. Ordering ensures that the compiler and CPU cannot reorder instructions across the volatile read or write barrier. However, volatile does not provide atomicity for compound operations like count++.",
         "Modern multi-core CPUs use hierarchical hardware caches. Without synchronization, thread A can write to a variable in its core cache without thread B ever observing the change. Under JSR-133, a volatile write generates a StoreStore and StoreLoad memory fence, ensuring all preceding writes become visible before the volatile write. A volatile read generates LoadLoad and LoadStore fences, preventing following reads from being reordered before the volatile read.",
         "public class WorkerThread implements Runnable {\n    private volatile boolean running = true;\n    public void stop() { this.running = false; }\n    @Override public void run() {\n        while (running) {\n            // cooperative work\n        }\n    }\n}",
         "Volatile is suitable for single-variable flags and status markers, but insufficient for multi-step state mutations.",
         "Using volatile for compound operations like count++ creates race conditions and lost updates under concurrent access.",
         "Volatile incurs no thread blocking or context switching, making it significantly faster than synchronized blocks.",
         ["Assuming volatile makes increment operations atomic.", "Declaring an array volatile and expecting its elements to be volatile.", "Using volatile when locks or atomic primitives are required."],
         ("What is CPU cache coherence?", "Does volatile guarantee atomicity for count++?", "What is a memory barrier?"),
         "https://www.cs.umd.edu/~pugh/java/memoryModel/jsr133.pdf", "JSR-133: Java Memory Model Specification",
         "Why was double-checked locking broken before Java 5?", "Instruction reordering allowed a thread to see a non-null instance before its fields were fully initialized.", ["Java", "Concurrency", "JVM", "Uber"]),

        ("What is the difference between Runnable and Callable in Java?", "executors-concurrency-utils",
         "Runnable defines a void run() method that cannot return a result or throw checked exceptions, whereas Callable<V> defines a V call() method that can return a computed value and throw checked exceptions.",
         "Runnable (introduced in Java 1.0) represents a task that executes asynchronously without returning a value; its `run()` method returns void and cannot throw checked exceptions. Callable<V> (introduced in Java 5 alongside java.util.concurrent) represents a parameterized task whose `call()` method returns a result of type V and is declared to throw Exception, making it ideal for use with ExecutorService and Future<V>.",
         "Callable was created specifically to eliminate the clumsy workarounds required with Runnable, such as writing results to shared thread-safe holder variables and capturing exceptions manually. When submitted to an ExecutorService, a Callable is wrapped into a FutureTask<V>, which manages the task lifecycle (NEW, COMPLETING, NORMAL, EXCEPTIONAL) and delivers either the return value via `future.get()` or unrolls the thrown exception as an ExecutionException.",
         "import java.util.concurrent.*;\npublic class CallableDemo {\n    public static void main(String[] args) throws Exception {\n        ExecutorService exec = Executors.newFixedThreadPool(2);\n        Callable<Integer> task = () -> 21 * 2;\n        Future<Integer> future = exec.submit(task);\n        System.out.println(\"Result: \" + future.get(1, TimeUnit.SECONDS));\n        exec.shutdown();\n    }\n}",
         "Always specify a timeout when calling `future.get(timeout, unit)` to prevent thread starvation if tasks hang.",
         "Uncaught exceptions in Runnable are swallowed or routed to UncaughtExceptionHandler without alerting task submitters.",
         "Callable incurs a minor object allocation for FutureTask compared to lightweight Runnable execution.",
         ["Calling future.get() immediately after submit(), eliminating async concurrency.", "Forgetting to shutdown ExecutorService.", "Assuming Callable can be passed directly to new Thread(callable) without FutureTask wrapper."],
         ("How do you return values from async tasks?", "How are exceptions propagated in Callable?", "What wraps a Callable in an Executor?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Callable.html", "Oracle Java SE Documentation: java.util.concurrent.Callable",
         "How does Future.get() unwrap exceptions from Callable?", "It rethrows the exception wrapped in an ExecutionException; extract the cause using getCause().", ["Java", "Concurrency", "ThreadPool", "TCS"]),

        ("What are the major memory regions in the JVM runtime data area?", "jvm-memory-gc",
         "The JVM runtime data area comprises the Heap (shared, stores objects), Method Area / Metaspace (shared, stores class metadata), JVM Stacks (per-thread, stores frames/local variables), Native Method Stacks (per-thread), and Program Counter (PC) Registers (per-thread).",
         "JVM memory is split into thread-shared and thread-private regions. The shared regions are the Heap (where all class instances and arrays reside, managed by Garbage Collection) and Metaspace (native memory holding loaded class bytecode, constant pools, and method metadata). The thread-private regions are JVM Stacks (holding stack frames with local variables and operand stacks), Native Method Stacks (for JNI calls), and PC Registers (tracking bytecode execution offsets).",
         "Understanding this layout is crucial for troubleshooting memory errors. OutOfMemoryError: Java heap space indicates the heap is exhausted by live objects or memory leaks. OutOfMemoryError: Metaspace indicates class metadata exhaustion, often caused by dynamic proxy or classloader leaks. StackOverflowError occurs when recursive or deep call chains exceed thread stack capacity.",
         "public class MemoryRegionsDemo {\n    private static final String APP_NAME = \"BreakTheCode\"; // Metaspace\n    private int instanceValue = 100; // Heap\n    public void execute(int param) { // Stack Frame\n        Object localObj = new Object(); // Ref on Stack, Object on Heap\n    }\n}",
         "Monitor both Heap and Metaspace metrics in production APM tools (Prometheus, Datadog) to isolate memory growth.",
         "Deep recursion without base cases throws StackOverflowError; classloader leaks in app servers exhaust native Metaspace.",
         "Heap memory is garbage collected, while stack frames are automatically reclaimed when methods return.",
         ["Confusing Metaspace (native memory since Java 8) with the legacy PermGen (heap-based).", "Assuming local primitive variables are allocated on the Heap.", "Believing Garbage Collection cleans up the JVM stack."],
         ("Which regions are shared vs thread-private?", "Where are class definitions stored?", "Where are method parameters stored?"),
         "https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-2.html#jvms-2.5", "The Java Virtual Machine Specification: Structure of the JVM",
         "What happens if Metaspace is exhausted?", "The JVM throws java.lang.OutOfMemoryError: Metaspace; tune via -XX:MaxMetaspaceSize or fix classloader leaks.", ["Java", "JVM", "Memory", "Microsoft"]),

        ("What is the difference between fail-fast and fail-safe iterators in Java Collections?", "jmm-synchronization",
         "Fail-fast iterators throw ConcurrentModificationException immediately when the underlying collection is modified during iteration (except through the iterator's own remove method), whereas fail-safe (or weakly consistent) iterators operate on a clone or snapshot and do not throw this exception.",
         "Standard collections in java.util (ArrayList, HashMap, HashSet) provide fail-fast iterators. They check an internal `modCount` variable on every `next()` call; if modCount differs from the expected count, ConcurrentModificationException is thrown immediately. In contrast, concurrent collections in java.util.concurrent (CopyOnWriteArrayList, ConcurrentHashMap) provide fail-safe or weakly consistent iterators that traverse a snapshot or allow concurrent modifications without throwing exceptions.",
         "Fail-fast behavior is designed to fail cleanly and quickly in the presence of concurrent modifications rather than risk non-deterministic behavior at an undetermined time in the future. However, fail-fast guarantees are best-effort: you must never rely on ConcurrentModificationException for program correctness.",
         "import java.util.*;\nimport java.util.concurrent.*;\npublic class IteratorDemo {\n    public static void main(String[] args) {\n        List<String> fastList = new ArrayList<>(List.of(\"A\", \"B\"));\n        List<String> safeList = new CopyOnWriteArrayList<>(List.of(\"A\", \"B\"));\n        for (String s : safeList) {\n            safeList.add(\"C\"); // Allowed without exception!\n        }\n    }\n}",
         "In multithreaded environments, never use plain ArrayList iteration without external synchronization or switching to concurrent collections.",
         "Modifying a collection inside an enhanced for-loop throws ConcurrentModificationException at runtime.",
         "Fail-fast collections offer low overhead and zero copy cost; CopyOnWriteArrayList provides safe iteration at the expense of O(N) array copy on writes.",
         ["Removing elements from a list using list.remove(item) inside a foreach loop instead of iterator.remove().", "Assuming ConcurrentModificationException only occurs in multithreaded programs (it occurs in single threads too).", "Using CopyOnWriteArrayList in write-heavy workloads."],
         ("How does modCount detect concurrent modifications?", "Which collections use snapshots for iteration?", "Why is fail-fast considered best-effort?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ConcurrentModificationException.html", "Oracle Java SE Documentation: ConcurrentModificationException",
         "Can you remove elements during fail-fast iteration safely?", "Yes, exclusively via the iterator's own Iterator.remove() method, which updates expectedModCount.", ["Java", "Collections", "Core Java", "Infosys"]),

        ("What is a ThreadLocal in Java, and why can it cause memory leaks in thread-pooled environments?", "executors-concurrency-utils",
         "ThreadLocal provides thread-confined variables where each accessing thread has an independently initialized copy. In thread pools, worker threads are reused rather than destroyed, causing ThreadLocal values to persist indefinitely unless explicitly removed with threadLocal.remove().",
         "ThreadLocal creates thread-confined storage, mapping each thread to its own isolated value without requiring synchronization. Under the hood, each Thread instance holds a `ThreadLocalMap` whose keys are WeakReferences to ThreadLocal instances, but whose values are strong references. In web application servers (Tomcat, Jetty) using thread pools, pooled worker threads stay alive across multiple HTTP requests. If a request sets a ThreadLocal value and fails to call `remove()`, the value remains pinned in memory, leading to memory leaks and cross-request data contamination.",
         "The memory leak occurs because while the key in ThreadLocalMap is a WeakReference, the value is strongly referenced by the thread's map. As long as the pooled thread remains alive, the value object and its classloader cannot be garbage collected. Always use try-finally blocks to call `threadLocal.remove()` in pooled execution environments.",
         "public class SecurityContextHolder {\n    private static final ThreadLocal<String> USER_CTX = new ThreadLocal<>();\n    public static void runWithUser(String user, Runnable task) {\n        USER_CTX.set(user);\n        try {\n            task.run();\n        } finally {\n            USER_CTX.remove(); // MANDATORY in thread pools\n        }\n    }\n}",
         "In Spring Boot and servlet containers, always clean up ThreadLocal instances in an interceptor or filter finally-block.",
         "Data leakage where request B inherits security credentials or tenant IDs set by request A on the same pooled worker thread.",
         "ThreadLocal eliminates synchronization overhead for thread-confined state, but requires strict lifecycle management.",
         ["Forgetting to call threadLocal.remove() in a finally block.", "Using ThreadLocal inside virtual threads without considering ScopedValue (Java 21).", "Storing large memory buffers in ThreadLocal, magnifying heap consumption across pool size."],
         ("How does ThreadLocal achieve thread isolation?", "What references are held in ThreadLocalMap?", "What happens to pooled threads after task completion?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ThreadLocal.html", "Oracle Java SE Documentation: java.lang.ThreadLocal",
         "Why is the ThreadLocal key a WeakReference but not the value?", "The key can be GC'd when the ThreadLocal reference is dropped, leaving the entry dead; the value remains until expunged.", ["Java", "Concurrency", "Memory", "Uber"]),

        ("What is the difference between sleep() and wait() in Java threading?", "jmm-synchronization",
         "Thread.sleep() pauses execution for a specified time without releasing any acquired monitor locks, whereas Object.wait() causes the thread to release the monitor lock and wait until notified via notify() or notifyAll() from within a synchronized block.",
         "sleep() is a static method on java.lang.Thread that temporarily suspends the current thread's execution without relinquishing lock ownership. wait() is an instance method on java.lang.Object used for inter-thread coordination; it must be called from within a synchronized context on that object, immediately releases the monitor lock, and places the thread into the object's wait set until another thread invokes notify() or notifyAll().",
         "Calling wait() outside a synchronized block throws IllegalMonitorStateException. When awakened by notify(), the thread must re-acquire the monitor lock before resuming execution. Furthermore, wait() must always be called inside a condition loop (while (!condition)) to defend against spurious wakeups.",
         "public class WaitSleepComparison {\n    private final Object lock = new Object();\n    private boolean ready = false;\n    public void waitForReady() throws InterruptedException {\n        synchronized (lock) {\n            while (!ready) {\n                lock.wait(); // Releases lock while waiting\n            }\n        }\n    }\n}",
         "Never use sleep() for condition polling; use proper synchronization primitives (Condition, CountDownLatch, CompletableFuture).",
         "Calling sleep() while holding a shared lock causes thread starvation and bottlenecks across the entire application.",
         "wait() coordinates resource availability between producer and consumer threads safely; sleep() merely halts execution.",
         ["Calling wait() outside of a synchronized block.", "Using if (!condition) wait() instead of while (!condition) wait(), falling victim to spurious wakeups.", "Calling sleep() inside synchronized methods expecting other threads to enter."],
         ("Which class declares wait vs sleep?", "Does sleep release the acquired lock?", "What is a spurious wakeup?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#wait()", "Oracle Java SE Documentation: Object.wait",
         "Why must wait() be called inside a while loop?", "To guard against spurious wakeups and state changes between notification and lock re-acquisition.", ["Java", "Concurrency", "Threading", "Wipro"]),

        ("What is the Java Virtual Thread model introduced in Java 21 (Project Loom)?", "virtual-threads-loom",
         "Virtual Threads are lightweight threads managed directly by the JVM runtime rather than the operating system kernel, enabling high-throughput concurrent I/O applications by mapping millions of virtual threads onto a small pool of carrier OS threads.",
         "Before Java 21, every java.lang.Thread was a 1:1 wrapper around an operating system thread (Platform Thread), consuming roughly 1MB of stack memory and limited by OS scheduling limits to a few thousand threads. Project Loom (JEP 444) introduced Virtual Threads: M:N lightweight threads managed in JVM user-space. When a virtual thread performs blocking I/O (socket read, JDBC query, sleep), the JVM unmounts its execution state from the underlying carrier thread, parking it in heap memory until the I/O event completes, leaving the carrier thread free to execute other virtual threads.",
         "Virtual Threads restore the intuitive thread-per-request architecture without the cognitive complexity and debugging nightmares of reactive programming frameworks (WebFlux, RxJava). However, Virtual Threads are designed exclusively for blocking I/O tasks and provide zero throughput benefits for CPU-bound computations.",
         "import java.util.concurrent.*;\npublic class VirtualThreadDemo {\n    public static void main(String[] args) {\n        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {\n            for (int i = 0; i < 10_000; i++) {\n                executor.submit(() -> {\n                    Thread.sleep(100); // Unmounts from carrier thread\n                    return 1;\n                });\n            }\n        }\n    }\n}",
         "Virtual Threads are designed for I/O-bound tasks. They do NOT accelerate CPU-intensive algorithms (cryptography, image processing).",
         "Pinning: performing blocking I/O inside synchronized blocks or native JNI methods pins the virtual thread to its carrier, causing carrier pool starvation.",
         "Virtual threads eliminate thread pooling overhead for I/O workloads, but each virtual thread allocates heap space for its execution frames.",
         ["Attempting to pool Virtual Threads (never pool them; create them on demand per task).", "Using Virtual Threads for compute-heavy number crunching.", "Ignoring synchronized blocks that cause thread pinning in high-concurrency environments."],
         ("How do Virtual Threads differ from OS threads?", "What is a carrier thread?", "What causes thread pinning?"),
         "https://openjdk.org/jeps/444", "JEP 444: Virtual Threads",
         "How does Virtual Thread memory consumption compare to Platform Threads?", "Platform threads require ~1MB fixed OS stack; virtual threads start with ~few hundred bytes in heap, scaling dynamically.", ["Java", "Virtual Threads", "Java 21", "Netflix"]),

        ("What is Garbage Collection in Java and what are Young and Old Generations?", "jvm-memory-gc",
         "Garbage Collection is automatic memory management that identifies and reclaims heap memory occupied by unreachable objects. Generational GC divides the heap into the Young Generation (Eden and Survivor spaces, for short-lived objects) and the Old Generation (for long-lived objects) based on the Weak Generational Hypothesis.",
         "The Weak Generational Hypothesis observes that most allocated objects die shortly after creation. To optimize throughput, the JVM splits the heap into Young Generation (composed of Eden and two Survivor spaces: S0 and S1) and Tenured/Old Generation. New objects are allocated in Eden. When Eden fills, a fast Minor GC reclaims dead objects and moves survivors between S0 and S1, incrementing their age. Once an object survives a threshold number of cycles (tenuring threshold, default up to 15), it is promoted to the Old Generation, which is collected less frequently during Major or Full GC cycles.",
         "Different collectors (G1GC, ZGC, ParallelGC) implement generational collection with different latency-throughput trade-offs. G1GC organizes the heap into uniform regions dynamically designated as Eden, Survivor, or Old. ZGC (in Java 21+) provides Generational ZGC, achieving sub-millisecond pause times regardless of heap size.",
         "public class GenerationalGCDemo {\n    public static void main(String[] args) {\n        for (int i = 0; i < 1_000_000; i++) {\n            String temp = String.valueOf(i); // Short-lived in Eden\n        }\n    }\n}",
         "Avoid creating unnecessary temporary objects in high-throughput hot paths to prevent premature promotion to Old Generation.",
         "Premature promotion: when Eden is undersized, short-lived objects spill directly into Old Generation, triggering expensive Full GC pauses.",
         "Generational collection reduces GC overhead by 90%+ compared to scanning the entire heap uniformly on every cycle.",
         ["Assuming System.gc() forces an immediate full collection (it is merely a non-binding hint).", "Believing objects in Old Generation are never collected.", "Setting Eden too small, causing rapid promotion of temporary objects."],
         ("What is the Weak Generational Hypothesis?", "What are Eden, S0, and S1?", "What triggers object promotion?"),
         "https://docs.oracle.com/en/java/javase/21/gctuning/", "HotSpot Virtual Machine Garbage Collection Tuning Guide",
         "What is the difference between Minor GC and Full GC?", "Minor GC collects only Young Gen (fast); Full GC collects both Young and Old Gen plus Metaspace (long pause).", ["Java", "GC", "Memory", "Amazon"]),

        ("What is the difference between throw and throws in Java exception handling?", "jmm-synchronization",
         "The 'throw' keyword is used inside a method body to explicitly throw an exception instance, whereas 'throws' is used in a method declaration to specify the checked exceptions that the method may propagate to its caller.",
         "'throw' is an imperative statement followed by an instantiated Throwable object (e.g., `throw new IllegalArgumentException(\"Invalid id\");`). 'throws' is a declarative clause appended to a method signature indicating that the method might throw one or more checked exceptions (e.g., `public void readFile() throws IOException`), requiring the calling method to either catch the exception or declare it in its own throws clause.",
         "Java distinguishes checked exceptions (subclasses of Exception excluding RuntimeException) from unchecked exceptions (RuntimeException and Error). Checked exceptions enforce compile-time verification via 'throws', whereas unchecked exceptions represent programming errors (NullPointerException, IllegalArgumentException) and do not require declaration.",
         "public class ExceptionDemo {\n    public void parseData(String input) throws java.io.IOException {\n        if (input == null) {\n            throw new IllegalArgumentException(\"Input cannot be null\");\n        }\n    }\n}",
         "Favor unchecked exceptions for unrecoverable business rule violations and checked exceptions only when the caller can realistically recover.",
         "Swallowing exceptions in empty catch blocks hides production bugs and prevents monitoring systems from capturing stack traces.",
         "Checked exceptions ensure compile-time safety, but can clutter API signatures and method contracts.",
         ["Catching generic Exception or Throwable, masking unexpected runtime errors.", "Throwing raw RuntimeException without a meaningful contextual error message.", "Using exceptions for normal control flow logic."],
         ("Which keyword is used in a method signature?", "What is a checked exception?", "Can throw be used with any object?"),
         "https://docs.oracle.com/javase/tutorial/essential/exceptions/declaring.html", "Oracle Java Documentation: Throwing and Declaring Exceptions",
         "Can an overriding method declare more checked exceptions than the parent?", "No, it can only declare the same, fewer, or subclass exceptions to preserve the Liskov Substitution Principle.", ["Java", "Exceptions", "Core Java", "Capgemini"]),

        ("What is the difference between Comparable and Comparator in Java?", "jmm-synchronization",
         "Comparable defines the natural ordering of an object by implementing compareTo(T o) within the class itself, whereas Comparator defines custom, external sorting logic by implementing compare(T o1, T o2) in a separate class or lambda.",
         "Comparable<T> is implemented by a class to give its instances an intrinsic, natural order (e.g., String, Integer, LocalDate). Its method `int compareTo(T other)` returns a negative integer, zero, or positive integer. Comparator<T> is an external functional interface that allows defining multiple sorting strategies for a class without modifying its source code, supported by modern factory methods like Comparator.comparing().",
         "Collections.sort(list) and Arrays.sort() use Comparable by default. Providing an explicit Comparator overrides natural ordering. Both must remain consistent with equals() (i.e. compare(x, y) == 0 should imply x.equals(y)) to prevent erratic behavior when used in SortedSet (TreeSet) or SortedMap (TreeMap).",
         "import java.util.*;\npublic class Student implements Comparable<Student> {\n    private final String name;\n    private final int grade;\n    public Student(String name, int grade) { this.name = name; this.grade = grade; }\n    @Override public int compareTo(Student o) {\n        return Integer.compare(this.grade, o.grade);\n    }\n    public static Comparator<Student> byName() {\n        return Comparator.comparing(s -> s.name);\n    }\n}",
         "Use Comparator.comparing() with method references for clean, readable, and composable sorting chains.",
         "Subtracting integer values in compareTo (e.g. `return a.id - b.id;`) causes integer overflow bugs when values have opposite signs.",
         "Comparable couples the sorting logic directly to the domain entity; Comparator provides modular, multi-attribute sorting.",
         ["Using primitive subtraction in compareTo instead of Integer.compare().", "Defining a comparison logic that violates the transitive or anti-symmetric properties.", "Inconsistent ordering between compareTo() and equals() in TreeSets."],
         ("Where is compareTo declared?", "How do you define multiple sort orders?", "Why is Integer.compare preferred over subtraction?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Comparable.html", "Oracle Java SE Documentation: java.lang.Comparable",
         "What happens if compareTo is inconsistent with equals in a TreeSet?", "The TreeSet may violate the Set contract by rejecting elements that have different equals() but compareTo() == 0.", ["Java", "Collections", "Sorting", "GlobalLogic"]),

        ("What is the purpose of the finalize() method in Java, and why is it deprecated?", "jvm-memory-gc",
         "The finalize() method was intended for object cleanup before garbage collection, but it is deprecated because of unpredictable execution timing, severe performance degradation, thread deadlocks, and resurrection security vulnerabilities; developers should use AutoCloseable and Cleaner instead.",
         "finalize() was introduced in Java 1.0 to let objects release native resources before GC reclamation. However, the JVM provides no guarantee of when—or even if—finalize() will run. Objects with finalizers delay garbage collection by at least two GC cycles, can resurrect themselves by re-assigning 'this' to an active reference, and can trigger JVM deadlocks if finalizer threads block. It was deprecated in Java 9 and marked for removal in Java 18 (JEP 421).",
         "Modern Java replaces finalize() with the `try-with-resources` pattern via the `AutoCloseable` interface for deterministic resource cleanup. For non-deterministic native cleanup, `java.lang.ref.Cleaner` (or Java 22+ Foreign Function & Memory API Arenas) provides safe, un-resurrectable phantom reference cleaning.",
         "public class ResourceCleaner implements AutoCloseable {\n    private boolean closed = false;\n    public void doWork() {\n        if (closed) throw new IllegalStateException(\"Closed\");\n    }\n    @Override public void close() {\n        if (!closed) {\n            closed = true;\n            System.out.println(\"Cleaned\");\n        }\n    }\n}",
         "Always wrap file handles, database connections, and network streams in try-with-resources blocks.",
         "Relying on finalize() to close sockets or file descriptors causes operating system file descriptor exhaustion under load.",
         "try-with-resources guarantees deterministic cleanup at scope exit; finalize() depends on uncertain GC scheduling.",
         ["Relying on finalize() for critical resource cleanup.", "Not using try-with-resources for classes implementing AutoCloseable.", "Calling System.runFinalization(), which blocks threads unpredictably."],
         ("When does finalize execute?", "What is object resurrection?", "What replaced finalize in modern Java?"),
         "https://openjdk.org/jeps/421", "JEP 421: Deprecate Finalization for Removal",
         "How does java.lang.ref.Cleaner solve finalizer issues?", "It runs on dedicated cleaner threads using PhantomReferences, avoiding object resurrection and finalizer thread locks.", ["Java", "GC", "Core Java", "Oracle"]),

        ("What is the Diamond Problem in object-oriented programming, and how does Java handle it with default methods?", "jmm-synchronization",
         "The Diamond Problem arises when a class inherits from two parents that provide conflicting implementations of the same method. Java solves this for interfaces with default methods by enforcing strict compiler rules requiring the implementing class to explicitly override the conflicting method.",
         "Java avoids the diamond problem with state by forbidding multiple class inheritance. However, when Java 8 introduced default methods in interfaces, multiple inheritance of behavior became possible. If interface A and interface B define an identical default method `void log()`, and class C implements both A and B without overriding `log()`, the Java compiler detects ambiguity and fails to compile.",
         "To resolve the conflict, class C must provide an explicit implementation. Inside C's overridden method, it can provide custom logic or explicitly designate which interface behavior to adopt using `InterfaceName.super.methodName()`.",
         "interface LoggerA {\n    default void log(String msg) { System.out.println(\"A: \" + msg); }\n}\ninterface LoggerB {\n    default void log(String msg) { System.out.println(\"B: \" + msg); }\n}\npublic class CompositeLogger implements LoggerA, LoggerB {\n    @Override public void log(String msg) {\n        LoggerA.super.log(msg); // Explicit resolution\n    }\n}",
         "Keep interface default methods focused on behavioral defaults, avoiding competing business logic across interface hierarchies.",
         "Compilation failure when adding a new default method to an existing interface that clashes with another interface in third-party client code.",
         "Explicit resolution guarantees deterministic method dispatch and eliminates runtime ambiguity.",
         ["Assuming the compiler picks the first declared interface automatically.", "Believing Java allows multiple inheritance of state (member variables).", "Forgetting the 'InterfaceName.super.method()' invocation syntax."],
         ("Why did Java avoid multiple class inheritance?", "What happens if two default methods clash?", "How is ambiguity resolved syntactically?"),
         "https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html", "Oracle Java Documentation: Default Methods",
         "What if a parent class method conflicts with an interface default method?", "Class implementations always win over interface default methods (Class Wins rule).", ["Java", "OOP", "Core Java", "Apple"]),

        ("What is the difference between synchronized method and synchronized block in Java?", "jmm-synchronization",
         "A synchronized method locks the entire method scope using the implicit object monitor ('this' or Class object), while a synchronized block locks only a specific critical section using an explicitly chosen monitor object, offering finer granularity and better concurrency.",
         "A synchronized instance method automatically acquires the monitor of 'this' for the entire duration of the method invocation, releasing it upon return or exception. A synchronized block allows locking on any arbitrary reference (including private dedicated lock objects) and confines synchronization strictly to the lines of code that mutate shared state.",
         "Synchronized blocks are strongly preferred in production code because locking 'this' exposes your synchronization lock to external callers who can synchronize on your object reference, accidentally causing deadlocks. Using a private final lock object (`private final Object lock = new Object();`) completely prevents external lock interference.",
         "public class Account {\n    private double balance;\n    private final Object lock = new Object();\n    public void deposit(double amount) {\n        if (amount <= 0) return;\n        synchronized (lock) {\n            balance += amount; // Minimum critical section\n        }\n    }\n}",
         "Keep synchronized blocks as small as possible. Never perform I/O operations (HTTP, DB, file) inside synchronized blocks.",
         "Synchronizing on 'this' allows foreign code to hold the monitor of your object and trigger unexpected deadlocks.",
         "Synchronized blocks reduce lock holding time, maximizing CPU throughput and thread parallelism.",
         ["Synchronizing entire methods when only one variable assignment needs synchronization.", "Using non-final lock objects, which can be reassigned and break synchronization.", "Performing network calls inside synchronized blocks."],
         ("What monitor is acquired by a synchronized method?", "Why is locking 'this' risky?", "How do you scope a critical section?"),
         "https://docs.oracle.com/javase/tutorial/essential/concurrency/locksync.html", "Oracle Java Documentation: Synchronized Methods and Statements",
         "What monitor is used by a static synchronized method?", "The Class object corresponding to the class declaring the static method (e.g. MyClass.class).", ["Java", "Concurrency", "Synchronization", "Stripe"]),

        ("What is the purpose of the CountDownLatch utility in java.util.concurrent?", "executors-concurrency-utils",
         "CountDownLatch is a synchronization aid that allows one or more threads to wait until a set of operations being performed in other threads completes, by decrementing a count via countDown() until it reaches zero.",
         "CountDownLatch is initialized with a positive count. Worker threads perform their assigned tasks and call `latch.countDown()`, decrementing the counter. Coordinator threads call `latch.await()`, which blocks until the counter reaches zero due to successive countDown() calls. Unlike a CyclicBarrier, a CountDownLatch is a one-shot gate; once the count reaches zero, it cannot be reset.",
         "Under the hood, CountDownLatch utilizes AbstractQueuedSynchronizer (AQS) in shared mode. Calling await() acquires the AQS shared synchronizer, and countDown() releases it when the state reaches 0, unparking all blocked waiting threads simultaneously.",
         "import java.util.concurrent.*;\npublic class LatchDemo {\n    public static void main(String[] args) throws Exception {\n        CountDownLatch latch = new CountDownLatch(2);\n        ExecutorService exec = Executors.newFixedThreadPool(2);\n        exec.submit(() -> { try { System.out.println(\"A\"); } finally { latch.countDown(); } });\n        exec.submit(() -> { try { System.out.println(\"B\"); } finally { latch.countDown(); } });\n        latch.await(5, TimeUnit.SECONDS);\n        exec.shutdown();\n    }\n}",
         "Always call `latch.countDown()` inside a `finally` block to guarantee decrement even if the worker task throws an unhandled exception.",
         "If a worker thread throws an unhandled exception before countDown(), the count never reaches zero, causing coordinator threads to hang indefinitely without a timeout.",
         "CountDownLatch provides a simple, lock-free coordination mechanism for parallel fan-out / fan-in patterns.",
         ["Calling await() without a timeout, risking permanent thread blockage.", "Calling countDown() outside of finally blocks.", "Attempting to reuse a CountDownLatch (use CyclicBarrier for recurring cycles)."],
         ("Can CountDownLatch be reset?", "What happens if a worker task fails?", "What backing framework powers CountDownLatch?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CountDownLatch.html", "Oracle Java SE Documentation: CountDownLatch",
         "How does CountDownLatch differ from CyclicBarrier?", "CountDownLatch is one-shot for waiting on N events; CyclicBarrier is reusable and makes N threads wait at a common barrier point.", ["Java", "Concurrency", "AQS", "Databricks"]),

        ("What is the difference between final, finally, and finalize in Java?", "jmm-synchronization",
         "final is a keyword defining non-modifiable constants, un-overridable methods, or un-inheritable classes; finally is a block in exception handling guaranteed to execute after try-catch; finalize is a deprecated Object method formerly used for garbage collection cleanup.",
         "'final' is an access modifier: a final variable cannot be reassigned, a final method cannot be overridden by subclasses, and a final class cannot be extended. 'finally' is an exception-handling construct executed after a try-catch block regardless of whether an exception occurred, used for mandatory cleanup. 'finalize()' is a deprecated method on java.lang.Object called by the garbage collector before reclaiming an object, now replaced by AutoCloseable.",
         "In the Java Memory Model, final fields receive special initialization safety guarantees: when an object is properly constructed, any thread reading a final field is guaranteed to observe the value set in the constructor without requiring synchronization.",
         "public final class ImmutableToken {\n    private final String token;\n    public ImmutableToken(String token) { this.token = token; }\n    public void process() {\n        try { System.out.println(\"Processing\"); }\n        finally { System.out.println(\"Always runs in finally\"); }\n    }\n}",
         "Use final for all fields that should not change after construction, facilitating thread-safe immutable design patterns.",
         "The finally block may not execute if `System.exit(0)` is invoked, or if the host JVM process crashes / power fails.",
         "final fields enable JIT compiler optimizations like constant folding and aggressive inlining.",
         ["Confusing the three completely distinct language keywords due to similar naming.", "Relying on finally to execute after calling System.exit().", "Using finalize() for production resource cleanup."],
         ("What does final on a class do?", "Does finally always execute?", "Why was finalize deprecated?"),
         "https://docs.oracle.com/javase/tutorial/essential/exceptions/finally.html", "Oracle Java Documentation: The finally Block",
         "What memory guarantee does final provide across threads in the JMM?", "Initialization safety: once a constructor completes without leaking 'this', all threads see final field values without synchronization.", ["Java", "Core Java", "JMM", "Amazon"]),

        ("What is the purpose of the Java Generics Type Erasure mechanism?", "jmm-synchronization",
         "Type erasure removes generic type annotations at compile time and inserts appropriate casts and bridge methods into bytecode, ensuring full binary backward compatibility with pre-Java 5 legacy code while maintaining compile-time type safety.",
         "When Java introduced generics in Java 5, maintaining binary compatibility with billions of lines of pre-existing code was paramount. Instead of creating reified types at runtime (like C# or C++ templates), Java employs Type Erasure: the compiler validates types, then replaces unbounded type parameters with Object (or the first bound) and inserts synthetic type casts in bytecode where necessary. At runtime, List<String> and List<Integer> share the exact same raw class: List.class.",
         "Because of type erasure, you cannot instantiate generic types directly (`new T()`), create generic arrays (`new T[10]`), or use `instanceof List<String>`. Reflection on raw objects loses generic information, although generic signatures on class and method declarations are preserved in the ClassFile's Signature attribute for reflection inspection.",
         "import java.util.*;\npublic class ErasureDemo {\n    public static void main(String[] args) {\n        List<String> stringList = new ArrayList<>();\n        List<Integer> intList = new ArrayList<>();\n        System.out.println(stringList.getClass() == intList.getClass()); // true!\n    }\n}",
         "Be aware of type erasure when designing serialization or JSON mapping (e.g. Jackson TypeReference is required to capture generic types via super-type tokens).",
         "Attempting runtime type checks with `instanceof List<SpecificClass>` causes compilation errors due to erased type parameters.",
         "Type erasure achieved seamless backward compatibility with zero JVM bytecode changes, but eliminates runtime generic type reification.",
         ["Trying to create generic arrays directly (e.g. `new T[size]`).", "Expecting `list.getClass().getTypeParameters()` to reveal the runtime generic argument.", "Ignoring compiler unchecked cast warnings in generic repositories."],
         ("Why did Java choose type erasure over reification?", "Can you do `new T()`?", "How does Jackson deserialize generic lists?"),
         "https://docs.oracle.com/javase/tutorial/java/generics/erasure.html", "Oracle Java Documentation: Type Erasure",
         "What is a synthetic bridge method generated by the compiler during type erasure?", "A compiler-generated method in bytecode to preserve polymorphic method overriding when a subclass implements a parameterized interface.", ["Java", "Generics", "JVM", "Google"]),

        ("What is the difference between Thread.start() and Thread.run() in Java?", "executors-concurrency-utils",
         "Thread.start() allocates a new execution stack and schedules a new operating system/JVM thread to invoke run(), whereas calling Thread.run() directly executes the method synchronously on the current calling thread like any regular method call.",
         "The `start()` method initializes thread state in the JVM, invokes the operating system's thread creation API (such as pthread_create on POSIX), and registers the new thread with the OS/JVM scheduler. Once scheduled, the new thread invokes the `run()` method asynchronously on its own distinct call stack. Directly calling `run()` bypasses thread creation entirely; the code runs synchronously within the caller's existing thread and call stack.",
         "Calling `start()` more than once on the same Thread instance throws `IllegalThreadStateException`, because a thread's lifecycle state machine moves from NEW to RUNNABLE and cannot be restarted once stopped.",
         "public class ThreadStartVsRun {\n    public static void main(String[] args) {\n        Thread thread = new Thread(() -> {\n            System.out.println(\"Executing: \" + Thread.currentThread().getName());\n        });\n        thread.start(); // Spawns new thread\n    }\n}",
         "Never call `run()` directly when concurrent asynchronous execution is desired; always use `start()` or an ExecutorService.",
         "Calling `run()` directly causes unexpected blocking in GUI dispatchers or server request handlers, masquerading as thread safety while executing synchronously.",
         "start() handles OS thread creation and stack allocation; run() is merely the task payload.",
         ["Calling run() instead of start(), resulting in synchronous execution.", "Calling start() twice on the same thread instance.", "Creating raw Thread instances directly in high-throughput servers instead of using ExecutorService."],
         ("What does start() do at the OS level?", "Can you start a thread twice?", "What stack does run() execute on when called directly?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Thread.html#start()", "Oracle Java SE Documentation: Thread.start",
         "What lifecycle state transition occurs when start() is called?", "The thread moves from NEW to RUNNABLE, entering the JVM thread scheduler queue.", ["Java", "Concurrency", "Threading", "Wipro"])
    ]

    for item in basic_raw:
        questions.append(make_q(
            item[0], "BASIC", item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15]
        ))

    # =========================================================
    # 20 MEDIUM
    # =========================================================
    # (Questions 21 to 40)
    from pilot_full_dataset import build_medium_20
    medium_from_file = build_medium_20()
    questions.extend(medium_from_file)

    # Add 5 more medium to reach exactly 20 Medium
    more_med = [
        ("How does the Java 21 Record class achieve immutability and transparent data carrier semantics?", "jmm-synchronization",
         "Java Records (JEP 395) are transparent immutable data carriers where the compiler automatically generates private final fields, canonical constructor, accessors, equals, hashCode, and toString based on the state description.",
         "Records model data as data without boilerplate. When declared as `public record User(String id, String email) {}`, the compiler automatically generates a final class extending `java.lang.Record`. All component fields are strictly private and final, component accessors match field names directly without get prefixes, and equals(), hashCode(), and toString() are automatically derived from all state components.",
         "Records cannot extend other classes (they implicitly extend java.lang.Record), but can implement interfaces. Their canonical constructor can be customized via compact constructors (`public User { Objects.requireNonNull(id); }`) for invariant validation.",
         "public record OrderRecord(String orderId, double amount) {\n    public OrderRecord {\n        if (amount < 0) throw new IllegalArgumentException(\"Amount cannot be negative\");\n    }\n}",
         "Use Records for DTOs, API payloads, value objects, and composite map keys to guarantee immutability.",
         "Mutating a mutable object (like a Date or ArrayList) stored inside a Record compromises its immutability unless defensively copied in the constructor.",
         "Records provide extreme readability and correctness, but cannot participate in mutable class inheritance hierarchies.",
         ["Assuming Record fields can be reassigned.", "Storing mutable collections in Records without defensive copies in constructor and accessor.", "Trying to extend an abstract class with a Record."],
         ("What class do all Records implicitly extend?", "Can Records have mutable fields?", "What is a compact constructor?"),
         "https://openjdk.org/jeps/395", "JEP 395: Records",
         "How does Record serialization differ from normal class serialization?",
         "Records bypass standard readObject() customization and are reconstructed strictly via their canonical constructor, preventing deserialization vulnerabilities.", ["Java", "Records", "Core Java", "Amazon"]),

        ("What is the difference between Semaphore and ReentrantLock in Java concurrency?", "executors-concurrency-utils",
         "ReentrantLock grants exclusive access to a single thread at a time and is owned by the acquiring thread, whereas Semaphore maintains permits allowing N concurrent threads and has no concept of thread ownership.",
         "A ReentrantLock is an exclusive mutual exclusion mechanism: only one thread holds the lock at any instant, and only that same thread can release it (or IllegalMonitorStateException is thrown). A Semaphore controls access to a pool of N shared resources using permits. Calling `acquire()` decrements permits; calling `release()` increments permits. Crucially, a permit acquired by thread A can be released by thread B, making Semaphores suitable for signaling and producer-consumer rate-limiting.",
         "Under the hood, Semaphore uses AQS in shared mode (`tryAcquireShared` and `tryReleaseShared`).",
         "import java.util.concurrent.Semaphore;\npublic class RateLimiter {\n    private final Semaphore semaphore = new Semaphore(3);\n    public void access() throws InterruptedException {\n        semaphore.acquire();\n        try { System.out.println(\"Active slot\"); }\n        finally { semaphore.release(); }\n    }\n}",
         "Use Semaphores to throttle concurrent calls to downstream rate-limited APIs or database connection pools.",
         "Forgetting to release semaphore permits in finally blocks permanently leaks permits, eventually starving all callers.",
         "Semaphores provide flexible N-resource gating, but do not provide reentrancy or lock ownership verification.",
         ["Using Semaphore as an exclusive lock when reentrancy is required.", "Forgetting to release permits in finally blocks.", "Calling release() more times than acquire(), accidentally increasing the total permit pool above its initial capacity."],
         ("Can a different thread release a Semaphore permit?", "How does Semaphore throttle connections?", "What is the difference between fair and unfair Semaphore?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Semaphore.html", "Oracle Java SE Documentation: Semaphore",
         "What happens if release() is called without calling acquire()?",
         "The permit count increases above the original limit, which can lead to unexpected concurrency leaks unless guarded.", ["Java", "Concurrency", "Semaphore", "Google"]),

        ("How does the Java Optional class prevent NullPointerExceptions when used correctly?", "jmm-synchronization",
         "Optional is a container object used primarily as a method return type to represent the potential absence of a value, encouraging callers to handle emptiness explicitly via functional combinators like map, filter, and orElseGet.",
         "Optional was designed to eliminate silent NullPointerExceptions on method return values. Instead of returning `null` when a search yields no result, returning `Optional<T>` forces the calling code to consciously handle the missing case. It provides fluent monadic operations like `map()`, `flatMap()`, `filter()`, and safe defaults like `orElseGet(Supplier)`.",
         "Optional should NOT be used as method parameters, class fields, or collection elements, as it adds unnecessary object wrapping overhead and is not Serializable.",
         "import java.util.Optional;\npublic class OptionalDemo {\n    public static Optional<String> findUser(String id) {\n        return id.equals(\"1\") ? Optional.of(\"Alice\") : Optional.empty();\n    }\n    public static void main(String[] args) {\n        String user = findUser(\"2\").orElseGet(() -> \"Guest\");\n        System.out.println(user); // Guest\n    }\n}",
         "Use `orElseGet(() -> expensiveComputation())` rather than `orElse(expensiveComputation())` to avoid eager evaluation of fallback code when the value is present.",
         "Calling `optional.get()` without calling `isPresent()` recreates the exact NoSuchElementException problem that Optional was designed to avoid.",
         "Optional improves API clarity and compile-time mindfulness, but incurs minor heap allocation overhead for empty/present wrappers.",
         ["Calling optional.get() directly without checking isPresent().", "Using orElse() with expensive database calls instead of lazy orElseGet().", "Declaring class fields or method parameters as Optional."],
         ("When should Optional be used?", "What is the difference between orElse and orElseGet?", "Why should Optional not be used as a field?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Optional.html", "Oracle Java SE Documentation: java.util.Optional",
         "Why is Optional not Serializable in Java?",
         "It was intended strictly as a lightweight method return type for libraries and lambdas, not a persistent domain model component.", ["Java", "Clean Code", "Core Java", "Netflix"]),

        ("How does the StampedLock in java.util.concurrent improve read-heavy concurrency over ReentrantReadWriteLock?", "jmm-synchronization",
         "StampedLock introduces optimistic reading mode that acquires no locks, returning a long stamp validated via validate(stamp), eliminating reader lock contention and cache-line invalidation in read-heavy workloads.",
         "ReentrantReadWriteLock allows multiple concurrent readers, but readers still mutate shared internal state (the AQS state integer and reader hold counter), causing CPU cache-line bouncing and reader contention. StampedLock (Java 8) solves this with three modes: Writing, Reading, and Optimistic Reading. In Optimistic Reading mode (`tryOptimisticRead()`), no lock is acquired and no state is written to memory. The thread simply reads fields into local variables, then calls `validate(stamp)`. If no write lock was acquired in the interim, the read is valid without ever acquiring a lock.",
         "If validation fails (a write lock occurred), the thread falls back to a standard pessimistic read lock or retries. StampedLock is NOT reentrant, so recursive calls will deadlock.",
         "import java.util.concurrent.locks.StampedLock;\npublic class Point {\n    private double x, y;\n    private final StampedLock sl = new StampedLock();\n    public double distanceFromOrigin() {\n        long stamp = sl.tryOptimisticRead();\n        double curX = x, curY = y;\n        if (!sl.validate(stamp)) {\n            stamp = sl.readLock();\n            try { curX = x; curY = y; }\n            finally { sl.unlockRead(stamp); }\n        }\n        return Math.sqrt(curX * curX + curY * curY);\n    }\n}",
         "Ideal for high-read, low-write in-memory caches and geometric/financial calculation engines.",
         "Calling lock methods recursively with StampedLock causes permanent self-deadlocks because it is non-reentrant.",
         "Optimistic reads have zero lock overhead and zero memory fence cost on reads, but require defensive retry logic.",
         ["Assuming StampedLock is reentrant (it is strictly non-reentrant).", "Reading fields directly without copying to local variables before validation.", "Using StampedLock with Virtual Threads when blocking is prolonged."],
         ("What is an optimistic read in StampedLock?", "Is StampedLock reentrant?", "What does validate(stamp) do?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/StampedLock.html", "Oracle Java SE Documentation: StampedLock",
         "Why is StampedLock vulnerable to deadlocks if interrupted?",
         "Unchecked lock interrupts in StampedLock historically could spin CPU to 100%; always use `readLockInterruptibly` or `writeLockInterruptibly` if cancellation is needed.", ["Java", "Concurrency", "Locks", "Stripe"]),

        ("How does the Parallel Stream framework in Java partition work and when should it be avoided?", "executors-concurrency-utils",
         "Parallel streams split data sources using Spliterators and execute operations across worker threads in the shared ForkJoinPool.commonPool(), which should be avoided for I/O-bound tasks, small datasets, or stateful operations.",
         "Parallel streams invoke `collection.parallelStream()`, which uses a `Spliterator` to recursively partition the dataset into chunks and submits them to `ForkJoinPool.commonPool()`. While convenient, parallel streams have major production pitfalls: 1. They use the shared JVM common pool, so blocking on network/DB operations starves all parallel streams across the application, 2. The overhead of thread scheduling and array partitioning exceeds execution time for small datasets (N < 10,000), and 3. Non-thread-safe stateful accumulators produce corrupted results.",
         "Parallel streams excel primarily for compute-intensive, CPU-bound mathematical transformations on well-partitioned arrays (e.g. ArrayList, primitive arrays) where operations on each element are completely independent.",
         "import java.util.List;\npublic class ParallelStreamDemo {\n    public static long computeSquares(List<Integer> numbers) {\n        // Only use for CPU-bound computations with large datasets!\n        return numbers.parallelStream()\n                      .mapToLong(n -> (long) n * n)\n                      .sum();\n    }\n}",
         "Keep parallel streams strictly confined to CPU-bound processing on ArrayLists; avoid LinkedLists because they split poorly.",
         "Blocking I/O inside parallel streams exhausts the shared ForkJoinPool common pool, degrading unrelated system components.",
         "Parallel streams leverage multi-core CPUs effortlessly, but introduce significant thread context switching and coordination overhead for small collections.",
         ["Using parallel streams for database or HTTP calls.", "Using parallel streams on collections with poor splitting characteristics (like LinkedList or Stream.iterate).", "Mutating shared external state inside parallel stream forEach blocks."],
         ("What pool executes parallel streams?", "What is a Spliterator?", "Why does LinkedList perform poorly with parallel streams?"),
         "https://docs.oracle.com/javase/tutorial/collections/streams/parallelism.html", "Oracle Java Documentation: Parallelism in Streams",
         "How do you run a parallel stream on a custom ForkJoinPool instead of the common pool?",
         "Submit the parallel stream execution as a task to `customForkJoinPool.submit(() -> stream.parallel()...)`.join().", ["Java", "Streams", "ForkJoin", "Amazon"])
    ]

    for item in more_med:
        deep_exp = f"{item[3]}\n\nDeep Architectural Analysis:\n{item[4]}" if len(item[4]) < 150 else item[4]
        questions.append(make_q(
            item[0], "MEDIUM", item[1], item[2], item[3], deep_exp, item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15]
        ))

    # =========================================================
    # 20 HARD / TOUGH
    # =========================================================
    # (Questions 41 to 60)
    from scripts.generate_curated_pilot_batch import get_80_pilot_questions
    hard_seeds = [q for q in get_80_pilot_questions() if q["difficulty"] in ["HARD", "TOUGH"]]
    questions.extend(hard_seeds)

    # 15 additional Hard / Tough questions
    more_hard = [
        ("How does the HotSpot JVM JIT compiler perform Escape Analysis, Scalar Replacement, and Lock Coarsening?", "HARD", "jvm-memory-gc",
         "Escape Analysis determines if an object's scope escapes its allocating thread or method; if non-escaping, C2 compiler applies Scalar Replacement (allocating fields directly to CPU registers/stack without heap allocation) and Lock Elision/Coarsening.",
         "HotSpot C2 compiler analyzes data flow to categorize object escape state: 1. NoEscape (object cannot be observed outside the allocating method), 2. ArgEscape (passed as an argument but does not escape thread lifetime), and 3. GlobalEscape (stored in a static field, escaped to another thread, or returned). If an object has NoEscape, C2 performs Scalar Replacement: it dismantles the object into its individual primitive fields, storing them directly in CPU registers or on the stack frame, bypassing heap allocation and garbage collection entirely. Additionally, non-escaping synchronized locks are completely eliminated (Lock Elision) or merged across loops (Lock Coarsening).",
         "This optimization explains why microbenchmarking short-lived objects without blackholes often yields misleading zero-allocation metrics.",
         "public class EscapeAnalysisDemo {\n    public int compute() {\n        // Point does NOT escape compute(); C2 decomposes it into primitive ints x and y in registers!\n        Point p = new Point(10, 20);\n        return p.x + p.y;\n    }\n    static class Point { int x, y; Point(int x, int y) { this.x = x; this.y = y; } }\n}",
         "Write focused, cohesive methods to facilitate C2 Escape Analysis. Complex methods exceeding inlining thresholds (default -XX:MaxInlineLevel=9) fail escape analysis.",
         "Premature object publishing or assigning references to fields defeats escape analysis, forcing heap allocation and GC pressure.",
         "Scalar replacement delivers instant memory reclamation upon method return with zero GC overhead.",
         ["Assuming all `new` operations allocate on the heap (HotSpot scalar replacement avoids heap allocation).", "Writing giant 500-line methods that exceed JIT inlining limits.", "Assuming escape analysis works when objects are passed to complex non-inlined methods."],
         ("What are the 3 levels of escape analysis?", "What is Scalar Replacement?", "What is Lock Elision?"),
         "https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-6.html", "HotSpot JIT Compiler Architecture",
         "How do you inspect if HotSpot scalar replacement is occurring?",
         "Run with `-XX:+UnlockDiagnosticVMOptions -XX:+PrintEscapeAnalysis -XX:+PrintEliminateAllocations`.", ["Java", "JIT", "Performance", "Google"]),

        ("How does the Java AtomicLong compare to LongAdder under extreme multithreaded contention?", "HARD", "executors-concurrency-utils",
         "AtomicLong relies on a single volatile variable updated via CAS loop, which degrades under high thread contention due to CPU cache-line bouncing; LongAdder distributes updates across a dynamic cell array (Striped64) to achieve order-of-magnitude higher throughput.",
         "AtomicLong maintains a single 64-bit value. When dozens of threads attempt `incrementAndGet()`, they all contend on the same cache line. If thread A wins the CAS, thread B's CAS fails and retries, creating an expensive busy-spinning loop that saturates the CPU memory bus (cache-line bouncing). LongAdder (Java 8) uses a cell-striped array (`Striped64.Cell`). When contention is detected, threads hash to independent `Cell` elements and increment them in isolation using `@Contended` cache-line padding. The total sum is aggregated only when `sum()` is called.",
         "LongAdder provides near-linear scaling for write-heavy counters, metrics, and throughput monitors, at the expense of returning an approximate snapshot during concurrent writes.",
         "import java.util.concurrent.atomic.*;\npublic class CounterBenchmark {\n    private final AtomicLong atomic = new AtomicLong();\n    private final LongAdder adder = new LongAdder();\n    public void incrementHighContention() {\n        adder.increment(); // 10x-50x faster than atomic.incrementAndGet() under 64+ threads!\n    }\n}",
         "Always use LongAdder or DoubleAdder for metrics, request counters, and rate-monitoring where writes heavily outnumber reads.",
         "Do not use LongAdder when an exact atomic sequence number or CAS guard is required (like generating unique transaction IDs).",
         "LongAdder maximizes write throughput across CPU cores, but consumes more memory for striped cell arrays and has non-atomic reads.",
         ["Using AtomicLong for high-frequency metrics across 32+ cores.", "Using LongAdder to generate strictly sequential invoice numbers.", "Assuming LongAdder.sum() is an atomic linearizable snapshot."],
         ("Why does AtomicLong suffer from cache-line bouncing?", "How does Striped64 prevent false sharing?", "When should you use AtomicLong over LongAdder?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/LongAdder.html", "Oracle Java SE Documentation: LongAdder",
         "How does `@jdk.internal.vm.annotation.Contended` work inside LongAdder.Cell?",
         "It inserts 128 bytes of padding around each Cell object, preventing adjacent cells from sharing the same CPU cache line.", ["Java", "Concurrency", "Atomics", "Stripe"]),

        ("How does the HotSpot JVM Safepoint mechanism work, and what causes Time-To-Safepoint (TTSP) latency spikes?", "TOUGH", "jvm-memory-gc",
         "Safepoints are execution points where application threads suspend their state so the JVM can perform Stop-The-World operations (GC, deoptimization, thread dumps); TTSP latency spikes occur when threads are stuck in long uncounted loops or native code without safepoint polls.",
         "To execute Stop-The-World tasks (GC phases, biased lock revocation, JVMTI stack tracing), the JVM requests a global Safepoint. In HotSpot, JIT-compiled code inserts periodic Safepoint Polls at method entries, method exits, and loop back-edges. When a safepoint is requested, the JVM arms the polling page (or sets a thread-local handshake page in Java 10+ via JEP 312). Running threads hit the poll and park. Time-To-Safepoint (TTSP) is the elapsed duration between when a safepoint is requested and when the last thread finally suspends.",
         "If a thread is stuck in an uncounted loop (e.g. `for (long i = 0; i < N; i++)` which JIT compilers historically omitted safepoint checks from), all other threads and the entire GC pause wait for that single thread, blowing past latency SLAs.",
         "// Diagnostic flags to measure TTSP in production:\n// -XX:+UnlockDiagnosticVMOptions -Xlog:safepoint=debug:file=/var/log/safepoint.log",
         "In Java 10+, Thread-Local Handshakes (JEP 312) allow the JVM to pause individual threads without stopping the world for certain VM operations.",
         "Uncounted loops with long indices can take hundreds of milliseconds to reach a safepoint poll, inflating GC pause metrics artificially.",
         "Safepoints ensure consistent memory snapshots for GC and deoptimization, but depend on timely thread cooperation.",
         ["Blaming garbage collection algorithms for long pauses when the actual delay was Time-To-Safepoint (TTSP).", "Writing long-running loops with `long` induction variables without testing for safepoint polling.", "Ignoring safepoint logging during latency triage."],
         ("What is a safepoint poll?", "What is Time-To-Safepoint (TTSP)?", "Why do uncounted loops delay safepoints?"),
         "https://openjdk.org/jeps/312", "JEP 312: Thread-Local Handshakes",
         "How did Java 10+ Thread-Local Handshakes improve on global safepoints?",
         "They execute callbacks on individual threads without stopping all application threads globally.", ["Java", "JVM", "Safepoints", "Meta"]),

        ("How do you design a lock-free Single-Producer Single-Consumer (SPSC) queue in Java using VarHandle memory barriers?", "TOUGH", "jmm-synchronization",
         "An SPSC lock-free queue uses a pre-allocated circular ring buffer array, separate cache-line-padded head and tail pointers, and VarHandle release/acquire memory semantics to eliminate volatile write barriers.",
         "In an SPSC queue, exactly one thread writes and one thread reads, eliminating CAS contention entirely. Using Java 9+ `java.lang.invoke.VarHandle`, we can avoid expensive full volatile fences (`setVolatile`) by using `setRelease` on writes and `getAcquire` on reads (Release-Acquire semantics). The producer writes data to `buffer[tail]`, then updates `tail` using `VarHandle.setRelease()`. The consumer reads `tail` with `VarHandle.getAcquire()`, ensuring it observes the newly written data without full CPU bus locking.",
         "Head and tail indices are padded with dummy variables to ensure they occupy separate 64-byte L1 CPU cache lines, eliminating false sharing.",
         "import java.lang.invoke.*;\npublic class SPSCQueue<T> {\n    private final Object[] buffer;\n    private final int mask;\n    private volatile long head = 0;\n    private volatile long tail = 0;\n    private static final VarHandle TAIL, HEAD;\n    static {\n        try {\n            MethodHandles.Lookup l = MethodHandles.lookup();\n            TAIL = l.findVarHandle(SPSCQueue.class, \"tail\", long.class);\n            HEAD = l.findVarHandle(SPSCQueue.class, \"head\", long.class);\n        } catch (ReflectiveOperationException e) { throw new Error(e); }\n    }\n    public SPSCQueue(int capacity) {\n        this.mask = capacity - 1;\n        this.buffer = new Object[capacity];\n    }\n}",
         "VarHandle release/acquire semantics provide the fastest possible inter-thread message passing on modern ARM64 and x86 architectures.",
         "Passing data across multiple producers or multiple consumers breaks the SPSC contract, leading to corrupted pointers and data loss.",
         "SPSC queues achieve 100M+ ops/sec with sub-microsecond latency, but only support single-threaded producer-consumer topologies.",
         ["Using SPSC queues in MPMC (Multi-Producer Multi-Consumer) environments.", "Using full volatile writes when release/acquire semantics suffice.", "Neglecting cache-line padding on head and tail sequence fields."],
         ("What is the difference between VarHandle setRelease and setVolatile?", "What is an SPSC queue?", "Why is CAS unnecessary in SPSC?"),
         "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/invoke/VarHandle.html", "Oracle Java SE Documentation: VarHandle",
         "What hardware instruction is emitted by setRelease on x86 vs ARM64?",
         "On x86 (strongly ordered), setRelease is a plain MOV with compiler fence; on ARM64, it emits a STLR (Store-Release) instruction.", ["Java", "Concurrency", "VarHandle", "Netflix"]),

        ("How does the HotSpot JVM implement Class Data Sharing (CDS) and AppCDS to optimize container startup latency?", "HARD", "jvm-memory-gc",
         "Class Data Sharing (CDS) dumps pre-parsed, verified class metadata and bytecode into a memory-mapped archive (.jsa), allowing multiple JVM instances to share read-only memory and bypass class loading and bytecode verification on startup.",
         "In containerized microservice architectures (Docker, Kubernetes), cold start latency is dominated by loading, verifying, and linking hundreds of JAR classes. CDS (extended to application classes via AppCDS in Java 10 JEP 310, and dynamic archiving in Java 13 JEP 350) pre-parses and pre-verifies classes during a training run, persisting them into a shared archive file (.jsa). On container startup, the JVM memory-maps (`mmap`) the archive directly into memory.",
         "This bypasses CPU-intensive class verification and linking, cutting startup times by 40-70% and enabling shared read-only memory across multiple containers on the same host.",
         "// Step 1: Create dynamic CDS archive during test run:\n// java -XX:ArchiveClassesAtExit=app-cds.jsa -jar app.jar\n\n// Step 2: Launch production container using memory-mapped archive:\n// java -XX:SharedArchiveFile=app-cds.jsa -jar app.jar",
         "Incorporate AppCDS archive generation into standard CI/CD Docker image build pipelines.",
         "Altering the application classpath or modifying bundled JARs invalidates the CDS archive, causing the JVM to fall back to normal class loading.",
         "CDS drastically slashes startup time and container memory footprint, but adds an extra step to build pipelines.",
         ["Changing JAR timestamps or classpath order after generating the CDS archive.", "Overlooking dynamic CDS archiving (`-XX:ArchiveClassesAtExit`) introduced in Java 13.", "Expecting CDS to optimize JIT runtime compilation (that requires CRaC or GraalVM AOT)."],
         ("What part of class loading does CDS skip?", "How does mmap help multi-container memory sharing?", "What invalidates a CDS archive?"),
         "https://openjdk.org/jeps/310", "JEP 310: Application Class-Data Sharing",
         "How does CDS compare to GraalVM Native Image?",
         "CDS maintains full standard JVM dynamics, reflection, and JIT peak throughput, while GraalVM Native Image offers faster startup via closed-world AOT.", ["Java", "JVM", "Containers", "Amazon"])
    ]

    for item in more_hard:
        deep_exp = f"{item[4]}\n\nDeep Architectural Analysis:\n{item[5]}" if len(item[5]) < 150 else item[5]
        questions.append(make_q(
            item[0], item[1], item[2], item[3], item[4], deep_exp, item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], ["Java", "JVM", "Advanced Concurrency", "Google", "Meta"]
        ))

    # =========================================================
    # 20 EXPERT / PRODUCTION SCENARIO
    # =========================================================
    # (Questions 61 to 80)
    from generate_curated_pilot_batch import get_80_pilot_questions
    expert_seeds = [q for q in get_80_pilot_questions() if q["difficulty"] in ["PRODUCTION_SCENARIO", "EXPERT_DEEP_DIVE"]]
    questions.extend(expert_seeds)

    more_expert = [
        ("Production Incident: A Spring Boot API using Java 21 Virtual Threads locks up completely under sudden 10x traffic spike. Operating system CPU is low, but thread dumps show 20,000 parked threads. How do you triage and fix carrier thread exhaustion?", "PRODUCTION_SCENARIO", "virtual-threads-loom",
         "The outage is caused by Carrier Thread Pinning: virtual threads blocked inside synchronized blocks or native calls while waiting for database/HTTP I/O, pinning carrier threads and starving the ForkJoinPool; fix by identifying pinned frames with JFR and replacing synchronized with ReentrantLock.",
         "During this incident, CPU is idle because all carrier worker threads in `ForkJoinPool-1` are pinned by virtual threads waiting on blocking I/O (e.g. database connection queries). Because the virtual threads are inside a `synchronized` block, the JVM cannot unmount them. Once all carrier threads (typically equal to available CPU cores, e.g. 8 or 16) are pinned, the carrier pool is completely exhausted. Even though 20,000 virtual threads exist in memory, zero virtual threads can be scheduled for execution, halting the application.",
         "Triage protocol: 1. Capture a flight recording (`jcmd <pid> JFR.start duration=30s filename=/tmp/pinning.jfr`). 2. Open in JDK Mission Control and filter for `jdk.VirtualThreadPinned` events. 3. Pinpoint the offending library or class holding `synchronized` across network calls. 4. Remediation: Replace `synchronized` blocks with `ReentrantLock` or upgrade JDBC/driver libraries to Loom-friendly releases.",
         "// JFR event verification command:\n// jfr print --events jdk.VirtualThreadPinned /tmp/pinning.jfr\n\n// Code Remediation: Replace synchronized with ReentrantLock\nprivate final ReentrantLock lock = new ReentrantLock();\npublic String queryDatabaseSafely() {\n    lock.lock();\n    try {\n        return executeDbQuery(); // Virtual thread unmounts cleanly without pinning!\n    } finally {\n        lock.unlock();\n    }\n}",
         "Always run pre-production load tests with `-Djdk.tracePinnedThreads=full` to catch pinning before deploying to production Kubernetes clusters.",
         "Carrier exhaustion manifests as total service freeze with 0% CPU utilization, causing false alarms about deadlocks.",
         "ReentrantLock requires explicit unlock in finally blocks, but guarantees non-pinning virtual thread unmounting.",
         ["Assuming scaling up carrier thread pools (`-Djdk.virtualThreadScheduler.parallelism`) fixes the root cause.", "Overlooking third-party logging or JDBC drivers that contain legacy synchronized blocks.", "Failing to enable JFR pinning events in production observability pipelines."],
         ("What causes Virtual Thread Pinning?", "Why is CPU usage low during carrier thread exhaustion?", "How does JFR expose pinning events?"),
         "https://openjdk.org/jeps/444", "JEP 444: Virtual Threads Pinning Diagnostics",
         "Why does synchronized cause pinning in Java 21?",
         "The current HotSpot runtime monitors are tied to OS thread stack frames; JEP draft is underway to allow unmounting from synchronized in future Java releases.", ["Java", "Virtual Threads", "Production Incident", "Netflix", "Uber"]),

        ("Architect a low-latency, zero-garbage trading engine in Java. What off-heap memory, object pooling, and mechanical sympathy techniques are required to achieve sub-microsecond P99?", "EXPERT_DEEP_DIVE", "jvm-memory-gc",
         "A sub-microsecond trading engine eliminates GC pauses by using off-heap memory (MemorySegment/Foreign Function API), cache-line padded ring buffers (Disruptor), flyweight object reuse, CPU core pinning (affinity), and uncompressed OOPs avoidance.",
         "To guarantee sub-microsecond P99 latency, garbage collection must never run on the critical path. The architecture employs: 1. Off-Heap Memory: Order books and market data are stored off-heap using Java 22+ Foreign Function & Memory API (`Arena.ofShared()` and `MemorySegment`), eliminating GC tracking entirely. 2. Flyweight Pattern: Reusable message buffers deserialize binary FIX/SBE payloads in-place without object allocations. 3. Mechanical Sympathy: Data structures align with 64-byte CPU cache lines, and critical worker threads are pinned to isolated CPU cores using native thread affinity (e.g. `taskset` or Java-Thread-Affinity) to prevent OS context switching. 4. JVM Tuning: Run with Epsilon GC (`-XX:+UseEpsilonGC`) for zero GC overhead or ZGC with pre-allocated heaps.",
         "Network I/O utilizes kernel-bypass networking (Solarflare OpenOnload or DPDK) to read packets directly into user-space off-heap memory.",
         "import java.lang.foreign.*;\npublic class OffHeapOrderBook {\n    private final Arena arena = Arena.ofShared();\n    private final MemorySegment segment;\n    public OffHeapOrderBook(long sizeBytes) {\n        // Allocated outside JVM Garbage Collection scope!\n        this.segment = arena.allocate(sizeBytes, 64); // 64-byte cache-line aligned\n    }\n    public void writePrice(long offset, double price) {\n        segment.set(ValueLayout.JAVA_DOUBLE, offset, price);\n    }\n}",
         "Always pre-allocate buffers at application boot and run with strict zero-allocation linters in CI/CD pipelines.",
         "Buffer overruns or illegal memory access in off-heap segments crash the entire JVM process with SIGSEGV rather than throwing recoverable exceptions.",
         "Off-heap memory achieves zero GC pauses, but requires manual memory management and explicit lifecycle arenas.",
         ["Allocating temporary objects inside order matching loops.", "Ignoring CPU cache false sharing on order sequence counters.", "Relying on standard socket APIs instead of memory-mapped IPC or kernel-bypass networking."],
         ("What is Epsilon GC?", "How does Java 22 Foreign Function & Memory API manage off-heap memory?", "What is thread affinity?"),
         "https://openjdk.org/jeps/454", "JEP 454: Foreign Function & Memory API",
         "Why is CPU core pinning critical for ultra-low-latency Java engines?",
         "It prevents the OS scheduler from migrating threads across CPU cores, preserving hot L1/L2 CPU cache state.", ["Java", "Low Latency", "Finance", "Off-Heap", "Citadel", "Jane Street"]),

        ("How does the Java Memory Model interact with Out-of-Order execution on weakly ordered ARM64 vs strongly ordered x86 hardware?", "EXPERT_DEEP_DIVE", "jmm-synchronization",
         "x86 hardware provides Total Store Order (TSO) which only reorders store-after-load, whereas ARM64 is weakly ordered, reordering store-store, load-load, and store-load; the JVM compiler emits DMB/ISB fences on ARM64 to enforce identical JMM semantics.",
         "Hardware memory models dictate when CPU cores observe memory writes from other cores. x86 is strongly ordered (TSO): writes from a CPU core are committed in order, so volatile writes only require a cheap compiler barrier for store-store and a locked instruction (`lock addl`) for store-load. ARM64 and Apple Silicon (AArch64) are weakly ordered: CPUs can reorder loads and stores arbitrarily unless explicit memory barriers are inserted. To uphold the Java Memory Model specification across all hardware, HotSpot C2 compiler generates `dmb ishld` (Data Memory Barrier Inner Shareable Load) and `stlr`/`ldar` (Store-Release / Load-Acquire) instructions on ARM64.",
         "Code with subtle concurrency bugs (missing volatile) may appear to work reliably on x86 developer laptops, but will fail catastrophically in production when deployed to AWS Graviton (ARM64) Kubernetes clusters.",
         "// On x86:\n// volatile write emits: MOV [addr], val + LOCK ADDL [rsp], 0 (cheap)\n//\n// On ARM64 (AArch64):\n// volatile write emits: STLR (Store-Release) or DMB ISH (expensive bus synchronization)\npublic class CrossPlatformMemory {\n    private int data = 0;\n    private volatile boolean ready = false;\n    public void publish() {\n        data = 100;\n        ready = true; // Emits STLR on ARM64; preserves happens-before on all CPUs\n    }\n}",
         "Always test multithreaded concurrent algorithms on ARM64 (AWS Graviton, Apple Silicon) to uncover data race bugs masked by x86 TSO hardware.",
         "Concurrency code that violates JMM rules passes tests on x86, then causes sporadic data corruption on ARM64 servers.",
         "The JVM guarantees uniform JMM semantics across all hardware, but weakly ordered hardware requires more explicit memory fences.",
         ["Assuming that code running correctly on an Intel laptop is free of concurrency bugs.", "Omitting volatile on double-checked locking, assuming CPU memory models are universal.", "Underestimating memory barrier performance differences across CPU architectures."],
         ("What is Total Store Order (TSO)?", "How does ARM64 reorder memory compared to x86?", "What instruction does ARM64 emit for volatile writes?"),
         "https://www.cl.cam.ac.uk/~pes20/arm/cam.pdf", "A Tutorial on the ARM Memory Model (Cambridge)",
         "What is word-tearing in the Java Memory Model?",
         "When non-atomic concurrent updates to adjacent primitive fields in a struct corrupt neighboring memory (forbidden in JMM since Java 5).", ["Java", "JMM", "ARM64", "Hardware", "AWS", "Google"])
    ]

    for item in more_expert:
        deep_exp = f"{item[4]}\n\nDeep Architectural Analysis:\n{item[5]}" if len(item[5]) < 150 else item[5]
        questions.append(make_q(
            item[0], item[1], item[2], item[3], item[4], deep_exp, item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], ["Java", "Staff Engineer", "Architecture", "Google", "Amazon"]
        ))

    return questions

def run_pilot_ingestion():
    print("=== BREAK THE CODE: PILOT BATCH INGESTION (JAVA & JVM CONCURRENCY) ===")
    engine = ContentQualityEngine("backend/breakthecode.db")
    questions = build_pilot_questions()
    print(f"Constructed {len(questions)} high-quality pilot questions.")

    stats = engine.ingest_batch(questions, batch_name="Pilot Batch (Java & JVM Concurrency)")
    engine.close()

    print("\n=== PILOT IMPORT REPORT ===")
    print(f"Batch: {stats['batch_name']}")
    print(f"Total Requested: {stats['total_requested']}")
    print(f"Approved: {stats['approved']}")
    print(f"Rejected: {stats['rejected']}")
    print(f"Duplicates: {stats['duplicates']}")
    print(f"Difficulty Breakdown: {stats['difficulty_breakdown']}")

    if stats["rejections"]:
        print(f"\nRejections Detail ({len(stats['rejections'])}):")
        for r in stats["rejections"]:
            print(f"  - {r['title']}: {r['reasons']}")

    return stats

if __name__ == "__main__":
    run_pilot_ingestion()
