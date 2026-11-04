import sqlite3
from pathlib import Path

from security import hash_password

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT,
            password_hash TEXT,
            security_mode TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            locked_until TEXT
        )
    """)

    # Update an existing database if these columns are missing
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if "failed_attempts" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0"
        )

    if "locked_until" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN locked_until TEXT"
        )

    connection.commit()
    connection.close()


def create_demo_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, password_hash, security_mode)
        VALUES (?, ?, ?, ?)
    """, ("weak_user", "cat123", None, "vulnerable"))

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, password_hash, security_mode)
        VALUES (?, ?, ?, ?)
    """, (
        "secure_user",
        None,
        hash_password("StrongDemo@123"),
        "protected"
    ))

    connection.commit()
    connection.close()


def get_user(username):
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    return user


if __name__ == "__main__":
    initialize_database()
    create_demo_users()

    print("BruteForceX database initialized successfully!")
    print("Demo accounts created successfully!")