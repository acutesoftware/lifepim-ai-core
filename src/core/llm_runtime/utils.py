
from langchain_ollama import ChatOllama
from .config_llm import LLM_CONFIG

_LLM_CACHE = {}

def get_ollama_llm(model_name, temperature=0):
    if model_name not in _LLM_CACHE:
        _LLM_CACHE[model_name] = ChatOllama(
            model=model_name,
            temperature=temperature
        )
    return _LLM_CACHE[model_name]


def count_tokens(model_name: str, text: str, show_debug: str = 'Y') -> int:
    """
    Count tokens using Ollama's actual tokenizer.
    This reflects the true token usage for the model.
    """

    llm = get_ollama_llm(model_name)
    tot_tokens = llm.get_num_tokens(text)

    if show_debug == 'Y':
        tot_words = len(text.split())
        print("\nMODEL_NAME (Ollama) =", model_name)
        print(f"prompt has {tot_tokens} tokens for {tot_words} words")

    return tot_tokens


def count_tokens_huggingface(ollama_model_name: str, text: str, show_debug: str = 'Y') -> int:
    """
    return an exact count of actual tokens from the model instead 
    of using the Ollama LangChain 'estimate' - BUT, this version
    uses http to go to huggingface to get transformer details and 
    will fail if some models are 'gated' (eg Google), so DONT USE THIS.
    
    OLD - I though it was important to avoid  going over the token limit 
    (ideally keep to 500 tokens for 8B model), but actual limits are 2k
     so not as big as an issue = so use the ollama 'estimate')
    """

    TOKENIZER_CACHE = {}

    tokenizer_source = cfg.MODEL_TOKENIZERS[ollama_model_name]

    if tokenizer_source not in TOKENIZER_CACHE:
        TOKENIZER_CACHE[tokenizer_source] = AutoTokenizer.from_pretrained(
            tokenizer_source,
            use_fast=True
        )

    tokenizer = TOKENIZER_CACHE[tokenizer_source]

    tot_tokens = len(tokenizer.encode(text, add_special_tokens=False))

    if show_debug == 'Y':
        tot_words = count_words(text)
        print('\nMODEL_NAME (Ollama)          = '  + ollama_model_name)
        print('maps to HuggingFace Model ID = '  + tokenizer_source)
        print('prompt has = ' + str(tot_tokens) + ' tokens for ' + str(tot_words) + ' words. Prompt = ' + str(text))

    return tot_tokens

               
def count_words(text):
    """
    This is only here for comparison and it belongs in the same spot.
    """
    return len(text.split())

