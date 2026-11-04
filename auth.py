import sqlite3
from datetime import datetime, timedelta, timezone

from database import DB_PATH, get_user
from security import verify_password

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 60


def authenticate_user(username, password):
    user = get_user(username)

    if user is None:
        return False, "Invalid username or password."

    # Vulnerable account: deliberately has no lockout protection
    if user["security_mode"] == "vulnerable":
        if password == user["password"]:
            return True, "Login successful!"

        return False, "Incorrect password."

    # Protected account: check lockout status
    now = datetime.now(timezone.utc)

    if user["locked_until"]:
        lock_time = datetime.fromisoformat(user["locked_until"])

        if now < lock_time:
            remaining = int((lock_time - now).total_seconds()) + 1
            return False, f"Account locked! Try again in {remaining} seconds."

    # Check Argon2 password hash
    if verify_password(user["password_hash"], password):

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users
            SET failed_attempts = 0, locked_until = NULL
            WHERE username = ?
        """, (username,))

        connection.commit()
        connection.close()

        return True, "Login successful! Account is protected."

    # Incorrect password
    attempts = user["failed_attempts"] + 1

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if attempts >= MAX_ATTEMPTS:
        lock_time = now + timedelta(seconds=LOCKOUT_SECONDS)

        cursor.execute("""
            UPDATE users
            SET failed_attempts = ?, locked_until = ?
            WHERE username = ?
        """, (attempts, lock_time.isoformat(), username))

        message = "Too many failed attempts! Account locked for 60 seconds."

    else:
        cursor.execute("""
            UPDATE users
            SET failed_attempts = ?
            WHERE username = ?
        """, (attempts, username))

        message = f"Incorrect password. Attempts: {attempts}/{MAX_ATTEMPTS}"

    connection.commit()
    connection.close()

    return False, message