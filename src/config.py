import os
from dotenv import load_dotenv
import logging

# Load environment variables from `.env`
load_dotenv()

# === Directories and Files ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.path.join(BASE_DIR, "LOCAL_RAG")

RECORDS_FILE = "data/pinecone_records.json"
INDEX_FILE = os.path.join(INDEX_DIR, "griffith_index.faiss")
ID_MAP_FILE = os.path.join(INDEX_DIR, "id_map.json")
TEXT_STORE_FILE = os.path.join(INDEX_DIR, "text_store.json")

IMAGE_RECORDS_FILE = "data/img_chuncks.json"
IMAGE_INDEX_FILE = os.path.join(INDEX_DIR, "griffith_image_index.faiss")
IMAGE_ID_MAP_FILE = os.path.join(INDEX_DIR, "image_id_map.json")
IMAGE_STORE_FILE = os.path.join(INDEX_DIR, "image_store.json")

# === Embedding Model ===
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# === Logging ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
DEBUG_LOG_FILE = os.path.join(BASE_DIR, "debug.log")

# === Pinecone ===
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "griffith-college")
PINECONE_IMAGE_INDEX_NAME = os.getenv(
    "PINECONE_IMAGE_INDEX_NAME", "griffith-college-images"
)
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "200-history")

# === HuggingFace ===
HF_API_KEY = os.getenv("INFERENCE_API_KEY", "")

# === Models ===
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "meta-llama/Llama-3.2-3B-Instruct")


def setup_logging():
    if LOG_LEVEL == "DEBUG":
        logging.basicConfig(
            filename=DEBUG_LOG_FILE,
            level=logging.DEBUG,
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
