# Configuration Summary — LifePIM AI Core

Concise reference for all runtime configuration parameters.  
Defaults are chosen to balance **local performance**, **RAG quality**, and **prompt stability**.

---

### REPO_ROOT : Repository root path
Base path for all other folders (derived from config file location).  
Changing the depth affects all paths; incorrect values will break file discovery.

---

### DOCS_FOLDER : Source documents directory
Folder containing documents to be indexed and searched via RAG (default: `/docs`).  
Changing contents or location requires rebuilding the vector store.

---

### VECTOR_CACHE_DIR : Vector store storage directory
Directory where vector indexes and related databases are stored.  
Slow disks or network paths here directly impact indexing and query performance.

---

### DB_FILE_METADATA : Metadata database path
SQLite database storing metadata about indexed files and chunks.  
Changing it switches metadata “universes” but does not require a rebuild.

---

### DB_FILE : Chat memory database path
SQLite database storing conversation history and summaries.  
Deleting or changing it resets chat memory without affecting retrieval.

---

### PROVIDER : LLM runtime provider
Selects the backend used to run the language model (default: `ollama`).  
Changing providers requires compatible runtime support and parameter mapping. 

---

### MODEL_NAME : LLM model identifier
Specifies the model run by the provider (default: `gpt-oss:20b`).  
Larger models improve instruction-following and RAG grounding but increase latency and resource usage.

---

### EMBED_MODEL : Embedding model for vector search
Model used to embed documents and queries (default: `nomic-embed-text`).  
Changing this **requires a full vector rebuild**; stronger embeddings improve recall at the cost of indexing time.

---

### TEMPERATURE : Generation randomness
Controls creativity vs determinism (default: `0.67`).  
Lower values (0.0–0.3) produce factual, stable outputs; higher values (0.7–1.0+) increase creativity but risk hallucination.

---

### MAX_TOKENS : Output token limit
Maximum tokens generated per response (default: `512`).  
Lower values are faster but may truncate answers; higher values allow fuller responses but increase latency.

---

### MAX_CONTEXT_MESSAGES : Chat memory depth
Number of recent chat turns kept before summarisation (default: `5`).  
Higher values increase conversational continuity but consume prompt budget quickly. (TODO - truncate or summarise LLM responses when getting detailed answers OR reduce chat memory depth)

---

### TOP_K : Retrieved document count
Number of retrieved chunks injected into the prompt (default: `5`).  
Small values reduce noise; large values (>8–10) often confuse the model due to excessive context.

---

### EFFECTIVE_CONTEXT_LIMIT : Prompt token safety cap
Maximum total tokens allowed in the assembled prompt (default: `2200`).  
Raising this allows richer context but risks overflow and “lost-in-the-middle” effects.

---

### VECTOR_DB : Vector database backend
Backend used for vector storage and similarity search (default: `faiss`).  
Changing requires a rebuild and may affect performance and persistence format.

---

### CHUNK_SIZE : Document chunk size
Size of chunks created during indexing (default: `351`).  
Smaller chunks improve precision; larger chunks preserve context but reduce retrieval sharpness.

---

### CHUNK_OVERLAP : Chunk overlap size
Overlap between adjacent chunks (default: `40`).  
Prevents boundary context loss but increases index size and near-duplicate retrieval if too large.

---

## Rebuild required when changing
- `EMBED_MODEL`
- `VECTOR_DB`
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- document corpus contents

## No rebuild required when changing
- `MODEL_NAME`
- `TEMPERATURE`
- `MAX_TOKENS`
- `TOP_K`
- `MAX_CONTEXT_MESSAGES`
- `EFFECTIVE_CONTEXT_LIMIT`

