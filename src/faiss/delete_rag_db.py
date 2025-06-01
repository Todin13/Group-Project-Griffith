import os
import src.config as config

# Use the path from config
index_file = config.INDEX_FILE

if os.path.exists(index_file):
    os.remove(index_file)
    print(f"🗑️  Deleted FAISS index file: '{index_file}'")
else:
    print(f"❌ File '{index_file}' does not exist.")
