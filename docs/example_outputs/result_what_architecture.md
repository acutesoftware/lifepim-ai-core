(.venv) D:\DATA_LLM\dev\lifepim-ai-core\src>python test_ai_cli.py what is the architecture of lifepima-ai-core
d:\DATA_LLM\dev\lifepim-ai-core\.venv\Lib\site-packages\langchain_core\_api\deprecation.py:26: UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
  from pydantic.v1.fields import FieldInfo as FieldInfoV1
prompt = what is the architecture of lifepima-ai-core
factory.py: build_chain() params = {'model': 'gpt-oss:20b', 'temperature': 0.67, 'max_tokens': 512}
[vectorstore] query='what is the architecture of lifepima-ai-core' top_k=5
## High‑level architecture of **lifepim‑ai‑core**

```
┌──────────────────────┐
│  USER / API Layer    │
│  └─ ask(query)       │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│  Retrieval Engine     │
│  ├─ Text ingestion    │
│  │   • Folder filter  │
│  │   • Metadata file  │
│  │   • Chunking /     │
│  │   re‑chunking      │
│  ├─ Metadata DB       │
│  │   • Document‑to‑   │
│  │   chunk trace      │
│  │   • Chunk stats    │
│  ├─ Vector Store      │
│  │   • Embedding model│
│  │   • Search (vector)│
│  └─ Retrieval API     │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│  Prompt Assembly      │
│  ├─ Template engine   │
│  ├─ Context injection │
│  └─ Final prompt      │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│  LLM Runtime Provider │
│  ├─ PROVIDER          │
│  │   (default: ollama│
│  │    or openai)      │
│  ├─ MODEL_NAME        │
│  │   (default: gpt‑oss:20b│
│  │    or qwen3‑coder‑30b)│
│  ├─ EMBED_MODEL       │
│  │   (used for vector │
│  │    search)         │
│  └─ API wrapper       │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│  LLM Response         │
│  └─ Text output        │
└──────────────────────┘
```

### 1. Ingestion & preprocessing

| Component | What it does | Key features |
|-----------|--------------|--------------|
| **Folder filtering** | Excludes or includes directories based on user rules | Configurable inclusion/exclusion lists |
| **Metadata extraction** | Pulls file metadata (size, type, timestamps) into a lightweight DB | Enables quick file‑level queries |
| **Chunking / re‑chunking** | Splits documents into manageable chunks (overlap, size limits) | Generates `chunk statistics` (size, overlap, count, coverage) |
| **Document‑to‑chunk traceability** | Keeps a mapping from original doc → chunk IDs | Useful for provenance and debugging |

### 2. Vector search & retrieval

| Component | What it does | Key features |
|-----------|--------------|--------------|
| **Embedding model** | Converts each chunk into a dense vector | Configurable via `EMBED_MODEL` (e.g., `text-embedding-ada-002`, `sentence‑transformers/all-MiniLM-L6-v2`) |
| **Vector store** | Stores embeddings and supports similarity search | Can be backed by FAISS, Milvus, or a simple in‑memory DB |
| **Retrieval API** | Accepts a query, retrieves top‑k relevant chunks | Uses the configured embedding model for query embedding |

### 3. Prompt assembly

* Pulls the retrieved chunks.
* Inserts them into a prompt template (configurable).
* Adds system/user instructions and any other context.
* Produces a single prompt string to send to the LLM.

### 4. LLM runtime provider

| Setting | Default | Notes |
|---------|---------|-------|
| **PROVIDER** | `ollama` | Supports OpenAI, Azure, local Ollama, etc. |
| **MODEL_NAME** | `gpt-oss:20b` | Can be swapped to `qwen3-coder:30b` (≈32B) or any other supported model. |
| **EMBED_MODEL** | (same as retrieval) | Keeps the same embedding model for consistency. |

The provider layer abstracts the underlying API, handling token limits, streaming, and error handling.

### 5. ask() lifecycle (as per the sequence diagram)

1. **User query** → `ask()` function.
2. **Retrieval**: query is embedded, searched against the vector store, and top chunks are returned.
3. **Prompt assembly**: chunks + template → final prompt.
4. **LLM call**: prompt sent to the runtime provider.
5. **Response**: text returned to the user.

This flow is fully documented in the LifePIM AI Core sequence diagram (`sample_docs/LifePIM AI Core sequence diagram.pdf`).

---

## Summary

- **Data ingestion** → **Chunking & metadata** → **Vector store**
- **Retrieval** + **Prompt assembly** → **LLM runtime** → **Response**
- Configuration knobs (`PROVIDER`, `MODEL_NAME`, `EMBED_MODEL`) let you swap back‑ends or models without touching the core logic.
- All modules are independent, making the system extensible (e.g., add a new embedding model, switch to a different vector DB, or plug in a new LLM provider).

That is the overall architecture of **lifepim‑ai‑core**.
