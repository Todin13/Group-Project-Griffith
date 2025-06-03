def is_about_chatbot(question: str) -> bool:
    chatbot_keywords = [
        "who are you",
        "what are you",
        "what's your role",
        "your job",
        "your task",
        "what do you do",
        "your goal",
        "your purpose",
        "tell me about yourself",
        "what can you do",
        "who made you",
        "are you real",
        "are you an ai",
        "how do you work",
        "how were you trained",
    ]

    question_lower = question.lower()
    return any(keyword in question_lower for keyword in chatbot_keywords)
