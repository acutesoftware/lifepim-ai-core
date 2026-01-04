from langchain_core.prompts import ChatPromptTemplate
from .config_llm import LLM_CONFIG


def build_prompt():
    text = LLM_CONFIG.base_prompt

    if LLM_CONFIG.personality:
        text += f"\nPersonality:\n{LLM_CONFIG.personality}"

    return ChatPromptTemplate.from_messages([
        ("system", text),
        ("human", "{input}")
    ])