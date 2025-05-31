# 🎓 Group Project — BSc Computer Science @ Griffith College

A practical exploration of Retrieval-Augmented Generation (RAG) using PDF data, vector search with Pinecone, and large language models like TinyLlama and LLaMA 3.1-8B.

## 📂 Data Extraction & Processing

To extract and prepare the content from PDF files, the project uses several shell scripts and tools:

| Tool / Script                                                | Purpose                                                           |
| ------------------------------------------------------------ | ----------------------------------------------------------------- |
| `pdfimages`                                                  | Extract images from PDFs                                          |
| `pdftotext`                                                  | Extract raw text from PDFs                                        |
| [clean.sh](./code/pdf_manipulation/clean.sh)                 | Clean and sanitize the extracted text                             |
| [split_txt.sh](./code/pdf_manipulation/split_txt.sh)         | Split text into chapters, summaries, and bibliographies           |
| [create_chunks.sh](./code/pdf_manipulation/create_chunks.sh) | Break the text into chunks suitable for embedding                 |
| [pdf_to_chunk.sh](./code/pdf_manipulation/pdf_to_chunk.sh)   | Master script: combines cleaning, splitting, and chunking for RAG |

## 🧠 Model Choices

### 🔹 [TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) — _~2.5 GB_

- ✅ Lightweight and deployable on low-resource machines
- ⚠️ Slower response time (~30 seconds) and prone to hallucinations, especially with larger context input

### 🔸 [LLaMA 3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) — _~15 GB_

- ✅ Much more capable with faster responses, higher token capacity, and better context handling
- ⚠️ Requires significantly more hardware resources
- 📜 **Note**: You must accept the [**LLAMA 3.1 COMMUNITY LICENSE AGREEMENT**](./LLAMA%203.1%20COMMUNITY%20LICENSE%20AGREEMENT) before use

## 🚀 Initialize the App

### 🔧 Prerequisites

Ensure the following are installed on your system:

- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
- [poetry](https://python-poetry.org/docs/#installing-manually)

### ⚙️ Setup Instructions

Install Python 3.13 and dependencies:

    pyenv install 3.13
    pyenv local 3.13
    make prepare

## 🧱 Create the RAG

### 🌲 Pinecone Setup

1.  Create a free account at [Pinecone](https://app.pinecone.io/?sessionType=login)
2.  Copy your API key and paste it into the `.env` file like so:

         PINECONE_API_KEY=your_token_here

3.  Prepare and upload the data:

         make data-transfo # Clean, split, and chunk the data
         make populate # Upload to Pinecone

## 🔍 Get the Model

### 🧠 Accessing LLaMA 3.1-8B

1.  Create or log in to a [Hugging Face account](https://huggingface.co/login)
2.  Visit the [LLaMA 3.1-8B model page](https://huggingface.co/meta-llama/Llama-3.1-8B)
3.  Accept the [LLAMA 3.1 COMMUNITY LICENSE AGREEMENT](./LLAMA%203.1%20COMMUNITY%20LICENSE%20AGREEMENT)
4.  Log in via CLI:

         make login

5.  (Optional) To enable debug logging, add this to your `.env` file:

         LOG_LEVEL="DEBUG"

6.  Run the application:

         make run

## ✅ Summary

| Component      | Description                                                 |
| -------------- | ----------------------------------------------------------- |
| **Data Tools** | Shell scripts for image/text extraction, cleaning, chunking |
| **Vector DB**  | Pinecone for storing and retrieving semantic chunks         |
| **LLMs**       | TinyLlama (lightweight), LLaMA 3.1-8B (advanced)            |
| **License**    | Required for LLaMA 3.1-8B usage via Hugging Face            |
| **Setup**      | Python 3.13 via pyenv, Poetry for dependency management     |
