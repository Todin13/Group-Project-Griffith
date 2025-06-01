import os
import json
import time
import logging
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import src.config as config

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

# Load FAISS index
print("Loading FAISS index...")
index = faiss.read_index(config.INDEX_FILE)

# Load ID map (int ID → string _id)
with open(config.ID_MAP_FILE, "r", encoding="utf-8") as f:
    id_map = json.load(f)

# Load text store (int ID → full record)
with open(config.TEXT_STORE_FILE, "r", encoding="utf-8") as f:
    text_store = json.load(f)

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)

def get_context_retrieval(query, top_k=10):
    start_time = time.time()
    if config.LOG_LEVEL == "DEBUG":
        logger.debug(f"FAISS search start: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

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

        if config.LOG_LEVEL == "DEBUG":
            logger.debug(f"Hit #{i} (distance: {dist:.4f}): ID {record_id} - Text: {chunk_text}")

    if config.LOG_LEVEL == "DEBUG":
        logger.debug(f"FAISS search end: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        logger.debug(f"FAISS search duration: {elapsed:.3f} seconds")
        logger.debug(f"FAISS retrieved hits count: {len(results)}")

    print(f"FAISS search took {elapsed:.3f} seconds, found {len(context_chunks)} results")

    token_count = "N/A"
    read_units = "N/A"
    rerank_units = "N/A"

    return context_chunks, token_count, read_units, rerank_units
