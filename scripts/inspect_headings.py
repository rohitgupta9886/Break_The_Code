import sqlite3

conn = sqlite3.connect('backend/breakthecode.db')
cursor = conn.cursor()

cursor.execute('SELECT id, title, question_type, difficulty, short_answer, interview_ready_answer, code_example FROM questions')
rows = cursor.fetchall()

print(f"Total questions in database: {len(rows)}")

question_starters = ("what", "how", "why", "when", "which", "where", "who", "can", "does", "is", "are", "do", "explain", "describe", "compare", "differentiate", "design", "implement")

headings = []
for r in rows:
    qid, title, qtype, diff, sa, ira, code = r
    clean_title = title.strip()
    first_word = clean_title.split()[0].lower() if clean_title else ""
    is_q = clean_title.endswith('?')
    
    # Check if title looks like a heading rather than a question
    # E.g. Doesn't end in '?' OR starts like a topic/heading ("Topic Name", "X vs Y", "Concept: Detail", etc.)
    # Or starts with "Analyze...", "Architect a...", "A high-throughput..."
    if not is_q or first_word not in question_starters:
        headings.append(r)

print(f"Total headings/non-standard questions identified: {len(headings)}")
print("\n--- SAMPLE HEADING-LIKE TITLES (First 35) ---")
for r in headings[:35]:
    print(f"[{r[3]}] ({r[2]}) {r[1]}")

conn.close()
