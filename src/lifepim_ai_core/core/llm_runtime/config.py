import importlib.util

from . import defaults as _defaults


def _load_user_config():
    config_path = _defaults.REPO_ROOT / "my_app" / "lifepim_config.py"
    if not config_path.exists():
        return None

    spec = importlib.util.spec_from_file_location("lifepim_config", config_path)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _apply_defaults():
    for name in _defaults.DEFAULT_FIELDS:
        globals()[name] = getattr(_defaults, name)


def _apply_user_overrides(module):
    if module is None:
        return

    for name in _defaults.DEFAULT_FIELDS:
        if hasattr(module, name):
            globals()[name] = getattr(module, name)


_apply_defaults()
_apply_user_overrides(_load_user_config())


class LLMConfig:
    def __init__(self):
        self.base_prompt = "You are a helpful assistant."
        self.model = MODEL_NAME
        self.embed_model = EMBED_MODEL
        self.temperature = TEMPERATURE
        self.enable_rag = True
        self.max_tokens = MAX_TOKENS
        self.personality = "you are an assistant"
        self.max_context_messages = MAX_CONTEXT_MESSAGES
        self.top_k = TOP_K
        self.EFFECTIVE_CONTEXT_LIMIT = EFFECTIVE_CONTEXT_LIMIT


LLM_CONFIG = LLMConfig()
