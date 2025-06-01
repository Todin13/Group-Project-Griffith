# 🎓 Group Project — BSc Computer Science @ Griffith College

A practical exploration of Retrieval-Augmented Generation (RAG) using PDF data, vector search with Pinecone, and large language models like TinyLlama and LLaMA 3.1-8B.

## 📂 Data Extraction & Processing

To extract and prepare the content from PDF files, the project uses several shell scripts and tools:

| Tool / Script                                                | Purpose                                                           |
| ------------------------------------------------------------ | ----------------------------------------------------------------- |
| [pdfimages](https://www.xpdfreader.com/pdfimages-man.html)   | Extract images from PDFs                                          |
| [pdftotext](https://www.xpdfreader.com/pdftotext-man.html)   | Extract raw text from PDFs                                        |
| [clean.sh](./code/pdf_manipulation/clean.sh)                 | Clean and sanitize the extracted text                             |
| [split_txt.sh](./code/pdf_manipulation/split_txt.sh)         | Split text into chapters, summaries, and bibliographies           |
| [create_chunks.sh](./code/pdf_manipulation/create_chunks.sh) | Break the text into chunks suitable for embedding                 |
| [pdf_to_chunk.sh](./code/pdf_manipulation/pdf_to_chunk.sh)   | Master script: combines cleaning, splitting, and chunking for RAG |

## 🧠 Model Choices

### 🔹 [TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) — _~2.5 GB_

- ✅ Lightweight and deployable on low-resource machines
- ⚠️ Prone to hallucinations, especially with larger context input
- Take around 30 second to answer with a NVIDIA GeForece RTX 2060 Mobile and an Intel i5-10300H

### 🔸 [LLaMA 3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) — _~15 GB_

- ✅ Much more capable with faster responses, higher token capacity, and better context handling
- ⚠️ Requires significantly more hardware resources
- Take around 3 minutes to answer with a NVIDIA GeForece RTX 2060 Mobile and an Intel i5-10300H
- 📜 **Note**: You must accept the [**LLAMA 3.1 COMMUNITY LICENSE AGREEMENT**](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/blob/main/LICENSE) before use

### 🔸 [LLaMA 3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) — _~6.5 GB_

- ✅ Smaller than 8B version but still powerful with instruction-following capabilities
- ⚠️ Requires moderate hardware resources compared to larger LLaMA models
- Take around 1 minutes to answer with a NVIDIA GeForece RTX 2060 Mobile and an Intel i5-10300H
- 📜 **Note**: You must accept the [**LLAMA 3.2 COMMUNITY LICENSE AGREEMENT**](.https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct/blob/main/LICENSE.txt) before use

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
2.  Visit the [Llama 3.2-3B-Instruct model page](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)
3.  Accept the [LLAMA 3.2 COMMUNITY LICENSE AGREEMENT](./LLAMA%203.2%20COMMUNITY%20LICENSE%20AGREEMENT)
4.  Log in via CLI:

         make login

5.  (Optional) To enable debug logging, add this to your `.env` file:

         LOG_LEVEL="D│ ├── faiss/ # FAISS-based local vector database alternativeEBUG"

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

## 📁 Project Structure

The project is organized as follows:

        root/
        ├── src/
        │   ├── app/                    # Frontend logic, app design, and integration principles
        │   ├── core/                   # Core backend logic: RAG orchestration and model interaction
        │   ├── faiss/                  # FAISS-based local vector database alternative
        │   ├── pdf_manipulation/       # Scripts to clean, split, and chunk PDF data
        │   ├── pinecone/               # Pinecone vector DB configuration and indexing logic
        │   └── main.py                 # Entry point: application bootstrap and launch logic
        │
        ├── .env.example                # Example environment configuration file
        ├── .gitignore                  # Git configuration to ignore local/dev files
        ├── Griffith College 200 Years.pdf # Source document used in the RAG pipeline
        ├── LICENSE                     # Open-source project license
        ├── LLAMA 3.2 COMMUNITY LICENSE AGREEMENT  # Required license agreement for using LLaMA 3.2 models
        ├── Makefile                    # Automation commands for setup, data processing, and deployment
        ├── pyproject.toml              # Poetry project configuration and dependencies
        ├── README.md                   # Project documentation

Each directory and file is purposefully designed to keep the app modular, easy to maintain, and scalable for LLM-powered applications using Retrieval-Augmented Generation (RAG).
