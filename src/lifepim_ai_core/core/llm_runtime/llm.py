class LLMRuntime:
    def __init__(self, cfg, chain, model_params: dict):
        self._chain = chain
        self._params = model_params
        self.cfg = cfg

    # ---- configuration ----

    def set_temperature(self, value: float):
        self._params["temperature"] = value
        self._rebuild_chain()

    def set_max_tokens(self, value: int):
        self._params["max_tokens"] = value
        self._rebuild_chain()

    # ---- invocation ----

    def invoke_OLD(self, prompt: str) -> str:
        result = self._chain.invoke({"input": prompt})
        return result.content

    def invoke(self, prompt: str) -> str:
        result = self._chain.invoke(prompt)  # pass plain string
        return getattr(result, "content", str(result))

    async def stream(self, prompt: str):
        async for chunk in self._chain.astream(prompt):  # pass string
            yield getattr(chunk, "content", str(chunk))

    # ---- internals ----

    def _rebuild_chain(self):
        from .factory import rebuild_chain
        self._chain = rebuild_chain(self.cfg, self._params)
