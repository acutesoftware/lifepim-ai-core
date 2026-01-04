import core.llm_runtime.runtime as llm_rt
import asyncio 

from core.llm_runtime import config_llm as cfg

prompt = "hello - who are you?"

def test_invoke():
    llm_instance = llm_rt.get_llm(cfg)
    result = llm_instance.invoke(prompt)
    print(result)

async def test_stream():
    llm_instance = llm_rt.get_llm(cfg)

    async for token in llm_instance.stream(prompt):
        print(token, end="", flush=True)
    print()  # newline at end


import sys
if __name__ == "__main__":
    prompt = ' '.join(s for s in sys.argv[1:])
    print('prompt = ' + prompt)
    #test_invoke()
    asyncio.run(test_stream())
