# core/llm_runtime/vectorstore/search.py
# This is the main entry point for VECTOR search (not LLM search)
# things to add later go here such as :
#   hybrid search, 
#   corpus-specific logic
#   admin vs user search


from . import vectorstore as mod_vectorstore 

def search(cfg, query: str, *, top_k: int = 5):
    """
    Semantic search entrypoint.
    This is where we add future logic:
    - reranking
    - hybrid search
    - filters
    - score shaping
    """
    print(f"[vectorstore] query='{query}' top_k={top_k}")
    return mod_vectorstore.similarity_search(
        cfg=cfg, 
        query_text=query,
        top_k=top_k,
    )
