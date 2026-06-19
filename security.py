import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime

ph = PasswordHasher()
DB_NAME = "users.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL,
        attempts INTEGER DEFAULT 0,
        last_login TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_default_user():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not cursor.fetchone():
        hashed_pw = ph.hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", hashed_pw)
        )
        conn.commit()

    conn.close()


def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash, attempts FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return False, "User not found", 0

    password_hash, attempts = result

    if attempts >= 5:
        conn.close()
        return False, "Account locked (too many attempts)", attempts

    try:
        ph.verify(password_hash, password)

        previous_attempts = attempts

        cursor.execute("""
        UPDATE users
        SET attempts = 0, last_login = ?
        WHERE username = ?
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))

        conn.commit()
        conn.close()

        return True, "Login successful", previous_attempts

    except VerifyMismatchError:
        cursor.execute("""
        UPDATE users
        SET attempts = attempts + 1
        WHERE username = ?
        """, (username,))
        conn.commit()
        conn.close()

        return False, "Incorrect password", attempts + 1


def get_user_info(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT attempts, last_login FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    conn.close()
    return result


def change_password(username, new_password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    new_hash = ph.hash(new_password)

    cursor.execute("""
    UPDATE users
    SET password_hash = ?
    WHERE username = ?
    """, (new_hash, username))

    conn.commit()
    conn.close()
