# 🎓 Group Project — BSc Computer Science @ Griffith College

A practical exploration of Retrieval-Augmented Generation (RAG) using PDF data, vector search with Pinecone, and large language models like TinyLlama and LLaMA 3.1-8B.

## 📂 Data Extraction & Processing

To extract and prepare the content from PDF files, the project uses several shell scripts and tools:

| Tool / Script                                                            | Purpose                                                             |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| [pdfimages](https://www.xpdfreader.com/pdfimages-man.html)               | Extract images from PDFs                                            |
| [pdftotext](https://www.xpdfreader.com/pdftotext-man.html)               | Extract raw text from PDFs                                          |
| [magick](https://imagemagick.org/index.php)                              | CLI tool from ImageMagick used to convert and process image formats |
| [clean.sh](./code/pdf_manipulation/clean.sh)                             | Clean and sanitize the extracted text                               |
| [split_txt.sh](./code/pdf_manipulation/split_txt.sh)                     | Split text into chapters, summaries, and bibliographies             |
| [create_chunks.sh](./code/pdf_manipulation/create_chunks.sh)             | Break the text into chunks suitable for embedding                   |
| [pdf_to_chunk.sh](./code/pdf_manipulation/pdf_to_chunk.sh)               | Master script: combines cleaning, splitting, and chunking for RAG   |
| [convert_ppm_to_jpeg.sh](./code/pdf_manipulation/convert_ppm_to_jpeg.sh) | Convert `.ppm` images (from `pdfimages`) to `.jpg` format           |

## 🧠 Model Choices

### Local Model

#### 🔹 [TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) — _~2.5 GB_

- Tried
- ✅ Lightweight and deployable on low-resource machines
- ⚠️ Prone to hallucinations, especially with larger context input
- Take around 30 second to answer with a NVIDIA GeForece RTX 2060 Mobile and an Intel i5-10300H

#### 🔸 [LLaMA 3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) — _~15 GB_

- Tried
- ✅ Much more capable with faster responses, higher token capacity, and better context handling
- ⚠️ Requires significantly more hardware resources
- Take around 3 minutes to answer with a NVIDIA GeForece RTX 2060 Mobile and an Intel i5-10300H
- 📜 **Note**: You must accept the [**LLAMA 3.1 COMMUNITY LICENSE AGREEMENT**](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/blob/main/LICENSE) before use

#### [LLaMA 3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) — _~6.5 GB_

- Actual one
- ✅ Smaller than 8B version but still powerful with instruction-following capabilities
- ⚠️ Requires moderate hardware resources compared to larger LLaMA models
- Take around 1 minutes and 30 seconds to answer with a NVIDIA GeForece RTX 2060 Mobile and an Intel i5-10300H
- 📜 **Note**: You must accept the [**LLAMA 3.2 COMMUNITY LICENSE AGREEMENT**](.https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct/blob/main/LICENSE.txt) before use

### Hugging Face Inference API Model

### 🔸 [Mistral-Small-3.1-24B-Instruct](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) — _In Hugging Face Cloud_

- ✅ 24B parameters — strong instruction-following and reasoning capabilities
- 🌐 **Cloud-hosted** model: requires an active internet connection and only a small part of the request are free
- ⚠️ Cannot run locally due to model size and hosting constraints

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

         make data-transfo      # Clean, split, and chunk the data
         make pinecone-populate # Upload to Pinecone

### Faiss Setup

1.  Prepare and upload the data:

         make data-transfo      # Clean, split, and chunk the data
         make faiss-populate    # Create the Faiss database

## 🔍 Get the Model

### 🧠 Accessing LLaMA 3.2-3B

1.  Create or log in to a [Hugging Face account](https://huggingface.co/login)
2.  Visit the [Llama 3.2-3B-Instruct model page](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)
3.  Accept the [LLAMA 3.2 COMMUNITY LICENSE AGREEMENT](./LLAMA%203.2%20COMMUNITY%20LICENSE%20AGREEMENT)
4.  Log in via CLI:

         make login

5.  (Optional) To enable debug logging, add this to your `.env` file:

         LOG_LEVEL="DEBUG"

6.  Run the application:

         make run

### 🧠 Accessing Mistral Small 3.1-24B

1.  Create or log in to a [Hugging Face account](https://huggingface.co/login)
2.  Visit the [Mistral Small 3.1-24B Instruct model page](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) and accept toshare your contact informations
3.  Create an Inference token [here](https://huggingface.co/settings/tokens/new?tokenType=fineGrained)
4.  Copy the key to the `.env` file:

         INFERENCE_API_KEY="your token"

5.  (Optional) To enable debug logging, add this to your `.env` file:

         LOG_LEVEL="DEBUG"

6.  Run the application:

         make run

## 📁 Project Structure

The project is organized as follows:

        root/
        ├── src/
        │   ├── app/                                # Frontend logic, app design, and integration principles
        │   ├── core/                               # Core backend logic: RAG orchestration and model interaction
        │   ├── faiss/                              # FAISS-based local vector database alternative
        │   ├── pdf_manipulation/                   # Scripts to clean, split, and chunk PDF data
        │   ├── pinecone/                           # Pinecone vector DB configuration and indexing logic
        │   ├── config.py                           # Configuration management (login key, data-folder, ...)
        │   └── main.py                             # Entry point: application bootstrap and launch logic
        │
        ├── .env.example                            # Example environment configuration file
        ├── .gitignore                              # Git configuration to ignore local/dev files
        ├── Griffith College 200 Years.pdf          # Source document used in the RAG pipeline
        ├── LICENSE                                 # Open-source project license
        ├── LLAMA 3.2 COMMUNITY LICENSE AGREEMENT   # Required license agreement for using LLaMA 3.2 models
        ├── Makefile                                # Automation commands for setup, data processing, and deployment
        ├── pyproject.toml                          # Poetry project configuration and dependencies
        ├── README.md                               # Project documentation

Each directory and file is purposefully designed to keep the app modular, easy to maintain, and scalable for LLM-powered applications using Retrieval-Augmented Generation (RAG).

## 🖼️ PyQt Desktop Application

The project includes a desktop graphical interface built with **PyQt5**, designed to make the chatbot feel intuitive and modern — similar to popular AI chat apps.

### 💡 App Features

| Feature                        | Description                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| 🪟 PyQt-based GUI              | Responsive and styled with flexible layouts                                                 |
| 💬 Chat bubble display         | User and assistant messages are rendered in styled speech bubbles with name annotations     |
| ✍️ Typing animation            | Assistant answers are typed out letter by letter to simulate thinking                       |
| 📜 First-launch license screen | Displays the full text of LICENSE and LLaMA agreement before allowing app usage             |
| ⚙ Settings dropdown            | Allows the user to view terms again, or change the active model (local or cloud-based)      |
| 🔐 API key input               | If the cloud model is selected, user is prompted to input and save their Hugging Face token |

The entire interface is modular, clean, and ready for scaling with additional settings, themes, or history persistence.

---

## 📦 Python Dependencies Explained

Here’s a breakdown of every library listed in [`pyproject.toml`](./pyproject.toml) and their purpose in this project:

| Package                   | Purpose                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------- |
| **torch**                 | Used for running LLMs locally via PyTorch-backed models                                       |
| **transformers**          | Hugging Face’s library for model loading, tokenization, generation                            |
| **sentence-transformers** | Provides powerful embeddings for vector indexing (e.g., MiniLM, BGE)                          |
| **tqdm**                  | Adds elegant progress bars during PDF processing and chunking workflows                       |
| **accelerate**            | Speeds up multi-device (CPU/GPU) execution of LLMs and pipelines                              |
| **scikit-learn**          | Required by sentence-transformers and some vector similarity utilities                        |
| **pymupdf**               | Extracts text from PDFs (used instead of `PyPDF2` for better layout and font handling)        |
| **langchain**             | Provides RAG orchestration tools (chains, retrievers, prompt templates, etc.)                 |
| **black**                 | Code formatter to ensure clean, consistent style across scripts                               |
| **vulture**               | Detects unused Python code for cleanup and optimization                                       |
| **python-dotenv**         | Loads secret environment variables from `.env` file (e.g., API keys)                          |
| **pinecone**              | Used for sending chunks to Pinecone’s vector database and retrieving top-K relevant matches   |
| **faiss-cpu**             | Local alternative to Pinecone for vector storage and similarity search (offline mode support) |
| **pyqt5**                 | Core GUI library for the desktop application (chat interface, forms, settings dropdown, etc.) |

---

## 🧠 LLM Control via UI

The desktop app allows the user to choose the model backend from the GUI:

- `"local"` → uses a LLaMA-based model installed locally (no internet required)
- `"api"` → sends the question to Hugging Face's Inference API and returns the generated response

The selected option and API key are stored in a `.model_config` file like this:

```ini
MODEL_TYPE=api
INFERENCE_API_KEY=hf_xxx...
```

This file is automatically created and updated when the user interacts with the model settings menu in the GUI.

## ✅ Summary

| Component             | Description                                                                                                                                                       |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data Tools**        | Shell scripts leveraging `pdfimages` and `pdftotext` to extract images and text, then cleaning, splitting, and chunking PDFs for RAG                              |
| **Vector DBs**        | Pinecone cloud for vector indexing and retrieval, with an optional local FAISS alternative                                                                        |
| **Local Models**      | TinyLlama-1.1B (lightweight, low-resource), LLaMA 3.1-8B and LLaMA 3.2-3B (more powerful, larger context)                                                         |
| **Cloud Models**      | Mistral-Small-3.1-24B-Instruct accessed via Hugging Face Inference API (requires internet connection)                                                             |
| **Licensing**         | Must accept LLAMA 3.1 and 3.2 Community License Agreements before using corresponding models                                                                      |
| **Setup**             | Uses Python 3.13 managed by pyenv, with dependencies handled by Poetry                                                                                            |
| **Automation**        | Makefile targets for preparing data (`make data-transfo`), populating vector DBs (`make pinecone-populate` and `make faiss-populate`), login, and running the app |
| **Project Structure** | Modular organization under `src/` with dedicated folders for app, core logic, vector DB interfaces, PDF processing, and configuration                             |
