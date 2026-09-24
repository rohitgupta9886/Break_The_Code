"""
Curriculum Transformer for Java Backend & JVM Concurrency Track.
Transforms raw topic headings into high-caliber Java engineering interview questions,
structured answers, and syntax-valid Java concurrency / JVM code.
"""

def transform_java_topic(topic_title: str, level: str, sec_slug: str, sec_name: str) -> dict:
    t = topic_title.strip()
    question_title = format_java_question(t, level)
    short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes = generate_java_dna(t, level, sec_slug, sec_name, question_title)
    
    return {
        "title": question_title,
        "short_answer": short_ans,
        "interview_ready_answer": ready_ans,
        "deep_explanation": deep_exp,
        "code_example": code_ex,
        "architecture_notes": arch_flow,
        "why_interviewer_asks": why_ask,
        "interviewer_intent": f"Evaluates senior Java engineering depth, memory visibility, low-level bytecode semantics, lock-free concurrency, and JVM performance tuning at {level} depth.",
        "production_considerations": f"In production Java systems, ensure {t} is profiled with JFR, monitored for GC pause duration SLAs, and tested under sustained multi-threaded contention.",
        "failure_modes": fail_modes,
        "tradeoffs": tradeoffs,
        "common_mistakes": mistakes
    }

def format_java_question(topic: str, level: str) -> str:
    mappings = {
        "Java Memory Model (JMM) Basics": "How does the Java Memory Model (JMM) govern thread memory visibility, CPU caches, and instruction reordering?",
        "The volatile Keyword Role": "What guarantees does the volatile keyword provide in Java, and why does it prevent instruction reordering without providing atomicity?",
        "synchronized Method vs Block": "What is the internal bytecode difference between a synchronized method (ACC_SYNCHRONIZED) and a synchronized block (monitorenter/monitorexit)?",
        "Happens-Before Relationship": "What is the Happens-Before relationship in the Java Memory Model, and how does it establish memory visibility across concurrent threads?",
        "Thread Visibility Issues": "How do CPU core L1/L2 caches cause thread visibility issues in multi-threaded Java applications, and how does JMM resolve them?",
        "Race Condition Definition": "What constitutes a race condition in concurrent Java programs, and how do you differentiate check-then-act from read-modify-write races?",
        "Deadlock Conditions (Coffman)": "What are Coffman's four conditions for deadlock, and how do you prevent circular wait in high-concurrency Java services?",
        "AtomicInteger and CAS (Compare-And-Swap)": "How does AtomicInteger leverage hardware-level Compare-And-Swap (CAS) instructions to achieve non-blocking thread safety?",
        "Intrinsic Locks (Monitor Locks)": "How do intrinsic monitor locks in Java transition through biased, lightweight, and heavyweight states in the HotSpot JVM?",
        "Double-Checked Locking Pattern": "Why is the volatile keyword mandatory in the Double-Checked Locking singleton pattern to prevent partially constructed object escapes?",
        "Thread Local Storage (ThreadLocal)": "How does ThreadLocal achieve per-thread data isolation, and why can it cause silent memory leaks in pooled thread environments?",
        
        "ThreadPoolExecutor Core Components": "What are the core constructor parameters of ThreadPoolExecutor, and in what exact sequence does it allocate threads and queue tasks?",
        "CorePoolSize vs MaximumPoolSize": "Under what precise conditions does ThreadPoolExecutor scale threads from corePoolSize to maximumPoolSize?",
        "WorkQueue Types (ArrayBlockingQueue vs LinkedBlockingQueue)": "How do different BlockingQueue implementations (ArrayBlockingQueue, LinkedBlockingQueue, SynchronousQueue) impact thread pool throughput and backpressure?",
        "RejectedExecutionHandler Policies": "What are the four standard RejectedExecutionHandler policies in Java, and how do you implement a graceful caller-runs or metrics-logging policy?",
        "CompletableFuture Asynchronous Chaining": "How do CompletableFuture supplyAsync, thenApply, thenCompose, and thenCombine orchestrate non-blocking asynchronous pipelines?",
        "ForkJoinPool and Work Stealing": "How does ForkJoinPool's work-stealing algorithm minimize thread contention, and why is it preferred for divide-and-conquer workloads?",
        "Thread Pool Sizing Guidelines (CPU vs I/O)": "How do you mathematically size a Java thread pool based on CPU core count, target CPU utilization, and wait-to-service time ratios (W/S)?",
        
        "What are Virtual Threads (Project Loom)": "What are Virtual Threads in Java 21 (Project Loom), and how do they decouple application threads from underlying OS kernel threads?",
        "Platform Threads vs Virtual Threads": "How do Virtual Threads differ from traditional Platform Threads in terms of memory footprint, context switching overhead, and thread lifecycle?",
        "Carrier Threads Concept": "How does the JVM ForkJoinPool schedule Virtual Threads onto underlying OS Carrier Threads during blocking I/O operations?",
        "Carrier Thread Pinning via synchronized Blocks": "What is Carrier Thread Pinning in Java 21 Virtual Threads, why does it occur with synchronized blocks or native JNI methods, and how do you fix it?",
        "Replacing synchronized with ReentrantLock for Loom": "Why is replacing synchronized blocks with ReentrantLock recommended when migrating high-concurrency applications to Virtual Threads?",
        "Virtual Thread Pooling Anti-Pattern": "Why is pooling Virtual Threads considered an anti-pattern in Java 21, and how does the thread-per-task paradigm change resource management?",
        "Structured Concurrency Introduction": "How does Structured Concurrency (StructuredTaskScope) treat multiple concurrent tasks running in separate virtual threads as a single atomic unit of work?",
        "Scoped Values Overview": "What architectural problem do Scoped Values solve in Java 21 compared to ThreadLocal when handling immutable context across thousands of virtual threads?",
        
        "JVM Memory Structure (Heap, Stack, Metaspace)": "How is JVM memory partitioned between Heap, Stack frames, Metaspace, and Off-Heap native memory in modern 64-bit HotSpot JVMs?",
        "Eden, Survivor, and Tenured Spaces": "How do objects transition across Eden, Survivor (S0/S1), and Tenured generational heap spaces during minor GC cycles?",
        "Minor GC vs Major GC vs Full GC": "What triggers Minor GC, Major GC, and Full GC in Java, and what are their respective Stop-The-World (STW) pause characteristics?",
        "G1GC Region Architecture Overview": "How does the Garbage-First (G1) collector partition heap memory into dynamic regions, and how does it prioritize regions based on garbage density?",
        "ZGC Low-Latency Goal": "How does the Z Garbage Collector (ZGC) achieve sub-millisecond Stop-The-World pauses using colored pointers and load barriers regardless of heap size?",
        "Metaspace OutOfMemoryError Causes": "What causes java.lang.OutOfMemoryError: Metaspace, and how do dynamic class generation and classloader leaks trigger it?",
        "Analyzing Heap Dumps with Eclipse MAT": "How do you analyze a production JVM heap dump (.hprof) using Eclipse Memory Analyzer (MAT) to differentiate Shallow Heap from Retained Heap?"
    }
    
    if topic in mappings:
        return mappings[topic]
        
    clean = topic.replace(":", "").replace("?", "").strip()
    if clean.lower().startswith("what") or clean.lower().startswith("how") or clean.lower().startswith("why"):
        return clean + ("?" if not clean.endswith("?") else "")
        
    if level == "L1":
        return f"What is the role of {clean} in Java backend development, and how does it function inside the JVM?"
    else:
        return f"How do you optimize and debug {clean} in production Java systems under heavy concurrent load?"

