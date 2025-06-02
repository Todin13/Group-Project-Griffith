from pinecone import Pinecone
import src.config as config

# Initialize Pinecone client using API key from config
pc = Pinecone(api_key=config.PINECONE_API_KEY)

# List all indexes
indexes = pc.list_indexes()
print(f"Found indexes: {[idx['name'] for idx in indexes]}")

# Delete each index
for idx in indexes:
    index_name = idx["name"]
    print(f"Deleting index: {index_name}")
    pc.delete_index(index_name)

print("✅ All indexes deleted successfully.")
