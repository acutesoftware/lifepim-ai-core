import sqlite3

def create_schema_memory(db_path: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    print('created memory database at ' + str(db_path))

def create_schema(db_path: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # FILES table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE,
        file_name TEXT,
        file_type TEXT,
        file_size INTEGER,
        date_modified TIMESTAMP,
        date_created TIMESTAMP,
        date_accessed TIMESTAMP,
        file_owner TEXT
    )
    """)

    # Documents table - list of files processed
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER,
        classif_01 TEXT,
        classif_02 TEXT,
        classif_03 TEXT,
        classif_04 TEXT,
        file_type TEXT,
        rating TEXT,
        num_chunks INTEGER,
        date_refreshed TIMESTAMP
    )
    """)

    # DOCUMENT Chunks table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS document_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER,
        chunk_index INTEGER,
        chunk_text TEXT,
        FOREIGN KEY(file_id) REFERENCES files(id)
    )
    """)

    # CHUNK_STATS table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunk_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk_id INTEGER,
        stat_name TEXT,
        stat_value REAL,
        FOREIGN KEY(chunk_id) REFERENCES document_chunks(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversation_state (
        chat_id TEXT PRIMARY KEY,
        state_json TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()
    print(f"Database schema created at {db_path}")
