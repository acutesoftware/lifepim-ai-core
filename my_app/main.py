import asyncio
import sys

import lifepim_ai_core.core.llm_runtime.runtime as llm_rt
from lifepim_ai_core.core.llm_runtime import config as cfg


async def run_prompt(prompt: str) -> None:
    llm_instance = llm_rt.get_llm(cfg)
    async for token in llm_instance.stream(prompt):
        print(token, end="", flush=True)
    print()


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        prompt = input("Enter a prompt: ").strip()

    asyncio.run(run_prompt(prompt))
