import os

# Path to the FAISS index file
INDEX_FILE = "LOCAL_RAG/griffith_index.faiss"

if os.path.exists(INDEX_FILE):
    os.remove(INDEX_FILE)
    print(f"🗑️  Deleted FAISS index file: '{INDEX_FILE}'")
else:
    print(f"❌ File '{INDEX_FILE}' does not exist.")
