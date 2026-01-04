import sqlite3
from typing import Dict, Any, List

def insert_many_stats(db_path: str, stats_to_insert: list):
    """
    Inserts a list of stats into the database efficiently using a single transaction.
    
    Args:
        db_path (str): Path to the SQLite database.
        stats_to_insert (list): A list of tuples, where each tuple is
                                (chunk_id, stat_name, stat_value).
    """
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        
        cur.executemany("""
            INSERT INTO chunk_stats (chunk_id, stat_name, stat_value)
            VALUES (?, ?, ?)
        """, stats_to_insert)


def insert_stat(db_path: str, chunk_id: int, stat_name: str, stat_value: float) -> int:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    print('WARNING DJM - dont use this function - use insert_many_stats instead')
    cur.execute("""
        INSERT INTO chunk_stats (chunk_id, stat_name, stat_value)
        VALUES (?, ?, ?)
    """, (chunk_id, stat_name, stat_value))
    conn.commit()
    stat_id = cur.lastrowid
    conn.close()
    return stat_id

def get_stats_for_chunk(db_path: str, chunk_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM chunk_stats WHERE chunk_id=?", (chunk_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
