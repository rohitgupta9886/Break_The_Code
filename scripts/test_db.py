import sqlite3

conn = sqlite3.connect('backend/breakthecode.db', timeout=5)
print("Connected successfully.")
cur = conn.cursor()
cur.execute('SELECT count(*) FROM questions')
print("Total questions in backend/breakthecode.db:", cur.fetchone()[0])
conn.close()
print("Closed connection.")
