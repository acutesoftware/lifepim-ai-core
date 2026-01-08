
import time 
from langchain_core.runnables import RunnableLambda

import core.llm_runtime.vectorstore.vectorstore as mod_vectorstore # import build_retriever
from .config import LLM_CONFIG

def maybe_wrap_with_rag(cfg, chain):
    if not LLM_CONFIG.enable_rag:
        return chain

    retriever = mod_vectorstore.build_retriever(cfg)

    def inject_context(prompt: str):
        docs = retriever.invoke(prompt)
        context = "\n".join(d.page_content for d in docs)
        return f"Context:\n{context}\n\nQuestion:\n{prompt}"

    return RunnableLambda(inject_context) | chain

