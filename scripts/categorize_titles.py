import sqlite3

conn = sqlite3.connect('backend/breakthecode.db')
cursor = conn.cursor()
cursor.execute('SELECT id, title, question_type, difficulty, technology_id, short_answer, interview_ready_answer, deep_explanation, code_example FROM questions')
rows = cursor.fetchall()

pure_headings = []
imperative_analyze = []
imperative_architect = []
scenarios = []
standard_questions = []

for r in rows:
    title = r[1].strip()
    if title.startswith("Analyze the performance bottlenecks"):
        imperative_analyze.append(r)
    elif title.startswith("Architect a globally"):
        imperative_architect.append(r)
    elif "encounters severe latency degradation due to" in title or "How do you triage" in title:
        scenarios.append(r)
    elif not title.endswith("?"):
        pure_headings.append(r)
    else:
        standard_questions.append(r)

print(f"Total: {len(rows)}")
print(f"Imperative 'Analyze...': {len(imperative_analyze)}")
print(f"Imperative 'Architect...': {len(imperative_architect)}")
print(f"Scenarios: {len(scenarios)}")
print(f"Pure headings without question mark: {len(pure_headings)}")
print(f"Standard questions ending with ?: {len(standard_questions)}")

print("\n--- SAMPLE PURE HEADINGS ---")
for r in pure_headings[:30]:
    print(f"[{r[3]}] ({r[2]}) {r[1]}")

print("\n--- SAMPLE STANDARD QUESTIONS ---")
for r in standard_questions[:15]:
    print(f"[{r[3]}] ({r[2]}) {r[1]}")

conn.close()
