from pathlib import Path
from langchain_core.documents import Document
import importlib

# -------------------------------------------------
# Identity
# -------------------------------------------------

def load_identity(personality: str) -> str:
    # Import relative to *this* module’s package:
    # e.g. if this file is lifepim_ai_core.core.identity.py
    # then __package__ is "lifepim_ai_core.core"
    base_pkg = __package__.rsplit(".", 1)[0]  # -> "lifepim_ai_core.core"
    personalities_pkg = f"{base_pkg}.core.personalities"

    try:
        mod = importlib.import_module(f".{personality}", package=personalities_pkg)
    except ModuleNotFoundError as e:
        # Only treat it as "missing personality" if it was that module specifically
        # (otherwise you hide real import bugs inside the personality module)
        if e.name in (f"{personalities_pkg}.{personality}", personality):
            raise ValueError(f"Personality preset '{personality}' not found in {personalities_pkg}") from e
        raise

    try:
        return mod.SYSTEM_PROMPT.strip()
    except AttributeError as e:
        raise ValueError(f"Personality '{personality}' has no SYSTEM_PROMPT") from e

# -------------------------------------------------
# State
# -------------------------------------------------

def format_state(state):
    if not state:
        return "No active state."

    print("DEBUG prompt_builder: state =", state)

    lines = []

    if getattr(state, "active_topic", None):
        lines.append(f"- Topic: {state.active_topic}")

    if getattr(state, "active_person", None):
        lines.append(f"- Person: {state.active_person}")

    if getattr(state, "depth", None):
        lines.append(f"- Depth: {state.depth}")

    if getattr(state, "mood", None):
        lines.append(f"- Mood: {state.mood}")

    return "\n".join(lines) if lines else "No active state."


# -------------------------------------------------
# Dialogue
# -------------------------------------------------

def format_recent_turns(turns):
    """
    turns = [{role: 'User'|'AI', content: str}, ...]
    """
    if not turns:
        return "No previous dialogue."

    lines = []
    for t in turns:
        role = t.get("role", "").upper()
        content = t.get("content", "")
        lines.append(f"{role}: {content}")

    return "\n".join(lines)


# -------------------------------------------------
# Docs
# -------------------------------------------------

def format_docs(docs):
    """
    Accepts:
      - list[Document]
      - dict with key 'results' -> list[Document]
    Returns a clean, readable RAG context block.
    """

    if not docs:
        return "No supporting documents retrieved."

    # Unwrap search result dict if needed
    if isinstance(docs, dict):
        docs = docs.get("results", [])

    if not docs:
        return "No supporting documents retrieved."

    blocks = []

    for i, doc in enumerate(docs, start=1):
        if not isinstance(doc, Document):
            continue  # defensive: ignore junk

        meta = doc.metadata or {}

        source = meta.get("source", "Unknown source")
        chunk_id = meta.get("chunk_id")
        file_id = meta.get("file_id")

        header_parts = [f"[{i}] {source}"]
        if chunk_id is not None:
            header_parts.append(f"chunk {chunk_id}")
        if file_id is not None:
            header_parts.append(f"file {file_id}")

        header = " | ".join(header_parts)

        text = doc.page_content.strip()

        blocks.append(f"{header}\n{text}")

    if not blocks:
        return "No supporting documents retrieved."

    return "\n\n".join(blocks)


# -------------------------------------------------
# Prompt assembly
# -------------------------------------------------

def build_prompt(
    *,
    user_input,
    personality,
    corpus,
    mode,
    conversation_state,
    recent_turns,
    retrieved_docs,
):
    identity_text = load_identity(personality)
    state_block = format_state(conversation_state)
    dialogue_block = format_recent_turns(recent_turns)
    docs_block = format_docs(retrieved_docs)

    return f"""
SYSTEM:
{identity_text}

--- CONVERSATION STATE ---
{state_block}

--- SUPPORTING DOCUMENTS ---
{docs_block}

--- RECENT DIALOGUE ---
{dialogue_block}

USER:
{user_input}
""".strip()


# ---------- Future Work -------------
def custom_prompt_for_model(model_name, system_prompt):
    if "gemma" in model_name.lower():
        return strip_identity(system_prompt)
    return system_prompt
       

def strip_identity(orig_prompt):
    """removes:
        “I am…”
        “You are…”
        “AI:”
        “Assistant:”
     """ 
    print('TODO - the Gemma family needs a specific prompt format as at Dec 2025')  
    return orig_prompt