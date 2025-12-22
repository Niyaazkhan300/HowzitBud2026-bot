import os
import sqlite3 as lite

class DatabaseManager:
    def __init__(self, path: str):
        # Ensure parent directory exists
        db_dir = os.path.dirname(path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # Connect to SQLite file (creates it if missing)
        self.conn = lite.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Example tables — adjust to your bot’s needs
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            balance REAL DEFAULT 0
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product TEXT,
            quantity INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        self.conn.commit()

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass
