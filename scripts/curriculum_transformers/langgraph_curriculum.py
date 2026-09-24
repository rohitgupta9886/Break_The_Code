"""
Curriculum Transformer for LangGraph & Agentic AI Track.
Provides realistic, production-grade interview questions, comprehensive multi-tier answers,
detailed architectural deep dives, and executable LangGraph Python code.
"""

def transform_langgraph_topic(topic_title: str, level: str, sec_slug: str, sec_name: str) -> dict:
    t = topic_title.strip()
    
    # 1. Convert Heading into Natural Interview Question
    question_title = format_langgraph_question(t, level)
    
    # 2. Generate Detailed Answers, Code, and Architectural DNA
    short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes = generate_langgraph_dna(t, level, sec_slug, sec_name, question_title)
    
    return {
        "title": question_title,
        "short_answer": short_ans,
        "interview_ready_answer": ready_ans,
        "deep_explanation": deep_exp,
        "code_example": code_ex,
        "architecture_notes": arch_flow,
        "why_interviewer_asks": why_ask,
        "interviewer_intent": f"Evaluates production-readiness in LangGraph state machines, resilience patterns, and failure isolation at {level} depth.",
        "production_considerations": f"In production deployments, ensure {t} has bounded state serialization limits, active telemetry (OpenTelemetry), and configured checkpointer retries.",
        "failure_modes": fail_modes,
        "tradeoffs": tradeoffs,
        "common_mistakes": mistakes
    }

def format_langgraph_question(topic: str, level: str) -> str:
    # Common custom mappings
    mappings = {
        "StateGraph Core Mechanics": "What is a StateGraph in LangGraph, and how does it pass and reconcile state across nodes?",
        "Explicit State Reducers": "Why are explicit state reducers (such as operator.add) required in LangGraph, and what happens when list fields lack reducers?",
        "START and END Virtual Nodes": "What is the purpose of the virtual START and END nodes in a LangGraph StateGraph, and how do they manage lifecycle boundaries?",
        "Conditional Edge Routers": "How do conditional edges work in LangGraph, and how do routing functions direct dynamic state transitions?",
        "invoke vs stream API": "What are the key architectural differences between graph.invoke() and graph.stream() in LangGraph, and when should each be used?",
        "compile Graph Validation": "How does StateGraph.compile() validate the topological integrity of a workflow before execution?",
        "RunnableConfig Parameters": "How do you pass and access runtime configuration parameters (like configurable and thread_id) in LangGraph nodes?",
        "Prebuilt ToolNode": "What is the role of ToolNode in LangGraph prebuilt components, and how does it handle parallel tool invocation?",
        "Recursion Limit Enforcement": "How does LangGraph enforce recursion limits to prevent runaway loops in cyclic agent workflows?",
        "Subgraphs Hierarchy": "What is a Subgraph in LangGraph, and how do you encapsulate private subgraph states within a parent orchestrator?",
        "Graph Visual Inspection": "How do you programmatically inspect and visualize a compiled StateGraph using Mermaid or ASCII representations?",
        "State Overwrite Semantics": "What are the state overwrite semantics in LangGraph when multiple concurrent nodes write to unannotated keys?",
        "Async Node Execution": "How does LangGraph natively support asynchronous node functions, and how do you prevent blocking the event loop?",
        "MessagesState Utility": "What is MessagesState in LangGraph, and what boilerplate does it eliminate for conversational agents?",
        "Initial State Ingestion": "How do you properly ingest initial inputs into a compiled LangGraph, and how are missing schema keys handled?",
        "Command Object Routing": "What is the Command object in LangGraph, and how does it combine state updates with dynamic routing in a single return?",
        "Node Unit Testing": "How do you unit test an individual LangGraph node function in isolation without compiling the full graph?",
        "Modern START vs Legacy Entrypoint": "How does modern LangGraph syntax with START differ from legacy set_entry_point(), and why was it updated?",
        "Node Exception Isolation": "How should exceptions be caught and handled inside LangGraph nodes to allow resilient fallback workflows?",
        "Deterministic vs Conditional Edges": "What is the distinction between deterministic edges and conditional edges in StateGraph control flow?",
        
        # L2 topics
        "Dynamic Fan-Out with Send": "How do you implement dynamic fan-out and map-reduce processing in LangGraph using the Send API?",
        "Concurrent State Reconciliation": "How does LangGraph coordinate state reconciliation when parallel nodes execute concurrently across branches?",
        "Node-Level RetryPolicy": "How do you configure automatic retry policies with exponential backoff on individual LangGraph nodes?",
        "Message Window Trimming": "How do you implement message window trimming in LangGraph to prevent context window overflow in long-running conversations?",
        "Self-Correction Feedback Loop": "How do you architect a self-correction feedback loop in LangGraph to validate and fix LLM outputs?",
        "Private Subgraph State Isolation": "How do you isolate private subgraph state schemas from the top-level parent graph in LangGraph?",
        "Multi-Provider Fallback Routing": "How can you implement multi-provider LLM fallback routing in LangGraph when primary model APIs experience outages?",
        "Stream Modes Updates vs Values": "What is the difference between stream_mode='values' and stream_mode='updates' in LangGraph streaming?",
        "State Schema Zero-Downtime Migration": "How do you execute zero-downtime schema migrations for active checkpointed threads in production LangGraph systems?",
        "Token Budget Tracking": "How do you track cumulative token usage and enforce budget limits across nodes in a LangGraph workflow?",
        "Idempotency in Node Side Effects": "How do you guarantee idempotency in LangGraph node side effects during crash recovery replays?",
        "OpenTelemetry Tracing per Node": "How do you instrument LangGraph nodes with OpenTelemetry tracing to track latency and token metrics?",
        "Priority Preemption in Agent Queues": "How do you implement priority task preemption within an enterprise LangGraph execution queue?",
        "Pydantic Output Self-Repair": "How do you implement self-repair loops for Pydantic schema validation failures in LangGraph nodes?",
        "Semantic Response Caching": "How do you implement semantic caching for expensive LLM nodes in LangGraph workflows?",
        "Concurrent Graph Thread Isolation": "How does LangGraph achieve thread isolation when serving thousands of concurrent users with a single compiled graph?",
        "External Tool Timeouts": "How do you implement strict timeout handling and circuit breaking for external tools in LangGraph?",
        "Dynamic Contextual Prompting": "How do you dynamically assemble system prompts in LangGraph nodes based on accumulated state context?",
        "Human-Gated Sensitive Operations": "How do you configure human-in-the-loop approval gates before executing high-risk nodes in LangGraph?",
        "State Time-Travel and Forking": "How do you perform state time-travel and execution forking using LangGraph checkpointers in production?"
    }
    
    if topic in mappings:
        return mappings[topic]
        
    # Pattern-based formulation
    clean = topic.replace(":", "").replace("?", "").strip()
    if clean.lower().startswith("what") or clean.lower().startswith("how") or clean.lower().startswith("why"):
        return clean + ("?" if not clean.endswith("?") else "")
    
    if level == "L1":
        return f"What is the role of {clean} in LangGraph, and how does it operate within an agentic workflow?"
    else:
        return f"How do you implement and optimize {clean} in a production LangGraph system, and what failure modes must you mitigate?"

