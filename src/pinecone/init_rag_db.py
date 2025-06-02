import json
import time
from pinecone import Pinecone

# Import configurations
import src.config as config

# Initialize Pinecone client
pc = Pinecone(api_key=config.PINECONE_API_KEY)

# Check if index exists, create it with embedded model if not
if not pc.has_index(config.PINECONE_INDEX_NAME):
    pc.create_index_for_model(
        name=config.PINECONE_INDEX_NAME,
        cloud="aws",
        region="us-east-1",
        embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}},
    )
    print(f"Created index '{config.PINECONE_INDEX_NAME}' with embedded model")
else:
    print(f"Index '{config.PINECONE_INDEX_NAME}' exists")

# Load your JSON records
with open(config.RECORDS_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Loaded {len(records)} records from JSON")

# Target the index
dense_index = pc.Index(config.PINECONE_INDEX_NAME)

# Prepare records for upsert
upsert_records = []
for record in records:
    upsert_records.append(
        {
            "_id": record["_id"],
            "chunk_text": record.get("chunk_text", ""),
            "category": record.get("category", ""),
        }
    )


def batch_iterable(iterable, batch_size=96):
    """Yield successive batch_size-sized chunks from iterable."""
    for i in range(0, len(iterable), batch_size):
        yield iterable[i : i + batch_size]


# Upsert in batches
for batch in batch_iterable(upsert_records, batch_size=96):
    dense_index.upsert_records(config.PINECONE_NAMESPACE, batch)

print(f"Upserted {len(upsert_records)} records to index '{config.PINECONE_INDEX_NAME}'")

# Wait before checking index stats
time.sleep(10)

# View stats
stats = dense_index.describe_index_stats()
print(stats)
