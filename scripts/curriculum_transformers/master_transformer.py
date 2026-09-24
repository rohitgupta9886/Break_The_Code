"""
Master Curriculum Question Transformer.
Routes questions from all tracks to specialized curriculum generators,
ensuring every question title is a proper interview question ending in '?'
and every answer has rich, explainable multi-tier DNA and realistic code.
"""

from .langgraph_curriculum import transform_langgraph_topic
from .rag_curriculum import transform_rag_topic
from .java_curriculum import transform_java_topic
from .dsa_curriculum import transform_dsa_topic
from .system_design_curriculum import transform_system_design_topic
from .dimensions_curriculum import transform_imperative_or_dimension_question

def transform_question(
    qid: str,
    title: str,
    tech_slug: str,
    tech_name: str,
    topic_slug: str,
    topic_name: str,
    difficulty: str,
    depth: str,
    question_type: str
) -> dict:
    t = title.strip()
    
    # Case 1: Imperative prompts ("Analyze the performance...", "Architect a globally...", "Explain...")
    if (
        t.startswith("Analyze the performance bottlenecks") or 
        t.startswith("Architect a globally") or 
        t.startswith("Explain Time Complexity") or 
        t.startswith("Explain the Sliding Window")
    ):
        return transform_imperative_or_dimension_question(
            qid, t, tech_slug, tech_name, difficulty, question_type
        )
        
    # Case 2: Canonical Sections with colon suffix
    # e.g., "StateGraph Core Mechanics: Foundational Mechanics & Concepts"
    # or "Dynamic Fan-Out with Send: Production Architecture & Implementation"
    topic_raw = t
    level = "L1"
    if ": Foundational Mechanics & Concepts" in t:
        topic_raw = t.replace(": Foundational Mechanics & Concepts", "").strip()
        level = "L1"
    elif ": Production Architecture & Implementation" in t:
        topic_raw = t.replace(": Production Architecture & Implementation", "").strip()
        level = "L2"
    elif not t.endswith("?"):
        # Any other heading without question mark
        topic_raw = t
        level = "L1" if difficulty == "BASIC" else "L2"
        
    # Dispatch by technology
    if tech_slug == "langgraph":
        return transform_langgraph_topic(topic_raw, level, topic_slug or "state-graphs-nodes", topic_name or "LangGraph StateGraph")
    elif tech_slug == "rag-vector-db":
        return transform_rag_topic(topic_raw, level, topic_slug or "vector-indexing", topic_name or "RAG & Vector Retrieval")
    elif tech_slug == "java-backend":
        return transform_java_topic(topic_raw, level, topic_slug or "jvm-concurrency", topic_name or "Java & JVM Concurrency")
    elif tech_slug == "dsa":
        return transform_dsa_topic(topic_raw, level, topic_slug or "algorithms", topic_name or "DSA & Algorithms")
    elif tech_slug == "system-design":
        return transform_system_design_topic(topic_raw, level, topic_slug or "distributed-systems", topic_name or "System Design")
    else:
        # Fallback to system design transformer
        return transform_system_design_topic(topic_raw, level, topic_slug or "architecture", topic_name or "System Architecture")
