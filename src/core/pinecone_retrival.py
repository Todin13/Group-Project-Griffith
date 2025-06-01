from pinecone import Pinecone
import os
from dotenv import load_dotenv
import logging
import time

# Load env vars
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "griffith-college-chunks"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
NAMESPACE = "200-history"

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

# Initialize Pinecone client and index
pc = Pinecone(api_key=PINECONE_API_KEY)
dense_index = pc.Index(INDEX_NAME)

def get_context_retrieval(query, top_k=10):
    start_time = time.time()
    reranked_results = dense_index.search(
        namespace=NAMESPACE,
        query={"top_k": top_k, "inputs": {"text": query}},
        rerank={
            "model": "bge-reranker-v2-m3",
            "top_n": top_k,
            "rank_fields": ["chunk_text"],
        },
    )
    end_time = time.time()
    elapsed = end_time - start_time

    hits = reranked_results["result"].get("hits", [])
    context_chunks = [hit["fields"].get("chunk_text", "") for hit in hits]

    token_count = reranked_results.get("usage", {}).get("embed_total_tokens", "N/A")
    read_units = reranked_results.get("usage", {}).get("read_units", "N/A")
    rerank_units = reranked_results.get("usage", {}).get("rerank_units", "N/A")

    if LOG_LEVEL == "DEBUG":
        logging.debug(f"Pinecone search start: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
        logging.debug(f"Pinecone search end: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        logging.debug(f"Pinecone search duration: {elapsed:.3f} seconds")
        logging.debug(f"Pinecone retrieved hits count: {len(hits)}")
        for i, hit in enumerate(hits, 1):
            chunk_text = hit["fields"].get("chunk_text", "<no chunk_text>")
            score = hit.get("score", "N/A")
            logging.debug(f"Hit #{i} (score: {score}): {chunk_text}")

    return context_chunks, token_count, read_units, rerank_units