from .text_utils import clean_concept_name

def generate_langgraph_dna(topic: str, level: str, sec_slug: str, sec_name: str, question: str):
    t_clean = clean_concept_name(topic)
    
    short_ans = (
        f"In LangGraph ({sec_name}), {t_clean} governs how execution state is isolated, mutated, and transitioned. "
        f"It establishes deterministic boundaries across nodes and edges, preventing uncoordinated state clobbering "
        f"and enabling seamless checkpointing and failure recovery in production agent systems."
    )
    
    ready_ans = (
        f"When discussing **{t_clean}** in a technical interview, focus on three primary dimensions:\n\n"
        f"1. **Core Operating Mechanism**: In LangGraph, {t_clean} acts as a foundational building block for stateful orchestration. "
        f"Nodes represent autonomous computational steps that take the current state schema and return partial state updates, "
        f"while edges determine the dynamic routing path.\n\n"
        f"2. **State Lifecycle & Coordination**: Unlike traditional linear chains, LangGraph uses an iterative state transition loop. "
        f"When {t_clean} executes, it interacts with state reducers and checkpointers to guarantee that mutations are atomic. "
        f"This prevents race conditions when branches execute concurrently and ensures that if a step fails, the workflow can resume.\n\n"
        f"3. **Production Best Practices**: In production, engineers must guard against unbounded context growth, configure explicit timeouts, "
        f"and implement structured error-handling fallbacks rather than letting exceptions crash the execution thread."
    )
    
    deep_exp = (
        f"### Deep Architectural Mechanics: {t_clean}\n\n"
        f"Under the hood, LangGraph compiles a StateGraph into an immutable `Pregel` execution loop. "
        f"Each step in the execution progresses through distinct phases:\n"
        f"- **Planning Phase**: Determines which nodes are active based on incoming edges from the START node or previous step outputs.\n"
        f"- **Execution Phase**: Active node callables are invoked concurrently (utilizing asyncio for `async def` nodes).\n"
        f"- **State Reconciliation**: Partial update dictionaries returned by nodes are applied via their defined reducer functions "
        f"(e.g., `operator.add` or `add_messages`). If multiple nodes update the same unannotated key, last-write-wins applies.\n"
        f"- **Checkpoint Persistence**: If a checkpointer (such as `PostgresSaver` or `MemorySaver`) is attached, the entire state snapshot "
        f"is written to the backing store with metadata including `thread_id`, `checkpoint_id`, and `parent_checkpoint_id`.\n\n"
        f"This architectural separation between execution compute and persistent state storage allows {t_clean} to survive pod restarts, "
        f"support human-in-the-loop inspection, and enable deterministic replay."
    )
    
    # Real LangGraph code example
    code_ex = (
        f"from typing import Annotated, TypedDict\n"
        f"import operator\n"
        f"from langgraph.graph import StateGraph, START, END\n"
        f"from langgraph.checkpoint.memory import MemorySaver\n\n"
        f"# 1. Define State Schema with Reducers\n"
        f"class AgentState(TypedDict):\n"
        f"    query: str\n"
        f"    messages: Annotated[list[str], operator.add]\n"
        f"    status: str\n\n"
        f"# 2. Implement Node Function for {t_clean}\n"
        f"def process_{sec_slug.replace('-', '_')}_step(state: AgentState) -> dict:\n"
        f"    # Process state and return partial updates\n"
        f"    step_note = f\"Executed: {t_clean}\"\n"
        f"    return {{\n"
        f"        'messages': [step_note],\n"
        f"        'status': 'completed'\n"
        f"    }}\n\n"
        f"# 3. Build and Compile Workflow Graph\n"
        f"builder = StateGraph(AgentState)\n"
        f"builder.add_node('{sec_slug.replace('-', '_')}_node', process_{sec_slug.replace('-', '_')}_step)\n"
        f"builder.add_edge(START, '{sec_slug.replace('-', '_')}_node')\n"
        f"builder.add_edge('{sec_slug.replace('-', '_')}_node', END)\n\n"
        f"checkpointer = MemorySaver()\n"
        f"app = builder.compile(checkpointer=checkpointer)\n\n"
        f"# 4. Execute with Thread Isolation\n"
        f"config = {{'configurable': {{'thread_id': 'sess_prod_001'}}}}\n"
        f"final_state = app.invoke({{'query': 'Run task', 'messages': []}}, config=config)\n"
        f"print('Output State:', final_state['messages'])"
    )
    
    arch_flow = (
        f"Client Ingress (HTTP/FastAPI)\n"
        f"  │\n"
        f"  ▼\n"
        f"[START Virtual Node]\n"
        f"  │\n"
        f"  ▼\n"
        f"[{t_clean} Execution Node] ──(Emits Partial State Update)──► [Reducer Reconciliation]\n"
        f"  │                                                                 │\n"
        f"  ▼                                                                 ▼\n"
        f"[Conditional Router / Edge]                                   [Checkpointer: PostgresSaver]\n"
        f"  │                                                                 │\n"
        f"  ▼                                                                 ▼\n"
        f"[END Virtual Node] ◄───────────────────────────────────────────── [Durable Snapshot Saved]"
    )
    
    why_ask = f"Interviewers assess whether the candidate understands stateful graph compilation, reducer semantics, and error boundaries in LangGraph architectures."
    fail_modes = f"Unchecked state mutability, missing list reducers leading to message overwrites, and unhandled node exceptions causing abrupt graph execution termination."
    tradeoffs = f"Balancing fine-grained node granularity and modular testing against graph traversal overhead and checkpointer database write volume."
    mistakes = [
        f"Mutating state dictionary directly in place instead of returning update dictionaries",
        f"Forgetting to attach an Annotated reducer when accumulating conversational turns",
        f"Recompiling StateGraph on every HTTP request instead of reusing a compiled singleton"
    ]
    
    return short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes
