(.venv) D:\DATA_LLM\dev\lifepim-ai-core\src>python test_ai_cli.py what temperature should I set the RAG LLM to

prompt = what temperature should I set the RAG LLM to
factory.py: build_chain() params = {'model': 'gpt-oss:20b', 'temperature': 0.67, 'max_tokens': 512}
[vectorstore] query='what temperature should I set the RAG LLM to' top_k=5
**RAG‑LLM temperature recommendation**

| Model | Suggested temperature | Why |
|-------|-----------------------|-----|
| **qwen2.5‑14b‑instruct** | **0.2–0.3** (or 0.2 if you want the strictest grounding) | The docs state that “good grounded answer behaviour” is achieved at *lower* temperatures (0.2–0.5). 0.2–0.3 gives a good balance between determinism and a touch of variety. |
| **phi3.5‑3.8b** (quick‑experiment model) | **0.3–0.4** | For tiny‑but‑capable models the default is modestly higher, but still lower than the 0.7–1.0 range typical for open‑domain chat. 0.3–0.4 keeps the answers grounded while allowing a little nuance. |
| **Any RAG‑enabled model** | **≤ 0.4** | In general, a temperature ≤ 0.4 keeps the model from hallucinating and ensures it sticks to the retrieved context. 0.1–0.2 is the safest, 0.3–0.4 gives a little flexibility. |

**Bottom line**

Set your RAG LLM’s temperature to **0.2–0.3** (or 0.3–0.4 for smaller models). That range gives you grounded, reliable answers while still allowing the model to be a bit expressive. If you need *extra* strictness, drop it to 0.1.

(.venv) D:\DATA_LLM\dev\lifepim-ai-core\src>