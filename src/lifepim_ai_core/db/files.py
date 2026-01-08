import sqlite3
from typing import Dict, Any, List


def insert_many_files(db_path: str, files_to_insert: list):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.executemany("""
            INSERT INTO files (file_path, file_name, file_type, file_size, 
                        date_modified, date_created, date_accessed, file_owner)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, files_to_insert)

def insert_file(db_path: str, file_metadata: Dict[str, Any]) -> int:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO files (file_path, file_name, file_type, file_size, 
                        date_modified, date_created, date_accessed, file_owner)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        file_metadata["file_path"],
        file_metadata.get("file_name"),
        file_metadata.get("file_type"),
        file_metadata.get("file_size"),
        file_metadata.get("last_modified"),
    ))
    conn.commit()
    file_id = cur.lastrowid
    conn.close()
    return file_id

def get_all_files(db_path: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM files")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
