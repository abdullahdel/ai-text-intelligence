import os
from psycopg2 import pool
from app.utils.logger import logger


connection_pool: pool.SimpleConnectionPool | None = None


def init_db():
    conn = None
    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            logger.info("creating database table")

            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS analyses (
                                                                   id SERIAL PRIMARY KEY,
                                                                   text TEXT,
                                                                   analysis TEXT,
                                                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                           """)

            cursor.execute("""
                           ALTER TABLE analyses
                               ADD COLUMN IF NOT EXISTS source_type TEXT NOT NULL DEFAULT 'manual'
                           """)

            cursor.execute("""
                           ALTER TABLE analyses
                               ADD COLUMN IF NOT EXISTS source_name TEXT
                           """)

        conn.commit()

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

def save_analysis(input_text:str, analysis:str, source_type="manual", source_name=None):
    conn = None
    try:
            conn = get_connection()
            with conn.cursor() as cursor:
                logger.info("Saving analysis to database")
                cursor.execute("""
                               INSERT INTO analyses (text, analysis, source_type, source_name)
                               VALUES (%s, %s, %s, %s)
                               """, (input_text, analysis, source_type, source_name))
            conn.commit()
    finally:
        if conn:
            release_connection(conn)


def get_all_analyses(limit: int = 10, offset: int = 0):
    conn = None
    try:
            conn = get_connection()
            with conn.cursor() as cursor:
                logger.info("Fetching analyses from database")
                cursor.execute("""
                               SELECT id, text, analysis, source_type, source_name, created_at
                               FROM analyses
                               ORDER BY created_at DESC
                                LIMIT %s
                               OFFSET %s
                               """, (limit,offset))

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
            "source_type": row[3],
            "source_name": row[4],
            "created_at": row[5].isoformat()
        })

    return analyses


def get_analysis_by_id(analysis_id: int):
    conn = None
    try:
            conn = get_connection()
            with conn.cursor() as cursor:
                logger.info("query analyses by id from database")
                cursor.execute("""
                               SELECT id, text, analysis, source_type, source_name, created_at
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
        "source_type": row[3],
        "source_name": row[4],
        "created_at": row[5].isoformat()
    }

def delete_analysis(analysis_id: int):
    conn = None
    try:
        logger.info("Deleting analysis from database")
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM analyses
                WHERE id = %s
            """,(analysis_id,))

        conn.commit()

    finally:
        if conn:
            release_connection(conn)
