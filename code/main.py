import torch
from transformers import pipeline
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import logging

# Load env vars
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "griffith-college-chunks"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
NAMESPACE = "200-history"

# Configure logging
if LOG_LEVEL == "DEBUG":
    logging.basicConfig(filename="debug.log", level=logging.DEBUG, filemode='a',
                        format='%(asctime)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO)

# Initialize Pinecone client and index
pc = Pinecone(api_key=PINECONE_API_KEY)
dense_index = pc.Index(INDEX_NAME)

# TinyLlama generation pipeline
pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

system_message = {
    "role": "system",
    "content": "You are a helpful assistant that specializes in the history of Griffith College Dublin from 1813 to 2013. Answer questions using the retrieved historical context.",
}


def get_context_retrieval(query, top_k=10):
    reranked_results = dense_index.search(
        namespace=NAMESPACE,
        query={
            "top_k": top_k,
            "inputs": {
                "text": query
            }
        },
        rerank={
            "model": "bge-reranker-v2-m3",
            "top_n": top_k,
            "rank_fields": ["chunk_text"]
        }
    )

    hits = reranked_results['result'].get('hits', [])
    context_chunks = [hit['fields'].get('chunk_text', '') for hit in hits]

    # Extract usage metrics
    token_count = reranked_results.get('usage', {}).get('embed_total_tokens', 'N/A')
    read_units = reranked_results.get('usage', {}).get('read_units', 'N/A')
    rerank_units = reranked_results.get('usage', {}).get('rerank_units', 'N/A')

    return context_chunks, token_count, read_units, rerank_units


print("Griffith HistoryBot is ready. Ask about the college's history! Type 'exit' to quit.")

while True:
    user_input = input("\n💬 You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Goodbye! Stay curious about Griffith College.")
        break

    # Get context and usage
    context_chunks, tokens, read_units, rerank_units = get_context_retrieval(user_input, top_k=5)
    context = "\n\n".join(context_chunks)

    messages = [
        system_message,
        {
            "role": "user",
            "content": (
                f"Here is some reference material about Griffith College:\n\n{context}\n\n"
                f"Using this information, please answer the following question:\n{user_input}"
            ),
        }
    ]

    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    outputs = pipe(
        prompt,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )

    answer = outputs[0]["generated_text"][len(prompt):].strip()
    print("\n📚 GriffithBot:", answer)

    # Debug logging
    if LOG_LEVEL == "DEBUG":
        log_message = (
            f"\nQUESTION: {user_input}\n"
            f"TOKENS USED: {tokens}\n"
            f"READ UNITS USED: {read_units}\n"
            f"RERANK UNITS USED: {rerank_units}\n"
            f"RETRIEVED CHUNKS:\n" +
            "\n---\n".join(context_chunks) +
            f"\nANSWER:\n{answer}\n"
        )
        logging.debug(log_message)
