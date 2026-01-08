import json
import os
import time

from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from lifepim_ai_core.core.llm_runtime import config as cfg
from lifepim_ai_core.db.chunks import get_all_chunks

CHECKPOINT_FILENAME = "vectorstore_build_state.json"
DEFAULT_BATCH_FILES = 50


def build_embeddings():
    if cfg.EMBED_MODEL.lower() == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-small")
    if cfg.EMBED_MODEL.lower() == "huggingface":
        from langchain_community.embeddings import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if cfg.EMBED_MODEL.lower() == "nomic-embed-text":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(model=cfg.EMBED_MODEL)

    raise ValueError(f"Unsupported embedding model: {cfg.EMBED_MODEL}")


def load_checkpoint(checkpoint_path):
    if not os.path.exists(checkpoint_path):
        return set()
    with open(checkpoint_path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return set(data.get("processed_file_ids", []))


def save_checkpoint(checkpoint_path, processed_file_ids):
    with open(checkpoint_path, "w", encoding="utf-8") as handle:
        json.dump({"processed_file_ids": sorted(processed_file_ids)}, handle, indent=2)


def load_or_create_vectorstore(embeddings):
    os.makedirs(cfg.VECTOR_CACHE_DIR, exist_ok=True)
    if cfg.VECTOR_DB.lower() == "faiss":
        if os.path.exists(os.path.join(cfg.VECTOR_CACHE_DIR, "index.faiss")):
            return FAISS.load_local(
                cfg.VECTOR_CACHE_DIR,
                embeddings,
                allow_dangerous_deserialization=True,
            )
        return None
    if cfg.VECTOR_DB.lower() == "chroma":
        return Chroma(persist_directory=cfg.VECTOR_CACHE_DIR, embedding_function=embeddings)
    raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")


def persist_vectorstore(vectorstore):
    if cfg.VECTOR_DB.lower() == "faiss":
        vectorstore.save_local(cfg.VECTOR_CACHE_DIR)
    elif cfg.VECTOR_DB.lower() == "chroma":
        vectorstore.persist()
    else:
        raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")


def build_vectorstore_in_batches(
    docs_by_file,
    batch_files,
    processed_file_ids,
    checkpoint_path,
):
    embeddings = build_embeddings()
    vectorstore = load_or_create_vectorstore(embeddings)

    file_ids = [file_id for file_id in docs_by_file if file_id not in processed_file_ids]
    total_files = len(file_ids)
    if total_files == 0:
        return vectorstore, 0

    for start in range(0, total_files, batch_files):
        batch_file_ids = file_ids[start : start + batch_files]
        batch_docs = []
        for file_id in batch_file_ids:
            batch_docs.extend(docs_by_file[file_id])

        if not batch_docs:
            continue

        if vectorstore is None:
            if cfg.VECTOR_DB.lower() == "faiss":
                vectorstore = FAISS.from_documents(batch_docs, embeddings)
            elif cfg.VECTOR_DB.lower() == "chroma":
                vectorstore = Chroma.from_documents(
                    batch_docs,
                    embeddings,
                    persist_directory=cfg.VECTOR_CACHE_DIR,
                )
            else:
                raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")
        else:
            vectorstore.add_documents(batch_docs)

        persist_vectorstore(vectorstore)
        processed_file_ids.update(batch_file_ids)
        save_checkpoint(checkpoint_path, processed_file_ids)

    return vectorstore, len(processed_file_ids)


if __name__ == "__main__":
    start = time.time()

    print("Loading chunks from DB...")
    chunk_rows = get_all_chunks(cfg.DB_FILE_METADATA)

    docs_by_file = {}
    for row in chunk_rows:
        file_id = row["file_id"]
        docs_by_file.setdefault(file_id, []).append(
            Document(
                page_content=row["chunk_text"],
                metadata={
                    "chunk_id": row["chunk_id"],
                    "file_id": row["file_id"],
                    "source": row["file_path"],
                },
            )
        )

    total_chunks = sum(len(docs) for docs in docs_by_file.values())
    print(f"Loaded {total_chunks} chunks across {len(docs_by_file)} files.")

    batch_files = int(os.getenv("VECTORSTORE_BATCH_FILES", DEFAULT_BATCH_FILES))
    checkpoint_path = os.path.join(cfg.VECTOR_CACHE_DIR, CHECKPOINT_FILENAME)
    processed_file_ids = load_checkpoint(checkpoint_path)
    if processed_file_ids:
        print(f"Resuming from checkpoint with {len(processed_file_ids)} files already processed.")

    print(f"Building vectorstore in batches of {batch_files} files...")
    vectorstore, processed_count = build_vectorstore_in_batches(
        docs_by_file,
        batch_files,
        processed_file_ids,
        checkpoint_path,
    )

    if vectorstore is None:
        print("No new documents were processed.")
    else:
        print(
            f"Vectorstore built with {total_chunks} docs using {cfg.VECTOR_DB.upper()}."
        )
        print(f"Stored at: {cfg.VECTOR_CACHE_DIR}")
        print(f"Processed {processed_count} files.")
        print(f"Done in {time.time()-start:.2f}s")
