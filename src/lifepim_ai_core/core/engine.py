from . import retriever, prompt_builder

# Prompts are kept as plain strings (not SystemMessage/HumanMessage)
# so the RAG engine remains provider-agnostic, debuggable, and easy
# to mutate (context injection, truncation, replay, logging).
# Message objects are applied only at the provider adapter layer.

def handle_turn(
    cfg,
    *,
    user_input,
    personality,
    corpus,
    mode,
    conversation_state,
    recent_turns,
):
    docs = retriever.search(
        cfg,
        user_input,
        corpus=corpus,
        mode=mode,
    )

    prompt = prompt_builder.build_prompt(
        user_input=user_input,
        personality=personality,
        corpus=corpus,
        mode=mode,
        conversation_state=conversation_state,
        recent_turns=recent_turns,
        retrieved_docs=docs,
    )

    return prompt
