# core/retriever.py
#from core.llm_runtime.vectorstore import search as vector_search
from .llm_runtime.vectorstore import search as mod_search

def search(cfg, query, *, corpus, mode = 'rag'):
    print(f"[retriever] query='{query}' corpus='{corpus}' mode='{mode}'")
    
    if mode in ("rag", "chat"):        
        return mod_search.search(cfg, query)
    print('core/retriever.py : WARNING - search mode not valid, returning no search results')
    return []
