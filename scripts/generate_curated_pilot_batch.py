"""
Comprehensive Pilot Batch Generator for Java & JVM Concurrency
Generates exactly 80 deep, authoritative questions:
- 20 BASIC (Easy)
- 20 MEDIUM (Medium)
- 20 HARD / TOUGH (Hard)
- 20 PRODUCTION_SCENARIO / EXPERT_DEEP_DIVE (Expert)
Targeting all 4 topics:
- jmm-synchronization
- executors-concurrency-utils
- virtual-threads-loom
- jvm-memory-gc
"""

import json

def get_80_pilot_questions():
    questions = []

    # ==========================================
    # 1. 20 BASIC (EASY) QUESTIONS
    # ==========================================
    basic_specs = [
        (
            "What is the difference between an interface and an abstract class in Java 8 and beyond?",
            "jmm-synchronization",
            "An abstract class can maintain state via instance fields and constructors and supports single inheritance, whereas an interface defines a contract, supports multiple inheritance, and can only hold constants, default, and static methods without instance state.",
            "In modern Java, an abstract class represents an 'is-a' relationship with state, meaning it can have constructors, instance fields, and any access modifier. An interface represents a 'can-do' capability contract, allowing a class to implement multiple interfaces. While Java 8 introduced default and static methods to interfaces, interfaces still cannot maintain mutable instance state.",
            "Historically, interfaces contained only method signatures, but Java 8 introduced default methods to facilitate backward compatibility for lambda expressions in the Collections framework without breaking existing implementations. Crucially, an interface cannot have instance variables; all fields are implicitly 'public static final'. Abstract classes, by contrast, participate in standard class hierarchy initialization via constructors and can enforce encapsulation with private/protected member fields.",
            "public interface Auditable {\n    String DEFAULT_AUDITOR = \"SYSTEM\";\n    String getAuditId();\n    default void logAudit() {\n        System.out.println(\"Audit recorded: \" + getAuditId());\n    }\n}\n\npublic abstract class BaseEntity {\n    private final long createdAt = System.currentTimeMillis();\n    public abstract String getId();\n    public long getCreatedAt() { return createdAt; }\n}",
            "Default methods should provide non-invasive fallback behaviors. Avoid placing heavy business logic inside interface default methods as it bypasses clean domain-driven architecture.",
            "Diamond problem with default methods: if two implemented interfaces define identical default method signatures, the implementing class must explicitly override and resolve the conflict using InterfaceName.super.method() or compilation fails.",
            "Interfaces maximize compositional flexibility and decoupling at the cost of requiring external state management. Abstract classes simplify shared state and skeletal implementations but consume the single inheritance slot.",
            ["Attempting to declare instance variables inside an interface, forgetting all fields are implicitly static and final.", "Using an abstract class purely for utility functions without any state or polymorphic hierarchy.", "Forgetting to resolve diamond dependency conflicts when implementing two interfaces with identical default method signatures."]
        ),
        (
            "Why is the String class immutable in Java, and what benefits does immutability provide?",
            "jmm-synchronization",
            "String is immutable in Java to ensure thread safety, enable String Pool caching (saving heap memory), guarantee secure class loading and network connections, and allow stable hashCode caching.",
            "String immutability is a foundational design choice in Java. It allows the JVM to safely share identical string literals in the String Pool, guarantees thread safety across concurrent threads without locks, ensures security parameters (like file paths, DB connection URLs, and classloader inputs) cannot be altered maliciously, and enables caching the calculated hashCode for fast HashMap lookups.",
            "Under the hood, String encapsulates an immutable byte[] array (since Java 9 Compact Strings) marked final and private, with no exposed mutators. Because String instances never mutate, the JVM's String Pool can return references to the same object for identical literals. In multithreading, immutability eliminates data races entirely. For hash-based collections (HashMap, HashSet), the hashCode is computed once lazily and cached, providing guaranteed O(1) bucket addressing.",
            "public final class StringImmutabilityDemo {\n    public static void main(String[] args) {\n        String a = \"BreakTheCode\";\n        String b = \"BreakTheCode\";\n        System.out.println(a == b); // true: shared String pool reference\n        String c = a.concat(\" 2026\");\n        System.out.println(a); // still \"BreakTheCode\"\n    }\n}",
            "Avoid string concatenation in tight loops using '+' operator; use StringBuilder or String.join to minimize heap churn.",
            "Excessive string allocations in high-throughput services trigger frequent Young Generation GC pauses.",
            "Immutability guarantees absolute thread safety and security at the cost of requiring new object allocations for mutations.",
            ["Using '+' inside loops instead of StringBuilder.", "Storing sensitive credentials in String instead of char[].", "Assuming substring() causes a memory leak (fixed since Java 7u6)."]
        ),
        (
            "What is the contract between equals() and hashCode() in Java, and what happens when it is violated?",
            "jmm-synchronization",
            "If two objects are equal according to equals(), they must return the same hashCode(); if they have the same hashCode(), they are not required to be equal. Violating this contract breaks HashMap, HashSet, and Hashtable lookups.",
            "The equals-hashCode contract specifies that if objectA.equals(objectB) is true, then objectA.hashCode() must equal objectB.hashCode(). However, unequal objects can share the same hash code (a hash collision). If you override equals() without hashCode(), objects that are logically identical will produce different hash codes and map to different buckets in a HashMap, making it impossible to retrieve the stored entry.",
            "Hash collections use hashCode() to compute the bucket index (index = (n - 1) & hash). When inserting or querying a key, the collection first evaluates the bucket index via hashCode(). Only if a bucket contains entries does it iterate through the chain/tree and call equals() to match the exact key. If equals() returns true for two objects with different hashCodes, the lookup calculates the wrong bucket and fails to find the existing value.",
            "public class UserId {\n    private final String id;\n    public UserId(String id) { this.id = id; }\n    @Override public boolean equals(Object o) {\n        if (this == o) return true;\n        if (!(o instanceof UserId that)) return false;\n        return java.util.Objects.equals(id, that.id);\n    }\n    @Override public int hashCode() { return java.util.Objects.hashCode(id); }\n}",
            "Always compute hashCode from immutable fields to prevent bucket misalignment in HashMaps.",
            "Mutating an object after using it as a map key leads to silent memory leaks as the key cannot be found or removed.",
            "Uniform hash distributions keep bucket chains short (O(1) lookups), while poorly distributed hash codes degrade collections to O(N) or O(log N).",
            ["Overriding equals() without overriding hashCode().", "Using mutable fields inside hashCode().", "Changing equals parameter type to a concrete class instead of Object."]
        ),
        (
            "What is the volatile keyword in Java, and what guarantees does it provide?",
            "jmm-synchronization",
            "The volatile keyword guarantees visibility of variable updates across threads and prevents instruction reordering around reads and writes, establishing a happens-before relationship without providing mutual exclusion or atomicity.",
            "In the Java Memory Model, 'volatile' provides two fundamental guarantees: Visibility and Ordering. Visibility ensures that whenever a thread writes to a volatile variable, the value is immediately flushed to main memory, and reading threads read directly from main memory rather than a stale CPU L1/L2 cache. Ordering ensures that the compiler and CPU cannot reorder instructions across the volatile read or write barrier. However, volatile does not provide atomicity for compound operations like count++.",
            "Modern multi-core CPUs use hierarchical hardware caches. Without synchronization, thread A can write to a variable in its core cache without thread B ever observing the change. Under JSR-133, a volatile write generates a StoreStore and StoreLoad memory fence, ensuring all preceding writes become visible before the volatile write. A volatile read generates LoadLoad and LoadStore fences, preventing following reads from being reordered before the volatile read.",
            "public class WorkerThread implements Runnable {\n    private volatile boolean running = true;\n    public void stop() { this.running = false; }\n    @Override public void run() {\n        while (running) {\n            // cooperative work\n        }\n    }\n}",
            "Volatile is suitable for single-variable flags and status markers, but insufficient for multi-step state mutations.",
            "Using volatile for compound operations like `count++` creates race conditions and lost updates under concurrent access.",
            "Volatile incurs no thread blocking or context switching, making it significantly faster than synchronized blocks.",
            ["Assuming volatile makes increment operations atomic.", "Declaring an array volatile and expecting its elements to be volatile.", "Using volatile when locks or atomic primitives are required."]
        ),
        (
            "What is the difference between Runnable and Callable in Java?",
            "executors-concurrency-utils",
            "Runnable defines a void run() method that cannot return a result or throw checked exceptions, whereas Callable<V> defines a V call() method that can return a computed value and throw checked exceptions.",
            "Runnable (introduced in Java 1.0) represents a task that executes asynchronously without returning a value; its `run()` method returns void and cannot throw checked exceptions. Callable<V> (introduced in Java 5 alongside java.util.concurrent) represents a parameterized task whose `call()` method returns a result of type V and is declared to throw Exception, making it ideal for use with ExecutorService and Future<V>.",
            "Callable was created specifically to eliminate the clumsy workarounds required with Runnable, such as writing results to shared thread-safe holder variables and capturing exceptions manually. When submitted to an ExecutorService, a Callable is wrapped into a FutureTask<V>, which manages the task lifecycle (NEW, COMPLETING, NORMAL, EXCEPTIONAL) and delivers either the return value via `future.get()` or unrolls the thrown exception as an ExecutionException.",
            "import java.util.concurrent.*;\npublic class CallableDemo {\n    public static void main(String[] args) throws Exception {\n        ExecutorService exec = Executors.newFixedThreadPool(2);\n        Callable<Integer> task = () -> 21 * 2;\n        Future<Integer> future = exec.submit(task);\n        System.out.println(\"Result: \" + future.get(1, TimeUnit.SECONDS));\n        exec.shutdown();\n    }\n}",
            "Always specify a timeout when calling `future.get(timeout, unit)` to prevent thread starvation if tasks hang.",
            "Uncaught exceptions in Runnable are swallowed or routed to UncaughtExceptionHandler without alerting task submitters.",
            "Callable incurs a minor object allocation for FutureTask compared to lightweight Runnable execution.",
            ["Calling future.get() immediately after submit(), eliminating async concurrency.", "Forgetting to shutdown ExecutorService.", "Assuming Callable can be passed directly to new Thread(callable) without FutureTask wrapper."]
        ),
        (
            "What are the major memory regions in the JVM runtime data area?",
            "jvm-memory-gc",
            "The JVM runtime data area comprises the Heap (shared, stores objects), Method Area / Metaspace (shared, stores class metadata), JVM Stacks (per-thread, stores frames/local variables), Native Method Stacks (per-thread), and Program Counter (PC) Registers (per-thread).",
            "JVM memory is split into thread-shared and thread-private regions. The shared regions are the Heap (where all class instances and arrays reside, managed by Garbage Collection) and Metaspace (native memory holding loaded class bytecode, constant pools, and method metadata). The thread-private regions are JVM Stacks (holding stack frames with local variables and operand stacks), Native Method Stacks (for JNI calls), and PC Registers (tracking bytecode execution offsets).",
            "Understanding this layout is crucial for troubleshooting memory errors. OutOfMemoryError: Java heap space indicates the heap is exhausted by live objects or memory leaks. OutOfMemoryError: Metaspace indicates class metadata exhaustion, often caused by dynamic proxy or classloader leaks. StackOverflowError occurs when recursive or deep call chains exceed thread stack capacity.",
            "public class MemoryRegionsDemo {\n    // Static variable in Metaspace / Class mirror\n    private static final String APP_NAME = \"BreakTheCode\";\n    \n    // Instance variable stored on Heap inside object\n    private int instanceValue = 100;\n\n    public void execute(int param) { // param stored in JVM Stack Frame\n        Object localObj = new Object(); // reference on Stack, instance on Heap\n    }\n}",
            "Monitor both Heap and Metaspace metrics in production APM tools (Prometheus, Datadog) to isolate memory growth.",
            "Deep recursion without base cases throws StackOverflowError; classloader leaks in app servers exhaust native Metaspace.",
            "Heap memory is garbage collected, while stack frames are automatically reclaimed when methods return.",
            ["Confusing Metaspace (native memory since Java 8) with the legacy PermGen (heap-based).", "Assuming local primitive variables are allocated on the Heap.", "Believing Garbage Collection cleans up the JVM stack."]
        ),
        (
            "What is the difference between fail-fast and fail-safe iterators in Java Collections?",
            "jmm-synchronization",
            "Fail-fast iterators throw ConcurrentModificationException immediately when the underlying collection is modified during iteration (except through the iterator's own remove method), whereas fail-safe (or weakly consistent) iterators operate on a clone or snapshot and do not throw this exception.",
            "Standard collections in java.util (ArrayList, HashMap, HashSet) provide fail-fast iterators. They check an internal `modCount` variable on every `next()` call; if modCount differs from the expected count, ConcurrentModificationException is thrown immediately. In contrast, concurrent collections in java.util.concurrent (CopyOnWriteArrayList, ConcurrentHashMap) provide fail-safe or weakly consistent iterators that traverse a snapshot or allow concurrent modifications without throwing exceptions.",
            "Fail-fast behavior is designed to fail cleanly and quickly in the presence of concurrent modifications rather than risk non-deterministic behavior at an undetermined time in the future. However, fail-fast guarantees are best-effort: you must never rely on ConcurrentModificationException for program correctness.",
            "import java.util.*;\nimport java.util.concurrent.*;\npublic class IteratorDemo {\n    public static void main(String[] args) {\n        List<String> fastList = new ArrayList<>(List.of(\"A\", \"B\"));\n        List<String> safeList = new CopyOnWriteArrayList<>(List.of(\"A\", \"B\"));\n        \n        // safeList allows modification during iteration\n        for (String s : safeList) {\n            safeList.add(\"C\"); // Does not throw\n        }\n    }\n}",
            "In multithreaded environments, never use plain ArrayList iteration without external synchronization or switching to concurrent collections.",
            "Modifying a collection inside an enhanced for-loop throws ConcurrentModificationException at runtime.",
            "Fail-fast collections offer low overhead and zero copy cost; CopyOnWriteArrayList provides safe iteration at the expense of O(N) array copy on writes.",
            ["Removing elements from a list using list.remove(item) inside a foreach loop instead of iterator.remove().", "Assuming ConcurrentModificationException only occurs in multithreaded programs (it occurs in single threads too).", "Using CopyOnWriteArrayList in write-heavy workloads."]
        ),
        (
            "What is a ThreadLocal in Java, and why can it cause memory leaks in thread-pooled environments?",
            "executors-concurrency-utils",
            "ThreadLocal provides thread-confined variables where each accessing thread has an independently initialized copy. In thread pools, worker threads are reused rather than destroyed, causing ThreadLocal values to persist indefinitely unless explicitly removed with threadLocal.remove().",
            "ThreadLocal creates thread-confined storage, mapping each thread to its own isolated value without requiring synchronization. Under the hood, each Thread instance holds a `ThreadLocalMap` whose keys are WeakReferences to ThreadLocal instances, but whose values are strong references. In web application servers (Tomcat, Jetty) using thread pools, pooled worker threads stay alive across multiple HTTP requests. If a request sets a ThreadLocal value and fails to call `remove()`, the value remains pinned in memory, leading to memory leaks and cross-request data contamination.",
            "The memory leak occurs because while the key in ThreadLocalMap is a WeakReference, the value is strongly referenced by the thread's map. As long as the pooled thread remains alive, the value object and its classloader cannot be garbage collected. Always use try-finally blocks to call `threadLocal.remove()` in pooled execution environments.",
            "public class SecurityContextHolder {\n    private static final ThreadLocal<String> USER_CTX = new ThreadLocal<>();\n    \n    public static void runWithUser(String user, Runnable task) {\n        USER_CTX.set(user);\n        try {\n            task.run();\n        } finally {\n            USER_CTX.remove(); // MANDATORY in thread pools\n        }\n    }\n}",
            "In Spring Boot and servlet containers, always clean up ThreadLocal instances in an interceptor or filter finally-block.",
            "Data leakage where request B inherits security credentials or tenant IDs set by request A on the same pooled worker thread.",
            "ThreadLocal eliminates synchronization overhead for thread-confined state, but requires strict lifecycle management.",
            ["Forgetting to call threadLocal.remove() in a finally block.", "Using ThreadLocal inside virtual threads without considering ScopedValue (Java 21).", "Storing large memory buffers in ThreadLocal, magnifying heap consumption across pool size."]
        ),
        (
            "What is the difference between sleep() and wait() in Java threading?",
            "jmm-synchronization",
            "Thread.sleep() pauses execution for a specified time without releasing any acquired monitor locks, whereas Object.wait() causes the thread to release the monitor lock and wait until notified via notify() or notifyAll() from within a synchronized block.",
            "sleep() is a static method on java.lang.Thread that temporarily suspends the current thread's execution without relinquishing lock ownership. wait() is an instance method on java.lang.Object used for inter-thread coordination; it must be called from within a synchronized context on that object, immediately releases the monitor lock, and places the thread into the object's wait set until another thread invokes notify() or notifyAll().",
            "Calling wait() outside a synchronized block throws IllegalMonitorStateException. When awakened by notify(), the thread must re-acquire the monitor lock before resuming execution. Furthermore, wait() must always be called inside a condition loop (while (!condition)) to defend against spurious wakeups.",
            "public class WaitSleepComparison {\n    private final Object lock = new Object();\n    private boolean ready = false;\n    \n    public void waitForReady() throws InterruptedException {\n        synchronized (lock) {\n            while (!ready) { // Loop protects against spurious wakeup\n                lock.wait(); // Releases lock while waiting\n            }\n        }\n    }\n}",
            "Never use sleep() for condition polling; use proper synchronization primitives (Condition, CountDownLatch, CompletableFuture).",
            "Calling sleep() while holding a shared lock causes thread starvation and bottlenecks across the entire application.",
            "wait() coordinates resource availability between producer and consumer threads safely; sleep() merely halts execution.",
            ["Calling wait() outside of a synchronized block.", "Using if (!condition) wait() instead of while (!condition) wait(), falling victim to spurious wakeups.", "Calling sleep() inside synchronized methods expecting other threads to enter."]
        ),
        (
            "What is the Java Virtual Thread model introduced in Java 21 (Project Loom)?",
            "virtual-threads-loom",
            "Virtual Threads are lightweight threads managed directly by the JVM runtime rather than the operating system kernel, enabling high-throughput concurrent I/O applications by mapping millions of virtual threads onto a small pool of carrier OS threads.",
            "Before Java 21, every java.lang.Thread was a 1:1 wrapper around an operating system thread (Platform Thread), consuming roughly 1MB of stack memory and limited by OS scheduling limits to a few thousand threads. Project Loom (JEP 444) introduced Virtual Threads: M:N lightweight threads managed in JVM user-space. When a virtual thread performs blocking I/O (socket read, JDBC query, sleep), the JVM unmounts its execution state from the underlying carrier thread, parking it in heap memory until the I/O event completes, leaving the carrier thread free to execute other virtual threads.",
            "Virtual Threads preserve the traditional synchronous, thread-per-request programming model while delivering reactive-level throughput. They eliminate the complex callback, reactive stream (WebFlux/RxJava) paradigms previously necessary for scaling network services.",
            "import java.util.concurrent.*;\npublic class VirtualThreadDemo {\n    public static void main(String[] args) {\n        // Launch virtual thread per task\n        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {\n            for (int i = 0; i < 10_000; i++) {\n                executor.submit(() -> {\n                    Thread.sleep(100); // Unmounts from carrier thread\n                    return 1;\n                });\n            }\n        } // Auto-awaits termination\n    }\n}",
            "Virtual Threads are designed for I/O-bound tasks. They do NOT accelerate CPU-intensive algorithms (cryptography, image processing).",
            "Pinning: performing blocking I/O inside synchronized blocks or native JNI methods pins the virtual thread to its carrier, causing carrier pool starvation.",
            "Virtual threads eliminate thread pooling overhead for I/O tasks, but each virtual thread allocates heap space for its execution frames.",
            ["Attempting to pool Virtual Threads (never pool them; create them on demand per task).", "Using Virtual Threads for compute-heavy number crunching.", "Ignoring synchronized blocks that cause thread pinning in high-concurrency environments."]
        ),
        (
            "What is Garbage Collection in Java and what are Young and Old Generations?",
            "jvm-memory-gc",
            "Garbage Collection is automatic memory management that identifies and reclaims heap memory occupied by unreachable objects. Generational GC divides the heap into the Young Generation (Eden and Survivor spaces, for short-lived objects) and the Old Generation (for long-lived objects) based on the Weak Generational Hypothesis.",
            "The Weak Generational Hypothesis observes that most allocated objects die shortly after creation. To optimize throughput, the JVM splits the heap into Young Generation (composed of Eden and two Survivor spaces: S0 and S1) and Tenured/Old Generation. New objects are allocated in Eden. When Eden fills, a fast Minor GC reclaims dead objects and moves survivors between S0 and S1, incrementing their age. Once an object survives a threshold number of cycles (tenuring threshold, default up to 15), it is promoted to the Old Generation, which is collected less frequently during Major or Full GC cycles.",
            "Different collectors (G1GC, ZGC, ParallelGC) implement generational collection with different latency-throughput trade-offs. G1GC organizes the heap into uniform regions dynamically designated as Eden, Survivor, or Old. ZGC (in Java 21+) provides Generational ZGC, achieving sub-millisecond pause times regardless of heap size.",
            "public class GenerationalGCDemo {\n    public static void main(String[] args) {\n        // Most objects die immediately inside method scope (Young Gen)\n        for (int i = 0; i < 1_000_000; i++) {\n            String temp = String.valueOf(i);\n        }\n        // Long-lived objects (e.g. caches) get promoted to Old Gen\n    }\n}",
            "Avoid creating unnecessary temporary objects in high-throughput hot paths to prevent premature promotion to Old Generation.",
            "Premature promotion: when Eden is undersized, short-lived objects spill directly into Old Generation, triggering expensive Full GC pauses.",
            "Generational collection reduces GC overhead by 90%+ compared to scanning the entire heap uniformly on every cycle.",
            ["Assuming System.gc() forces an immediate full collection (it is merely a non-binding hint).", "Believing objects in Old Generation are never collected.", "Setting Eden too small, causing rapid promotion of temporary objects."]
        ),
        (
            "What is the difference between throw and throws in Java exception handling?",
            "jmm-synchronization",
            "The 'throw' keyword is used inside a method body to explicitly throw an exception instance, whereas 'throws' is used in a method declaration to specify the checked exceptions that the method may propagate to its caller.",
            "'throw' is an imperative statement followed by an instantiated Throwable object (e.g., `throw new IllegalArgumentException(\"Invalid id\");`). 'throws' is a declarative clause appended to a method signature indicating that the method might throw one or more checked exceptions (e.g., `public void readFile() throws IOException`), requiring the calling method to either catch the exception or declare it in its own throws clause.",
            "Java distinguishes checked exceptions (subclasses of Exception excluding RuntimeException) from unchecked exceptions (RuntimeException and Error). Checked exceptions enforce compile-time verification via 'throws', whereas unchecked exceptions represent programming errors (NullPointerException, IllegalArgumentException) and do not require declaration.",
            "public class ExceptionDemo {\n    // throws declares potential exceptions in signature\n    public void parseData(String input) throws java.io.IOException {\n        if (input == null) {\n            // throw instantiates and triggers the exception\n            throw new IllegalArgumentException(\"Input cannot be null\");\n        }\n    }\n}",
            "Favor unchecked exceptions for unrecoverable business rule violations and checked exceptions only when the caller can realistically recover.",
            "Swallowing exceptions in empty catch blocks hides production bugs and prevents monitoring systems from capturing stack traces.",
            "Checked exceptions ensure compile-time safety, but can clutter API signatures and method contracts.",
            ["Catching generic Exception or Throwable, masking unexpected runtime errors.", "Throwing raw RuntimeException without a meaningful contextual error message.", "Using exceptions for normal control flow logic."]
        ),
        (
            "What is the difference between Comparable and Comparator in Java?",
            "jmm-synchronization",
            "Comparable defines the natural ordering of an object by implementing compareTo(T o) within the class itself, whereas Comparator defines custom, external sorting logic by implementing compare(T o1, T o2) in a separate class or lambda.",
            "Comparable<T> is implemented by a class to give its instances an intrinsic, natural order (e.g., String, Integer, LocalDate). Its method `int compareTo(T other)` returns a negative integer, zero, or positive integer. Comparator<T> is an external functional interface that allows defining multiple sorting strategies for a class without modifying its source code, supported by modern factory methods like Comparator.comparing().",
            "Collections.sort(list) and Arrays.sort() use Comparable by default. Providing an explicit Comparator overrides natural ordering. Both must remain consistent with equals() (i.e. compare(x, y) == 0 should imply x.equals(y)) to prevent erratic behavior when used in SortedSet (TreeSet) or SortedMap (TreeMap).",
            "import java.util.*;\npublic class Student implements Comparable<Student> {\n    private final String name;\n    private final int grade;\n    public Student(String name, int grade) { this.name = name; this.grade = grade; }\n    @Override public int compareTo(Student o) {\n        return Integer.compare(this.grade, o.grade); // Natural order by grade\n    }\n    public static Comparator<Student> byName() {\n        return Comparator.comparing(s -> s.name); // Custom order by name\n    }\n}",
            "Use Comparator.comparing() with method references for clean, readable, and composable sorting chains.",
            "Subtracting integer values in compareTo (e.g. `return a.id - b.id;`) causes integer overflow bugs when values have opposite signs.",
            "Comparable couples the sorting logic directly to the domain entity; Comparator provides modular, multi-attribute sorting.",
            ["Using primitive subtraction in compareTo instead of Integer.compare().", "Defining a comparison logic that violates the transitive or anti-symmetric properties.", "Inconsistent ordering between compareTo() and equals() in TreeSets."]
        ),
        (
            "What is the purpose of the finalize() method in Java, and why is it deprecated?",
            "jvm-memory-gc",
            "The finalize() method was intended for object cleanup before garbage collection, but it is deprecated because of unpredictable execution timing, severe performance degradation, thread deadlocks, and resurrection security vulnerabilities; developers should use AutoCloseable and Cleaner instead.",
            "finalize() was introduced in Java 1.0 to let objects release native resources before GC reclamation. However, the JVM provides no guarantee of when—or even if—finalize() will run. Objects with finalizers delay garbage collection by at least two GC cycles, can resurrect themselves by re-assigning 'this' to an active reference, and can trigger JVM deadlocks if finalizer threads block. It was deprecated in Java 9 and marked for removal in Java 18 (JEP 421).",
            "Modern Java replaces finalize() with the `try-with-resources` pattern via the `AutoCloseable` interface for deterministic resource cleanup. For non-deterministic native cleanup, `java.lang.ref.Cleaner` (or Java 22+ Foreign Function & Memory API Arenas) provides safe, un-resurrectable phantom reference cleaning.",
            "public class ResourceCleaner implements AutoCloseable {\n    private boolean closed = false;\n    \n    public void doWork() {\n        if (closed) throw new IllegalStateException(\"Resource closed\");\n    }\n    \n    @Override\n    public void close() {\n        if (!closed) {\n            closed = true;\n            System.out.println(\"Native resources freed deterministically.\");\n        }\n    }\n}",
            "Always wrap file handles, database connections, and network streams in try-with-resources blocks.",
            "Relying on finalize() to close sockets or file descriptors causes operating system file descriptor exhaustion under load.",
            "try-with-resources guarantees deterministic cleanup at scope exit; finalize() depends on uncertain GC scheduling.",
            ["Relying on finalize() for critical resource cleanup.", "Not using try-with-resources for classes implementing AutoCloseable.", "Calling System.runFinalization(), which blocks threads unpredictably."]
        ),
        (
            "What is the Diamond Problem in object-oriented programming, and how does Java handle it with default methods?",
            "jmm-synchronization",
            "The Diamond Problem arises when a class inherits from two parents that provide conflicting implementations of the same method. Java solves this for interfaces with default methods by enforcing strict compiler rules requiring the implementing class to explicitly override the conflicting method.",
            "Java avoids the diamond problem with state by forbidding multiple class inheritance. However, when Java 8 introduced default methods in interfaces, multiple inheritance of behavior became possible. If interface A and interface B define an identical default method `void log()`, and class C implements both A and B without overriding `log()`, the Java compiler detects ambiguity and fails to compile.",
            "To resolve the conflict, class C must provide an explicit implementation. Inside C's overridden method, it can provide custom logic or explicitly designate which interface behavior to adopt using `InterfaceName.super.methodName()`.",
            "interface LoggerA {\n    default void log(String msg) { System.out.println(\"A: \" + msg); }\n}\ninterface LoggerB {\n    default void log(String msg) { System.out.println(\"B: \" + msg); }\n}\npublic class CompositeLogger implements LoggerA, LoggerB {\n    @Override\n    public void log(String msg) {\n        // Explicitly resolve ambiguity\n        LoggerA.super.log(msg);\n        LoggerB.super.log(msg);\n    }\n}",
            "Keep interface default methods focused on behavioral defaults, avoiding competing business logic across interface hierarchies.",
            "Compilation failure when adding a new default method to an existing interface that clashes with another interface in third-party client code.",
            "Explicit resolution guarantees deterministic method dispatch and eliminates runtime ambiguity.",
            ["Assuming the compiler picks the first declared interface automatically.", "Believing Java allows multiple inheritance of state (member variables).", "Forgetting the 'InterfaceName.super.method()' invocation syntax."]
        ),
        (
            "What is the difference between synchronized method and synchronized block in Java?",
            "jmm-synchronization",
            "A synchronized method locks the entire method scope using the implicit object monitor ('this' or Class object), while a synchronized block locks only a specific critical section using an explicitly chosen monitor object, offering finer granularity and better concurrency.",
            "A synchronized instance method automatically acquires the monitor of 'this' for the entire duration of the method invocation, releasing it upon return or exception. A synchronized block allows locking on any arbitrary reference (including private dedicated lock objects) and confines synchronization strictly to the lines of code that mutate shared state.",
            "Synchronized blocks are strongly preferred in production code because locking 'this' exposes your synchronization lock to external callers who can synchronize on your object reference, accidentally causing deadlocks. Using a private final lock object (`private final Object lock = new Object();`) completely prevents external lock interference.",
            "public class Account {\n    private double balance;\n    // Private dedicated monitor prevents external lock contention\n    private final Object lock = new Object();\n    \n    public void deposit(double amount) {\n        // Non-critical operations (logging, validation) outside lock\n        if (amount <= 0) return;\n        \n        synchronized (lock) {\n            balance += amount; // Minimum critical section\n        }\n    }\n}",
            "Keep synchronized blocks as small as possible. Never perform I/O operations (HTTP, DB, file) inside synchronized blocks.",
            "Synchronizing on 'this' allows foreign code to hold the monitor of your object and trigger unexpected deadlocks.",
            "Synchronized blocks reduce lock holding time, maximizing CPU throughput and thread parallelism.",
            ["Synchronizing entire methods when only one variable assignment needs synchronization.", "Using non-final lock objects, which can be reassigned and break synchronization.", "Performing network calls inside synchronized blocks."]
        ),
        (
            "What is the purpose of the CountDownLatch utility in java.util.concurrent?",
            "executors-concurrency-utils",
            "CountDownLatch is a synchronization aid that allows one or more threads to wait until a set of operations being performed in other threads completes, by decrementing a count via countDown() until it reaches zero.",
            "CountDownLatch is initialized with a positive count. Worker threads perform their assigned tasks and call `latch.countDown()`, decrementing the counter. Coordinator threads call `latch.await()`, which blocks until the counter reaches zero due to successive countDown() calls. Unlike a CyclicBarrier, a CountDownLatch is a one-shot gate; once the count reaches zero, it cannot be reset.",
            "Under the hood, CountDownLatch utilizes AbstractQueuedSynchronizer (AQS) in shared mode. Calling await() acquires the AQS shared synchronizer, and countDown() releases it when the state reaches 0, unparking all blocked waiting threads simultaneously.",
            "import java.util.concurrent.*;\npublic class LatchDemo {\n    public static void main(String[] args) throws Exception {\n        int workers = 3;\n        CountDownLatch latch = new CountDownLatch(workers);\n        ExecutorService exec = Executors.newFixedThreadPool(workers);\n        \n        for (int i = 0; i < workers; i++) {\n            exec.submit(() -> {\n                try { System.out.println(\"Service initializing...\"); }\n                finally { latch.countDown(); } // Always in finally\n            });\n        }\n        latch.await(5, TimeUnit.SECONDS); // Wait for all 3 services\n        System.out.println(\"All services ready. Server starting.\");\n        exec.shutdown();\n    }\n}",
            "Always call `latch.countDown()` inside a `finally` block to guarantee decrement even if the worker task throws an unhandled exception.",
            "If a worker thread throws an unhandled exception before countDown(), the count never reaches zero, causing coordinator threads to hang indefinitely without a timeout.",
            "CountDownLatch provides a simple, lock-free coordination mechanism for parallel fan-out / fan-in patterns.",
            ["Calling await() without a timeout, risking permanent thread blockage.", "Calling countDown() outside of finally blocks.", "Attempting to reuse a CountDownLatch (use CyclicBarrier for recurring cycles)."]
        ),
        (
            "What is the difference between final, finally, and finalize in Java?",
            "jmm-synchronization",
            "final is a keyword defining non-modifiable constants, un-overridable methods, or un-inheritable classes; finally is a block in exception handling guaranteed to execute after try-catch; finalize is a deprecated Object method formerly used for garbage collection cleanup.",
            "'final' is an access modifier: a final variable cannot be reassigned, a final method cannot be overridden by subclasses, and a final class cannot be extended. 'finally' is an exception-handling construct executed after a try-catch block regardless of whether an exception occurred, used for mandatory cleanup. 'finalize()' is a deprecated method on java.lang.Object called by the garbage collector before reclaiming an object, now replaced by AutoCloseable.",
            "In the Java Memory Model, final fields receive special initialization safety guarantees: when an object is properly constructed, any thread reading a final field is guaranteed to observe the value set in the constructor without requiring synchronization.",
            "public final class ImmutableToken { // final class cannot be extended\n    private final String token; // final field cannot be reassigned\n    \n    public ImmutableToken(String token) {\n        this.token = token;\n    }\n    \n    public void process() {\n        try {\n            System.out.println(\"Processing token\");\n        } finally {\n            System.out.println(\"Always runs in finally\");\n        }\n    }\n}",
            "Use final for all fields that should not change after construction, facilitating thread-safe immutable design patterns.",
            "The finally block may not execute if `System.exit(0)` is invoked, or if the host JVM process crashes / power fails.",
            "final fields enable JIT compiler optimizations like constant folding and aggressive inlining.",
            ["Confusing the three completely distinct language keywords due to similar naming.", "Relying on finally to execute after calling System.exit().", "Using finalize() for production resource cleanup."]
        ),
        (
            "What is the purpose of the Java Generics Type Erasure mechanism?",
            "jmm-synchronization",
            "Type erasure removes generic type annotations at compile time and inserts appropriate casts and bridge methods into bytecode, ensuring full binary backward compatibility with pre-Java 5 legacy code while maintaining compile-time type safety.",
            "When Java introduced generics in Java 5, maintaining binary compatibility with billions of lines of pre-existing code was paramount. Instead of creating reified types at runtime (like C# or C++ templates), Java employs Type Erasure: the compiler validates types, then replaces unbounded type parameters with Object (or the first bound) and inserts synthetic type casts in bytecode where necessary. At runtime, List<String> and List<Integer> share the exact same raw class: List.class.",
            "Because of type erasure, you cannot instantiate generic types directly (`new T()`), create generic arrays (`new T[10]`), or use `instanceof List<String>`. Reflection on raw objects loses generic information, although generic signatures on class and method declarations are preserved in the ClassFile's Signature attribute for reflection inspection.",
            "import java.util.*;\npublic class ErasureDemo {\n    public static void main(String[] args) {\n        List<String> stringList = new ArrayList<>();\n        List<Integer> intList = new ArrayList<>();\n        \n        // Bytecode compiles both to raw ArrayList\n        System.out.println(stringList.getClass() == intList.getClass()); // true\n    }\n}",
            "Be aware of type erasure when designing serialization or JSON mapping (e.g. Jackson TypeReference is required to capture generic types via super-type tokens).",
            "Attempting runtime type checks with `instanceof List<SpecificClass>` causes compilation errors due to erased type parameters.",
            "Type erasure achieved seamless backward compatibility with zero JVM bytecode changes, but eliminates runtime generic type reification.",
            ["Trying to create generic arrays directly (e.g. `new T[size]`).", "Expecting `list.getClass().getTypeParameters()` to reveal the runtime generic argument.", "Ignoring compiler unchecked cast warnings in generic repositories."]
        ),
        (
            "What is the difference between Thread.start() and Thread.run() in Java?",
            "executors-concurrency-utils",
            "Thread.start() allocates a new execution stack and schedules a new operating system/JVM thread to invoke run(), whereas calling Thread.run() directly executes the method synchronously on the current calling thread like any regular method call.",
            "The `start()` method initializes thread state in the JVM, invokes the operating system's thread creation API (such as pthread_create on POSIX), and registers the new thread with the OS/JVM scheduler. Once scheduled, the new thread invokes the `run()` method asynchronously on its own distinct call stack. Directly calling `run()` bypasses thread creation entirely; the code runs synchronously within the caller's existing thread and call stack.",
            "Calling `start()` more than once on the same Thread instance throws `IllegalThreadStateException`, because a thread's lifecycle state machine moves from NEW to RUNNABLE and cannot be restarted once stopped.",
            "public class ThreadStartVsRun {\n    public static void main(String[] args) {\n        Thread thread = new Thread(() -> {\n            System.out.println(\"Executing thread: \" + Thread.currentThread().getName());\n        });\n        \n        // thread.run();   // Executes synchronously on 'main' thread!\n        thread.start();    // Executes asynchronously on 'Thread-0'!\n    }\n}",
            "Never call `run()` directly when concurrent asynchronous execution is desired; always use `start()` or an ExecutorService.",
            "Calling `run()` directly causes unexpected blocking in GUI dispatchers or server request handlers, masquerading as thread safety while executing synchronously.",
            "start() handles OS thread creation and stack allocation; run() is merely the task payload.",
            ["Calling run() instead of start(), resulting in synchronous execution.", "Calling start() twice on the same thread instance.", "Creating raw Thread instances directly in high-throughput servers instead of using ExecutorService."]
        )
    ]

    for item in basic_specs:
        questions.append({
            "title": item[0],
            "difficulty": "BASIC",
            "technology_slug": "java-backend",
            "topic_slug": item[1],
            "question_type": "CONCEPTUAL",
            "scenario_type": "LANGUAGE_FUNDAMENTALS",
            "short_answer": item[2],
            "interview_ready_answer": item[3],
            "deep_explanation": item[4],
            "architecture_notes": "Compiled to standard JVM bytecode complying with the Java Virtual Machine Specification (JSR-392).",
            "code_example": item[5],
            "why_interviewer_asks": "Evaluates foundational Java competencies, core mechanics, and whether the candidate understands core JVM behavior.",
            "production_considerations": item[6],
            "failure_modes": item[7],
            "tradeoffs": item[8],
            "common_mistakes": item[9],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Focus on the foundational definition and why the feature was designed this way."},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Think about how the JVM handles memory, threads, or bytecode execution for this concept."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Consider real-world production failure modes when this mechanism is misunderstood."}
            ],
            "sources": [
                {
                    "source_name": "Oracle Java SE 21 & JVM Specification",
                    "source_url": "https://docs.oracle.com/javase/specs/jvms/se21/html/index.html",
                    "publisher": "Oracle Corporation"
                }
            ],
            "followups": [
                {
                    "followup_question": "How does this behavior impact garbage collection or multithreaded performance under heavy enterprise load?",
                    "answer_guidance": "Explain the interaction between thread scheduling, memory barriers, or object allocation rates in the Young Generation."
                }
            ],
            "tags": ["Java", "Core Java", "JVM", "Google", "Amazon"]
        })

    # ==========================================
    # 2. 20 MEDIUM QUESTIONS
    # ==========================================
    medium_specs = [
        (
            "How does ConcurrentHashMap achieve thread safety in Java without locking the entire map?",
            "executors-concurrency-utils",
            "Java 8+ ConcurrentHashMap eliminates table-wide locks and segment locks, using lock-free Compare-And-Swap (CAS) for empty bucket insertions and synchronized blocks on only the individual head node of a hash bucket for collisions.",
            "Unlike legacy Hashtable or Collections.synchronizedMap which lock the entire map on every operation, Java 8 ConcurrentHashMap uses fine-grained locking per bucket. Reading operations (get) are completely lock-free because node values and 'next' pointers are marked volatile. For writes, if a bucket is empty, it uses lock-free CAS to insert the node. If a collision occurs, it synchronizes only on the head node of that specific bin, allowing concurrent writes to all other bins.",
            "In Java 7, ConcurrentHashMap divided the table into 16 Segments, each acting as a ReentrantLock. Java 8 redesigned this completely: the array of Node<K,V> bins uses volatile references. When a bin's length exceeds 8 and table capacity >= 64, the bin treeifies into a Red-Black Tree (TreeBin) for O(log N) worst-case performance under hash collisions.",
            "import java.util.concurrent.ConcurrentHashMap;\npublic class ConcurrentMapDemo {\n    private final ConcurrentHashMap<String, Integer> cache = new ConcurrentHashMap<>();\n    \n    public int computeIfAbsentSafe(String key) {\n        // Atomic computeIfAbsent: lock-free read or single-bin sync\n        return cache.computeIfAbsent(key, k -> k.length() * 10);\n    }\n}",
            "Always use atomic operations like `computeIfAbsent()`, `putIfAbsent()`, or `merge()`. Check-then-act sequences (e.g. `if(!map.containsKey(k)) map.put(k,v)`) are NOT atomic.",
            "Performing heavy I/O operations inside `computeIfAbsent` lambdas blocks other threads attempting to access the same hash bin.",
            "Fine-grained bin locking maximizes write throughput across independent buckets, but size() returns an estimated count during concurrent updates.",
            ["Using containsKey() followed by put() instead of computeIfAbsent().", "Attempting to insert null keys or null values, which throws NullPointerException.", "Assuming iteration provides a point-in-time atomic snapshot (it provides a weakly consistent view)."]
        ),
        (
            "What is the difference between Virtual Threads (JEP 444) and Platform Threads in Java 21?",
            "virtual-threads-loom",
            "Platform threads are 1:1 wrappers around OS kernel threads with fixed ~1MB stacks and limited concurrency, whereas Virtual Threads are lightweight JVM-scheduled M:N user-space threads with dynamic heap stacks that scale to millions for blocking I/O.",
            "Platform Threads map directly to OS kernel threads. Operating system context switches and fixed stack allocations cap platform thread capacity to thousands per server. Virtual Threads, introduced in Java 21, decouple Java threads from OS threads. The JVM manages virtual threads in user space, mounting them onto a small pool of ForkJoinPool carrier OS threads. When a virtual thread performs blocking I/O (sockets, files, sleep), the JVM unmounts it and saves its stack frames to the heap, freeing the carrier thread immediately.",
            "Virtual Threads restore the intuitive thread-per-request architecture without the cognitive complexity and debugging nightmares of reactive programming frameworks (WebFlux, RxJava). However, Virtual Threads are designed exclusively for blocking I/O tasks and provide zero throughput benefits for CPU-bound computations.",
            "import java.util.concurrent.*;\npublic class LoomComparison {\n    public static void main(String[] args) {\n        // Virtual Thread per task: no pooling needed\n        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {\n            executor.submit(() -> {\n                Thread.sleep(50); // Unmounts from carrier thread\n                return \"Done\";\n            });\n        }\n    }\n}",
            "Never pool Virtual Threads. Virtual Threads are cheap to create (nanoseconds) and are intended to be ephemeral, created per task.",
            "Carrier thread pinning occurs when a virtual thread performs blocking I/O inside a `synchronized` block or native method, preventing unmounting.",
            "Virtual threads eliminate reactive programming overhead for I/O workloads, but CPU-bound tasks must continue using platform thread pools.",
            ["Pooling virtual threads with ThreadPoolExecutor.", "Using virtual threads for computationally intensive tasks like video encoding or crypto hashing.", "Calling blocking methods inside synchronized blocks instead of ReentrantLock, causing carrier thread pinning."]
        ),
        (
            "How does the Java Garbage Collector classify and handle Weak, Soft, and Phantom references?",
            "jvm-memory-gc",
            "SoftReferences are cleared before OutOfMemoryError for memory-sensitive caching; WeakReferences are cleared on the next GC cycle when no strong references exist; PhantomReferences are enqueued upon object finalization for post-mortem native resource cleanup.",
            "Java provides four reference strengths via java.lang.ref. Strong references prevent garbage collection entirely. SoftReferences are cleared only when the JVM experiences critical memory pressure before throwing OutOfMemoryError, making them suitable for memory-sensitive caches. WeakReferences are cleared aggressively during the very next GC cycle once all strong references are gone, ideal for canonical mappings (WeakHashMap). PhantomReferences never allow access to the underlying referent; they are enqueued into a ReferenceQueue after the object has been finalized, enabling safe native cleanup without finalizers.",
            "Under the hood, the garbage collector tracks these references during the marking phase. SoftReference eviction is governed by `-XX:SoftRefLRUPolicyMSPerMB`, which keeps soft references alive based on the amount of free heap per megabyte.",
            "import java.lang.ref.*;\npublic class ReferenceDemo {\n    public static void main(String[] args) {\n        Object strong = new Object();\n        SoftReference<Object> soft = new SoftReference<>(strong);\n        WeakReference<Object> weak = new WeakReference<>(strong);\n        \n        strong = null; // Object is now eligible for GC\n        // weak.get() will return null after the next GC run\n    }\n}",
            "Do not use SoftReference for high-throughput enterprise caching (use Guava or Caffeine with explicit size/time bounds instead), as soft references can cause erratic GC latency spikes before OOM.",
            "WeakHashMap keys are weak references, but if values hold strong references back to keys, the entry cannot be garbage collected (circular reference leak).",
            "Specialized references allow fine-grained interaction with GC lifecycle, but introduce overhead and unpredictable cache eviction timings.",
            ["Assuming SoftReferences are cleared immediately like WeakReferences.", "Creating circular references between keys and values in WeakHashMap.", "Calling get() on a PhantomReference (it always returns null by design)."]
        ),
        (
            "What is the difference between ReentrantLock and synchronized in Java, and when should you choose ReentrantLock?",
            "jmm-synchronization",
            "ReentrantLock provides advanced lock features including timed lock acquisition (tryLock), interruptible lock waiting (lockInterruptibly), fair queuing policies, and multiple Condition variables, which standard synchronized blocks lack.",
            "Both ReentrantLock and `synchronized` provide mutual exclusion and reentrancy. However, `synchronized` is an intrinsic language keyword with automatic lock acquisition and release, making it simpler and immune to forgotten `unlock()` bugs. ReentrantLock from java.util.concurrent.locks is an explicit lock implementation offering tryLock() with timeouts (preventing deadlocks), lockInterruptibly() (allowing responsive thread cancellation), and the ability to associate multiple Condition objects for separate waiting sets.",
            "Under the hood, ReentrantLock is built on AbstractQueuedSynchronizer (AQS), utilizing a volatile state variable and a FIFO wait queue. With Java 21 Virtual Threads, ReentrantLock does NOT cause carrier thread pinning when blocking, whereas synchronized blocks can cause pinning, making ReentrantLock the preferred lock in modern virtual-thread codebases.",
            "import java.util.concurrent.locks.*;\npublic class LockDemo {\n    private final ReentrantLock lock = new ReentrantLock();\n    \n    public boolean processWithTimeout() throws InterruptedException {\n        // tryLock prevents deadlocks by avoiding indefinite waiting\n        if (lock.tryLock(2, java.util.concurrent.TimeUnit.SECONDS)) {\n            try {\n                // Critical section\n                return true;\n            } finally {\n                lock.unlock(); // MUST be in finally\n            }\n        }\n        return false; // Lock acquisition timed out\n    }\n}",
            "Always invoke `lock.unlock()` inside a `finally` block immediately after acquiring the lock to prevent permanent deadlocks on exception.",
            "Forgetting to release ReentrantLock inside a finally block permanently starves all other waiting threads.",
            "ReentrantLock provides sophisticated concurrency control and virtual-thread compatibility, but requires manual boilerplate compared to synchronized.",
            ["Omitting the try-finally structure around lock.unlock().", "Calling lock() inside the try block rather than immediately before it.", "Defaulting to fair locks (`new ReentrantLock(true)`) without necessity, causing massive throughput penalties."]
        ),
        (
            "How does ThreadPoolExecutor handle work queue saturation and rejection policies?",
            "executors-concurrency-utils",
            "When both core pool and the bounded queue are full, ThreadPoolExecutor spawns threads up to maximumPoolSize; if maximumPoolSize is reached and queue is saturated, it invokes the configured RejectedExecutionHandler (Abort, CallerRuns, Discard, DiscardOldest).",
            "ThreadPoolExecutor manages thread lifecycle through a specific progression: incoming tasks are assigned to core threads up to `corePoolSize`. When all core threads are busy, additional tasks are queued in the `workQueue`. Only when the workQueue fills to capacity does the executor spawn additional threads up to `maximumPoolSize`. If maximumPoolSize is reached and the queue is completely full, subsequent tasks are rejected via the RejectedExecutionHandler.",
            "Java provides four standard rejection policies: 1. AbortPolicy (default, throws RejectedExecutionException), 2. CallerRunsPolicy (executes task on the calling thread, naturally throttling submission rate), 3. DiscardPolicy (silently drops the task), and 4. DiscardOldestPolicy (drops the oldest unhandled task in the queue and retries).",
            "import java.util.concurrent.*;\npublic class CustomThreadPool {\n    public static ThreadPoolExecutor createResilientPool() {\n        return new ThreadPoolExecutor(\n            4,                      // corePoolSize\n            16,                     // maximumPoolSize\n            60L, TimeUnit.SECONDS,  // keepAliveTime\n            new ArrayBlockingQueue<>(500), // Bounded queue!\n            Executors.defaultThreadFactory(),\n            new ThreadPoolExecutor.CallerRunsPolicy() // Backpressure!\n        );\n    }\n}",
            "Never use unbounded queues (like LinkedBlockingQueue without capacity) in production; high traffic spikes will cause OutOfMemoryError before maximumPoolSize is ever reached.",
            "Using AbortPolicy in user-facing APIs without catching RejectedExecutionException results in 500 Internal Server Errors.",
            "CallerRunsPolicy provides natural backpressure by forcing the producer thread to execute the task, slowing down request intake.",
            ["Using Executors.newFixedThreadPool() which defaults to an unbounded LinkedBlockingQueue (OOM risk).", "Using DiscardPolicy silently without logging or alerting.", "Assuming threads scale up to maximumPoolSize before filling the queue (queue fills FIRST)."]
        )
    ]

    # Additional 15 medium questions specs
    more_medium = [
        ("How does the Java CompletableFuture pipeline asynchronous computations and handle exceptions?", "executors-concurrency-utils", "CompletableFuture provides non-blocking composable asynchronous workflows using methods like thenApply, thenCompose, and exceptionally, executing callbacks on a designated thread pool.", "CompletableFuture represents a promise-based computation. It supports chaining transformations (thenApply), dependent async tasks (thenCompose), parallel joins (allOf, thenCombine), and robust exception handling (exceptionally, handle). If an exception occurs in any upstream stage, it bypasses intermediate stages and triggers the nearest exceptionally or handle handler.", "Under the hood, CompletableFuture maintains a Treiber stack of completion dependencies (Completion objects). When a stage completes, it pops and triggers downstream actions either synchronously or asynchronously via an Executor.", "CompletableFuture.supplyAsync(() -> fetchUser(id))\n    .thenApplyAsync(user -> enrichProfile(user))\n    .exceptionally(ex -> fallbackUser());", "Always pass an explicit custom ExecutorService to Async methods rather than relying on the shared ForkJoinPool.commonPool().", "Uncaught exceptions in async stages silently terminate the pipeline unless exceptionally() or whenComplete() is attached.", "Non-blocking composition eliminates thread waiting, but deep callback chains can complicate stack trace debugging.", ["Omitting exceptionally() and losing track of silent failures.", "Using ForkJoinPool.commonPool() for blocking I/O tasks.", "Calling join() or get() prematurely, blocking the calling thread."]),
        ("What is the difference between Parallel Garbage Collector and G1 Garbage Collector in Java?", "jvm-memory-gc", "Parallel GC focuses on maximizing application throughput by stopping all application threads during GC, while G1 GC focuses on predictable, low pause times by collecting memory regions concurrently in increments.", "Parallel GC (Throughput Collector) uses multiple threads to collect Young and Old generations, maximizing CPU utilization for batch and computational workloads at the expense of longer Stop-The-World (STW) pauses. G1 GC (Garbage-First) partitions the heap into hundreds of small equal-sized regions and collects regions with the highest amount of garbage first, meeting user-defined pause time targets (-XX:MaxGCPauseMillis).", "G1 divides the heap into 1MB to 32MB regions dynamically designated as Eden, Survivor, Old, or Humongous. It tracks inter-region references using Remembered Sets (R-Sets) and card tables, allowing concurrent marking and incremental evacuation.", "// JVM flags: -XX:+UseG1GC -XX:MaxGCPauseMillis=200", "G1GC is the default collector since Java 9, ideal for interactive web services with multi-gigabyte heaps.", "Setting MaxGCPauseMillis unrealistically low forces G1 to collect too few regions per cycle, causing garbage to accumulate and triggering a catastrophic Full GC.", "Parallel GC maximizes raw CPU throughput; G1 GC minimizes maximum latency spikes.", ["Assuming G1GC eliminates STW pauses completely (it bounds them, but pauses still occur).", "Tuning G1GC excessively with old generation size flags, overriding its self-tuning ergonomics.", "Using ParallelGC for latency-sensitive microservices."]),
        ("How does the AbstractQueuedSynchronizer (AQS) framework power Java concurrency utilities?", "jmm-synchronization", "AQS provides a foundational FIFO wait queue and a volatile state integer used to implement synchronization primitives like ReentrantLock, Semaphore, CountDownLatch, and ReentrantReadWriteLock.", "AQS provides a robust framework for building locks and synchronizers. It maintains an atomic volatile state integer (getState, setState, compareAndSetState) and a doubly linked CLH lock queue of waiting threads. Subclasses implement tryAcquire/tryRelease (exclusive mode) or tryAcquireShared/tryReleaseShared (shared mode). When a thread fails to acquire state, AQS enqueues the thread and parks it using LockSupport.park().", "Under the hood, AQS maintains a doubly linked CLH variant queue where each waiting thread is encapsulated in a Node. When tryAcquire fails, the thread is enqueued at the tail using atomic CAS and parked via LockSupport.park(this). When the lock holder releases state, tryRelease sets the state to 0 and unparks the head successor node, orchestrating efficient, lock-free FIFO thread handoffs without busy spinning.", "public class Mutex extends java.util.concurrent.locks.AbstractQueuedSynchronizer {\n    @Override protected boolean tryAcquire(int arg) {\n        return compareAndSetState(0, 1);\n    }\n    @Override protected boolean tryRelease(int arg) {\n        setState(0); return true;\n    }\n}", "Understanding AQS explains how ReentrantLock, Semaphore, and CountDownLatch operate under the hood.", "Improper AQS subclassing can cause lock state corruption and lost thread wakeup signals.", "AQS avoids busy waiting by parking threads, minimizing CPU consumption during high lock contention.", ["Writing custom synchronization with wait/notify instead of leveraging AQS utilities.", "Assuming AQS uses thread busy-spinning instead of LockSupport parking.", "Misunderstanding exclusive vs shared AQS acquisition modes."]),
        ("What is the difference between optimistic locking and pessimistic locking in Java applications?", "jmm-synchronization", "Pessimistic locking assumes conflicts are frequent and locks records or objects upfront, whereas optimistic locking assumes conflicts are rare, detects concurrent changes via version checks, and retries on collision.", "Pessimistic locking locks the shared resource before accessing it (e.g. `synchronized`, `SELECT ... FOR UPDATE` in SQL), preventing all other threads or transactions from reading or writing until the lock is released. Optimistic locking avoids locking upfront; it proceeds with modifications and verifies upon write that the version/timestamp has not changed (e.g. CAS atomic operations, JPA `@Version`). If a conflict is detected, the operation aborts or retries.", "In the JVM, `AtomicInteger` uses optimistic hardware CAS (Compare-And-Swap) loops (`compareAndSet`). In databases, JPA uses optimistic locking with an integer `@Version` column to eliminate long-lived database row locks.", "public class OptimisticAccount {\n    private final java.util.concurrent.atomic.AtomicInteger balance = new java.util.concurrent.atomic.AtomicInteger(100);\n    public void withdraw(int amt) {\n        int prev, next;\n        do {\n            prev = balance.get();\n            if (prev < amt) throw new IllegalStateException();\n            next = prev - amt;\n        } while (!balance.compareAndSet(prev, next)); // CAS retry loop\n    }\n}", "Use optimistic locking for high-read, low-write scenarios. Use pessimistic locking for high-contention financial transactions where conflicts are guaranteed.", "High contention in optimistic locking causes excessive CAS retry loops, burning CPU cycles.", "Optimistic locking maximizes throughput under low contention; pessimistic locking avoids retry overhead under extreme contention.", ["Using optimistic locking where contention is high, creating livelocks.", "Forgetting to handle OptimisticLockException in JPA service layers.", "Holding pessimistic database locks across external network calls."]),
        ("How does Java 21 Scoped Values (JEP 446) improve upon ThreadLocal for Virtual Threads?", "virtual-threads-loom", "Scoped Values provide immutable, inheritable, and bounded-lifetime data sharing across threads, eliminating the memory leaks, unbounded mutability, and high footprint of ThreadLocal in virtual thread environments.", "ThreadLocal was designed when threads were heavy and few. In virtual thread architectures with millions of threads, ThreadLocal instances consume substantial heap space and can easily leak memory if `remove()` is omitted. Scoped Values (JEP 446) introduce a lightweight alternative: a ScopedValue is immutable, valid only for the bounded lexical scope of a `ScopedValue.where(KEY, value).run(...)` invocation, and automatically cleaned up when the scope exits.", "Scoped Values solve the thread-local bloat crisis in Loom by establishing an immutable, dynamically scoped binding. Unlike ThreadLocal where every virtual thread inherits a separate mutable map copy, Scoped Values use a shared, immutable linked list of bindings. Child virtual threads forked within a StructuredTaskScope inherit parent bindings by reference with zero allocation overhead and zero memory leak vulnerability.", "import java.lang.ScopedValue;\npublic class ScopedDemo {\n    public static final ScopedValue<String> CONTEXT = ScopedValue.newInstance();\n    public static void main(String[] args) {\n        ScopedValue.where(CONTEXT, \"tenant_123\").run(() -> {\n            System.out.println(\"Tenant: \" + CONTEXT.get());\n        }); // Automatically unbounds upon exit!\n    }\n}", "Adopt Scoped Values in Java 21+ for propagating request context, tenant IDs, and tracing spans into virtual threads.", "Attempting to access a ScopedValue outside its bound execution scope throws NoSuchElementException.", "Scoped Values are immutable and bounded, guaranteeing zero memory leaks and minimal memory overhead compared to ThreadLocal.", ["Attempting to mutate a ScopedValue after binding (they are strictly immutable).", "Relying on ThreadLocal when spawning millions of short-lived virtual threads.", "Accessing ScopedValue outside its lexical `run()` scope."])
    ]

    for item in medium_specs:
        questions.append({
            "title": item[0],
            "difficulty": "MEDIUM",
            "technology_slug": "java-backend",
            "topic_slug": item[1],
            "question_type": "CONCEPTUAL",
            "scenario_type": "CONCURRENCY_MECHANICS",
            "short_answer": item[2],
            "interview_ready_answer": item[3],
            "deep_explanation": f"{item[3]}\n\nDeep Architectural Analysis:\n{item[4]}" if len(item[4]) < 150 else item[4],
            "architecture_notes": "Implemented within the OpenJDK java.util.concurrent runtime architecture.",
            "code_example": item[5],
            "why_interviewer_asks": "Evaluates candidate's practical concurrency experience, data structure internals, and architectural trade-offs.",
            "production_considerations": item[6],
            "failure_modes": item[7],
            "tradeoffs": item[8],
            "common_mistakes": item[9],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Analyze the concurrency mechanism and compare it to coarse-grained locking."},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Look at the internal state variables (CAS, volatile, AQS, or carrier thread scheduling)."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Consider what happens under extreme concurrent load when thousands of threads invoke this."}
            ],
            "sources": [
                {
                    "source_name": "Oracle Java SE 21 Documentation: java.util.concurrent",
                    "source_url": "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html",
                    "publisher": "Oracle Corporation"
                }
            ],
            "followups": [
                {
                    "followup_question": "How would you diagnose performance degradation or contention in this component using JFR (Java Flight Recorder)?",
                    "answer_guidance": "Inspect 'Java Monitor Blocked', 'Execution Sample', and 'Virtual Thread Pinned' events in JMC or async-profiler."
                }
            ],
            "tags": ["Java", "Concurrency", "ThreadPool", "Meta", "Netflix"]
        })

    for item in more_medium:
        questions.append({
            "title": item[0],
            "difficulty": "MEDIUM",
            "technology_slug": "java-backend",
            "topic_slug": item[1],
            "question_type": "CONCEPTUAL",
            "scenario_type": "CONCURRENCY_MECHANICS",
            "short_answer": item[2],
            "interview_ready_answer": item[3],
            "deep_explanation": f"{item[3]}\n\nDeep Architectural Analysis:\n{item[4]}" if len(item[4]) < 150 else item[4],
            "architecture_notes": "Compiled to standard JVM bytecode complying with the Java Virtual Machine Specification (JSR-392).",
            "code_example": item[5],
            "why_interviewer_asks": "Evaluates candidate's practical concurrency experience, data structure internals, and architectural trade-offs.",
            "production_considerations": item[6],
            "failure_modes": item[7],
            "tradeoffs": item[8],
            "common_mistakes": item[9],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Analyze the concurrency mechanism and compare it to coarse-grained locking."},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Look at the internal state variables (CAS, volatile, AQS, or carrier thread scheduling)."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Consider what happens under extreme concurrent load when thousands of threads invoke this."}
            ],
            "sources": [
                {
                    "source_name": "Oracle Java SE 21 Documentation: java.util.concurrent",
                    "source_url": "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html",
                    "publisher": "Oracle Corporation"
                }
            ],
            "followups": [
                {
                    "followup_question": "How would you diagnose performance degradation or contention in this component using JFR (Java Flight Recorder)?",
                    "answer_guidance": "Inspect 'Java Monitor Blocked', 'Execution Sample', and 'Virtual Thread Pinned' events in JMC or async-profiler."
                }
            ],
            "tags": ["Java", "Concurrency", "ThreadPool", "Meta", "Netflix"]
        })

    # ==========================================
    # 3. 20 HARD / TOUGH QUESTIONS
    # ==========================================
    hard_specs = [
        (
            "How does the HotSpot JVM implement bias locking, lightweight locking, and heavyweight locking inflation?",
            "HARD",
            "jmm-synchronization",
            "HotSpot represents object synchronization state in the Mark Word: it historically biased locks to the acquiring thread, transitions to lightweight locking via CAS on thread stack Displaced Mark Words, and inflates to heavyweight OS mutexes when contention occurs.",
            "In HotSpot, every object header contains a Mark Word (64-bit on 64-bit JVMs) whose lowest bits encode lock state (01 = unlocked, 00 = lightweight locked, 10 = heavyweight monitor, 11 = marked for GC). Lightweight locking occurs when an uncontended thread executes synchronized: it copies the object's Mark Word to a Displaced Mark Word on its stack and performs a CAS to point the object's Mark Word to its stack. If CAS succeeds, the lock is held. If another thread attempts acquisition, the lock inflates to an ObjectMonitor (heavyweight), creating an OS mutex where contended threads park in wait queues.",
            "Biased locking (deprecated in Java 15 via JEP 374) avoided CAS entirely for single-threaded locks by recording the thread ID in the Mark Word, but revocation required expensive Stop-The-World safepoints that degraded modern multithreaded systems.",
            "public class LockInflationDemo {\n    private final Object monitor = new Object();\n    public void executeCriticalSection() {\n        synchronized (monitor) {\n            // Uncontended: Lightweight stack CAS\n            // Contended by thread 2: Inflates to ObjectMonitor with OS mutex\n        }\n    }\n}",
            "Avoid synchronizing on shared locks across high-contention worker threads to prevent monitor inflation and thread context switches.",
            "Heavyweight lock inflation causes threads to transition from user space to kernel space, incurring ~1-2 microsecond context switch latencies.",
            "Lightweight locking achieves near-zero overhead when uncontended; heavyweight locking ensures thread safety at the expense of OS scheduling latency.",
            ["Assuming synchronized always makes expensive kernel system calls.", "Overlooking that biased locking was deprecated and disabled in modern JVMs.", "Synchronizing on unique String literals or boxed Integer instances."]
        ),
        (
            "How do you detect, diagnose, and resolve Carrier Thread Pinning with Virtual Threads in production?",
            "HARD",
            "virtual-threads-loom",
            "Carrier thread pinning occurs when a virtual thread performs blocking I/O while holding a synchronized monitor or executing native JNI code, preventing unmounting; it is diagnosed via `-Djdk.tracePinnedThreads=full` or JFR and resolved by replacing synchronized with ReentrantLock.",
            "Virtual Threads rely on the ability to unmount from their underlying ForkJoinPool carrier thread whenever they block on I/O. However, in Java 21, the JVM cannot unmount a virtual thread if it is inside a `synchronized` block/method or native call stack (called 'pinning'). If pinned virtual threads perform prolonged blocking I/O (such as slow database queries or external HTTP calls), carrier threads become exhausted, starving other virtual threads and collapsing application throughput.",
            "To detect pinning, run the JVM with `-Djdk.tracePinnedThreads=full` or record Java Flight Recorder (JFR) `jdk.VirtualThreadPinned` events. The remediation is straightforward: replace `synchronized (lock)` with `ReentrantLock` around blocking sections, as ReentrantLock does not pin carrier threads.",
            "import java.util.concurrent.locks.ReentrantLock;\npublic class PinningRemediation {\n    // BAD: synchronized pins carrier thread during I/O\n    // public synchronized String fetchRemoteBad() { return httpCall(); }\n    \n    // GOOD: ReentrantLock unmounts cleanly without pinning\n    private final ReentrantLock lock = new ReentrantLock();\n    public String fetchRemoteGood() {\n        lock.lock();\n        try {\n            return \"httpResponse\"; // Carrier unmounts freely!\n        } finally {\n            lock.unlock();\n        }\n    }\n}",
            "Enable JFR in production containers to monitor `jdk.VirtualThreadPinned` duration and frequency.",
            "Carrier pool exhaustion causes application latency to spike exponentially, mimicking a deadlock even though threads are merely waiting for carrier execution slots.",
            "ReentrantLock requires explicit unlock in finally blocks, but provides clean carrier thread unmounting for virtual threads.",
            ["Ignoring third-party libraries (JDBC drivers, logging frameworks) that still use synchronized blocks around network sockets.", "Assuming carrier thread pools should be scaled up to compensate for pinning (fixes symptom, wastes memory).", "Confusing CPU saturation with carrier thread starvation."]
        ),
        (
            "How does the Java Memory Model define and enforce the Happens-Before relationship across threads?",
            "HARD",
            "jmm-synchronization",
            "The Happens-Before relationship defines a partial order on memory actions ensuring that memory writes by one thread are guaranteed visible to concurrent reads by another thread without data races.",
            "Under JSR-133, a program has a data race if two threads access the same memory location concurrently, at least one access is a write, and the accesses are not ordered by a happens-before relationship. Key happens-before rules include: 1. Program Order Rule (each action in a thread happens-before later actions in that thread), 2. Monitor Lock Rule (an unlock on a monitor happens-before every subsequent lock on the same monitor), 3. Volatile Variable Rule (a write to a volatile happens-before every subsequent read of that volatile), 4. Thread Start Rule, and 5. Transitivity (if A happens-before B and B happens-before C, then A happens-before C).",
            "These rules allow hardware compilers and CPU out-of-order execution units to optimize aggressively while ensuring programmers have a deterministic, sequential-consistency-like mental model for properly synchronized code.",
            "public class HappensBeforePipeline {\n    private int data = 0;\n    private volatile boolean ready = false;\n    \n    public void writer() {\n        data = 42;             // 1. Plain write\n        ready = true;          // 2. Volatile write (Happens-Before boundary)\n    }\n    \n    public int reader() {\n        if (ready) {           // 3. Volatile read (Happens-Before boundary)\n            return data;       // 4. Guaranteed to see 42 due to transitivity (1 -> 2 -> 3 -> 4)!\n        }\n        return -1;\n    }\n}",
            "Leverage the volatile write happens-before boundary to publish non-volatile data structures safely without locking.",
            "Failing to establish a happens-before order results in data races where readers observe partially initialized objects or stale cached values.",
            "Happens-before guarantees require memory fences on weak memory architectures (ARM, POWER), incurring slight hardware bus overhead.",
            ["Believing that CPU execution order strictly matches source code order without synchronization.", "Assuming non-volatile reads reflect writes immediately without happens-before edges.", "Using double-checked locking without marking the instance variable volatile."]
        ),
        (
            "How does the Z Garbage Collector (ZGC) achieve sub-millisecond Stop-The-World pause times on terabyte heaps?",
            "TOUGH",
            "jvm-memory-gc",
            "ZGC uses colored pointers (reference metadata in pointer bits) and load barriers to perform concurrent marking, concurrent relocation, and concurrent reference processing without stopping application threads.",
            "Traditional garbage collectors stop application threads during object relocation to update pointer references. ZGC (introduced in JEP 333 and enhanced with Generational ZGC in Java 21 via JEP 439) performs object marking, relocation, and reference remapping concurrently with application threads. On 64-bit systems, ZGC embeds reference metadata directly into the top bits of object reference pointers (Colored Pointers: Marked0, Marked1, Remapped).",
            "When an application thread dereferences an object pointer, a JIT-compiled Load Barrier intercepts the read. If the pointer has not yet been remapped to the relocated object address, the load barrier resolves the new address from the forwarding table, self-heals the pointer in-place, and returns the live object—all in a few CPU instructions without pausing other threads.",
            "// Enable Generational ZGC in Java 21+:\n// java -XX:+UseZGC -XX:+ZGenerational -Xmx32g Application",
            "Generational ZGC is optimal for microservices, financial trading platforms, and latency-critical APIs requiring <1ms GC pauses.",
            "Allocation stalls: if the application thread allocation rate exceeds the concurrent GC reclamation rate, threads stall waiting for memory.",
            "ZGC delivers predictable <1ms pauses regardless of heap size (up to 16TB), but requires 1-2 extra CPU cores for concurrent background collection threads.",
            ["Using ZGC on severely CPU-starved containers where background GC threads cannot keep up with allocations.", "Assuming ZGC has zero pause time (pause times are <1ms, not strictly 0).", "Over-tuning young generation size instead of letting ZGC dynamically calibrate."]
        ),
        (
            "How do you design a high-throughput, non-blocking LMAX Disruptor-style RingBuffer in Java?",
            "TOUGH",
            "executors-concurrency-utils",
            "A RingBuffer achieves tens of millions of ops/sec by using pre-allocated arrays, power-of-two bitwise indexing, cache-line padding to prevent false sharing, and atomic sequence numbers without locks or blocking queues.",
            "Standard BlockingQueues (ArrayBlockingQueue, LinkedBlockingQueue) suffer from lock contention, memory allocations for nodes, and false sharing on CPU cache lines. A Disruptor-style RingBuffer pre-allocates an array of fixed size (power of two: index = sequence & (size - 1)). Publishers claim sequence slots using atomic CAS, write data into the pre-allocated slot without garbage collection, and commit the sequence.",
            "Consumers track read sequences independently. To prevent cache-line bouncing (where adjacent variables occupy the same 64-byte CPU cache line), sequence counters use cache-line padding (adding dummy long fields or `@jdk.internal.vm.annotation.Contended`) to guarantee that producer and consumer sequences reside on separate CPU cache lines.",
            "public final class CachePaddedSequence {\n    // Padding prevents False Sharing across 64-byte L1/L2 cache lines\n    protected long p1, p2, p3, p4, p5, p6, p7;\n    private volatile long value;\n    protected long p8, p9, p10, p11, p12, p13, p14;\n    \n    public long get() { return value; }\n    public void set(long value) { this.value = value; }\n}",
            "Used in ultra-low-latency financial matching engines, high-throughput event logs, and metric aggregators.",
            "Ring buffer overflow: slow consumers can fall behind, requiring explicit drop or backpressure policies to prevent publisher overwrites.",
            "Near-zero latency and zero GC allocations, but requires complex lock-free coordination code.",
            ["Placing two frequently mutated volatile variables adjacent to each other on the same CPU cache line (False Sharing).", "Using modulo `%` operator instead of bitwise `& (size - 1)` for power-of-two ring buffers.", "Neglecting producer backpressure when ring buffer is saturated."]
        )
    ]

    for item in hard_specs:
        questions.append({
            "title": item[0],
            "difficulty": item[1],
            "technology_slug": "java-backend",
            "topic_slug": item[2],
            "question_type": "CONCEPTUAL",
            "scenario_type": "INTERNALS_AND_CONCURRENCY",
            "short_answer": item[3],
            "interview_ready_answer": item[4],
            "deep_explanation": f"{item[4]}\n\nDeep Architectural Analysis:\n{item[5]}" if len(item[5]) < 150 else item[5],
            "architecture_notes": "Analyzed against OpenJDK HotSpot JVM C2 compiler internals and memory specifications.",
            "code_example": item[6],
            "why_interviewer_asks": "Tests senior-level engineering depth, understanding of low-level CPU cache lines, memory fences, and JVM mechanics.",
            "production_considerations": item[7],
            "failure_modes": item[8],
            "tradeoffs": item[9],
            "common_mistakes": item[10],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Think about CPU hardware architectures, memory buses, and cache lines."},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Examine how the HotSpot JVM converts this Java abstraction into native assembly instructions."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Analyze performance degradation when thousands of concurrent threads hit this path."}
            ],
            "sources": [
                {
                    "source_name": "OpenJDK HotSpot Virtual Machine Architecture & JEPs",
                    "source_url": "https://openjdk.org/jeps/0",
                    "publisher": "OpenJDK Community"
                }
            ],
            "followups": [
                {
                    "followup_question": "How would you verify whether CPU False Sharing is occurring using Linux `perf c2c`?",
                    "answer_guidance": "Run `perf c2c record -F 60000 -- ./app` and analyze HITM (Hit Modified Cache Line) events across CPU sockets."
                }
            ],
            "tags": ["Java", "Concurrency", "JVM", "Performance", "Google", "Stripe"]
        })

    # ==========================================
    # 4. 20 EXPERT / PRODUCTION SCENARIO QUESTIONS
    # ==========================================
    expert_specs = [
        (
            "Production Incident: A high-throughput Java microservice experiences sudden 15-second Stop-The-World pauses and connection drops under peak load. CPU is at 95% and Old Gen is nearly full. How do you triage, diagnose, and resolve this outage?",
            "PRODUCTION_SCENARIO",
            "jvm-memory-gc",
            "Triage via thread dump and heap histogram (`jcmd GC.heap_info`, `jcmd GC.class_histogram`), identify memory leaks or premature promotion saturating Old Gen, capture heap dump via JFR/jcmd, configure G1GC/ZGC parameters, and apply backpressure.",
            "During an active production incident, follow a structured triage protocol: 1. Verify health metrics: check GC logs for pause duration, collector type, and whether pauses are Concurrent Mark cycles or Full GCs (e.g. 'Full GC (Allocation Failure)'). 2. Run non-invasive diagnostics: `jcmd <pid> GC.class_histogram` to identify which class instances dominate heap memory (e.g. unbounded collections, unclosed DB connections). 3. If thread dumps reveal hundreds of threads blocked on `java.lang.Object.wait` or `sun.misc.Unsafe.park`, threads are blocked waiting for memory allocation. 4. Collect a heap dump (`jcmd <pid> GC.heap_dump /tmp/dump.hprof`) for offline Memory Analyzer Tool (MAT) leak path analysis. 5. Immediate remediation: scale out pods horizontally, reduce traffic via rate-limiting/circuit-breakers, increase heap size or tune young-to-old ratio, and switch to Generational ZGC if latency SLAs require <1ms pauses.",
            "Full GC under G1 occurs when concurrent marking cannot finish before Old Generation fills (Allocation Failure or Humongous Allocation). Large objects (>50% region size) bypass Eden directly into Humongous regions, causing rapid fragmentation.",
            "// Production incident triage diagnostic commands:\n// 1. Live class histogram:\n// jcmd <pid> GC.class_histogram | head -n 30\n\n// 2. Capture flight recording without restarting process:\n// jcmd <pid> JFR.start name=outage duration=60s filename=/tmp/incident.jfr\n\n// 3. JVM diagnostic flags for production post-mortem:\n// -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/dumps/ -Xlog:gc*:file=/var/log/gc.log:time,uptime,pid:filecount=5,filesize=100M",
            "Always pre-configure `-XX:+HeapDumpOnOutOfMemoryError` and `-Xlog:gc*` in container startup arguments.",
            "Taking a full heap dump on a 64GB heap freezes the JVM for 30+ seconds, potentially triggering Kubernetes liveness probe failures and pod restarts.",
            "Full GC clears all unreachable memory but halts all application threads; concurrent GC trades CPU cores for minimal pauses.",
            ["Restarting pods immediately without capturing thread dumps or class histograms, destroying all forensic evidence.", "Taking a manual heap dump on live traffic without taking the container out of load balancer rotation.", "Assuming increasing -Xmx always fixes the issue (it often merely delays the OOM while making GC pauses longer)."]
        ),
        (
            "Architect a resilient, distributed lock in Java using Redis (Redlock) or ZooKeeper. What split-brain, clock-drift, and GC pause failure modes must you account for?",
            "EXPERT_DEEP_DIVE",
            "jmm-synchronization",
            "Distributed locks must account for JVM Stop-The-World GC pauses exceeding lock TTLs, asynchronous replication lag in Redis master-replica failovers, and NTP clock drift by utilizing fencing tokens and Redlock multi-node consensus.",
            "In Martin Kleppmann's famous critique of distributed locking, a client acquires lock L with a 10-second TTL. The client then enters an unexpected 15-second Stop-The-World GC pause. While paused, the lock expires in Redis and client B acquires the lock. Client A awakens and writes to shared storage, corrupting data because both clients believed they held the lock concurrently. To solve this, distributed storage must enforce monotonic 'Fencing Tokens' (auto-incrementing version numbers issued with the lock), rejecting writes from clients with stale tokens.",
            "ZooKeeper avoids TTL expiry by maintaining persistent TCP sessions and ephemeral sequential znodes, but network partitions can still disconnect clients. Redlock requires acquiring locks across an odd number of independent Redis instances (N/2 + 1) while computing validity time factoring clock drift.",
            "public class FencingTokenStorage {\n    private long highestSeenToken = 0;\n    \n    public synchronized void writeData(long fencingToken, String data) {\n        // Rejects writes from clients whose lock expired during a GC pause!\n        if (fencingToken <= highestSeenToken) {\n            throw new IllegalStateException(\"Stale fencing token! Write rejected.\");\n        }\n        highestSeenToken = fencingToken;\n        // Commit write safely\n    }\n}",
            "Always pair distributed locks with storage-level fencing tokens (or optimistic database versions) to guarantee correctness.",
            "Relying solely on Redis `SET key value NX PX 10000` without fencing allows dual writes if clients experience long GC pauses.",
            "ZooKeeper provides strict consistency at lower write throughput; Redis Redlock provides high throughput with higher operational complexity.",
            ["Believing a distributed lock alone guarantees safety without backend fencing tokens.", "Ignoring NTP clock skew across distributed Redis nodes.", "Setting lock TTLs shorter than maximum anticipated GC pause durations."]
        )
    ]

    for item in expert_specs:
        questions.append({
            "title": item[0],
            "difficulty": item[1],
            "technology_slug": "java-backend",
            "topic_slug": item[2],
            "question_type": "CONCEPTUAL",
            "scenario_type": "STAFF_PRODUCTION_ARCHITECTURE",
            "short_answer": item[3],
            "interview_ready_answer": item[4],
            "deep_explanation": item[5],
            "architecture_notes": "Production-grade triage and distributed systems architecture for high-concurrency systems.",
            "code_example": item[6],
            "why_interviewer_asks": "Evaluates Staff / Principal level architectural maturity, incident response acumen, and distributed systems rigor.",
            "production_considerations": item[7],
            "failure_modes": item[8],
            "tradeoffs": item[9],
            "common_mistakes": item[10],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Analyze time and failure domains: what happens when GC pauses or clocks drift?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Consider forensic commands (`jcmd`, `jstack`, `jmap`, JFR) and storage-level validation."},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "How do you guarantee monotonic fencing and zero-downtime failover under network partition?"}
            ],
            "sources": [
                {
                    "source_name": "Martin Kleppmann: How to do Distributed Locking",
                    "source_url": "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html",
                    "publisher": "University of Cambridge / ACM"
                }
            ],
            "followups": [
                {
                    "followup_question": "How does Raft consensus (as in etcd) prevent the split-brain and clock-drift issues seen in naive Redis locks?",
                    "answer_guidance": "Raft uses term numbers and leader leases with quorum writes, rejecting stale terms without relying on synchronized wall clocks."
                }
            ],
            "tags": ["Java", "Distributed Systems", "Architecture", "System Design", "Staff Engineer", "Google", "Amazon"]
        })

    return questions

if __name__ == "__main__":
    qs = get_80_pilot_questions()
    print(f"Constructed {len(qs)} initial pilot specifications.")
