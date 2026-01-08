import os
import time
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

from core.llm_runtime import config as cfg
from db.chunks import get_all_chunks

def build_vectorstore(docs):
    """
    Create vectorstore from documents using configured embedding model.
    """
    # Choose embedding model
    if cfg.EMBED_MODEL.lower() == "openai":
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    elif cfg.EMBED_MODEL.lower() == "huggingface":
        from langchain_community.embeddings import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    elif cfg.EMBED_MODEL.lower() == "nomic-embed-text":
        from langchain_ollama import OllamaEmbeddings
        embeddings = OllamaEmbeddings(model=cfg.EMBED_MODEL)

    else:
        raise ValueError(f"Unsupported embedding model: {cfg.EMBED_MODEL}")

    # Choose vector store
    if cfg.VECTOR_DB.lower() == "faiss":
        vectorstore = FAISS.from_documents(docs, embeddings)
        os.makedirs(cfg.VECTOR_CACHE_DIR, exist_ok=True)
        vectorstore.save_local(cfg.VECTOR_CACHE_DIR)
    elif cfg.VECTOR_DB.lower() == "chroma":
        os.makedirs(cfg.VECTOR_CACHE_DIR, exist_ok=True)
        vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=cfg.VECTOR_CACHE_DIR)
        vectorstore.persist()
    else:
        raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")

    return vectorstore


if __name__ == "__main__":
    start = time.time()

    print("Loading chunks from DB...")
    chunk_rows = get_all_chunks(cfg.DB_FILE_METADATA)

    docs = [
        Document(
            page_content=row["chunk_text"],
            metadata={
                "chunk_id": row["chunk_id"],
                "file_id": row["file_id"],
                "source": row["file_path"],
            }
        )
        for row in chunk_rows
    ]
    print(f"Loaded {len(docs)} chunks.")

    print("Building vectorstore...")
    vs = build_vectorstore(docs)

    print(f"Vectorstore built with {len(docs)} docs using {cfg.VECTOR_DB.upper()}.")
    print(f"Stored at: {cfg.VECTOR_CACHE_DIR}")
    print(f"Done in {time.time()-start:.2f}s")
