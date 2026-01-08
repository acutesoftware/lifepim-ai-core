# default config file for lifepim-ai-core #
#
# REPO_ROOT = Path(__file__).resolve().parents[1]  # adjust depth if needed
# Example depths:
# .parents[0]  # same as .parent
# .parents[1]  # parent of parent
# .parents[2]  # grandparent
#
#

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]  # adjust depth if needed

DOCS_FOLDER = REPO_ROOT / "docs"  # this has a folder 'sample_docs' to show how doc types are ingested

VECTOR_CACHE_DIR = REPO_ROOT / "my_app" / "my_vectorstore"

DB_FILE_METADATA = VECTOR_CACHE_DIR / "metadata.db"
DB_FILE = VECTOR_CACHE_DIR / "chat_memory.db"

#  change your settings here

EMBED_MODEL = "nomic-embed-text"  # new embedding 30/12/2025 - should take longer to build be faster to query
# EMBED_MODEL = "huggingface"   # this was the original embedding, works fine
PROVIDER = "ollama"
MODEL_NAME = "gpt-oss:20b"
TEMPERATURE = 0.67
MAX_TOKENS = 512    # 256 is FAST, 512 is ok but slower - this is how much the model uses internally
MAX_CONTEXT_MESSAGES = 5  # adjust as needed (num chats before summarisation)
TOP_K = 5   # number of RAG search result docs. DONT increase to 10+ or you confuse model due to too many tokens
RAG_TOP_K = TOP_K
EFFECTIVE_CONTEXT_LIMIT = 2200  # safe limit for number of TOKENS going into system prompt

# needs rebuild if you change the ones below
VECTOR_DB = "faiss"
CHUNK_SIZE = 351
CHUNK_OVERLAP = 40

DEFAULT_FIELDS = [
    "REPO_ROOT",
    "DOCS_FOLDER",
    "VECTOR_CACHE_DIR",
    "DB_FILE_METADATA",
    "DB_FILE",
    "EMBED_MODEL",
    "PROVIDER",
    "MODEL_NAME",
    "TEMPERATURE",
    "MAX_TOKENS",
    "MAX_CONTEXT_MESSAGES",
    "TOP_K",
    "RAG_TOP_K",
    "EFFECTIVE_CONTEXT_LIMIT",
    "VECTOR_DB",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
]
