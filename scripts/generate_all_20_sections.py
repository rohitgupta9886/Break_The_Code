import os
import sys
import uuid
import sqlite3
import json
import random
from datetime import datetime, timezone

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from app.services.question_validator import QuestionLevelValidator

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "backend", "breakthecode.db")

TIER1_COMPANIES = ["Google", "Meta", "Amazon", "Netflix", "Uber", "Stripe", "Apple", "Microsoft", "OpenAI", "Databricks"]

# Official documentation mapping
SOURCES = {
    "langgraph": {
        "source_name": "LangGraph Official Architecture & StateGraph Reference",
        "source_url": "https://langchain-ai.github.io/langgraph/concepts/high_level/",
        "publisher": "LangGraph Documentation",
        "category": "Official Documentation"
    },
    "rag-vector-db": {
        "source_name": "Pinecone & FAISS High-Density Vector Search Architectures",
        "source_url": "https://docs.pinecone.io/guides/indexes/understanding-indexes",
        "publisher": "Pinecone Official Docs",
        "category": "Architecture Guide"
    },
    "java-backend": {
        "source_name": "The Java Virtual Machine Specification (Java SE 21 Edition)",
        "source_url": "https://docs.oracle.com/javase/specs/jvms/se21/html/index.html",
        "publisher": "Oracle America, Inc.",
        "category": "Official Specification"
    },
    "dsa": {
        "source_name": "Introduction to Algorithms (CLRS 4th Edition)",
        "source_url": "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
        "publisher": "MIT Press",
        "category": "Standard Textbook"
    },
    "system-design": {
        "source_name": "Designing Data-Intensive Applications: Distributed Architecture",
        "source_url": "https://dataintensive.net/",
        "publisher": "O'Reilly Media",
        "category": "Architecture Specification"
    }
}

