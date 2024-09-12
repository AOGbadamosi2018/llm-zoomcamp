import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="qt_assistant",
        user="your_username",
        password="your_password"
    )

def init_db():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                subject TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                conversation_id TEXT REFERENCES conversations(id),
                feedback INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

def save_conversation(conversation_id, question, answer, subject=None):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO conversations (id, question, answer, subject) VALUES (%s, %s, %s, %s)",
            (conversation_id, question, answer, subject)
        )
    conn.commit()
    conn.close()

def save_feedback(conversation_id, feedback):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO feedback (conversation_id, feedback) VALUES (%s, %s)",
            (conversation_id, feedback)
        )
    conn.commit()
    conn.close()

# Initialize the database when the module is imported
#init_db()