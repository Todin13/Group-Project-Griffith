import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Input/output files
RECORDS_FILE = "pinecone_records.json"
INDEX_DIR = "LOCAL_RAG"
os.makedirs(INDEX_DIR, exist_ok=True)

INDEX_FILE = os.path.join(INDEX_DIR, "griffith_index.faiss")
ID_MAP_FILE = os.path.join(INDEX_DIR, "id_map.json")          # FAISS int ID → original string _id
TEXT_STORE_FILE = os.path.join(INDEX_DIR, "text_store.json")  # FAISS int ID → chunk_text & metadata

# Load records from JSON
with open(RECORDS_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"✅ Loaded {len(records)} records from '{RECORDS_FILE}'")

# Initialize embedding model
print("🔄 Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Extract data from records
texts = [record["chunk_text"] for record in records]
original_ids = [record["_id"] for record in records]

# Save FAISS int ID → original string _id
id_map = {i: original_ids[i] for i in range(len(original_ids))}
with open(ID_MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(id_map, f, indent=2)
print(f"🧭 Saved ID mapping to '{ID_MAP_FILE}'")

# Save FAISS int ID → full record metadata (e.g., chunk_text, category)
text_store = {
    str(i): {
        "_id": original_ids[i],
        "chunk_text": texts[i],
        "category": records[i].get("category", "")
    }
    for i in range(len(original_ids))
}
with open(TEXT_STORE_FILE, "w", encoding="utf-8") as f:
    json.dump(text_store, f, indent=2)
print(f"📚 Saved text store to '{TEXT_STORE_FILE}'")

# Generate embeddings
print("🧠 Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add vectors to FAISS index
print("📦 Adding vectors to FAISS index...")
index.add(embeddings)

print(f"✅ FAISS index populated with {index.ntotal} vectors.")

# Save index to disk
faiss.write_index(index, INDEX_FILE)
print(f"💾 FAISS index saved to '{INDEX_FILE}'")
