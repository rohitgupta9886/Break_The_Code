import sqlite3

conn = sqlite3.connect('backend/breakthecode.db')
cursor = conn.cursor()

cursor.execute("SELECT id, title, difficulty, question_type FROM questions WHERE title NOT LIKE '%: %' AND title NOT LIKE '%?'")
rows = cursor.fetchall()
print(f"Count: {len(rows)}")
for r in rows:
    if not r[1].startswith('Analyze the performance'):
        print(f"[{r[2]}] ({r[3]}) {r[1]}")

conn.close()
