"""
s5_query_vectorstore.py

Interactive debug / utility tool for querying your vectorstore without running the full RAG chain.

Features:
  1) Search vectorstore (default top_k=30)
  2) Stats (total chunks, unique files/sources, db type, cache dir, on-disk size)
  3) List docs + chunk counts (optionally top N)
  4) Show config snapshot

Usage:
  python s5_query_vectorstore.py
  python s5_query_vectorstore.py --dir "D:/path/to/vector_cache"   (override cfg.VECTOR_CACHE_DIR)

"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from collections import Counter
from typing import Optional, Dict, Any, List, Tuple

from lifepim_ai_core.core.llm_runtime import config as cfg

# Vector stores
from langchain_community.vectorstores import FAISS, Chroma


# -----------------------------
# Embeddings (from config)
# -----------------------------
def build_embeddings():
    model = getattr(cfg, "EMBED_MODEL", "").lower().strip()

    if model == "openai":
        from langchain_openai import OpenAIEmbeddings

        # NOTE: if you ever use this, it is not "fully local"
        return OpenAIEmbeddings(model="text-embedding-3-small")

    if model == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if model == "nomic-embed-text":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(model=getattr(cfg, "EMBED_MODEL"))

    raise ValueError(f"Unsupported embedding model: {getattr(cfg, 'EMBED_MODEL', None)}")


# -----------------------------
# Vectorstore loader
# -----------------------------
def load_vectorstore(vector_dir: str, embeddings):
    vector_db = getattr(cfg, "VECTOR_DB", "").lower().strip()

    if not vector_db:
        raise ValueError("cfg.VECTOR_DB is not set.")

    if not vector_dir:
        raise ValueError("Vectorstore directory is empty.")

    if not os.path.exists(vector_dir):
        raise FileNotFoundError(f"Vectorstore cache not found at: {vector_dir}")

    if vector_db == "faiss":
        return FAISS.load_local(
            vector_dir,
            embeddings,
            allow_dangerous_deserialization=True,  # langchain uses pickle for FAISS docstore
        )

    if vector_db == "chroma":
        return Chroma(persist_directory=vector_dir, embedding_function=embeddings)

    raise ValueError(f"Unsupported vector DB: {getattr(cfg, 'VECTOR_DB', None)}")


# -----------------------------
# Helpers
# -----------------------------
def human_bytes(n: int) -> str:
    step = 1024.0
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(n)
    for u in units:
        if size < step:
            return f"{size:.1f} {u}"
        size /= step
    return f"{size:.1f} PB"


def dir_size_bytes(path: str) -> int:
    p = Path(path)
    if not p.exists():
        return 0
    total = 0
    for fp in p.rglob("*"):
        if fp.is_file():
            try:
                total += fp.stat().st_size
            except OSError:
                pass
    return total


def prompt_int(msg: str, default: int) -> int:
    raw = input(f"{msg} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("Invalid number; using default.")
        return default


def prompt_str(msg: str, default: str = "") -> str:
    raw = input(f"{msg}{' [' + default + ']' if default else ''}: ").strip()
    return raw if raw else default


def safe_meta(doc) -> Dict[str, Any]:
    try:
        return doc.metadata or {}
    except Exception:
        return {}


# -----------------------------
# Chroma metadata scan (batched)
# -----------------------------
def chroma_source_counts_batched(vs, batch_size: int = 5000) -> Counter:
    """
    Returns chunk counts per 'source' metadata key for Chroma.
    Uses vs.get(limit=..., offset=..., include=["metadatas"]) in batches.
    """
    counter = Counter()

    # Fast count if possible
    total = None
    try:
        total = int(vs._collection.count())  # type: ignore[attr-defined]
    except Exception:
        pass

    # If we can't count cheaply, we still can try a first batch and then loop until empty.
    offset = 0
    seen_any = False

    while True:
        kwargs = {"include": ["metadatas"], "limit": batch_size, "offset": offset}
        try:
            data = vs.get(**kwargs)
        except TypeError:
            # Older signature: vs.get(include=[...]) only (no paging)
            data = vs.get(include=["metadatas"])
            metadatas = data.get("metadatas", []) or []
            for m in metadatas:
                src = (m or {}).get("source", "Unknown")
                counter[src] += 1
            return counter

        metadatas = data.get("metadatas", []) or []
        if not metadatas:
            break

        seen_any = True
        for m in metadatas:
            src = (m or {}).get("source", "Unknown")
            counter[src] += 1

        offset += len(metadatas)

        if total is not None and offset >= total:
            break

        # If total unknown, stop when last batch was smaller than batch_size
        if total is None and len(metadatas) < batch_size:
            break

    if not seen_any:
        return Counter()

    return counter


# -----------------------------
# Actions
# -----------------------------
def action_search(vs):
    query = prompt_str("Query text", "")
    if not query:
        print("No query entered.")
        return

    top_k = prompt_int("Top K results", 30)

    t0 = time.time()
    results = vs.similarity_search(query, k=top_k)
    dt = time.time() - t0

    # --- Deduplicate by (file_id, chunk_id) ---
    seen = set()
    unique_results = []

    for doc in results:
        meta = safe_meta(doc)
        file_id = meta.get("file_id", meta.get("source", "UNKNOWN"))
        chunk_id = meta.get("chunk_id", meta.get("chunk"))

        key = (file_id, chunk_id)
        if key in seen:
            continue

        seen.add(key)
        unique_results.append(doc)

    print(f"\nRetrieved {len(unique_results)} unique chunks in {dt:.2f}s\n")

    for i, doc in enumerate(unique_results, start=1):
        meta = safe_meta(doc)
        src = meta.get("source", "Unknown")
        chunk_id = meta.get("chunk_id", meta.get("chunk", "N/A"))
        file_id = meta.get("file_id", "N/A")

        text = (doc.page_content or "").replace("\n", " ").strip()
        snippet = text[:300] + ("..." if len(text) > 300 else "")

        print(f"{i:02d}. Source: {src}")
        print(f"    Chunk ID: {chunk_id} | File ID: {file_id}")
        print(f"    Snippet: {snippet}\n")


def action_stats(vs, vector_dir: str):
    vector_db = getattr(cfg, "VECTOR_DB", "Unknown")
    embed_model = getattr(cfg, "EMBED_MODEL", "Unknown")

    on_disk = dir_size_bytes(vector_dir)

    total_chunks = None
    unique_sources = None

    if str(vector_db).lower() == "chroma":
        try:
            total_chunks = int(vs._collection.count())  # type: ignore[attr-defined]
        except Exception:
            total_chunks = None

        bs = prompt_int("Batch size", 5000)
        counter = chroma_source_counts_batched(vs, batch_size=bs)
        unique_sources = len(counter)
        print("\nTop sources by chunk count:")
        for src, cnt in counter.most_common(30):
            print(f"  {cnt:7d}  {src}")

    elif str(vector_db).lower() == "faiss":
        # FAISS: docstore holds Documents
        try:
            docstore = vs.docstore._dict  # type: ignore[attr-defined]
            total_chunks = len(docstore)
        except Exception:
            total_chunks = None

        counter = Counter()
        try:
            for _id, doc in vs.docstore._dict.items():  # type: ignore[attr-defined]
                meta = safe_meta(doc)
                src = meta.get("source", "Unknown")
                counter[src] += 1
            unique_sources = len(counter)
            print("\nTop sources by chunk count:")
            for src, cnt in counter.most_common(30):
                print(f"  {cnt:7d}  {src}")
        except Exception as e:
            print(f"Could not scan FAISS docstore: {e}")

    print("\n--- Vectorstore Stats ---")
    print(f"DB Type          : {vector_db}")
    print(f"Embed Model      : {embed_model}")
    print(f"Cache Dir        : {vector_dir}")
    print(f"On-disk size     : {human_bytes(on_disk)}")
    if total_chunks is not None:
        print(f"Total chunks     : {total_chunks}")
    else:
        print("Total chunks     : (unknown)")
    if unique_sources is not None:
        print(f"Unique sources   : {unique_sources}")
    print("-------------------------\n")


def action_list_docs(vs):
    vector_db = getattr(cfg, "VECTOR_DB", "").lower().strip()
    top_n = prompt_int("Show top N sources by chunk count", 50)

    counter = Counter()

    if vector_db == "chroma":
        bs = prompt_int("Batch size for metadata scan", 5000)
        counter = chroma_source_counts_batched(vs, batch_size=bs)

    elif vector_db == "faiss":
        try:
            for _id, doc in vs.docstore._dict.items():  # type: ignore[attr-defined]
                src = safe_meta(doc).get("source", "Unknown")
                counter[src] += 1
        except Exception as e:
            print(f"Could not scan FAISS docstore: {e}")
            return
    else:
        print(f"Unsupported vector DB: {getattr(cfg, 'VECTOR_DB', None)}")
        return

    if not counter:
        print("No documents/sources found (or metadata missing).")
        return

    print(f"\nUnique sources: {len(counter)}")
    print(f"Top {min(top_n, len(counter))} sources:\n")
    for src, cnt in counter.most_common(top_n):
        print(f"{cnt:7d}  {src}")
    print("")


def action_show_config(vector_dir: str):
    # Print a focused snapshot of likely-relevant config vars if present
    keys = [
        "VECTOR_DB",
        "VECTOR_CACHE_DIR",
        "DOCS_DIR",
        "EMBED_MODEL",
        "PROVIDER",
        "CHUNK_SIZE",
        "CHUNK_OVERLAP",
        "TOP_K",
        "RERANK_TOP_K",
        "MAX_TOKENS",
        "TEMPERATURE",
    ]

    print("\n--- Config Snapshot ---")
    for k in keys:
        if hasattr(cfg, k):
            print(f"{k:16} : {getattr(cfg, k)}")
    print(f"{'ACTIVE_DIR':16} : {vector_dir}")
    print("-----------------------\n")


# -----------------------------
# Main menu
# -----------------------------
def parse_cli_dir(argv: List[str]) -> Optional[str]:
    if "--dir" in argv:
        i = argv.index("--dir")
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def main():
    override_dir = parse_cli_dir(sys.argv[1:])
    vector_dir = override_dir or getattr(cfg, "VECTOR_CACHE_DIR", "")

    if not vector_dir:
        print("Error: cfg.VECTOR_CACHE_DIR is not set and no --dir override was provided.")
        sys.exit(1)

    embeddings = build_embeddings()

    # Lazy-load VS so menu can change dir without restarting
    vs = None

    def ensure_vs() -> Tuple[object, str]:
        nonlocal vs, vector_dir
        if vs is None:
            t0 = time.time()
            vs = load_vectorstore(vector_dir, embeddings)
            print(f"Loaded vectorstore in {time.time() - t0:.2f}s")
        return vs, vector_dir

    while True:
        print("\n=== Vectorstore Debug Menu ===")
        print("1) Search (similarity)")
        print("2) Stats (counts, size, optional per-source scan)")
        print("3) List docs/sources + chunk counts")
        print("4) Show config snapshot")
        print("5) Change vectorstore dir (override for this session)")
        print("0) Exit")
        choice = input("Select: ").strip()

        if choice == "0":
            print("Bye.")
            break

        if choice == "5":
            new_dir = prompt_str("New vectorstore dir", vector_dir)
            if not os.path.exists(new_dir):
                print(f"Directory does not exist: {new_dir}")
                continue
            vector_dir = new_dir
            vs = None  # force reload
            print("OK — directory updated (will reload on next action).")
            continue

        try:
            vs_obj, active_dir = ensure_vs()
        except Exception as e:
            print(f"Failed to load vectorstore: {e}")
            vs = None
            continue

        if choice == "1":
            action_search(vs_obj)
        elif choice == "2":
            action_stats(vs_obj, active_dir)
        elif choice == "3":
            action_list_docs(vs_obj)
        elif choice == "4":
            action_show_config(active_dir)
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
