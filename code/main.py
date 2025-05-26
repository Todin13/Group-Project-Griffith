import torch
from transformers import pipeline
from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "griffith-college-chunks"

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

def get_context_retrieval(query, top_k=4):
    # Search and rerank results
    reranked_results = dense_index.search(
        namespace="example-namespace",  # replace with your actual namespace
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

    hits = reranked_results['result']['hits']
    # Join the retrieved chunk_texts as context
    context = "\n\n".join(hit['fields']['chunk_text'] for hit in hits)
    return context

print("🏫 Griffith HistoryBot is ready. Ask about the college's history! Type 'exit' to quit.")

while True:
    user_input = input("\n💬 You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Goodbye! Stay curious about Griffith College.")
        break

    # Retrieve context using reranked search
    context = get_context_retrieval(user_input)

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

    print("\n📚 GriffithBot:", outputs[0]["generated_text"][len(prompt):].strip())
