from huggingface_hub import InferenceClient
import logging
import time
import src.config as config
from src.core.pinecone_retrival import get_context_retrieval

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

# Initialize HF InferenceClient using config
client = InferenceClient(
    provider="nebius",
    api_key=config.HF_API_KEY,
)

system_message = {
    "role": "system",
    "content": "You are a helpful assistant that specializes in the history of the Griffith College campus, including its buildings, people, and events. Answer questions using the retrieved historical context.",
}

def api_llm_question(user_input:str,get_context_retrieval): 
    question_time = time.time()
    logger.info("Received a question.")

    if config.LOG_LEVEL == "DEBUG":
        logger.debug(f"Question: {user_input}")

    # Get context
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

    # Logging
    if config.LOG_LEVEL == "DEBUG":
        logger.debug(f"LLM generation duration: {llm_end_time - llm_start_time:.3f} seconds")
        logger.debug(f"LLM answer:\n{answer}\n")
    
    return answer


if __name__ == "__main__":
    while True:

        print("Griffith HistoryBot is ready. Ask about the campus' history! Type 'exit' to quit.")
        
        user_input = input("\n💬 You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye! Stay curious about Griffith College.")
            break
        
        answer = api_llm_question(user_input, get_context_retrieval)

        print("\n📚 GriffithBot:", answer)