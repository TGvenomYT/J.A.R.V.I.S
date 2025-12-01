import sqlite3
from datetime import datetime

def create_connection():
    conn = sqlite3.connect('chat_history.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            jarvis_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_conversation(user_input, jarvis_response):
    """Save user and Jarvis conversation to database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (user_input, jarvis_response)
        VALUES (?, ?)
    ''', (user_input, jarvis_response))
    conn.commit()
    conn.close()

def fetch_conversations():
    """Retrieve the last 50 conversations from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_input, jarvis_response, timestamp FROM chat_history ORDER BY id DESC LIMIT 50")
    conversations = cursor.fetchall()
    conn.close()
    return conversations

# Create the table when the module is imported
create_table()
