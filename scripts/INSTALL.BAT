pip install langchain chromadb openai pymupdf

REM - download Ollama from https://ollama.com/download

pip install langchain-community

pip install unstructured

REM Windows PowerShell
REM  ollama pull nomic-embed-text
pip install faiss-cpu
pip install -U langchain-ollama

pip install flask


REM --- doc preprocessing

pip install textstat
pip install sentence-transformers

REM start powershell and run:
ollama pull mistral

REM - additional bits below may be needed on PCs with existing installs of libs

pip install langchain_openai
pip install -U langchain-huggingface
pip install --upgrade --force-reinstall numpy pandas scikit-learn


REM clustering

pip install hdbscan

REM after other subject installs, need old version of pip install tf-keras

pip install tf-keras

REM additional stuff
pip install markdown

pip install sentencepiece transformers tiktoken
pip install flask