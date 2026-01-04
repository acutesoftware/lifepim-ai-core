import sqlite3

def reset_table(db_path: str, table_name: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name}")
    conn.commit()
    conn.close()
    print(f"Cleared table {table_name}")

def reset_all(db_path: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM files")
    cur.execute("DELETE FROM document_chunks")
    cur.execute("DELETE FROM chunk_stats")
    conn.commit()
    conn.close()
    print("Cleared all tables")
