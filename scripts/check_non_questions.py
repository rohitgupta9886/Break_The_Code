import sqlite3

conn = sqlite3.connect('backend/breakthecode.db')
cursor = conn.cursor()

cursor.execute("SELECT id, title, technology_id, difficulty FROM questions")
rows = cursor.fetchall()

non_q = []
for r in rows:
    qid, title, tech_id, diff = r
    t = title.strip()
    if not t.endswith("?"):
        non_q.append((qid, title, diff))

print(f"Total non-question mark titles: {len(non_q)}")

colon_suffixes = set()
for qid, title, diff in non_q:
    if ":" in title:
        colon_suffixes.add(title.split(":")[-1].strip())

print("\nColon suffixes found:")
for s in colon_suffixes:
    print(f"  - '{s}'")

without_colon = [t for qid, t, diff in non_q if ":" not in t]
print(f"\nNon-question titles without colon ({len(without_colon)}):")
for t in without_colon[:30]:
    print(f"  - '{t}'")

conn.close()
