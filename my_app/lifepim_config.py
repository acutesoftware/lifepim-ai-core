from pathlib import Path

# Sample user config overrides for LifePIM AI Core.
# Edit this file to point at your own docs folder or tune model settings.

REPO_ROOT = Path(__file__).resolve().parents[1]

DOCS_FOLDER = REPO_ROOT / "docs"
VECTOR_CACHE_DIR = REPO_ROOT / "my_app" / "vectorstore"
VECTOR_CACHE_DIR = REPO_ROOT / "tests" / "data" / "sample_vectorstore"

EMBED_MODEL = "nomic-embed-text"
MODEL_NAME = "gpt-oss:20b"
TEMPERATURE = 0.2

TOP_K = 5
RAG_TOP_K = TOP_K
