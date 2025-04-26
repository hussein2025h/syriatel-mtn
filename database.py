import sqlite3
from datetime import datetime

DB_NAME = "requests.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        number TEXT,
        amount TEXT,
        operator TEXT,
        status TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_request(user_id, username, number, amount, operator):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO requests (user_id, username, number, amount, operator, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, username, number, amount, operator, "بانتظار", datetime.now().isoformat()))
    conn.commit()
    conn.close()

def update_status(user_id, status):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE requests SET status = ? WHERE user_id = ? AND status = 'بانتظار'", (status, user_id))
    conn.commit()
    conn.close()
