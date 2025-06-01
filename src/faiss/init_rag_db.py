import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import src.config as config

# Ensure index directory exists
os.makedirs(config.INDEX_DIR, exist_ok=True)

# Load records
with open(config.RECORDS_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"✅ Loaded {len(records)} records from '{config.RECORDS_FILE}'")

# Initialize embedding model
print("🔄 Loading embedding model...")
model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)

# Extract data
texts = [record["chunk_text"] for record in records]
original_ids = [record["_id"] for record in records]

# Save FAISS int ID → original string _id
id_map = {i: original_ids[i] for i in range(len(original_ids))}
with open(config.ID_MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(id_map, f, indent=2)
print(f"🧭 Saved ID mapping to '{config.ID_MAP_FILE}'")

# Save FAISS int ID → full metadata
text_store = {
    str(i): {
        "_id": original_ids[i],
        "chunk_text": texts[i],
        "category": records[i].get("category", "")
    }
    for i in range(len(original_ids))
}
with open(config.TEXT_STORE_FILE, "w", encoding="utf-8") as f:
    json.dump(text_store, f, indent=2)
print(f"📚 Saved text store to '{config.TEXT_STORE_FILE}'")

# Generate embeddings
print("🧠 Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add vectors to index
print("📦 Adding vectors to FAISS index...")
index.add(embeddings)
print(f"✅ FAISS index populated with {index.ntotal} vectors.")

# Save FAISS index
faiss.write_index(index, config.INDEX_FILE)
print(f"💾 FAISS index saved to '{config.INDEX_FILE}'")
