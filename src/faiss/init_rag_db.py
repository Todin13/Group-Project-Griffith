import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import src.config as config

# Ensure index directory exists
os.makedirs(config.INDEX_DIR, exist_ok=True)

# Load records (text)
with open(config.RECORDS_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"✅ Loaded {len(records)} records from '{config.RECORDS_FILE}'")

# Load image metadata
with open(config.IMAGE_RECORDS_FILE, "r", encoding="utf-8") as f:
    image_records = json.load(f)

print(f"🖼️ Loaded {len(image_records)} image records from '{config.IMAGE_RECORDS_FILE}'")

# Initialize embedding model
print("🔄 Loading embedding model...")
model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)

### TEXT INDEX ###
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
        "category": records[i].get("category", ""),
    }
    for i in range(len(original_ids))
}
with open(config.TEXT_STORE_FILE, "w", encoding="utf-8") as f:
    json.dump(text_store, f, indent=2)
print(f"📚 Saved text store to '{config.TEXT_STORE_FILE}'")

# Generate embeddings
print("🧠 Generating embeddings for text records...")
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Build and save FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print(f"✅ FAISS text index populated with {index.ntotal} vectors.")
faiss.write_index(index, config.INDEX_FILE)
print(f"💾 FAISS text index saved to '{config.INDEX_FILE}'")

### IMAGE INDEX ###
image_texts = [record["description"] for record in image_records]
image_ids = [record["id"] for record in image_records]

# Save FAISS int ID → original image ID
image_id_map = {i: image_ids[i] for i in range(len(image_ids))}
with open(config.IMAGE_ID_MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(image_id_map, f, indent=2)
print(f"🧭 Saved image ID mapping to '{config.IMAGE_ID_MAP_FILE}'")

# Save image metadata
image_store = {
    str(i): {
        "id": image_ids[i],
        "description": image_texts[i]
    }
    for i in range(len(image_ids))
}
with open(config.IMAGE_STORE_FILE, "w", encoding="utf-8") as f:
    json.dump(image_store, f, indent=2)
print(f"🖼️ Saved image store to '{config.IMAGE_STORE_FILE}'")

# Generate image embeddings
print("🧠 Generating embeddings for image records...")
image_embeddings = model.encode(image_texts, show_progress_bar=True)
image_embeddings = np.array(image_embeddings).astype("float32")

# Build and save image FAISS index
image_index = faiss.IndexFlatL2(image_embeddings.shape[1])
image_index.add(image_embeddings)
print(f"✅ FAISS image index populated with {image_index.ntotal} vectors.")
faiss.write_index(image_index, config.IMAGE_INDEX_FILE)
print(f"💾 FAISS image index saved to '{config.IMAGE_INDEX_FILE}'")
