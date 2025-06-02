import torch
from transformers import pipeline
import time
import logging
import src.config as config
from src.core.pinecone_retrival import get_context_retrieval
from src.core.question_analysis import is_about_chatbot

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

# Llama 3.2-3B generation pipeline
pipe = pipeline(
    "text-generation",
    model=config.LOCAL_MODEL,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

system_message = {
    "role": "system",
    "content": "You are a helpful assistant that specializes in the history of the Griffith College campus, including its buildings, people, and events. Answer questions using the retrieved historical context.",
}


def local_llm_question(user_input, get_context_retrieval):
    question_time = time.time()
    logger.info("Received a question.")

    if config.LOG_LEVEL == "DEBUG":
        logger.debug(f"Question: {user_input}")
        logger.debug(
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(question_time))}"
        )

    if is_about_chatbot(user_input):
        # Detect if user is asking about the chatbot
        context = ("You are GriffithBot, a helpful assistant that only answers questions related to the history of Griffith College, "
        "its campus, buildings, people, and events. If a user asks a question unrelated to Griffith College, politely "
        "refuse to answer and remind them of your specialty.")
    else:
        # Use RAG for Griffith College-related questions
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

    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    # Log LLM start time
    llm_start_time = time.time()
    if config.LOG_LEVEL == "DEBUG":
        logger.debug(
            f"LLM generation started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(llm_start_time))}"
        )

    # Generate response
    outputs = pipe(
        prompt,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )

    llm_end_time = time.time()
    answer = outputs[0]["generated_text"][len(prompt) :].strip()

    if config.LOG_LEVEL == "DEBUG":
        logger.debug(
            f"LLM generation ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(llm_end_time))}"
        )
        logger.debug(
            f"LLM generation duration: {llm_end_time - llm_start_time:.3f} seconds"
        )
        logger.debug(f"LLM answer:\n{answer}\n")

    return answer


if __name__ == "__main__":

    print(
        "Griffith HistoryBot is ready. Ask about the campus' history! Type 'exit' to quit."
    )

    while True:
        user_input = input("\n💬 You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye! Stay curious about Griffith College.")
            break
        answer = local_llm_question(user_input, get_context_retrieval)
        print("\n📚 GriffithBot:", answer)
        print(
            "Griffith HistoryBot is ready. Ask about the campus' history! Type 'exit' to quit."
        )
