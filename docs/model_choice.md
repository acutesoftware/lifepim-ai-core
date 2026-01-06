
# MODEL_CHOICE.md — Picking a local model for LifePIM AI Core (RAG)

This is a practical, “what should I try?” guide for common local models (Ollama-style names), grouped by **GPU VRAM** to make experimenting easy.
Notes assume a **local RAG workflow** (retrieve context → inject a small TOP_K → answer grounded in docs).

> VRAM guidance depends heavily on **quantization (Q4/Q5/Q8)** and context length. Treat the groups as “usually works” not gospel.

---

## 16GB GPU (comfortable for ~11B–20B; some 30B+ with aggressive quant/offload)

### gpt-oss:20b
OpenAI’s open-weight 20B model aimed at strong reasoning and developer/agentic use. 
Generally solid for RAG if you keep `TOP_K` small and prompts tight; can feel “serious” at low temperature and gets more personable around 0.5–0.8.

### deepseek-r1:14b (Distill)
A distilled reasoning model (R1 outputs distilled into smaller dense models) that tends to be strong at structured reasoning and “show your working” style tasks. 
For RAG: great when you want careful answers; can be wordier than Llama-family instruct models.

### gemma3:12b (and variants)
Google’s Gemma 3 instruction-tuned models are lightweight for their capability and can do strong QA/summarisation.
**Quirk:** Gemma-family chat formatting is stricter than many models; if your wrapper/template is wrong, it may ignore “system prompt” intent or behave oddly (common complaint). 

### llama3.2-vision:11b
Multimodal (text + image) model; great if you want “describe/understand this screenshot” alongside normal chat. 
For text-only RAG it’s fine, but you’re paying for vision capability you may not need.

### qwen2.5:14b-instruct
Very strong general instruct model with large context support; tends to be crisp and reliable for QA. 
For RAG: good “grounded answer” behaviour, especially at lower temps (0.2–0.5).

### qwen2.5-coder:14b-instruct
Coder-tuned sibling; better at reading/rewriting code, stack traces, and refactors. 
For RAG: excellent if your documents are technical and you want code-literate responses.

### qwen3-coder:32b (aka Qwen3-Coder-32B-Instruct)
A heavy hitter for coding + agentic tool-use; strong at code reasoning and long-form fixes. 
On 16GB this is often **tight** unless you use Q4-ish quant and/or partial CPU offload. If it fits, it’s fantastic for “RAG + codebase” workflows.

### gpt-oss-safeguard:20b (alternative)
Variant explicitly positioned to fit GPUs with ~16GB VRAM. 
If you want gpt-oss behaviour but fewer resource surprises, this can be a good pick.

---

## 8GB GPU (sweet spot: 7B–8B class models)

### llama3.1:8b (Instruct)
A strong, well-rounded instruct model: usually concise, accurate, and “naturally chatty” without being chaotic. 
For RAG: reliably uses provided context when the prompt labels it clearly and `TOP_K` stays small (3–6).

### ministral-3:8b
Mistral’s edge-focused family; designed to run well on a wide range of hardware (some variants include vision/tools support).  
For RAG: typically sharp and efficient; watch Ollama version requirements (some Ministral 3 builds require newer Ollama). 

### ministral-8b-instruct (aka Ministral-8B-Instruct-2410)
An 8B model optimized for efficient inference (sliding-window attention pattern) and long context variants exist. 
For RAG: a good “fast but smart” default; tends to follow instructions well and stays on-topic.

### deepseek-r1:8b (Distill)
Distilled from DeepSeek-R1, built on Llama3.1-8B-Instruct family; strong at reasoning for its size. 
For RAG: very effective when you want careful answers from small context; can get verbose—pair with lower `MAX_TOKENS` if needed.

### mistral:7b-instruct (classic)
Older but still a dependable “baseline”: responsive, reasonably grounded, widely supported. 
For RAG: good general assistant; not as strong as the newest 8B class on tricky reasoning, but stable.

### qwen2.5:7b-instruct
Strong multilingual general model with large context support; often a great “daily driver”. 
For RAG: tends to quote/anchor to context well when asked; good balance of chatty vs factual depending on temperature.

### qwen2.5-coder:7b-instruct
Coder-tuned; better at code, logs, stack traces, and structured output. 
For RAG: excellent if your indexed docs include lots of code snippets and technical notes.

### Dolphin (Llama 3.x fine-tune) (optional/alternative)
Dolphin-style fine-tunes often feel more “assistant-y” and tool-friendly. 
Tradeoff: sometimes less strict about guardrails/formatting; for RAG, keep temperature modest.

---

## 4GB GPU (tiny-but-capable models; best for quick experiments)

### phi3.5:3.8b
Lightweight 3.8B model that punches above its size; very fast and surprisingly competent for short tasks. 
For RAG: works well if you keep context tight and expectations realistic (short answers, limited nuance).

### qwen2.5:3b-instruct
A compact instruct model that’s still quite usable; good for “fast local assistant” setups. 
For RAG: decent factual grounding with small injected context; not great at long, multi-step reasoning.

### qwen2.5-coder:3b-instruct
Tiny coder model; good for quick code explanations and simple transforms. 
For RAG: nice for technical snippets, but don’t expect deep refactors.

### (Optional) llama3.2:3b-instruct (if you have it)
Common small Llama option; generally friendly and easy to prompt.  
For RAG: decent “chat with notes” model when you want speed over depth.

---

## No GPU (CPU-only friendly; expect slower tokens/sec)

### deepseek-r1:1.5b (Distill)
Very small distilled reasoning option; surprisingly good for basic reasoning given size. 
For RAG: works for simple QA with very small context; keep `MAX_TOKENS` low and be patient.

### qwen2.5:1.5b / 0.5b (Instruct)
Tiny “always runs” models; useful for testing pipelines and UI. 
For RAG: okay for keyword-ish Q&A and short summaries; weak at nuance.

### phi3.5:3.8b (CPU)
Still feasible on CPU in many setups (slower, but workable) and tends to behave better than most sub-4B models. {index=23}  
For RAG: one of the better CPU-only experiences if latency is acceptable.

---

## Quick “best default” picks for local RAG

- **16GB GPU:** `gpt-oss:20b` for reasoning/dev tasks, or `deepseek-r1:14b` for careful structured answers  
- **8GB GPU:** `llama3.1:8b` or `qwen2.5:7b-instruct` (best balance of speed + quality) 
- **4GB GPU:** `phi3.5:3.8b` (fast and surprisingly capable) 

---

## Practical prompting quirks (RAG-specific)

- **Keep TOP_K small (3–6)** and label retrieved context clearly.
- If a model is “chatty and imaginative”, drop `TEMPERATURE` to **0.2–0.4** for grounded answers.
- If a model “ignores system prompts”, suspect the **chat template / wrapper** first (Gemma-family is a common offender). 
