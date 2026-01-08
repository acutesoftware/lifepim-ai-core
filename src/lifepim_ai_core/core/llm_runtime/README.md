Runtime folder to manage the LLM - all LangChain imports should be in here only


## Folder structure 
core/llm_runtime/
  __init__.py
  runtime.py        # singleton access
  llm.py            # the class
  factory.py        # LangChain construction
  rag.py
  prompts.py
  config.py

  