from .text_utils import clean_concept_name

def generate_java_dna(topic: str, level: str, sec_slug: str, sec_name: str, question: str):
    t_clean = clean_concept_name(topic)
    
    short_ans = (
        f"In enterprise Java and JVM engineering ({sec_name}), {t_clean} governs how memory, thread concurrency, "
        f"and operating system resources are coordinated. It ensures thread-safe execution, prevents memory leaks, "
        f"and allows backend services to maintain predictable P99 latencies under high transaction volume."
    )
    
    ready_ans = (
        f"When answering **{t_clean}** in a senior Java engineering interview, articulate your answer through three structured phases:\n\n"
        f"1. **Core JVM & Concurrency Specification**: {t_clean} is defined by strict HotSpot execution semantics. "
        f"Whether managing hardware memory visibility via CPU cache lines (MESI protocol), orchestrating thread transitions, "
        f"or enforcing generational garbage collection boundaries, the JVM ensures safe publication and predictable memory layout.\n\n"
        f"2. **Internal Runtime Implementation**: Explain what occurs at the bytecode and OS kernel layer. "
        f"For example, monitor locks utilize object headers (Mark Word) transitioning from biased to lightweight CAS spinning, "
        f"and eventually inflating to OS mutexes. In thread execution, thread pools decouple runnable tasks from operating system schedulers.\n\n"
        f"3. **Production Pitfalls & Diagnostics**: In high-load microservices, misconfiguration causes carrier thread pinning, "
        f"thread pool exhaustion, or GC thrashing. Senior engineers leverage Java Flight Recorder (JFR), `jcmd`, and thread dumps "
        f"to inspect active carrier threads, monitor lock contention, and verify latency budgets."
    )
    
    deep_exp = (
        f"### Low-Level Architectural Deep Dive: {t_clean}\n\n"
        f"At the hardware architecture boundary, modern multi-socket server processors employ independent L1/L2 data caches per core "
        f"and a shared L3 cache. When multiple threads mutate shared memory without synchronization, CPU write buffers and cache incoherence "
        f"cause stale reads and out-of-order execution.\n\n"
        f"The Java Memory Model addresses this by defining **Happens-Before** rules. When `volatile` variables or monitor locks are accessed, "
        f"the JIT compiler emits hardware memory barriers (`LoadLoad`, `LoadStore`, `StoreStore`, `StoreLoad` / `mfence` on x86). "
        f"This forces dirty cache lines to flush to main memory and invalidates stale entries across peer CPU cores via bus snooping.\n\n"
        f"With the advent of Java 21 Virtual Threads (Loom), execution frames are allocated on the Java heap rather than the operating system C-stack. "
        f"When a virtual thread executes a blocking socket or file operation, the JVM unmounts its stack frame from the carrier thread, "
        f"parking it in heap memory and freeing the carrier OS thread to execute other virtual tasks."
    )
    
    # Real Java concurrency code example
    code_ex = (
        f"package com.breakthecode.concurrency;\n\n"
        f"import java.util.concurrent.*;\n"
        f"import java.util.concurrent.atomic.AtomicInteger;\n"
        f"import java.util.concurrent.locks.ReentrantLock;\n\n"
        f"/**\n"
        f" * Production demonstration of {t_clean}\n"
        f" * Showcases thread safety, non-blocking state transitions, and clean resource cleanup.\n"
        f" */\n"
        f"public class Resilient{sec_slug.replace('-', ' ').title().replace(' ', '')}Service {{\n"
        f"    private final ReentrantLock lock = new ReentrantLock();\n"
        f"    private final AtomicInteger activeOperations = new AtomicInteger(0);\n"
        f"    private volatile boolean isRunning = true;\n\n"
        f"    public CompletableFuture<String> executeTask(String payload) {{\n"
        f"        return CompletableFuture.supplyAsync(() -> {{\n"
        f"            if (!isRunning) {{\n"
        f"                throw new IllegalStateException(\"Service shutting down\");\n"
        f"            }}\n"
        f"            activeOperations.incrementAndGet();\n"
        f"            try {{\n"
        f"                // Thread-safe critical section with timed lock\n"
        f"                if (lock.tryLock(500, TimeUnit.MILLISECONDS)) {{\n"
        f"                    try {{\n"
        f"                        // Simulate business logic for: {t_clean}\n"
        f"                        return \"Processed: \" + payload + \" [Thread: \" + Thread.currentThread().getName() + \"]\";\n"
        f"                    }} finally {{\n"
        f"                        lock.unlock();\n"
        f"                    }}\n"
        f"                }} else {{\n"
        f"                    throw new TimeoutException(\"Unable to acquire lock within 500ms budget\");\n"
        f"                }}\n"
        f"            }} catch (InterruptedException | TimeoutException e) {{\n"
        f"                Thread.currentThread().interrupt();\n"
        f"                throw new CompletionException(e);\n"
        f"            }} finally {{\n"
        f"                activeOperations.decrementAndGet();\n"
        f"            }}\n"
        f"        }});\n"
        f"    }}\n\n"
        f"    public void shutdown() {{\n"
        f"        this.isRunning = false;\n"
        f"    }}\n"
        f"}}"
    )
    
    arch_flow = (
        f"Incoming Client HTTP Request\n"
        f"  │\n"
        f"  ▼\n"
        f"[Virtual Thread / Tomcat Thread Pool]\n"
        f"  │\n"
        f"  ▼\n"
        f"[{t_clean} Concurrency Boundary] ──(Acquire Lock / CAS Primitive)──► [CPU L1/L2 Hardware Cache]\n"
        f"  │                                                                           │ (Memory Barrier)\n"
        f"  ▼                                                                           ▼\n"
        f"[Non-Blocking I/O (NIO Channel)] ◄───(Unmounts from Carrier Thread)─── [Main RAM / Eden Space]\n"
        f"  │\n"
        f"  ▼\n"
        f"[Async CompletableFuture Pipeline] ──► [HTTP 200 Response with OpenTelemetry Span]"
    )
    
    why_ask = f"Interviewers assess whether the candidate understands memory visibility, non-blocking concurrency, thread pool saturation hazards, and JVM garbage collector tuning."
    fail_modes = f"Carrier thread pinning stalling the virtual thread scheduler, ThreadLocal memory leaks in pooled threads, and deadlocks caused by uncoordinated lock acquisition order."
    tradeoffs = f"Balancing coarse-grained locking simplicity against high-contention throughput, and heap allocation overhead against GC pause latency budgets."
    mistakes = [
        f"Using synchronized inside virtual threads on I/O operations, which pins the underlying carrier OS thread",
        f"Relying on ThreadLocal without calling .remove() in a web request filter, leaking objects across requests",
        f"Using unbounded queues (LinkedBlockingQueue) in ThreadPoolExecutor, leading to OutOfMemoryError under traffic spikes"
    ]
    
    return short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes
