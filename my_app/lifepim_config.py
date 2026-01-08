from pathlib import Path

# Sample user config overrides for LifePIM AI Core.
# Edit this file to point at your own docs folder or tune model settings.

REPO_ROOT = Path(__file__).resolve().parents[1]

DOCS_FOLDER = REPO_ROOT / "docs"
VECTOR_CACHE_DIR = REPO_ROOT / "my_app" / "my_vectorstore" # DEFAULT - works after rebuild on \docs\
#VECTOR_CACHE_DIR = r"E:\TEMP_PROCESS\rag_vectorcache\all_notes"  # vectorstore built - search TOK
#VECTOR_CACHE_DIR = r"E:\TEMP_PROCESS\rag_vectorcache\ebooks"  # chunks extracted, needs vectorstore built

DB_FILE_METADATA = VECTOR_CACHE_DIR / "metadata.db"
DB_FILE = VECTOR_CACHE_DIR / "chat_memory.db"


EMBED_MODEL = "nomic-embed-text"
MODEL_NAME = "gpt-oss:20b"
TEMPERATURE = 0.2
MAX_TOKENS = 256    # 256 is FAST, 512 is ok but slower - this is how much the model uses internally
TOP_K = 5
RAG_TOP_K = TOP_K
