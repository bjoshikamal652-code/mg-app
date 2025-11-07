import sqlite3

conn= sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, contact_number TEXT UNIQUE)""")
conn.commit()

def register(email, contact_number):
    try:
        if email and contact_number:
            cursor.execute("INSERT INTO users (email, contact_number) VALUES (?, ?)", (email, contact_number))
        elif email:
            cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
        elif contact_number:
            cursor.execute("INSERT INTO users (contact_number) VALUES (?)", (contact_number,))
        else:
            return False  # nothing to insert
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login(email, contact_number):
    if email and contact_number:
        cursor.execute("SELECT * FROM users WHERE email = ? AND contact_number = ?", (email, contact_number))
    elif email:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    elif contact_number:
        cursor.execute("SELECT * FROM users WHERE contact_number = ?", (contact_number,))
    else:
        return None
    return cursor.fetchone()

def home(email, contact_number):
    if email and contact_number:
        cursor.execute("SELECT * FROM users WHERE email = ? AND contact_number = ?", (email, contact_number,))
    elif email:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    elif contact_number:
        cursor.execute("SELECT * FROM users WHERE email = ?", (contact_number,))
    else:
        return None
    return cursor.fetchone()
