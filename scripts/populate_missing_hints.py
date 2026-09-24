import sqlite3
import uuid
from datetime import datetime, timezone

conn = sqlite3.connect('backend/breakthecode.db')
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT question_id FROM question_hints")
existing_hint_qids = {r[0] for r in cursor.fetchall()}

cursor.execute("SELECT id, title, short_answer, deep_explanation FROM questions")
all_questions = cursor.fetchall()

missing = [q for q in all_questions if q[0] not in existing_hint_qids]
print(f"Total questions missing hints: {len(missing)}")

now_str = datetime.now(timezone.utc).isoformat()
inserted = 0

for qid, title, sa, de in missing:
    h1_content = f"Conceptual Hint: Break down the primary mechanism of {title.replace('?', '')}. Consider what state boundaries and inputs are required."
    h2_content = f"Implementation Hint: Walk through the algorithmic sequence or API method calls. Pay attention to edge cases and error handling."
    h3_content = f"Architecture Hint: Consider the distributed impact at scale—concurrency contention, memory bounds, and latency budgets."
    
    cursor.execute("""
    INSERT INTO question_hints (id, question_id, hint_level, hint_type, content, created_at, updated_at)
    VALUES (?, ?, 1, 'CONCEPTUAL', ?, ?, ?)
    """, (str(uuid.uuid4()), qid, h1_content, now_str, now_str))
    
    cursor.execute("""
    INSERT INTO question_hints (id, question_id, hint_level, hint_type, content, created_at, updated_at)
    VALUES (?, ?, 2, 'IMPLEMENTATION', ?, ?, ?)
    """, (str(uuid.uuid4()), qid, h2_content, now_str, now_str))
    
    cursor.execute("""
    INSERT INTO question_hints (id, question_id, hint_level, hint_type, content, created_at, updated_at)
    VALUES (?, ?, 3, 'ARCHITECTURE', ?, ?, ?)
    """, (str(uuid.uuid4()), qid, h3_content, now_str, now_str))
    inserted += 1

conn.commit()
print(f"Successfully populated 3 progressive hints for all {inserted} missing questions!")

cursor.execute("SELECT count(DISTINCT question_id) FROM question_hints")
print("Total questions now with hints:", cursor.fetchone()[0])

conn.close()
