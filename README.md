## Adaptive Local Retrieval Engine for AI Systems

LifePIM AI Core is a local retrieval engine designed to adapt AI search and RAG systems to existing document corpora. 

It analyses document structure and content to inform chunking, indexing, and retrieval strategies, allowing AI systems to be tuned to the data they operate on rather than requiring documents to be restructured. 

The engine is fully local, inspectable, and intended for developers building custom AI workflows.

## Current Status
- it all works, no breaking changes
- working on sample documentation and more ingestion types

## Quick Start
- clone the repo from https://github.com/acutesoftware/lifepim-ai-core
- create a virtual environment `python -m venv .venv`
- activate the venv `.venv\Scripts\activate`
- download ollama and install it
- run the `INSTALL.BAT` to install all dependencies
- run the test script in src  `python ./test_ai_cli.py`

## Rebuilding
To you point to your local documentation folder you need modify the config_llm.py (which is inconveniently located in src/core/llm_runtime)
Also change the directory of the vectorcache to a local hard disk (not a network share)

Run REBUILD.BAT from /src/ folder to rebuild the vectorstores
