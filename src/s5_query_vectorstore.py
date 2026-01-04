import os
import sys
from langchain_core.documents import Document
import time 
from core.llm_runtime import config_llm as cfg

from collections import Counter


# NOTE:
# query_vectorstore is legacy and uses global config.
# corpus/mode are intentionally ignored here.
"""
When you should refactor s5_query_vectorstore

Do it when one of these becomes true:
 - You want two corpora loaded at once
 - You want admin mode to search a different DB
 - You want parallel retrievers
 - You want hot-swapping vectorstores without restart
 
"""
# Vector stores
from langchain_community.vectorstores import FAISS, Chroma

# Embeddings
if cfg.EMBED_MODEL.lower() == "openai":
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
elif cfg.EMBED_MODEL.lower() == "huggingface":
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

elif cfg.EMBED_MODEL.lower() == "nomic-embed-text":
    from langchain_ollama import OllamaEmbeddings
    embeddings = OllamaEmbeddings(model=cfg.EMBED_MODEL)


else:
    raise ValueError(f"Unsupported embedding model: {cfg.EMBED_MODEL}")


def load_vectorstore():
    """Load the vectorstore from disk."""
    if cfg.VECTOR_DB.lower() == "faiss":
        if not os.path.exists(cfg.VECTOR_CACHE_DIR):
            raise FileNotFoundError(f"FAISS cache not found at {cfg.VECTOR_CACHE_DIR}")
        return FAISS.load_local(
            cfg.VECTOR_CACHE_DIR,
            embeddings,
            allow_dangerous_deserialization=True  #  for pickle safety
        )
    elif cfg.VECTOR_DB.lower() == "chroma":
        if not os.path.exists(cfg.VECTOR_CACHE_DIR):
            raise FileNotFoundError(f"Chroma cache not found at {cfg.VECTOR_CACHE_DIR}")
        return Chroma(persist_directory=cfg.VECTOR_CACHE_DIR, embedding_function=embeddings)
    else:
        raise ValueError(f"Unsupported vector DB: {cfg.VECTOR_DB}")



def list_docs_with_chunk_counts():
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

def query_vectorstore(query_text: str, top_k: int = 5):
    start = time.time()
    vs = load_vectorstore()
    print(f"Loaded vectorstore in {time.time()-start:.2f}s")

    start = time.time()
    results = vs.similarity_search(query_text, k=top_k)
    print(f"Retrieved {len(results)} results in {time.time()-start:.2f}s")
    #print("results = " + str(results))
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_docs_with_chunk_counts()
        print("Usage: python s5_query_vectorstore.py \"your query here\" [top_k]")
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    print(f"Query: {query_text}")
    hits = query_vectorstore(query_text, top_k=top_k)

    if not hits:
        print("No results found.")
    else:
        print(f"Top {len(hits)} results:\n")
        for i, doc in enumerate(hits, start=1):
            meta = doc.metadata
            print(f"{i}. Source: {meta.get('source', 'Unknown')}")
            print(f"   Chunk ID: {meta.get('chunk_id', 'N/A')} | File ID: {meta.get('file_id', 'N/A')}")
            snippet = doc.page_content[:300].replace("\n", " ") + ("..." if len(doc.page_content) > 300 else "")
            print(f"   Snippet: {snippet}\n")
