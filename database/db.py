import sqlite3

conn = sqlite3.connect("imatter.db")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT UNIQUE,
            password TEXT,
            security_question TEXT,
            security_answer TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT,
            phone TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()

def get_all_contacts(user_id):
    cursor.execute("SELECT * FROM contacts WHERE user_id=?", (user_id,))
    return cursor.fetchall()

def insert_contact(user_id, name, phone):
    cursor.execute("INSERT INTO contacts(user_id, name, phone) VALUES (?, ?, ?)", (user_id, name, phone))
    conn.commit()

def update_contact(contact_id, name, phone):
    cursor.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, contact_id))
    conn.commit()

def delete_contact(contact_id):
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()

# --- User functions ---

def get_user_by_mobile(mobile):
    cursor.execute("SELECT * FROM users WHERE mobile=?", (mobile,))
    return cursor.fetchone()
    # returns: (id, mobile, password, security_question, security_answer)
    #           [0]   [1]      [2]          [3]                [4]

def create_user(mobile, password, security_question, security_answer):
    cursor.execute(
        "INSERT INTO users(mobile, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
        (mobile, password, security_question, security_answer)
    )
    conn.commit()

def update_user_password(mobile, new_password):
    cursor.execute("UPDATE users SET password=? WHERE mobile=?", (new_password, mobile))
    conn.commit()