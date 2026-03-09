import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"

def init_db():
    DATA_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS analyses (
                                                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                           input_text TEXT NOT NULL,
                                                           analysis TEXT NOT NULL,
                                                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   """)

    conn.commit()
    conn.close()

def save_analysis(input_text:str, analysis:str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO analyses (input_text, analysis)
                   VALUES (?, ?)
                   """, (input_text, analysis))

    conn.commit()
    conn.close()

def get_all_analyses(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT * FROM analyses 
                   ORDER BY created_at DESC
                   LIMIT ?
                   """,(limit,))

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

def get_analysis_by_id(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM analyses 
                   WHERE id = ?
                       """,(id,))

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

