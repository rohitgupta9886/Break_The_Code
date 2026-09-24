import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "breakthecode.db")
if not os.path.exists(db_path):
    # Check parent dir
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "breakthecode.db")

print(f"Connecting to {db_path}...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

indexes = [
    "CREATE INDEX IF NOT EXISTS ix_questions_tech_status ON questions(technology_id, status);",
    "CREATE INDEX IF NOT EXISTS ix_questions_diff_status ON questions(difficulty, status);",
    "CREATE INDEX IF NOT EXISTS ix_questions_tech_diff_status ON questions(technology_id, difficulty, status);",
    "CREATE INDEX IF NOT EXISTS ix_questions_created_at_desc ON questions(created_at DESC);",
    "CREATE INDEX IF NOT EXISTS ix_topics_technology_id ON topics(technology_id);",
    "CREATE INDEX IF NOT EXISTS ix_bookmarks_user_question ON bookmarks(user_id, question_id);",
    "CREATE INDEX IF NOT EXISTS ix_user_progress_user_tech ON user_progress(user_id, technology_id);",
    "CREATE INDEX IF NOT EXISTS ix_user_attempts_user_created ON user_attempts(user_id, created_at DESC);"
]

for idx_sql in indexes:
    try:
        cursor.execute(idx_sql)
        print(f"Executed: {idx_sql}")
    except Exception as e:
        print(f"Index error: {e}")

conn.commit()
conn.close()
print("All indexes applied successfully.")
