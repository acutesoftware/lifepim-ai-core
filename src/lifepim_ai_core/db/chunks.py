import sqlite3
from typing import Dict, Any, List

def insert_chunk(db_path: str, file_id: int, chunk_index: int, chunk_text: str) -> int:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO document_chunks (file_id, chunk_index, chunk_text)
        VALUES (?, ?, ?)
    """, (file_id, chunk_index, chunk_text))
    conn.commit()
    chunk_id = cur.lastrowid
    conn.close()
    return chunk_id


def get_chunks_for_file(db_path: str, file_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM document_chunks WHERE file_id=?", (file_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_chunks(db_path: str) -> List[Dict[str, Any]]:
    """
    Return all chunks with file metadata.
    Joins files + chunks so we can embed with full context.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id as chunk_id, c.chunk_text, c.file_id, f.file_path
        FROM document_chunks c
        JOIN files f ON c.file_id = f.id
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
