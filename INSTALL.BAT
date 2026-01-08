@echo off

REM Create & activate virtual env
REM python -m venv .venv
REM call .venv\Scripts\activate

REM Upgrade pip first
python -m pip install --upgrade pip

REM Core numeric / ML stack (install early)
pip install --upgrade numpy pandas scikit-learn

REM Core LLM + RAG libraries
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install langchain-huggingface
pip install -U langchain-ollama

REM Vector stores & embeddings
pip install chromadb
pip install faiss-cpu

REM Document ingestion & preprocessing
pip install pymupdf
pip install unstructured
pip install docx2txt
pip install markdown
pip install textstat

REM Embeddings / NLP
pip install sentence-transformers
pip install sentencepiece
pip install transformers

REM Clustering
pip install hdbscan


REM Ollama setup (run manually in PowerShell)
REM Download & install Ollama from:
REM https://ollama.com/download

REM Then run:
REM ollama pull nomic-embed-text
REM ollama pull mistral

echo.
echo INSTALL COMPLETE
echo If something fails, rerun with:
echo   pip install --upgrade --force-reinstall numpy scipy
