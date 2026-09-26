"""
Unified Batch Expansion Runner for BreakTheCode
Ingests calibrated high-caliber batches across all 5 technologies:
- Java & JVM Concurrency
- System Design
- RAG & Vector Databases
- LangGraph & Agentic AI
- DSA & Algorithms
All batches pass the strict 10-point gatekeeper, deduplication engine, and transactional safety.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))

from content_quality_engine import ContentQualityEngine
from batch_java_expansion import get_java_expansion_batch
from batch_system_design_expansion import get_system_design_expansion_batch
from batch_rag_expansion import get_rag_expansion_batch
from batch_langgraph_expansion import get_langgraph_expansion_batch
from batch_dsa_expansion import get_dsa_expansion_batch

def execute_all_expansions():
    print("====================================================================")
    print("BREAK THE CODE — MULTI-TRACK CONTENT EXPANSION & QUALITY ENGINE")
    print("====================================================================")

    db_path = "backend/breakthecode.db"
    engine = ContentQualityEngine(db_path)

    batches = [
        ("Java & JVM Concurrency Expansion", get_java_expansion_batch()),
        ("System Design Expansion", get_system_design_expansion_batch()),
        ("RAG & Vector Databases Expansion", get_rag_expansion_batch()),
        ("LangGraph & Agentic AI Expansion", get_langgraph_expansion_batch()),
        ("DSA & Algorithms Expansion", get_dsa_expansion_batch()),
    ]

    total_requested = 0
    total_approved = 0
    total_rejected = 0
    total_duplicates = 0
    batch_reports = []

    for name, questions in batches:
        print(f"\n---> Processing Batch: {name} ({len(questions)} candidates)...", flush=True)
        stats = engine.ingest_batch(questions, batch_name=name)
        total_requested += stats["total_requested"]
        total_approved += stats["approved"]
        total_rejected += stats["rejected"]
        total_duplicates += stats["duplicates"]
        batch_reports.append(stats)

        print(f"     Approved: {stats['approved']} | Duplicates: {stats['duplicates']} | Rejected: {stats['rejected']}", flush=True)
        if stats["rejections"]:
            for r in stats["rejections"]:
                print(f"     [REJECTED] {r['title']}: {r['reasons']}", flush=True)

    engine.close()

    print("\n====================================================================")
    print("FINAL MULTI-TRACK EXPANSION SUMMARY")
    print("====================================================================")
    print(f"Total Requested Across Batches: {total_requested}")
    print(f"Total Approved and Ingested:   {total_approved}")
    print(f"Total Duplicates Caught:       {total_duplicates}")
    print(f"Total Quality Gate Rejections: {total_rejected}")

    return {
        "total_requested": total_requested,
        "total_approved": total_approved,
        "total_duplicates": total_duplicates,
        "total_rejected": total_rejected,
        "batch_reports": batch_reports
    }

if __name__ == "__main__":
    execute_all_expansions()
