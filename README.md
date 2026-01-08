## Adaptive Local Retrieval Engine for AI Systems

LifePIM AI Core is a local retrieval engine designed to adapt AI search and RAG systems to existing document corpora. 

It analyses document structure and content to inform chunking, indexing, and retrieval strategies, allowing AI systems to be tuned to the data they operate on rather than requiring documents to be restructured. 

The engine is fully local, inspectable, and intended for developers building custom AI workflows.

## Current Status
- it all works, no breaking changes
- working on sample documentation and more ingestion types

## Quick Start

In a new folder, create a new Python 3.12 Virtual environment (doesnt work on 3.14) and clone this code from github

```
    py -3.12 -m venv .venv
    call .venv\Scripts\activate
    git clone https://github.com/acutesoftware/lifepim-ai-core.git
    cd lifepim-ai-core
```

Install the required libraries

`pip install -e .`

Build the vectorstore for the first time (this uses the sample docs provided)

`src\lifepim_ai_core\REBUILD.BAT`

Test the install via the sample 'my_app'

`python .\my_app\main.py short answer only - How does TEMPERATURE impact the search result`


Will return something like below:

```
    Temperature controls the randomness of the LLM’s output: a low value makes the answer 
    more deterministic and conservative, while a high value increases diversity and creativity, 
    but can also produce less focused or less accurate responses. It does not change which 
    chunks are retrieved, only how the final answer is generated.
```



## Rebuilding with your own docs
To you point to your local documentation folder you need modify the lifepim_config.py (in my_app)
Also change the directory of the vectorcache to a local hard disk (not a network share)

Change 
`DOCS_FOLDER = REPO_ROOT / "docs"`

to your document root folder


Run REBUILD.BAT from /src/ folder to rebuild the vectorstores
