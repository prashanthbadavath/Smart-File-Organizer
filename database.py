import sqlite3

DB_NAME = "file_history.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        old_location TEXT,
        new_location TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_history(file_name, old_location, new_location, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history (file_name, old_location, new_location, date)
    VALUES (?, ?, ?, ?)
    """, (file_name, old_location, new_location, date))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")

    data = cursor.fetchall()

    conn.close()

    return data


def clear_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")

    conn.commit()
    conn.close()


def get_last_record():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, file_name, old_location, new_location
        FROM history
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row


create_database()