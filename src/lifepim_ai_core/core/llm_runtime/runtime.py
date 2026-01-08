from .llm import LLMRuntime
from .factory import build_chain
from .config import LLM_CONFIG

_llm = None

def get_llm(cfg, force_reload=False):
    global _llm

    if _llm is None or force_reload:
        params = {
            "model": LLM_CONFIG.model,
            "temperature": LLM_CONFIG.temperature,
            "max_tokens": LLM_CONFIG.max_tokens,
        }
        chain = build_chain(cfg, params)
        _llm = LLMRuntime(cfg, chain, params)

    return _llm


