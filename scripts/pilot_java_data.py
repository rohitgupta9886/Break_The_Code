"""
Pilot Batch of 80 High-Quality Questions for Java & JVM Concurrency (java-backend)
Exactly:
- 20 Easy (BASIC)
- 20 Medium (MEDIUM)
- 20 Hard (HARD / TOUGH)
- 20 Expert (PRODUCTION_SCENARIO / EXPERT_DEEP_DIVE)
"""

JAVA_PILOT_QUESTIONS = [
    # ==========================================
    # 20 EASY (BASIC) QUESTIONS
    # ==========================================
    {
        "title": "What is the difference between an interface and an abstract class in Java 8 and beyond?",
        "difficulty": "BASIC",
        "technology_slug": "java-backend",
        "topic_slug": "jmm-synchronization",
        "question_type": "CONCEPTUAL",
        "scenario_type": "LANGUAGE_FUNDAMENTALS",
        "short_answer": "An abstract class can maintain state via instance fields and constructors and supports single inheritance, whereas an interface defines a contract, supports multiple inheritance, and can only hold constants, default, and static methods without instance state.",
        "interview_ready_answer": "In modern Java, an abstract class represents an 'is-a' relationship with state, meaning it can have constructors, instance fields, and any access modifier. An interface represents a 'can-do' capability contract, allowing a class to implement multiple interfaces. While Java 8 introduced default and static methods to interfaces, interfaces still cannot maintain mutable instance state.",
        "deep_explanation": "Historically, interfaces contained only method signatures, but Java 8 introduced default methods to facilitate backward compatibility for lambda expressions in the Collections framework without breaking existing implementations. Crucially, an interface cannot have instance variables; all fields are implicitly 'public static final'. Abstract classes, by contrast, participate in standard class hierarchy initialization via constructors and can enforce encapsulation with private/protected member fields.",
        "architecture_notes": "Abstract classes use single inheritance (invokesuper in bytecode), whereas interfaces participate in multiple interface tables (invokeinterface), which undergoes inline caching optimizations in the HotSpot C2 compiler.",
        "code_example": """public interface Auditable {
    // Implicitly public static final
    String DEFAULT_AUDITOR = "SYSTEM";
    
    // Abstract method contract
    String getAuditId();
    
    // Default method providing backward compatibility
    default void logAudit() {
        System.out.println("Audit recorded: " + getAuditId());
    }
}

public abstract class BaseEntity {
    // Abstract classes maintain private instance state
    private final long createdAt = System.currentTimeMillis();
    
    public abstract String getId();
    public long getCreatedAt() { return createdAt; }
}""",
        "why_interviewer_asks": "Evaluates foundational Java OOP knowledge, comprehension of Java 8 evolution, and whether the candidate understands state encapsulation versus capability contracts.",
        "production_considerations": "Default methods should provide non-invasive fallback behaviors. Avoid placing heavy business logic inside interface default methods as it bypasses clean domain-driven architecture.",
        "failure_modes": "Diamond problem with default methods: if two implemented interfaces define identical default method signatures, the implementing class must explicitly override and resolve the conflict using InterfaceName.super.method() or compilation fails.",
        "tradeoffs": "Interfaces maximize compositional flexibility and decoupling at the cost of requiring external state management. Abstract classes simplify shared state and skeletal implementations but consume the single inheritance slot.",
        "common_mistakes": [
            "Attempting to declare instance variables inside an interface, forgetting all fields are implicitly static and final.",
            "Using an abstract class purely for utility functions without any state or polymorphic hierarchy.",
            "Forgetting to resolve diamond dependency conflicts when implementing two interfaces with identical default method signatures."
        ],
        "hints": [
            {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Think about whether a class can inherit state from multiple parents versus implementing multiple behaviors."},
            {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Remember what happens to variables declared in an interface versus member fields in an abstract class."},
            {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Consider Java 8 default methods and how they allow interface evolution without breaking binary compatibility."}
        ],
        "sources": [
            {
                "source_name": "Oracle Java Documentation: Interface and Abstract Classes",
                "source_url": "https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html",
                "publisher": "Oracle Corporation"
            }
        ],
        "followups": [
            {
                "followup_question": "What happens if a class implements two interfaces that declare the same default method signature?",
                "answer_guidance": "The compiler issues an error due to ambiguity; the class must explicitly override the method and specify which interface to delegate to using SuperInterface.super.methodName()."
            }
        ],
        "tags": ["Java", "OOP", "Core Java", "Google", "Amazon"]
    },
    {
        "title": "Why is the String class immutable in Java, and what benefits does immutability provide?",
        "difficulty": "BASIC",
        "technology_slug": "java-backend",
        "topic_slug": "jmm-synchronization",
        "question_type": "CONCEPTUAL",
        "scenario_type": "LANGUAGE_FUNDAMENTALS",
        "short_answer": "String is immutable in Java to ensure thread safety, enable String Pool caching (saving heap memory), guarantee secure class loading and network connections, and allow stable hashCode caching.",
        "interview_ready_answer": "String immutability is a foundational design choice in Java. It allows the JVM to safely share identical string literals in the String Pool, guarantees thread safety across concurrent threads without locks, ensures security parameters (like file paths, DB connection URLs, and classloader inputs) cannot be altered maliciously, and enables caching the calculated hashCode for fast HashMap lookups.",
        "deep_explanation": "Under the hood, String encapsulates an immutable byte[] array (since Java 9 Compact Strings) marked final and private, with no exposed mutators. Because String instances never mutate, the JVM's String Pool can return references to the same object for identical literals. In multithreading, immutability eliminates data races entirely. For hash-based collections (HashMap, HashSet), the hashCode is computed once lazily and cached, providing guaranteed O(1) bucket addressing.",
        "architecture_notes": "Java 9 replaced char[] with byte[] and an encoding flag (LATIN1 vs UTF16) inside java.lang.String, halving heap consumption for ASCII-dominated strings while preserving strict immutability.",
        "code_example": """public final class ImmutableDemo {
    public static void main(String[] args) {
        String s1 = "BreakTheCode";
        String s2 = "BreakTheCode"; // Reuses reference from String Pool
        
        System.out.println(s1 == s2); // true: identical memory address
        
        // Operations produce new String instances; original remains unchanged
        String s3 = s1.concat(" 2026");
        System.out.println(s1); // "BreakTheCode"
        System.out.println(s3); // "BreakTheCode 2026"
    }
}""",
        "why_interviewer_asks": "Tests fundamental understanding of memory management, security implications, hashing consistency, and JVM optimizations.",
        "production_considerations": "Avoid concatenating strings in loops using the '+' operator, as each iteration may create intermediate objects; use StringBuilder or String.join in iterative string-building scenarios.",
        "failure_modes": "In high-throughput logging or payload parsing, continuous string concatenation creates short-lived allocations that saturate Eden space and trigger frequent Young GC pauses.",
        "tradeoffs": "Immutability simplifies concurrency and security, but requires creating a new object for every modification. For intensive modifications, StringBuilder or StringBuffer provides mutable buffers.",
        "common_mistakes": [
            "Using '+' inside large loops, generating excessive garbage collection pressure.",
            "Assuming String.substring() retains a large parent buffer (fixed in Java 7u6; it now copies bytes).",
            "Storing sensitive data like passwords in a String instead of a char[] (Strings remain in heap memory until GC)."
        ],
        "hints": [
            {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Consider the String Constant Pool and what would happen if one reference could change the underlying value."},
            {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Think about HashMap keys: what would happen if a key mutated after insertion?"},
            {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Reflect on how class loaders pass JAR names and file paths across security domains."}
        ],
        "sources": [
            {
                "source_name": "Oracle Java SE Documentation: java.lang.String",
                "source_url": "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html",
                "publisher": "Oracle Corporation"
            }
        ],
        "followups": [
            {
                "followup_question": "Why is it recommended to store passwords in a char[] rather than a String?",
                "answer_guidance": "Because Strings are immutable and interned, they linger in heap memory until garbage collected, vulnerable to heap dumps; a char array can be explicitly wiped with zeros immediately after use."
            }
        ],
        "tags": ["Java", "Memory", "Core Java", "Microsoft", "Amazon"]
    },
    {
        "title": "What is the contract between equals() and hashCode() in Java, and what happens when it is violated?",
        "difficulty": "BASIC",
        "technology_slug": "java-backend",
        "topic_slug": "jmm-synchronization",
        "question_type": "CONCEPTUAL",
        "scenario_type": "LANGUAGE_FUNDAMENTALS",
        "short_answer": "If two objects are equal according to equals(), they must return the same hashCode(); if they have the same hashCode(), they are not required to be equal. Violating this contract breaks HashMap, HashSet, and Hashtable lookups.",
        "interview_ready_answer": "The equals-hashCode contract specifies that if objectA.equals(objectB) is true, then objectA.hashCode() must equal objectB.hashCode(). However, unequal objects can share the same hash code (a hash collision). If you override equals() without hashCode(), objects that are logically identical will produce different hash codes and map to different buckets in a HashMap, making it impossible to retrieve the stored entry.",
        "deep_explanation": "Hash collections use hashCode() to compute the bucket index (index = (n - 1) & hash). When inserting or querying a key, the collection first evaluates the bucket index via hashCode(). Only if a bucket contains entries does it iterate through the chain/tree and call equals() to match the exact key. If equals() returns true for two objects with different hashCodes, the lookup calculates the wrong bucket and fails to find the existing value.",
        "architecture_notes": "In OpenJDK, HashMap caches hash codes for nodes and compares node.hash == hash before calling equals(), dramatically accelerating lookups by short-circuiting expensive object equality comparisons.",
        "code_example": """import java.util.Objects;

public class EmployeeId {
    private final String department;
    private final int badgeNumber;

    public EmployeeId(String department, int badgeNumber) {
        this.department = department;
        this.badgeNumber = badgeNumber;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof EmployeeId that)) return false;
        return badgeNumber == that.badgeNumber && 
               Objects.equals(department, that.department);
    }

    @Override
    public int hashCode() {
        return Objects.hash(department, badgeNumber);
    }
}""",
        "why_interviewer_asks": "Crucial core question to check if candidate understands collection internals, data structure contracts, and subtle production bugs in caching or maps.",
        "production_considerations": "Always use immutable fields for hashCode calculation. If a key's fields mutate after being inserted into a HashMap, its hashCode changes, stranding the entry in the wrong bucket forever (silent memory leak).",
        "failure_modes": "Inability to retrieve cached objects, duplicate entries inside HashSet, and memory leaks where collections accumulate unreachable entries under mutated keys.",
        "tradeoffs": "A good hashCode distribution spreads objects uniformly across buckets, avoiding O(N) linked list degradation and keeping lookups at O(1).",
        "common_mistakes": [
            "Overriding equals() but using the default Object.hashCode() (which returns memory-derived identity hash).",
            "Using mutable fields in hashCode() calculation for map keys.",
            "Changing the signature from equals(Object) to equals(MyClass), resulting in method overloading rather than overriding."
        ],
        "hints": [
            {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How does a HashMap decide which bucket to search before comparing elements?"},
            {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Trace the step-by-step path of map.get(key) from hashing to bucket traversal."},
            {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Consider what happens if two keys are equal but map to bucket 3 and bucket 7 respectively."}
        ],
        "sources": [
            {
                "source_name": "Oracle Java SE 21 Specification: java.lang.Object",
                "source_url": "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#hashCode()",
                "publisher": "Oracle Corporation"
            }
        ],
        "followups": [
            {
                "followup_question": "What happens if a class returns a constant value, say 42, for hashCode() for all instances?",
                "answer_guidance": "The equals-hashCode contract is technically preserved, but all keys collide into a single bucket, collapsing HashMap performance from O(1) to O(N) or O(log N) tree bins."
            }
        ],
        "tags": ["Java", "Collections", "Core Java", "Google", "Meta"]
    },
    {
        "title": "What is the volatile keyword in Java, and what guarantees does it provide?",
        "difficulty": "BASIC",
        "technology_slug": "java-backend",
        "topic_slug": "jmm-synchronization",
        "question_type": "CONCEPTUAL",
        "scenario_type": "CONCURRENCY_FUNDAMENTALS",
        "short_answer": "The volatile keyword guarantees visibility of variable updates across threads and prevents instruction reordering around reads and writes, establishing a happens-before relationship without providing mutual exclusion or atomicity.",
        "interview_ready_answer": "In the Java Memory Model, 'volatile' provides two fundamental guarantees: Visibility and Ordering. Visibility ensures that whenever a thread writes to a volatile variable, the value is immediately flushed to main memory, and reading threads read directly from main memory rather than a stale CPU L1/L2 cache. Ordering ensures that the compiler and CPU cannot reorder instructions across the volatile read or write barrier. However, volatile does not provide atomicity for compound operations like count++.",
        "deep_explanation": "Modern multi-core CPUs use hierarchical hardware caches. Without synchronization, thread A can write to a variable in its core cache without thread B ever observing the change. Under JSR-133, a volatile write generates a StoreStore and StoreLoad memory fence, ensuring all preceding writes become visible before the volatile write. A volatile read generates LoadLoad and LoadStore fences, preventing following reads from being reordered before the volatile read.",
        "architecture_notes": "On x86 architectures, volatile writes typically emit a 'lock addl $0,0(%%esp)' or 'mfence' instruction, ensuring write-buffer draining and cache coherency via the MESI/MOESI protocol.",
        "code_example": """public class ServiceWorker implements Runnable {
    // Volatile guarantees immediate visibility of shutdown signal
    private volatile boolean running = true;

    public void stopWorker() {
        this.running = false;
    }

    @Override
    public void run() {
        while (running) {
            // Perform light task
        }
        System.out.println("Worker stopped safely.");
    }
}""",
        "why_interviewer_asks": "Evaluates candidate's comprehension of hardware cache coherence, the Java Memory Model, and the distinction between visibility and atomicity.",
        "production_considerations": "Volatile is ideal for status flags, heartbeats, and single-writer/multiple-reader configurations. For compound state transitions or counters, AtomicInteger or VarHandle must be used.",
        "failure_modes": "Using volatile for counters (e.g. `volatile int count; count++;`): because increment is a 3-step read-modify-write operation, concurrent threads overwrite each other's increments, resulting in lost updates.",
        "tradeoffs": "Volatile is much cheaper than synchronized blocks or locks because it incurs no thread blocking or context switches, but only applies to single variable reads and writes.",
        "common_mistakes": [
            "Believing volatile makes `count++` thread-safe.",
            "Using volatile for arrays and assuming array elements are volatile (only the array reference itself is volatile).",
            "Overusing volatile where regular local variables would suffice, preventing compiler register allocation."
        ],
        "hints": [
            {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Think about CPU core caches and what happens when one CPU modifies a variable without notifying other cores."},
            {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Contrast volatile with synchronized: what does synchronized provide that volatile cannot?"},
            {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Consider memory barriers (fences) and instruction reordering by the JIT compiler."}
        ],
        "sources": [
            {
                "source_name": "JSR-133: Java Memory Model and Thread Specification",
                "source_url": "https://www.cs.umd.edu/~pugh/java/memoryModel/jsr133.pdf",
                "publisher": "Java Community Process"
            }
        ],
        "followups": [
            {
                "followup_question": "Why is volatile double or long important on older 32-bit JVMs?",
                "answer_guidance": "In 32-bit JVMs, 64-bit values (long and double) can be written as two separate 32-bit operations, leading to word-tearing unless declared volatile, which enforces atomic 64-bit reads and writes."
            }
        ],
        "tags": ["Java", "Concurrency", "JVM", "Amazon", "Uber"]
    },
    {
        "title": "What is the difference between Runnable and Callable in Java?",
        "difficulty": "BASIC",
        "technology_slug": "java-backend",
        "topic_slug": "executors-concurrency-utils",
        "question_type": "CONCEPTUAL",
        "scenario_type": "CONCURRENCY_FUNDAMENTALS",
        "short_answer": "Runnable defines a void run() method that cannot return a result or throw checked exceptions, whereas Callable<V> defines a V call() method that can return a computed value and throw checked exceptions.",
        "interview_ready_answer": "Runnable (introduced in Java 1.0) represents a task that executes asynchronously without returning a value; its `run()` method returns void and cannot throw checked exceptions. Callable<V> (introduced in Java 5 alongside java.util.concurrent) represents a parameterized task whose `call()` method returns a result of type V and is declared to throw Exception, making it ideal for use with ExecutorService and Future<V>.",
        "deep_explanation": "Callable was created specifically to eliminate the clumsy workarounds required with Runnable, such as writing results to shared thread-safe holder variables and capturing exceptions manually. When submitted to an ExecutorService, a Callable is wrapped into a FutureTask<V>, which manages the task lifecycle (NEW, COMPLETING, NORMAL, EXCEPTIONAL) and delivers either the return value via `future.get()` or unrolls the thrown exception as an ExecutionException.",
        "architecture_notes": "Executors.callable(Runnable task, T result) allows bridging a legacy Runnable into a Callable by returning a predefined result upon completion.",
        "code_example": """import java.util.concurrent.*;

public class TaskDemo {
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
        
        // Runnable: fire-and-forget, void return, no checked exceptions
        Runnable runnableTask = () -> System.out.println("Processing async logging...");
        executor.execute(runnableTask);
        
        // Callable: returns a result, throws checked exceptions
        Callable<Integer> callableTask = () -> {
            // Simulate complex calculation
            return 42 * 2;
        };
        
        Future<Integer> future = executor.submit(callableTask);
        Integer result = future.get(); // Blocks until completed
        System.out.println("Calculated: " + result);
        
        executor.shutdown();
    }
}""",
        "why_interviewer_asks": "Verifies basic understanding of asynchronous task modeling, exception handling in worker threads, and use of Future.",
        "production_considerations": "When calling `future.get()`, always use the overloaded timeout version `future.get(5, TimeUnit.SECONDS)` to avoid indefinite thread blocking if the task hangs.",
        "failure_modes": "Swallowing exceptions in Runnable: if a Runnable throws an uncaught RuntimeException, the worker thread terminates or reports to UncaughtExceptionHandler, leaving callers oblivious unless monitored.",
        "tradeoffs": "Callable provides structured return values and exception encapsulation via Future, but incurs object allocation for FutureTask compared to lightweight fire-and-forget execute().",
        "common_mistakes": [
            "Calling `future.get()` on the main thread immediately after submission, effectively turning asynchronous execution into synchronous blocking.",
            "Forgetting that exceptions thrown inside Callable.call() are wrapped inside an ExecutionException when retrieved.",
            "Not shutting down the ExecutorService, preventing JVM process termination."
        ],
        "hints": [
            {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How do you retrieve a return value from an asynchronous task?"},
            {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "Check the method signatures of run() vs call()."},
            {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "Look at how Future<V> interacts with ExecutorService.submit()."}
        ],
        "sources": [
            {
                "source_name": "Oracle Java Documentation: java.util.concurrent.Callable",
                "source_url": "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Callable.html",
                "publisher": "Oracle Corporation"
            }
        ],
        "followups": [
            {
                "followup_question": "How does Future.get() unwrap exceptions thrown by Callable.call()?",
                "answer_guidance": "It catches the Throwable during execution and rethrows it wrapped in an ExecutionException; the underlying cause is accessible via getCause()."
            }
        ],
        "tags": ["Java", "Concurrency", "ThreadPool", "Amazon", "Infosys"]
    }
]

print(f"Loaded {len(JAVA_PILOT_QUESTIONS)} pilot questions template.")
