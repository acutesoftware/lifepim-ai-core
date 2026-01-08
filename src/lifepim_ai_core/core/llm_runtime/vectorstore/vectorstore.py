import os
import sys
import time
from collections import Counter

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS, Chroma

def _build_embeddings(cfg):
    model = cfg.EMBED_MODEL.lower()

    if model == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model="text-embedding-3-small")

    if model == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    if model == "nomic-embed-text":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=cfg.EMBED_MODEL)

    raise ValueError(f"Unsupported embedding model: {cfg.EMBED_MODEL}")


def load_vectorstore(cfg):
    embeddings = _build_embeddings(cfg)

    if cfg.VECTOR_DB.lower() == "faiss":
        if not os.path.exists(cfg.VECTOR_CACHE_DIR):
            raise FileNotFoundError(
                f"FAISS cache not found at {cfg.VECTOR_CACHE_DIR}"
            )
        return FAISS.load_local(
            cfg.VECTOR_CACHE_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )

    if cfg.VECTOR_DB.lower() == "chroma":
        if not os.path.exists(cfg.VECTOR_CACHE_DIR):
            raise FileNotFoundError(
                f"Chroma cache not found at {cfg.VECTOR_CACHE_DIR}"
            )
        return Chroma(
            persist_directory=cfg.VECTOR_CACHE_DIR,
            embedding_function=embeddings
        )

    raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")



def build_retriever(cfg, top_k=None):
    vs = load_vectorstore(cfg)
    return vs.as_retriever(
        search_kwargs={"k": top_k or cfg.RAG_TOP_K}
    )


def similarity_search(cfg, query_text: str, top_k: int = 5):
    start = time.time()
    vs = load_vectorstore(cfg)
    load_time = time.time() - start

    start = time.time()
    results = vs.similarity_search(query_text, k=top_k)
    query_time = time.time() - start

    return {
        "results": results,
        "load_time": load_time,
        "query_time": query_time,
    }




#---------------------------------------------------------------
# Utilities for accessing / testing Vectorstore

def list_docs_with_chunk_counts():
    vs = load_vectorstore()
    counter = Counter()

    if cfg.VECTOR_DB.lower() == "chroma":
        all_data = vs.get(include=["metadatas"])
        for m in all_data.get("metadatas", []):
            counter[m.get("source", "Unknown")] += 1

    elif cfg.VECTOR_DB.lower() == "faiss":
        for doc in vs.docstore._dict.values():
            counter[doc.metadata.get("source", "Unknown")] += 1

    else:
        raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")

    return counter


def list_docs_with_chunk_counts_ORIG():
    """
    List all docs in the vectorstore with count of chunks per doc.
    """
    vs = load_vectorstore()

    if cfg.VECTOR_DB.lower() == "chroma":
        # Pull all stored metadata
        all_data = vs.get(include=["metadatas"])
        metadatas = all_data.get("metadatas", [])
        counter = Counter()

        for m in metadatas:
            src = m.get("source", "Unknown")
            counter[src] += 1

        print(f"Total documents: {len(counter)}")
        for doc, count in counter.items():
            print(f" - {doc}: {count} chunks")

    elif cfg.VECTOR_DB.lower() == "faiss":
        # FAISS + LangChain keeps a docstore
        counter = Counter()
        for _id, doc in vs.docstore._dict.items():
            src = doc.metadata.get("source", "Unknown")
            counter[src] += 1

        print(f"Total documents: {len(counter)}")
        for doc, count in counter.items():
            print(f" - {doc}: {count} chunks")

    else:
        raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        counts = list_docs_with_chunk_counts()
        print(f"Total documents: {len(counts)}")
        for doc, count in counts.items():
            print(f" - {doc}: {count} chunks")
        sys.exit(0)

    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    data = similarity_search(query, top_k=top_k)

    print(f"Loaded in {data['load_time']:.2f}s")
    print(f"Queried in {data['query_time']:.2f}s")

    for i, doc in enumerate(data["results"], 1):
        meta = doc.metadata
        snippet = doc.page_content[:300].replace("\n", " ")
        print(f"{i}. {meta.get('source')} — {snippet}...")
