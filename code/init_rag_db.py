import json
from dotenv import load_dotenv
import os
from pinecone import Pinecone

# Load variables from .env file
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

INDEX_NAME = "griffith-college-chunks"

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists, create it with embedded model if not
if not pc.has_index(INDEX_NAME):
    pc.create_index_for_model(
        name=INDEX_NAME,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "llama-text-embed-v2",
            "field_map": {"text": "chunk_text"}
        }
    )
    print(f"Created index '{INDEX_NAME}' with embedded model")
else:
    print(f"Index '{INDEX_NAME}' exists")

# Load your JSON records
with open("pinecone_records.json", "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Loaded {len(records)} records from JSON")

# Target the index
dense_index = pc.Index(INDEX_NAME)

# Prepare records for upsert in the correct format (id, metadata, no vector values needed)
upsert_records = []
for record in records:
    upsert_records.append({
    "_id": record["_id"],
    "chunk_text": record.get("chunk_text", ""),
    "category": record.get("category", ""),
    })

def batch_iterable(iterable, batch_size=96):
    """Yield successive batch_size-sized chunks from iterable."""
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]

# Upsert in batches of 96 or less
for batch in batch_iterable(upsert_records, batch_size=96):
    dense_index.upsert_records("200-history", batch)

print(f"Upserted {len(upsert_records)} records to index '{INDEX_NAME}'")

# Wait for the upserted vectors to be indexed
import time
time.sleep(10)

# View stats for the index
stats = dense_index.describe_index_stats()
print(stats)
