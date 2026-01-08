# conversation_state.py
# conversation_state.py
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ConversationState:
    turn_count: int = 0
    depth: str = "short"     # short | expanded
    mood: str = "neutral"   # optional, heuristic or LLM-driven

# ---------- FACTORY ----------

def new_state() -> ConversationState:
    return ConversationState()


# ---------- UPDATE LOGIC ----------
DEPTH_TRIGGERS = {"why", "how", "explain", "details", "more", "expand"}


def update_state(
    state: ConversationState,
    user_input: str,
) -> ConversationState:
    state.turn_count += 1

    text = user_input.lower()

    # lightweight depth heuristic
    if any(word in text for word in DEPTH_TRIGGERS):
        state.depth = "expanded"
    else:
        state.depth = "short"

    return state



# ---------- SERIALISATION ----------

def state_to_dict(state: ConversationState) -> dict:
    return asdict(state)


def state_from_dict(data: dict) -> ConversationState:
    return ConversationState(**data)
