import sqlite3

def create_database():
    conn = sqlite3.connect("file_history.db")
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

if __name__ == "__main__":
    create_database()
    print("Database created successfully!")
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
    INSERT INTO history(file_name, old_location, new_location, date)
    VALUES (?, ?, ?, ?)
    """, (file_name, old_location, new_location, date))

    conn.commit()
    conn.close()


create_database()
