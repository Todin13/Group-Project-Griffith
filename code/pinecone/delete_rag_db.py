from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# List all indexes
indexes = pc.list_indexes()
print(f"Found indexes: {[idx['name'] for idx in indexes]}")

# Delete each index
for idx in indexes:
    index_name = idx["name"]
    print(f"Deleting index: {index_name}")
    pc.delete_index(index_name)

print("✅ All indexes deleted successfully.")
