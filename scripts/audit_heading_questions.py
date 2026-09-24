import sqlite3
from collections import Counter

conn = sqlite3.connect('backend/breakthecode.db')
cursor = conn.cursor()

cursor.execute("""
SELECT q.id, q.title, q.difficulty, t.name as tech_name, top.name as topic_name, q.code_example, q.short_answer
FROM questions q
LEFT JOIN technologies t ON q.technology_id = t.id
LEFT JOIN topics top ON q.topic_id = top.id
""")
rows = cursor.fetchall()

def is_heading_or_improper(title):
    t = title.strip()
    if not t.endswith("?"):
        return True, "No question mark"
    if t.startswith("Analyze the performance bottlenecks"):
        return True, "Analyze imperative"
    if t.startswith("Architect a globally"):
        return True, "Architect imperative"
    if ": Foundational Mechanics" in t or ": Production Architecture" in t or ": Extreme Scale" in t:
        return True, "Colon suffix pattern"
    return False, "Proper"

categories = Counter()
reasons = Counter()
flagged = []

for r in rows:
    qid, title, diff, tech, topic, code, sa = r
    improper, reason = is_heading_or_improper(title)
    if improper:
        categories[tech] += 1
        reasons[reason] += 1
        flagged.append(r)

print(f"Total questions: {len(rows)}")
print(f"Total flagged heading/improper questions: {len(flagged)}")
print("\nBreakdown by reason:")
for reason, count in reasons.most_common():
    print(f"  {reason}: {count}")

print("\nBreakdown by technology:")
for tech, count in categories.most_common():
    print(f"  {tech}: {count}")

# Check placeholder code examples
cursor.execute("""
SELECT count(*) FROM questions 
WHERE code_example LIKE '%def handle_%' 
   OR code_example LIKE '%async def execute_resilient_%'
   OR code_example LIKE '%class Resilient%Handler:%'
""")
placeholder_codes = cursor.fetchone()[0]
print(f"\nQuestions with placeholder/templated code examples: {placeholder_codes}")

conn.close()
