import sqlite3

conn = sqlite3.connect('backend/breakthecode.db')
cursor = conn.cursor()

cursor.execute("""
SELECT id, title, question_type, difficulty, technology_id, short_answer, interview_ready_answer, deep_explanation, code_example 
FROM questions 
WHERE title LIKE '%: Foundational Mechanics & Concepts%' 
   OR title LIKE '%: Production Architecture & Implementation%'
   OR title LIKE '%: Extreme Scale & Hard Core Edge Cases%'
   OR title LIKE '%: Deep Production Pitfalls & Hardcore Scenarios%'
LIMIT 10
""")

rows = cursor.fetchall()
print(f"Sample section-format questions count: {len(rows)}")
for r in rows:
    print("=" * 80)
    print(f"ID: {r[0]}")
    print(f"TITLE: {r[1]}")
    print(f"SHORT ANSWER:\n{r[5][:200] if r[5] else 'None'}...")
    print(f"INTERVIEW READY ANSWER:\n{r[6][:200] if r[6] else 'None'}...")
    print(f"DEEP EXPLANATION:\n{r[7][:200] if r[7] else 'None'}...")
    print(f"CODE EXAMPLE:\n{r[8][:200] if r[8] else 'None'}...")

conn.close()
