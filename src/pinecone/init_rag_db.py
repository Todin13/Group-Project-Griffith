import json
import time
from pinecone import Pinecone

# Import configurations
import src.config as config

# Initialize Pinecone client
pc = Pinecone(api_key=config.PINECONE_API_KEY)

# === TEXT INDEX === #
# Check if text index exists
if not pc.has_index(config.PINECONE_INDEX_NAME):
    pc.create_index_for_model(
        name=config.PINECONE_INDEX_NAME,
        cloud="aws",
        region="us-east-1",
        embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}},
    )
    print(f"✅ Created text index '{config.PINECONE_INDEX_NAME}'")
else:
    print(f"ℹ️ Text index '{config.PINECONE_INDEX_NAME}' exists")

# Load text records
with open(config.RECORDS_FILE, "r", encoding="utf-8") as f:
    text_records = json.load(f)
print(f"📚 Loaded {len(text_records)} text records")

# Target the text index
text_index = pc.Index(config.PINECONE_INDEX_NAME)

# Prepare and upsert text records
def prepare_text_records(records):
    return [
        {
            "_id": r["_id"],
            "chunk_text": r.get("chunk_text", ""),
            "category": r.get("category", ""),
        }
        for r in records
    ]

def batch_iterable(iterable, batch_size=96):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]

for batch in batch_iterable(prepare_text_records(text_records)):
    text_index.upsert_records(config.PINECONE_NAMESPACE, batch)

print(f"✅ Upserted {len(text_records)} text records")

# === IMAGE INDEX === #
if not pc.has_index(config.PINECONE_IMAGE_INDEX_NAME):
    pc.create_index_for_model(
        name=config.PINECONE_IMAGE_INDEX_NAME,
        cloud="aws",
        region="us-east-1",
        embed={"model": "llama-text-embed-v2", "field_map": {"text": "description"}},
    )
    print(f"✅ Created image index '{config.PINECONE_IMAGE_INDEX_NAME}'")
else:
    print(f"ℹ️ Image index '{config.PINECONE_IMAGE_INDEX_NAME}' exists")

# Load image records
with open(config.IMAGE_RECORDS_FILE, "r", encoding="utf-8") as f:
    image_records = json.load(f)
print(f"🖼️ Loaded {len(image_records)} image records")

# Target the image index
image_index = pc.Index(config.PINECONE_IMAGE_INDEX_NAME)

# Prepare and upsert image records
def prepare_image_records(records):
    return [
        {
            "_id": r["id"],
            "description": r.get("description", "")
        }
        for r in records
    ]

for batch in batch_iterable(prepare_image_records(image_records)):
    image_index.upsert_records(config.PINECONE_NAMESPACE, batch)

print(f"✅ Upserted {len(image_records)} image records")

# Wait before checking stats
time.sleep(15)

# Show stats for both indexes
print("\n📊 Text Index Stats:")
print(text_index.describe_index_stats())

print("\n🖼️ Image Index Stats:")
print(image_index.describe_index_stats())