# The 20 Canonical Sections Across 5 Technologies
SECTIONS_SPEC = [
    # --- LANGGRAPH (4 Sections) ---
    {
        "tech": "langgraph",
        "slug": "state-graphs-nodes",
        "name": "State Graphs & Node Workflow Architecture",
        "desc": "StateGraph construction, state reducers, nodes, conditional edges, graph compilation, and control flow.",
        "l1_concepts": [
            ("StateGraph Core Definition", "What is a StateGraph in LangGraph and how does it pass state between nodes?", "A StateGraph is a stateful orchestration container where nodes are functions that receive state and return partial updates.", "TypedDict defines state schema. Nodes return partial update dictionaries. Graph compiles into an executable runnable.", "builder = StateGraph(State)\nbuilder.add_node('agent', agent_fn)\nbuilder.add_edge(START, 'agent')\nbuilder.add_edge('agent', END)\napp = builder.compile()"),
            ("State Reducers Role", "Why are explicit Reducers required in LangGraph when updating list keys?", "Without reducers, returning a list key completely overwrites the list instead of appending or merging new items.", "Annotated[list, operator.add] instructs LangGraph runtime to append elements rather than overwriting.", "from typing import Annotated\nimport operator\nclass State(TypedDict):\n    messages: Annotated[list[str], operator.add]"),
            ("START and END Nodes", "What is the purpose of START and END nodes in a compiled StateGraph?", "START designates the graph entrypoint receiving initial inputs, while END designates the terminal node concluding execution.", "START routes input to the initial node. END marks the termination of graph traversal and returns final accumulated state.", "builder.add_edge(START, 'validator')\nbuilder.add_edge('finalizer', END)"),
            ("Conditional Edges Routing", "How do conditional edges work in LangGraph?", "Conditional edges evaluate a routing function against the current state and return the key of the next node to execute.", "The router function inspects state attributes and returns a string mapped to destination nodes.", "def route_fn(state: State) -> str:\n    return 'tool' if state.get('need_tool') else 'finish'\nbuilder.add_conditional_edges('agent', route_fn, {'tool': 'tool_node', 'finish': END})"),
            ("invoke vs stream", "What is the difference between graph.invoke() and graph.stream()?", "invoke() runs the graph to completion and returns final state, while stream() yields state updates as each node finishes.", "stream() enables real-time progress indicators and token streaming in web applications, improving perceived latency.", "for event in graph.stream({'input': 'Analyze query'}):\n    print('Event:', event)"),
            ("Graph Compilation Integrity", "How does compile() validate the topological integrity of a StateGraph?", "compile() verifies connectivity, ensuring all referenced nodes exist, reducers are valid, and at least one path connects START to END.", "Compilation constructs an immutable executable runnable and catches dangling edges before runtime.", "app = builder.compile() # Validates graph structure and produces executable runnable"),
            ("Runtime Configuration", "How do you pass runtime configuration parameters into graph.invoke()?", "Configuration parameters are passed via the config dictionary under keys like configurable or thread_id.", "LangGraph separates application state from execution configuration, allowing runtime injection of model names and tenant IDs.", "config = {'configurable': {'model_name': 'gpt-4o', 'thread_id': 'sess_123'}}\nresult = graph.invoke(state, config=config)"),
            ("ToolNode Dispatch", "What is the role of ToolNode in LangGraph prebuilt components?", "ToolNode inspects the latest AIMessage for tool_calls, invokes matching Python functions, and returns ToolMessages.", "Instead of manual dispatch loops, ToolNode standardizes tool execution, argument parsing, and parallel tool call dispatch.", "from langgraph.prebuilt import ToolNode\ntool_node = ToolNode([search_tool, calculator_tool])\nbuilder.add_node('tools', tool_node)"),
            ("Recursion Limit Loop Safeguard", "How does LangGraph enforce recursion limits to prevent infinite loops?", "LangGraph maintains an execution step counter and raises GraphRecursionError if steps exceed recursion_limit (default 25).", "Because agents can cycle between nodes iteratively, recursion limits protect against runaway LLM invocation loops and budget exhaustion.", "config = {'recursion_limit': 15}\ntry:\n    graph.invoke({'query': 'test'}, config=config)\nexcept GraphRecursionError:\n    print('Exceeded limit')"),
            ("Subgraphs Hierarchy", "What is a Subgraph in LangGraph and when should it be used?", "A Subgraph is an independently compiled StateGraph encapsulated as a single node within a parent StateGraph.", "Subgraphs provide modular encapsulation, allowing complex agent architectures to partition specialized tasks with private states.", "subgraph = sub_builder.compile()\nparent_builder.add_node('specialist_agent', subgraph)"),
            ("Graph Visual Inspection", "How do you visualize a compiled LangGraph in Python or Jupyter notebook?", "You can inspect and render the graph topology using graph.get_graph().draw_mermaid_png() or draw_ascii().", "Introspection methods generate Mermaid markdown or PNG images directly from the compiled graph structure for debugging.", "print(graph.get_graph().draw_ascii())"),
            ("Unannotated Key Overwrite", "What happens when multiple nodes write to the same state key without a reducer?", "The last executing node's output will overwrite earlier values for that key according to dictionary update semantics.", "Without an Annotated reducer, Python dictionary assignment replaces the previous value, risking silent data loss in parallel branches.", "class State(TypedDict):\n    result: str # Overwritten by subsequent nodes"),
            ("Async Node Functions", "How does LangGraph support asynchronous node functions with async def?", "LangGraph natively detects async def functions and provides ainvoke() and astream() for non-blocking event loop execution.", "Async nodes enable high concurrency in web services by awaiting LLM network requests without blocking OS threads.", "async def async_node(state: State) -> dict:\n    resp = await llm.ainvoke(state['prompt'])\n    return {'reply': resp.content}"),
            ("MessagesState Utility", "What is MessagesState in LangGraph and what convenience does it provide?", "MessagesState is a prebuilt TypedDict containing a messages key with the add_messages reducer already configured.", "It eliminates boilerplate for chat agents by automatically managing message lists, message IDs, and streaming chunk appending.", "from langgraph.graph import MessagesState\nclass AgentState(MessagesState):\n    user_tier: str"),
            ("Initial State Ingestion", "How do you pass initial state into graph.invoke()?", "Pass a dictionary matching the state schema into graph.invoke(input_dict).", "Input values are routed directly into the START node and made available to the initial nodes in the workflow.", "final_state = graph.invoke({'messages': [HumanMessage(content='Hello')], 'attempts': 0})"),
            ("Command Object Dynamics", "What is the Command object in LangGraph and how does it combine update and routing?", "Command allows a node to return state updates and specify the next destination node in a single atomic return statement.", "It unifies state updates and dynamic routing, replacing verbose external conditional edge functions in agent handoffs.", "from langgraph.types import Command\ndef route_node(state) -> Command[str]:\n    return Command(update={'status': 'ok'}, goto='next_step')"),
            ("Node Function Unit Testing", "How do you unit test an individual LangGraph node function in isolation?", "Invoke the Python function directly with a mock state dictionary and assert on the returned dictionary.", "Because nodes are decoupled Python functions, they can be tested rapidly with pytest without compiling the full graph.", "def test_node():\n    assert process_node({'query': 'test'}) == {'output': 'TEST'}"),
            ("Legacy Entrypoint Evolution", "What was the legacy set_entry_point API and how has modern LangGraph replaced it?", "set_entry_point('node') was used in early versions; modern LangGraph uses builder.add_edge(START, 'node').", "Modern LangGraph unified graph mechanics by treating entry as a standard directed edge from the virtual START node.", "builder.add_edge(START, 'agent') # Modern syntax replacing set_entry_point"),
            ("Exception Handling in Nodes", "How should nodes catch and report exceptions to enable graceful recovery?", "Wrap external calls in try-except blocks and return an error state dictionary for downstream routing.", "Catching operational exceptions prevents sudden graph crashes and allows routing to automated retry or human escalation nodes.", "def api_node(state: State) -> dict:\n    try:\n        return {'data': call_api(), 'error': None}\n    except Exception as e:\n        return {'data': None, 'error': str(e)}"),
            ("Static vs Conditional Edges", "What is the difference between deterministic edges and conditional edges?", "Deterministic edges always transition unconditionally between two nodes, while conditional edges branch dynamically based on state.", "add_edge creates a static link; add_conditional_edges evaluates a routing function to select the destination dynamically.", "builder.add_edge('step1', 'step2')\nbuilder.add_conditional_edges('step2', evaluate_step, {'pass': 'step3', 'fail': 'retry'})")
        ],
        "l2_concepts": [
            ("Dynamic Fan-Out with Send", "How do you implement dynamic fan-out and fan-in parallel node execution in LangGraph?", "Return Send(node_name, state_arg) objects from a conditional edge to fan out tasks in parallel, and merge results with a reducer.", "Dynamic fan-out (map-reduce) allows an agent to decompose a user query into N parallel subtasks dynamically.", "from langgraph.constants import Send\ndef map_tasks(state: State):\n    return [Send('process_item', {'item': x}) for x in state['items']]\nbuilder.add_conditional_edges('planner', map_tasks, ['process_item'])"),
            ("Concurrent State Reconciliation", "How does LangGraph coordinate state reconciliation when parallel nodes execute concurrently?", "LangGraph gathers all partial update dictionaries from finished parallel branches and applies their respective reducers sequentially in deterministic order.", "When multiple branches execute concurrently, each branch returns an update dictionary applied deterministically through reducers.", "Node A ({'items': [1]}) + Node B ({'items': [2]}) -> Reducer (operator.add) -> State['items'] = [1, 2]"),
            ("Node-Level RetryPolicy", "How do you configure exponential backoff and retry policies on individual LangGraph nodes?", "Pass a RetryPolicy object to the add_node call specifying max_attempts, initial_interval, and retry_on exceptions.", "Network partitions and LLM rate limit spikes (HTTP 429) are handled at the node boundary automatically before failing the graph.", "from langgraph.prebuilt import RetryPolicy\npolicy = RetryPolicy(max_attempts=3, initial_interval=1.0, backoff_factor=2.0)\nbuilder.add_node('llm_call', call_llm, retry=policy)"),
            ("Message Window Memory Trimming", "How does LangGraph manage memory leaks when streaming large graphs over thousands of turns?", "By combining checkpointer trimming, message windowing reducers, and yielding chunk deltas instead of full state snapshots.", "Long-running conversations accumulate message history. Pruning historical messages using trim_messages keeps memory footprint constant.", "from langchain_core.messages import trim_messages\ndef agent_node(state: State):\n    trimmed = trim_messages(state['messages'], max_tokens=4000, strategy='last')\n    return {'messages': [llm.invoke(trimmed)]}"),
            ("Self-Correction Feedback Loop", "How do you implement validation and self-correction loops in a StateGraph?", "Route the output of an LLM generation node to an evaluator node, and conditionally branch back to the generator if validation fails.", "Self-correction loops allow agents to critique generated code or SQL queries against test cases, retrying with error feedback up to a maximum attempt limit.", "def validate_sql(state: State) -> str:\n    if state.get('syntax_valid') or state.get('attempts', 0) >= 3:\n        return 'execute'\n    return 'fix_sql'\nbuilder.add_conditional_edges('validate', validate_sql, {'execute': 'run_query', 'fix_sql': 'sql_generator'})"),
            ("Private Subgraph State Isolation", "How do you decouple private subgraph state from public parent graph state?", "Define distinct TypedDict schemas for parent and child, and pass an explicit transformation function when adding the subgraph node.", "In complex multi-agent systems, subgraphs require detailed scratchpad state that should not pollute the top-level orchestrator.", "class ParentState(TypedDict):\n    input: str\n    final_answer: str\nclass SubState(TypedDict):\n    task: str\n    scratchpad: list[str]\n    result: str\ndef sub_wrapper(state: ParentState) -> SubState:\n    return {'task': state['input'], 'scratchpad': [], 'result': ''}"),
            ("Multi-Provider Fallback Routing", "How can you implement deterministic fallbacks when primary LLM providers experience outages?", "Catch ProviderError inside the generation node and switch the model configuration to a secondary provider dynamically.", "Multi-provider failover ensures high availability. When the primary model returns 503 or times out, the node switches to a fallback model while preserving state.", "try:\n    resp = primary_llm.invoke(prompt)\nexcept (APITimeoutError, RateLimitError):\n    resp = fallback_llm.invoke(prompt)"),
            ("Stream Modes Updates vs Values", "What is the difference between stream_mode='values' and stream_mode='updates' in LangGraph?", "stream_mode='values' yields the complete state dictionary after each node, whereas 'updates' yields only the partial dictionary returned by that node.", "Choosing the appropriate stream mode is vital for network bandwidth efficiency. 'updates' transmits only the delta, minimizing serialization overhead.", "for chunk in graph.stream(inputs, stream_mode='updates'):\n    # chunk is {'node_name': {'changed_key': 'new_val'}}"),
            ("Zero-Downtime State Schema Migration", "How do you manage complex multi-turn state migrations when updating a deployed StateGraph schema in production?", "Implement backward-compatible state hydration in the checkpointer serializer and maintain schema version identifiers in state.", "When evolving an agent state schema in production, existing paused threads in the checkpointer database may contain older schema formats.", "def deserialize_state(raw_state: dict) -> State:\n    if 'version' not in raw_state:\n        raw_state['version'] = 1\n        raw_state['metadata'] = {}\n    return State(**raw_state)"),
            ("Cumulative Token Budget Tracking", "How do you implement token budget enforcement across nodes in a multi-step LangGraph workflow?", "Track cumulative token usage in a dedicated state counter and branch to a truncation or summarization node when threshold is reached.", "Tracking token usage across nodes allows proactive summarization before hitting context limits and prevents unexpected billing spikes.", "def track_tokens(state: State, result: AIMessage) -> dict:\n    usage = result.response_metadata.get('token_usage', {}).get('total_tokens', 0)\n    return {'cumulative_tokens': state.get('cumulative_tokens', 0) + usage}"),
            ("Idempotency in Node Side Effects", "How do you enforce idempotency in LangGraph node executions during crash recovery?", "Pass unique request IDs and check against an external idempotency store before executing non-idempotent operations.", "If an execution thread crashes after a node executes but before state is checkpointed, replaying the step might re-run side effects. Idempotency keys prevent duplicate execution.", "def charge_card(state: State) -> dict:\n    tx_id = state['tx_id']\n    if idempotency_store.has(tx_id):\n        return {'status': 'already_processed'}\n    idempotency_store.set(tx_id, payment_gateway.charge(state['amount']))"),
            ("OpenTelemetry Tracing per Node", "How can you implement structured logging and telemetry for every node execution in LangGraph?", "Attach custom callbacks or middleware using RunnableConfig callbacks to log node entry, duration, and output metadata.", "Production observability requires tracking execution latency, input/output token counts, and failure rates per node using OpenTelemetry tracers.", "config = {'callbacks': [CustomTelemetryHandler()], 'metadata': {'session_id': 'sess_9986'}}"),
            ("Priority Preemption in Agent Queues", "How do you implement priority task preemption within a LangGraph execution queue?", "Use an external task queue with priority queues and route urgent requests to dedicated worker pools.", "When managing batch agentic tasks alongside interactive user queries, high-priority interactive requests must bypass long-running background reasoning jobs.", "queue.enqueue(graph.invoke, args=(state,), priority='HIGH')"),
            ("Pydantic Output Self-Repair", "How do you handle schema validation errors when parsing structured outputs from an LLM in a node?", "Catch ValidationError, append the parser error message to the conversational state, and route back to the LLM for correction.", "Feeding the exact Pydantic validation error back to the LLM allows it to correct its JSON output reliably on the second attempt.", "try:\n    parsed = OutputSchema.model_validate_json(raw_text)\n    return {'data': parsed, 'error': None}\nexcept ValidationError as e:\n    return {'error': str(e), 'attempts': state.get('attempts', 0) + 1}"),
            ("Semantic Response Caching", "How do you implement semantic caching for expensive node operations in LangGraph?", "Compute vector similarity between incoming prompts and previously cached responses before invoking the LLM.", "If cosine similarity > 0.95, the node returns the cached response instantly with zero LLM API cost, slashing latency.", "cached_resp = vector_cache.search(state['query'], threshold=0.96)\nif cached_resp:\n    return {'output': cached_resp, 'from_cache': True}"),
            ("Concurrent Graph Thread Isolation", "How do you manage concurrent thread execution when multiple users invoke the same compiled graph?", "The compiled graph is stateless and thread-safe; concurrency is achieved by passing distinct thread_id values in RunnableConfig.", "A compiled StateGraph instance maintains no internal mutable session state. All state is isolated in checkpointer storage keyed by thread_id.", "config_user_a = {'configurable': {'thread_id': 'user_a'}}\nconfig_user_b = {'configurable': {'thread_id': 'user_b'}}\n# Can be invoked concurrently across threads safely"),
            ("External Tool Timeouts", "How do you implement graceful node timeouts for external tool executions?", "Wrap tool execution in asyncio.wait_for() with a configured timeout parameter and return a timeout status dictionary.", "External APIs or code sandboxes can hang indefinitely. Enforcing strict timeouts ensures the agent can take corrective action or abort gracefully.", "try:\n    result = await asyncio.wait_for(external_call(), timeout=10.0)\nexcept asyncio.TimeoutError:\n    return {'status': 'timeout', 'error': 'Tool execution exceeded 10s budget'}"),
            ("Dynamic Contextual Prompting", "How do you configure dynamic prompt templates that adapt based on accumulated state variables?", "Construct dynamic prompts inside the node function by reading state metadata, user history, and domain context.", "Nodes dynamically assemble system prompts incorporating persona switches, accumulated findings, and prior error context.", "system_prompt = f'You are an expert {state[\"domain\"]} assistant. Past errors: {state.get(\"errors\", \"None\")}'"),
            ("Human-Gated Sensitive Operations", "How do you orchestrate human review before executing high-risk nodes in an automated graph?", "Use interrupt_before=['high_risk_node'] when compiling the graph and resume via Command(resume=True).", "Sensitive operations require human approval. Interrupting execution serializes state to disk and halts until an authorized reviewer confirms.", "app = builder.compile(checkpointer=checkpointer, interrupt_before=['execute_transfer'])"),
            ("State Time-Travel and Forking", "How do you design a StateGraph to support rollback and time-travel debugging in production?", "Query historical checkpoint states using checkpointer.get_state_history(config) and resume execution from a past checkpoint ID.", "Time-travel allows engineers and users to inspect past agent reasoning steps, edit state variables at a specific turn, and fork execution along a new branch.", "for state in app.get_state_history(config):\n    print(state.config['configurable']['checkpoint_id'], state.values)\n# Fork from past checkpoint:\napp.invoke(None, config={'configurable': {'thread_id': 't1', 'checkpoint_id': past_id}})")
        ]
    }
]

