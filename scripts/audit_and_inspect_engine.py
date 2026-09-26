import sqlite3
import json
from collections import Counter, defaultdict

def main():
    conn = sqlite3.connect('backend/breakthecode.db')
    cursor = conn.cursor()

    # 1. Tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = sorted([r[0] for r in cursor.fetchall()])
    print("=== DATABASE TABLES ===")
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM `{t}`")
        cnt = cursor.fetchone()[0]
        print(f"  {t}: {cnt} rows")

    # 2. Check Question columns
    cursor.execute("PRAGMA table_info(questions)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n=== QUESTION COLUMNS ({len(columns)}) ===")
    print(", ".join(columns))

    # 3. Check for duplicates in questions
    cursor.execute("SELECT id, title, slug, technology_id, topic_id, difficulty FROM questions")
    questions = cursor.fetchall()

    title_map = defaultdict(list)
    slug_map = defaultdict(list)
    norm_title_map = defaultdict(list)

    for q in questions:
        qid, title, slug, tech_id, topic_id, diff = q
        title_map[title.strip()].append(q)
        slug_map[slug.strip()].append(q)
        norm = "".join(c.lower() for c in title if c.isalnum())
        norm_title_map[norm].append(q)

    exact_title_dupes = {t: qs for t, qs in title_map.items() if len(qs) > 1}
    exact_slug_dupes = {s: qs for s, qs in slug_map.items() if len(qs) > 1}
    near_dupes = {n: qs for n, qs in norm_title_map.items() if len(qs) > 1 and len(set(x[1] for x in qs)) > 1}

    print("\n=== DUPLICATE ANALYSIS ===")
    print(f"Total Questions: {len(questions)}")
    print(f"Exact Title Duplicates: {len(exact_title_dupes)}")
    print(f"Exact Slug Duplicates: {len(exact_slug_dupes)}")
    print(f"Near / Normalized Duplicates: {len(near_dupes)}")

    if exact_title_dupes:
        print("Sample exact duplicates:")
        for t, qs in list(exact_title_dupes.items())[:3]:
            print(f"  Title: '{t}' (count: {len(qs)})")

    # 4. Check Content Quality & Field Completeness
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN short_answer IS NULL OR length(trim(short_answer)) = 0 THEN 1 END) as missing_short,
            COUNT(CASE WHEN interview_ready_answer IS NULL OR length(trim(interview_ready_answer)) = 0 THEN 1 END) as missing_interview,
            COUNT(CASE WHEN deep_explanation IS NULL OR length(trim(deep_explanation)) = 0 THEN 1 END) as missing_deep,
            COUNT(CASE WHEN code_example IS NULL OR length(trim(code_example)) = 0 THEN 1 END) as missing_code,
            COUNT(CASE WHEN why_interviewer_asks IS NULL OR length(trim(why_interviewer_asks)) = 0 THEN 1 END) as missing_why,
            COUNT(CASE WHEN production_considerations IS NULL OR length(trim(production_considerations)) = 0 THEN 1 END) as missing_prod,
            COUNT(CASE WHEN failure_modes IS NULL OR length(trim(failure_modes)) = 0 THEN 1 END) as missing_fail,
            COUNT(CASE WHEN tradeoffs IS NULL OR length(trim(tradeoffs)) = 0 THEN 1 END) as missing_tradeoffs,
            COUNT(CASE WHEN common_mistakes IS NULL OR common_mistakes = '[]' THEN 1 END) as missing_mistakes
        FROM questions
    """)
    cq = cursor.fetchone()
    print("\n=== CONTENT QUALITY / FIELD COMPLETENESS ===")
    print(f"  Missing short_answer: {cq[0]}")
    print(f"  Missing interview_ready_answer: {cq[1]}")
    print(f"  Missing deep_explanation: {cq[2]}")
    print(f"  Missing code_example: {cq[3]}")
    print(f"  Missing why_interviewer_asks: {cq[4]}")
    print(f"  Missing production_considerations: {cq[5]}")
    print(f"  Missing failure_modes: {cq[6]}")
    print(f"  Missing tradeoffs: {cq[7]}")
    print(f"  Missing common_mistakes: {cq[8]}")

    # 5. Technology x Topic Matrix
    cursor.execute("""
        SELECT t.name, top.name, top.slug, COUNT(q.id)
        FROM technologies t
        JOIN topics top ON t.id = top.technology_id
        LEFT JOIN questions q ON top.id = q.topic_id
        GROUP BY top.id
        ORDER BY t.name, top.order_index
    """)
    matrix = cursor.fetchall()
    print("\n=== TOPIC COVERAGE MATRIX ===")
    curr_tech = ""
    for r in matrix:
        tech, top_name, top_slug, count = r
        if tech != curr_tech:
            curr_tech = tech
            print(f"\n{tech}:")
        print(f"  - {top_name} ({top_slug}): {count} questions")

    conn.close()

if __name__ == "__main__":
    main()
