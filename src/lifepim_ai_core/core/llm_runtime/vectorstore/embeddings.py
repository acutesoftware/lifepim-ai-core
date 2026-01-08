# core/llm_runtime/vectorstore/embeddings.py
# from .. import config_llm as cfg

def get_embeddings(cfg):
    if cfg.EMBED_MODEL.lower() == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model="text-embedding-3-small")

    if cfg.EMBED_MODEL.lower() == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    if cfg.EMBED_MODEL.lower() == "nomic-embed-text":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=cfg.EMBED_MODEL)

    raise ValueError("Unknown embedding model")
