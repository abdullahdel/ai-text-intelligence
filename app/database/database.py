import psycopg2
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(database_url)

def init_db():
    DATA_DIR.mkdir(exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS analyses (
                                                           id SERIAL PRIMARY KEY,
                                                           text TEXT,
                                                           analysis TEXT,
                                                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   """)

    conn.commit()
    conn.close()

def save_analysis(input_text:str, analysis:str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO analyses (text, analysis)
                   VALUES (%s, %s)
                   """, (input_text, analysis))

    conn.commit()
    conn.close()

def get_all_analyses(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT id, text, analysis, created_at
                   FROM analyses
                   ORDER BY created_at DESC
                       LIMIT %s
                   """, (limit,))

    rows = cursor.fetchall()
    analyses = []
    for row in rows:
        analyses.append({
            "id": row[0],
            "input_text": row[1],
            "analysis": row[2],
            "created_at": row[3]
        })

    conn.close()
    return analyses

def get_analysis_by_id(analysis_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT id, text, analysis, created_at
                   FROM analyses
                   WHERE id = %s
                   """, (analysis_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "input_text": row[1],
        "analysis": row[2],
        "created_at": row[3]
    }

