import sqlite3

def run_inspection():
    conn = sqlite3.connect('backend/breakthecode.db')
    cur = conn.cursor()
    print("=== QUESTIONS PER TECHNOLOGY ===")
    cur.execute('''
        SELECT t.name, t.slug, count(q.id) 
        FROM technologies t 
        LEFT JOIN topics tp ON tp.technology_id = t.id 
        LEFT JOIN questions q ON q.topic_id = tp.id 
        GROUP BY t.id
    ''')
    for row in cur.fetchall():
        print(f"  {row[0]} ({row[1]}): {row[2]} questions")

    print("\n=== QUESTIONS PER TOPIC ===")
    cur.execute('''
        SELECT t.slug, tp.slug, tp.name, count(q.id)
        FROM topics tp
        JOIN technologies t ON tp.technology_id = t.id
        LEFT JOIN questions q ON q.topic_id = tp.id
        GROUP BY tp.id
        ORDER BY t.slug, count(q.id) ASC
    ''')
    for row in cur.fetchall():
        print(f"  [{row[0]}] {row[1]} ({row[2]}): {row[3]} questions")

    print("\n=== QUESTIONS PER DIFFICULTY ===")
    cur.execute('SELECT difficulty, count(*) FROM questions GROUP BY difficulty ORDER BY count(*) DESC')
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

    conn.close()

if __name__ == '__main__':
    run_inspection()
