import os
import time
import sqlite3

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    PyMuPDFLoader,
    PyPDFLoader,
    Docx2txtLoader
)
from db import insert_chunk
from core.llm_runtime import config_llm as cfg


def load_file_content(file_path: str):
    """
    Load content from text/markdown/pdf files. Also XLS, DOCX 

    """
    ext = os.path.splitext(file_path)[1].lower()

    #meta_fs = file_metadata(path)

    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        #meta_content = pdf_metadata(path)
    elif file_path.lower().endswith(".docx"):
        loader = Docx2txtLoader(file_path)
        #meta_content = {}
    elif file_path.lower().endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        #meta_content = {}
    elif file_path.lower().endswith(".md"):
        loader = UnstructuredMarkdownLoader(file_path)
        #meta_content = {}
    else:
        #print(f"Skipping unsupported file: {file_path}")
        return None
    
    docs = loader.load()


    return " ".join([d.page_content for d in docs])


def split_into_chunks(text: str, chunk_size, overlap):
    """
    Split text into LangChain Document-like chunks.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)


def process_files(db_path, chunk_size, overlap):
    """
    Takes a list of files from the database, loads and splits them into chunks,
    and stores the chunks back in the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT id, file_path FROM files")
    files = cur.fetchall()
    conn.close()

    total_chunks = 0

    for row in files:
        file_id = row["id"]
        fpath = row["file_path"]

        try:
            text = load_file_content(fpath)
            chunks = split_into_chunks(text, chunk_size, overlap)

            for i, chunk in enumerate(chunks):
                insert_chunk(db_path,  file_id, i, chunk)

            print(f"{os.path.basename(fpath)} -> {len(chunks)} chunks")
            total_chunks += len(chunks)

        except Exception as e:
            print(f"Error loading {fpath}: {e}")

    print(f"Completed. {total_chunks} chunks stored.")


if __name__ == "__main__":
    start = time.time()
    process_files(cfg.DB_FILE_METADATA, cfg.CHUNK_SIZE, cfg.CHUNK_OVERLAP)
    print(f"Done in {time.time()-start:.2f}s")
