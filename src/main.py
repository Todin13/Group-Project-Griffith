from src.core.faiss_retrieval import get_context_retrieval
from src.core.api_llm import api_llm_question

if __name__ == "__main__":
    while True:

        print(
            "Griffith HistoryBot is ready. Ask about the campus' history! Type 'exit' to quit."
        )

        user_input = input("\n💬 You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye! Stay curious about Griffith College.")
            break

        answer = api_llm_question(user_input, get_context_retrieval)

        print("\n📚 GriffithBot:", answer)
