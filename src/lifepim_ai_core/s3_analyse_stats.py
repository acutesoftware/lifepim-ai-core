import time
import sqlite3
import re
from collections import Counter

from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer


from lifepim_ai_core.db import insert_many_stats 

# For clustering
from sentence_transformers import SentenceTransformer
import hdbscan
import numpy as np
from lifepim_ai_core.core.llm_runtime import config as cfg


def analyse_text(chunk_text: str):
    """
    Produce simple quality stats for a chunk.
    """
    words = re.findall(r"\w+", chunk_text.lower())
    unique_words = set(words)

    stats = {
        "num_chars": len(chunk_text),
        "num_words": len(words),
        "num_unique_words": len(unique_words),
        "avg_word_length": (sum(len(w) for w in words) / len(words)) if words else 0,
    }
    return stats


def process_chunks(db_path: str):
    # --- Part 1: Fetch data from the database ---
    # This part remains the same. It's efficient to fetch data in one go.
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT id, chunk_text FROM document_chunks")
    chunks = cur.fetchall()
    conn.close()

    # --- Part 2: Process data and prepare for batch insert ---
    
    # Create an empty list to hold all the stats we generate.
    stats_to_insert = []

    for row in chunks:
        chunk_id = row["id"]
        stats = analyse_text(row["chunk_text"])

        # Instead of inserting here, append the data to our list.
        for name, val in stats.items():
            stats_to_insert.append((chunk_id, name, val))

    # --- Part 3: Perform a single, fast batch insert ---
    if stats_to_insert:
        insert_many_stats(db_path, stats_to_insert)

    print(f"📊 Completed. {len(stats_to_insert)} stats inserted for {len(chunks)} chunks.")

def cluster_chunks(db_path: str, min_cluster_size: int = 5):
    """
    Cluster chunks by semantic similarity and store cluster IDs.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT id, chunk_text FROM document_chunks  limit 5000")
    chunks = cur.fetchall()

    if not chunks:
        print("⚠️ No chunks found to cluster.")
        conn.close()
        return

    # Prepare texts
    chunk_ids = [row["id"] for row in chunks]
    texts = [row["chunk_text"] for row in chunks]

    # Encode with sentence-transformers
    model = SentenceTransformer("all-MiniLM-L6-v2")  # small & fast
    embeddings = model.encode(texts, show_progress_bar=True)

    # Cluster with HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric="euclidean")
    labels = clusterer.fit_predict(embeddings)

    # collect cluster stats
    lst_clusters = []
    for cid, label in zip(chunk_ids, labels):
        #insert_stat(db_path, cid, "cluster_id", int(label))
        lst_clusters.append([cid, "cluster_id", int(label)])
        

    # Save to DB 

    insert_many_stats(db_path, lst_clusters)
    conn.close()
    print(f"🔗 Clustered {len(chunks)} chunks into {len(set(labels))} groups.")

def summarize_clusters(db_path: str, top_n: int = 10):
    """
    Summarize clusters using TF-IDF weighted keywords with stopword filtering.
    Falls back to raw frequency if cluster text is too small.
    Returns {cluster_id: [keywords]}.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all chunks + cluster labels
    cur.execute("""
        SELECT c.id, c.chunk_text, s.stat_value as cluster_id
        FROM document_chunks c
        JOIN chunk_stats s ON c.id = s.chunk_id
        WHERE s.stat_name = 'cluster_id'
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("⚠️ No clustered chunks found.")
        return {}

    clusters = defaultdict(list)
    for row in rows:
        cid = int(row["cluster_id"])
        clusters[cid].append(row["chunk_text"])

    summaries = {}
    for cid, docs in clusters.items():
        try:
            # Vectorize cluster texts
            vectorizer = TfidfVectorizer(
                stop_words="english",
                token_pattern=r"(?u)\b\w+\b",  # include numbers/underscores
                max_features=5000
            )
            tfidf_matrix = vectorizer.fit_transform(docs)

            if tfidf_matrix.shape[1] == 0:
                raise ValueError("Empty vocabulary")

            avg_scores = tfidf_matrix.mean(axis=0).A1
            terms = vectorizer.get_feature_names_out()
            top_indices = avg_scores.argsort()[::-1][:top_n]
            top_keywords = [terms[i] for i in top_indices]

        except ValueError:
            # Fallback: simple word counts
            all_words = " ".join(docs).lower().split()
            counter = Counter(all_words)
            top_keywords = [w for w, _ in counter.most_common(top_n)]

        summaries[cid] = top_keywords

    # Print nicely
    for cid, keywords in summaries.items():
        print(f"📂 Cluster {cid}: {', '.join(keywords)}")

    return summaries


if __name__ == "__main__":
    start = time.time()
    process_chunks(cfg.DB_FILE_METADATA)
    cluster_chunks(cfg.DB_FILE_METADATA)
    summarize_clusters(cfg.DB_FILE_METADATA, top_n = 10)
    print(f"⏱️ Done in {time.time()-start:.2f}s")
