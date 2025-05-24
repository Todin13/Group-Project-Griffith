from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Step 1: Load the cleaned text file
print("📄 Loading text file...")
loader = TextLoader("Griffith College 200 Years.txt")
pages = loader.load()

# Step 2: Split text into chunks
print("✂️ Splitting text into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
docs = splitter.split_documents(pages)

# Step 3: Load sentence-transformer embedding model
print("🔗 Embedding chunks...")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 4: Build FAISS vectorstore
print("💾 Building FAISS index...")
vectorstore = FAISS.from_documents(docs, embedding)
vectorstore.save_local("model/griffith_vectorstore")

print("✅ Vectorstore built and saved to model/griffith_vectorstore")
