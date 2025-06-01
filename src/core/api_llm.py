from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import logging
import time
from src.core.pinecone_retrival import get_context_retrieval

# Load env vars
load_dotenv()
HF_API_KEY = os.getenv("INFERENCE_API_KEY") 
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

# Initialize HF InferenceClient
client = InferenceClient(
    provider="nebius",
    api_key=HF_API_KEY,
)

system_message = {
    "role": "system",
    "content": "You are a helpful assistant that specializes in the history of the Griffith College campus, including its buildings, people, and events. Answer questions using the retrieved historical context.",
}

print(
    "Griffith HistoryBot is ready. Ask about the campus' history! Type 'exit' to quit."
)

while True:
    user_input = input("\n💬 You: ")
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Goodbye! Stay curious about Griffith College.")
        break

    # Log when question received
    question_time = time.time()
    if LOG_LEVEL == "DEBUG":
        logging.debug(f"Question received: {user_input}")

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

    # Inference API call
    llm_start_time = time.time()
    completion = client.chat.completions.create(
        model="mistralai/Mistral-Small-3.1-24B-Instruct-2503",
        messages=messages,
    )
    llm_end_time = time.time()

    answer = completion.choices[0].message.content.strip()
    print("\n📚 GriffithBot:", answer)

    # Log timings
    if LOG_LEVEL == "DEBUG":
        logging.debug(f"LLM generation duration: {llm_end_time - llm_start_time:.3f} seconds")
        logging.debug(f"LLM answer:\n{answer}\n")