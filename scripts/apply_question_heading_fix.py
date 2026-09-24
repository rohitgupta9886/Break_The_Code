"""
Script to apply the Question Heading Fix and Answer Enrichment across Break The Code database.
Transforms all heading-formatted titles into proper, natural interview questions ending with '?',
and populates rich, multi-tier answers, deep architectural explanations, and production-ready code.
"""

import os
import sys
import sqlite3
import json
from datetime import datetime, timezone

# Ensure project directories are in path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from curriculum_transformers.master_transformer import transform_question

DB_PATH = os.path.join(BASE_DIR, "backend", "breakthecode.db")

def is_target_for_fix(title: str, code_example: str, short_answer: str) -> bool:
    t = (title or "").strip()
    c = (code_example or "").strip()
    sa = (short_answer or "").strip()
    
    # 1. Title is a heading or imperative command
    if not t.endswith("?"):
        return True
    if t.startswith("Analyze the performance bottlenecks"):
        return True
    if t.startswith("Architect a globally"):
        return True
    if ": Foundational Mechanics" in t or ": Production Architecture" in t:
        return True
    if t.startswith("Explain Time Complexity") or t.startswith("Explain the Sliding Window"):
        return True
        
    # 2. Code example is placeholder
    if "def handle_" in c or "async def execute_resilient_" in c or ("class Resilient" in c and "execute_safe_step" in c):
        return True
        
    # 3. Short answer contains embedded question string
    if ", What is " in sa or ", How do you " in sa or ", How does " in sa:
        return True

    return False

def main():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        q.id, q.title, q.difficulty, q.interview_depth, q.question_type,
        t.slug as tech_slug, t.name as tech_name, 
        top.slug as topic_slug, top.name as topic_name,
        q.code_example, q.short_answer
    FROM questions q
    LEFT JOIN technologies t ON q.technology_id = t.id
    LEFT JOIN topics top ON q.topic_id = top.id
    """)
    rows = cursor.fetchall()
    print(f"Total questions in database: {len(rows)}")
    
    updated_count = 0
    title_fixed_count = 0
    code_upgraded_count = 0
    now_str = datetime.now(timezone.utc).isoformat()
    
    for r in rows:
        qid, title, diff, depth, qtype, tech_slug, tech_name, top_slug, top_name, code, sa = r
        
        if not is_target_for_fix(title, code, sa):
            continue
            
        # Transform question and content
        transformed = transform_question(
            qid=qid,
            title=title,
            tech_slug=tech_slug or "system-design",
            tech_name=tech_name or "System Design",
            topic_slug=top_slug or "architecture",
            topic_name=top_name or "System Architecture",
            difficulty=diff or "MEDIUM",
            depth=depth or "L2",
            question_type=qtype or "CONCEPTUAL"
        )
        
        new_title = transformed["title"]
        if new_title != title:
            title_fixed_count += 1
            
        old_is_placeholder = bool("def handle_" in (code or "") or "execute_resilient_" in (code or "") or "execute_safe_step" in (code or ""))
        if old_is_placeholder:
            code_upgraded_count += 1
            
        cursor.execute("""
        UPDATE questions SET
            title = ?,
            short_answer = ?,
            interview_ready_answer = ?,
            deep_explanation = ?,
            architecture_notes = ?,
            code_example = ?,
            why_interviewer_asks = ?,
            interviewer_intent = ?,
            production_considerations = ?,
            failure_modes = ?,
            tradeoffs = ?,
            common_mistakes = ?,
            updated_at = ?
        WHERE id = ?
        """, (
            new_title,
            transformed["short_answer"],
            transformed["interview_ready_answer"],
            transformed["deep_explanation"],
            transformed["architecture_notes"],
            transformed["code_example"],
            transformed["why_interviewer_asks"],
            transformed["interviewer_intent"],
            transformed["production_considerations"],
            transformed["failure_modes"],
            transformed["tradeoffs"],
            json.dumps(transformed["common_mistakes"]),
            now_str,
            qid
        ))
        updated_count += 1
        
    conn.commit()
    print(f"\nSuccessfully applied updates!")
    print(f"Total questions updated: {updated_count}")
    print(f"Titles transformed to proper questions: {title_fixed_count}")
    print(f"Placeholder codes replaced with real implementations: {code_upgraded_count}")
    
    # Verification checks
    cursor.execute("SELECT count(*) FROM questions WHERE title NOT LIKE '%?'")
    remaining_non_q = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT count(*) FROM questions 
    WHERE code_example LIKE '%def handle_%' 
       OR code_example LIKE '%async def execute_resilient_%'
    """)
    remaining_placeholder_code = cursor.fetchone()[0]
    
    print(f"\n--- VERIFICATION AUDIT ---")
    print(f"Questions without '?' at end: {remaining_non_q} (Goal: 0)")
    print(f"Questions with placeholder 'handle_' code: {remaining_placeholder_code} (Goal: 0)")
    
    # Sample verification
    cursor.execute("""
    SELECT title, short_answer, code_example 
    FROM questions 
    ORDER BY updated_at DESC 
    LIMIT 3
    """)
    samples = cursor.fetchall()
    print("\n--- SAMPLE ENRICHED QUESTIONS ---")
    for i, s in enumerate(samples, 1):
        print(f"\n[Sample {i}] Title: {s[0]}")
        print(f"Short Answer: {s[1][:120]}...")
        print(f"Code Preview:\n{s[2][:160]}...\n")
        
    conn.close()

if __name__ == "__main__":
    main()
