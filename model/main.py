from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import os

# Step 1: Load the document
pdf_path = "Griffith College 200 Years.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# Step 2: Chunk the document
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
docs = splitter.split_documents(pages)

# Step 3: Embed the chunks
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
if not os.path.exists("griffith_vectorstore/index.faiss"):
    print("Creating FAISS index...")
    vectorstore = FAISS.from_documents(docs, embedding)
    vectorstore.save_local("griffith_vectorstore")
else:
    print("Loading existing FAISS index...")
    vectorstore = FAISS.load_local("griffith_vectorstore", embedding)

# Step 4: Setup TinyLLaMA via Ollama
llm = Ollama(model="tinyllama")  # Make sure `ollama run tinyllama` is running

# Step 5: Setup RAG chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Step 6: Run the QA loop
print("📘 Griffith College History - Q&A Ready")
while True:
    query = input("\nAsk a question (or type 'exit'): ")
    if query.lower() in ["exit", "quit"]:
        break

    result = qa_chain(query)
    print("\nAnswer:\n", result["result"])

    print("\nSources:")
    for doc in result["source_documents"]:
        print("  -", doc.metadata.get("source", "PDF"))
