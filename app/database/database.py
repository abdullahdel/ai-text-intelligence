import psycopg2
from dotenv import load_dotenv
import os


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(database_url)

def init_db():

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS analyses (
                                                                   id SERIAL PRIMARY KEY,
                                                                   text TEXT,
                                                                   analysis TEXT,
                                                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                           """)



def save_analysis(input_text:str, analysis:str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO analyses (text, analysis)
                           VALUES (%s, %s)
                           """, (input_text, analysis))

def get_all_analyses(limit: int = 10):

    with get_connection() as conn:
        with conn.cursor() as cursor:
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

    return analyses


def get_analysis_by_id(analysis_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT id, text, analysis, created_at
                           FROM analyses
                           WHERE id = %s
                           """, (analysis_id,))

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "input_text": row[1],
        "analysis": row[2],
        "created_at": row[3]
    }

