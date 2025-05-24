# Group-Project-Griffith

Group Project Bachelor in Computer Science Griffith College

This project is an offline, local question-answering (Q&A) system that uses a local language model (LLM) to answer questions about the history of Griffith College based on a 200-year historical document. It supports natural language queries and uses retrieval-augmented generation (RAG) to provide context-aware responses.

---

## 🚀 Features

- **Fully Offline**: Runs on Raspberry Pi or other low-resource devices
- **No Internet Required**: All inference happens locally
- **RAG-Based Architecture**: Combines vector search with an LLM
- **Streamlit Frontend**: Clean web UI for interactive Q&A
- **Custom Data**: Based on Griffith College's 200-year history

---

## 🧠 Why I Chose TinyLLaMA for This Project

For this project — building a lightweight, offline, RAG-based Q&A system — I needed a language model that could:

- Run on low-resource hardware (like a Raspberry Pi)
- Work entirely offline with no API costs
- Integrate with RAG (Retrieval-Augmented Generation)
- Generate text answers from historical context

After comparing available open-source LLMs, I chose **TinyLLaMA (1.1B)** as the best balance between size, speed, and capabilities.

### 📊 Model Comparison Table

| Model         | Size      | RAM Needed        | Speed (CPU)   | RAG Capable | Offline Use | Notes                           |
| ------------- | --------- | ----------------- | ------------- | ----------- | ----------- | ------------------------------- |
| **TinyLLaMA** | 1.1B      | ✅ Low (~2GB)     | ✅ Fast       | ✅ Yes      | ✅ Yes      | Ideal for embedded/edge devices |
| Phi-2         | 2.7B      | ⚠️ Medium (4–6GB) | ⚠️ Slower     | ✅ Yes      | ✅ Yes      | Higher reasoning, heavier model |
| Mistral       | 7B        | ❌ High (8–16GB)  | ❌ Very slow  | ✅ Yes      | ✅ Yes      | Too large for Raspberry Pi      |
| GPT-4/GPT-3.5 | N/A (API) | N/A               | ✅ Fast (API) | ✅ Yes      | ❌ No       | Requires internet + paid access |

### ✅ Why TinyLLaMA Was the Best Fit

- **🧠 Small Size (1.1B)**: Runs on low-memory devices like Raspberry Pi.
- **🛠️ GGUF Format**: Quantized and accelerated with llama.cpp.
- **📦 Offline Support**: No internet or external APIs needed.
- **⚡ Real-Time Enough**: Fast enough for historical Q&A.
- **🧩 RAG Ready**: Works with FAISS and LangChain.
- **💰 Free**: Fully open-source and cost-free.

### ❗ Trade-offs

- **Shorter context window** (~1024 tokens)
- **Lower precision** than large-scale LLMs (GPT-4, etc.)
- **Best for factual recall**, not deep logic or reasoning

---

## 📂 Project Structure

griffith-qa/
├── app.py # Original app entry point
├── build_index.py # Script to build FAISS index from text
├── streamlit_app.py # Streamlit web UI
├── llm_loader.py # Loads TinyLLaMA using llama.cpp
├── model/
│ ├── Griffith College 200 Years.pdf
│ └── griffith_vectorstore/ # FAISS vector database
├── models/
│ └── tinyllama.gguf # Quantized TinyLLaMA model
├── requirements.txt
├── README.md

## ⚙️ Usage Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```
