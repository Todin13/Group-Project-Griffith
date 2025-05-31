import torch
from transformers import pipeline
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

# Llama 3.1-8B generation pipeline
pipe = pipeline(
    "text-generation",
    model="meta-llama/Llama-3.2-3B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

system_message = {
    "role": "system",
    "content": "You are a helpful assistant that specializes in the history of the Griffith College campus, including its buildings, people, and events. Answer questions using the retrieved historical context.",
}


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


print(
    "Griffith HistoryBot is ready. Ask about the campus' history! Type 'exit' to quit."
)

def ask_model(user_input):
    # Log when question received
    question_time = time.time()
    if LOG_LEVEL == "DEBUG":
        logging.debug(f"Question received: {user_input}")
        logging.debug(f"Question timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(question_time))}")

    # Get context and usage
    context_chunks, tokens, read_units, rerank_units = get_context_retrieval(
        user_input, top_k=5
    )
    context = "\n\n".join(context_chunks)

    messages = [
        system_message,
        {
            "role": "user",
            "content": (
                f"Here is some reference material about Griffith College:\n\n{context}\n\n"
                f"Using this information, please answer the following question:\n{user_input}"
            ),
        },
    ]

    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    # Log before LLM generation start
    llm_start_time = time.time()
    if LOG_LEVEL == "DEBUG":
        logging.debug(f"LLM generation start: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(llm_start_time))}")

    outputs = pipe(
        prompt,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )
    # save endtime of LLm
    llm_end_time = time.time()
    
    answer = outputs[0]["generated_text"][len(prompt) :]
   

    # Log after LLM generation end
    if LOG_LEVEL == "DEBUG":
        logging.debug(f"LLM generation end: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(llm_end_time))}")
        logging.debug(f"LLM generation duration: {llm_end_time - llm_start_time:.3f} seconds")
        logging.debug(f"LLM answer:\n{answer}\n")

    return answer