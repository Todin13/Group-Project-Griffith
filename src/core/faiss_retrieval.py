import os
import json
import time
import logging
import numpy as np
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure logging
if LOG_LEVEL == "DEBUG":
    logging.basicConfig(
        filename="debug.log",
        level=logging.DEBUG,
        filemode="a",
        format="%(asctime)s - %(message)s",
    )
else:
    logging.basicConfig(level=logging.INFO)

# File paths
INDEX_DIR = "LOCAL_RAG"
INDEX_FILE = os.path.join(INDEX_DIR, "griffith_index.faiss")
ID_MAP_FILE = os.path.join(INDEX_DIR, "id_map.json")
TEXT_STORE_FILE = os.path.join(INDEX_DIR, "text_store.json")

# Load FAISS index
print("Loading FAISS index...")
index = faiss.read_index(INDEX_FILE)

# Load ID map (int ID → string _id)
with open(ID_MAP_FILE, "r", encoding="utf-8") as f:
    id_map = json.load(f)

# Load text store (int ID → full record)
with open(TEXT_STORE_FILE, "r", encoding="utf-8") as f:
    text_store = json.load(f)

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_context_retrieval(query, top_k=10):
    start_time = time.time()
    if LOG_LEVEL == "DEBUG":
        logging.debug(f"FAISS search start: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    # Embed query
    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    # Search FAISS index
    distances, indices = index.search(query_vec, top_k)

    end_time = time.time()
    elapsed = end_time - start_time

    results = []
    context_chunks = []

    for i, (dist, idx) in enumerate(zip(distances[0], indices[0]), 1):
        if idx == -1:
            continue
        str_id = str(idx)
        record_id = id_map.get(str_id, "UNKNOWN_ID")
        chunk_text = text_store.get(str_id, {}).get("chunk_text", "<no text>")
        
        results.append({
            "id": record_id,
            "distance": float(dist),
            "chunk_text": chunk_text,
        })

        context_chunks.append(chunk_text)

        if LOG_LEVEL == "DEBUG":
            logging.debug(f"Hit #{i} (distance: {dist:.4f}): ID {record_id} - Text: {chunk_text}")

    if LOG_LEVEL == "DEBUG":
        logging.debug(f"FAISS search end: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        logging.debug(f"FAISS search duration: {elapsed:.3f} seconds")
        logging.debug(f"FAISS retrieved hits count: {len(results)}")

    print(f"FAISS search took {elapsed:.3f} seconds, found {len(context_chunks)} results")

    token_count = "N/A"
    read_units = "N/A"
    rerank_units = "N/A"

    return context_chunks, token_count, read_units, rerank_units
