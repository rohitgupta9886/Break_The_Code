import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "breakthecode.db")
db_path = os.path.abspath(db_path)

print(f"Migrating database at: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check and add users.last_active_date
cursor.execute("PRAGMA table_info(users)")
user_cols = [row[1] for row in cursor.fetchall()]
if "last_active_date" not in user_cols:
    print("Adding last_active_date column to users table...")
    cursor.execute("ALTER TABLE users ADD COLUMN last_active_date DATETIME")
    print("Added last_active_date successfully.")

# Check and add user_attempts.xp_earned
cursor.execute("PRAGMA table_info(user_attempts)")
attempt_cols = [row[1] for row in cursor.fetchall()]
if "xp_earned" not in attempt_cols:
    print("Adding xp_earned column to user_attempts table...")
    cursor.execute("ALTER TABLE user_attempts ADD COLUMN xp_earned INTEGER DEFAULT 0")
    print("Added xp_earned successfully.")

# Create spaced_repetition_cards table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS spaced_repetition_cards (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    question_id VARCHAR(36) NOT NULL,
    repetitions INTEGER NOT NULL DEFAULT 0,
    interval_days FLOAT NOT NULL DEFAULT 1.0,
    ease_factor FLOAT NOT NULL DEFAULT 2.5,
    next_review_at DATETIME NOT NULL,
    last_reviewed_at DATETIME,
    last_score FLOAT,
    status VARCHAR(20) NOT NULL DEFAULT 'LEARNING',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(question_id) REFERENCES questions(id) ON DELETE CASCADE
)
""")
cursor.execute("CREATE INDEX IF NOT EXISTS ix_spaced_repetition_cards_user_id ON spaced_repetition_cards (user_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS ix_spaced_repetition_cards_next_review_at ON spaced_repetition_cards (next_review_at)")
print("spaced_repetition_cards table verified.")

# Create user_badges table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_badges (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    badge_key VARCHAR(50) NOT NULL,
    badge_name VARCHAR(100) NOT NULL,
    badge_description VARCHAR(255) NOT NULL,
    icon VARCHAR(50) NOT NULL DEFAULT 'Trophy',
    unlocked_at DATETIME NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")
cursor.execute("CREATE INDEX IF NOT EXISTS ix_user_badges_user_id ON user_badges (user_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS ix_user_badges_badge_key ON user_badges (badge_key)")
print("user_badges table verified.")

conn.commit()
conn.close()
print("Migration completed successfully.")