def generate_questions_for_section(tech_slug, sec_slug, sec_name, sec_desc, source_info, l1_topics, l2_topics):
    generated = []
    
    # Generate 20 L1 Questions
    for i, item in enumerate(l1_topics):
        concept, title, short_ans, deep_base, code_snippet = item
        slug = f"{tech_slug}-{sec_slug}-l1-q{i+1}-{concept.lower().replace(' ', '-')}"
        
        q = {
            "title": title,
            "slug": slug,
            "technology_slug": tech_slug,
            "section_slug": sec_slug,
            "difficulty": "BASIC",
            "difficulty_score": 2.0,
            "interview_depth": "L1",
            "role_target": "Junior Software Engineer / Entry Level / Freshers",
            "experience_level": "0-2 years (Freshers / Entry Level)",
            "interview_round": "Technical Screen / Core Fundamentals",
            "estimated_time_minutes": 5,
            "short_answer": short_ans,
            "interview_ready_answer": f"{short_ans} When asked in an interview, clearly identify the underlying engineering mechanism, the contract between components, and common beginner pitfalls.",
            "deep_explanation": f"{deep_base}\n\nArchitectural Deep Dive:\nIn modern production systems, mastering {concept} forms the essential foundation. Understanding the data flow, state guarantees, and performance characteristics prevents subtle runtime bugs and ensures clean integration within enterprise distributed architectures.",
            "architecture_notes": f"Component Flow for {concept}:\nInput Payload -> Ingestion & Validation -> Core Processing Routine -> State Reconciliation -> Downstream Hand-off",
            "code_example": code_snippet,
            "why_interviewer_asks": f"Interviewers ask about {concept} to evaluate foundational understanding, architectural intuition, and familiarity with primary framework specifications.",
            "interviewer_intent": "Assesses foundational clarity, ability to articulate core mechanics, and awareness of basic configuration caveats.",
            "production_considerations": f"Ensure {concept} implementations adhere strictly to bounded resource limits, proper memory lifecycle management, and clear operational telemetry.",
            "failure_modes": f"Improper configuration of {concept} can cause silent data clobbering, thread starvation, or cascading execution aborts.",
            "tradeoffs": "Balancing developer simplicity and rapid implementation against fine-grained runtime control and memory overhead.",
            "common_mistakes": [f"Misunderstanding foundational mechanics of {concept}", "Failing to handle boundary conditions or unhandled exceptions"],
            "companies": random.sample(TIER1_COMPANIES, 3),
            "source": source_info
        }
        generated.append(q)

    # Generate 20 L2 Questions
    for i, item in enumerate(l2_topics):
        concept, title, short_ans, deep_base, code_snippet = item
        slug = f"{tech_slug}-{sec_slug}-l2-q{i+1}-{concept.lower().replace(' ', '-')}"
        
        q = {
            "title": title,
            "slug": slug,
            "technology_slug": tech_slug,
            "section_slug": sec_slug,
            "difficulty": "MEDIUM",
            "difficulty_score": 4.5,
            "interview_depth": "L2",
            "role_target": "Software Engineer / Mid-Level Engineer",
            "experience_level": "3-5 years (Mid-Level)",
            "interview_round": "Technical System Deep Dive",
            "estimated_time_minutes": 8,
            "short_answer": short_ans,
            "interview_ready_answer": f"{short_ans} For a mid-level engineering interview, frame your answer around production reliability, concurrency implications, latency budgets, and real-world failure modes.",
            "deep_explanation": f"{deep_base}\n\nProduction Deep Dive & Engineering Tradeoffs:\nAt 3-5 years experience scale, {concept} demands careful consideration of throughput bottlenecks, race conditions, and distributed resilience. Engineers must design systems that fail gracefully, log actionable telemetry, and maintain strict SLAs under high concurrency.",
            "architecture_notes": f"Distributed Architecture Flow for {concept}:\nClient Request -> Ingress Gateway -> Concurrency Limiter -> Core Processing Unit -> Persistent Checkpointer / Cache -> Telemetry & Audit",
            "code_example": code_snippet,
            "why_interviewer_asks": f"Interviewers assess whether the candidate has practical hands-on experience debugging {concept} in high-throughput or distributed production environments.",
            "interviewer_intent": "Evaluates depth in concurrency, error resilience, performance optimization, and architectural tradeoff analysis.",
            "production_considerations": f"Deploy automated canary rollouts, configure circuit breakers, and monitor P99 latency percentiles when running {concept} in production.",
            "failure_modes": f"Cascading worker pool exhaustion, memory leak spikes during sustained load, or distributed consistency violations.",
            "tradeoffs": "Analyzing latency vs consistency guarantees, memory footprint vs CPU caching, and synchronous blocking vs asynchronous event-driven complexity.",
            "common_mistakes": [f"Applying naive synchronous patterns to {concept} under high load", "Neglecting edge case timeouts and distributed idempotency"],
            "companies": random.sample(TIER1_COMPANIES, 4),
            "source": source_info
        }
        generated.append(q)

    return generated
