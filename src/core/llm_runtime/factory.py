
"""
1. All RAG logic lives inside factory.py
    - Callers never import vectorstore or retriever
    - CLI, web, and tests automatically use RAG if enabled in cfg
2. RAGWrapper handles retrieval + formatting
    - Pulls top-k docs from vectorstore
    - Formats them robustly for the prompt
3. WrappedChain makes the chain interface compatible with LLMRuntime
    - Supports both invoke(prompt) and astream(prompt)
    - Preserves token streaming
4. Config-driven
    - Toggle RAG: cfg.RAG_ENABLED
    - Top-k docs: cfg.RAG_TOP_K

"""

from langchain_ollama import ChatOllama
from .prompts import build_prompt
from .vectorstore.search import search as vector_search
from ..prompt_builder import format_docs
# from . import config_llm as cfg


class RAGWrapper:
    """
    Handles retrieval from vectorstore and injects supporting documents
    into the user prompt.
    """
    def __init__(self, cfg, top_k: int = 5):
        self.top_k = top_k
        self.cfg = cfg

    def apply(self, user_prompt: str) -> str:
        if not self.cfg.LLM_CONFIG.enable_rag:
            return user_prompt

        # Retrieve top-k docs from vectorstore
        search_result = vector_search(self.cfg, user_prompt, top_k=self.top_k)
        docs = search_result.get("results", [])

        # Format docs into a string
        context_block = format_docs(docs)

        # Inject context into final prompt
        return f"""
--- SUPPORTING DOCUMENTS ---
{context_block}

--- USER QUESTION ---
{user_prompt}
""".strip()


def build_chain(cfg, params: dict):
    """
    Build a chain that optionally includes RAG.
    Returns an object compatible with LLMRuntime (supports invoke() and astream()).
    """
    print(f'factory.py: build_chain() params = {params}')

    # Base LLM
    llm = ChatOllama(
        model=params["model"],
        temperature=params["temperature"],
        max_tokens=params["max_tokens"],
    )

    # Optionally wrap with RAG
    if cfg.LLM_CONFIG.enable_rag:
        rag_wrapper = RAGWrapper(cfg, top_k=getattr(cfg, "RAG_TOP_K", 5))

        class WrappedChain:
            def invoke(self, user_prompt: str):
                final_prompt = rag_wrapper.apply(user_prompt)
                # Pass plain string to LLM
                result = llm.invoke(final_prompt)
                return result

            async def astream(self, user_prompt: str):
                final_prompt = rag_wrapper.apply(user_prompt)
                async for chunk in llm.astream(final_prompt):
                    yield chunk

        chain = WrappedChain()
    else:
        # Simple chain without RAG
        class SimpleChain:
            def invoke(self, user_prompt: str):
                return llm.invoke(user_prompt)

            async def astream(self, user_prompt: str):
                async for chunk in llm.astream(user_prompt):
                    yield chunk

        chain = SimpleChain()

    return chain


def rebuild_chain(cfg, params: dict):
    """
    Rebuild chain after parameter changes (temperature, max_tokens, etc.)
    """
    return build_chain(cfg, params)
