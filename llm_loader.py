from langchain_community.llms import LlamaCpp

def load_llm(model_path="models/tinyllama.gguf", max_tokens=512, n_ctx=1024, n_batch=16):
    return LlamaCpp(
        model_path=model_path,
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        n_ctx=n_ctx,
        n_batch=n_batch,
        verbose=False
    )
