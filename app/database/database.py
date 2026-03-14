import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import pool

connection_pool: pool.SimpleConnectionPool | None = None


def init_db():
    conn = None
    try:
            conn = get_connection()

            with conn.cursor() as cursor:
                cursor.execute("""
                               CREATE TABLE IF NOT EXISTS analyses (
                                                                       id SERIAL PRIMARY KEY,
                                                                       text TEXT,
                                                                       analysis TEXT,
                                                                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                               )
                               """)
    finally:
        if conn:
            release_connection(conn)


def init_pool():
    global connection_pool

    database_url = os.getenv("DATABASE_URL")

    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=database_url
    )

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)

def save_analysis(input_text:str, analysis:str):
    conn = None
    try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                               INSERT INTO analyses (text, analysis)
                               VALUES (%s, %s)
                               """, (input_text, analysis))
            conn.commit()
    finally:
        if conn:
            release_connection(conn)


def get_all_analyses(limit: int = 10):
    conn = None
    try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                               SELECT id, text, analysis, created_at
                               FROM analyses
                               ORDER BY created_at DESC
                                   LIMIT %s
                               """, (limit,))

                rows = cursor.fetchall()
    finally:
        if conn:
            release_connection(conn)

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
    conn = None
    try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                               SELECT id, text, analysis, created_at
                               FROM analyses
                               WHERE id = %s
                               """, (analysis_id,))

                row = cursor.fetchone()
    finally:
        if conn:
            release_connection(conn)

    if row is None:
        return None

    return {
        "id": row[0],
        "input_text": row[1],
        "analysis": row[2],
        "created_at": row[3]
    }

