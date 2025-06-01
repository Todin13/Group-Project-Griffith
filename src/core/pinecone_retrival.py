from pinecone import Pinecone
import time
import logging
import src.config as config

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

# Initialize Pinecone client and index
pc = Pinecone(api_key=config.PINECONE_API_KEY)
dense_index = pc.Index(config.PINECONE_INDEX_NAME)

def get_context_retrieval(query, top_k=10):
    start_time = time.time()

    reranked_results = dense_index.search(
        namespace=config.PINECONE_NAMESPACE,
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

    if config.LOG_LEVEL == "DEBUG":
        logger.debug(f"Pinecone search started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
        logger.debug(f"Pinecone search ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        logger.debug(f"Pinecone search duration: {elapsed:.3f} seconds")
        logger.debug(f"Pinecone retrieved {len(hits)} hits")
        for i, hit in enumerate(hits, 1):
            chunk_text = hit["fields"].get("chunk_text", "<no chunk_text>")
            score = hit.get("score", "N/A")
            logger.debug(f"Hit #{i} (score: {score}): {chunk_text}")

    return context_chunks, token_count, read_units, rerank_units
