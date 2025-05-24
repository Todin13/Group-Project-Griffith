import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp

# Setup LLM
llm = LlamaCpp(
    model_path="model/tinyllama.gguf",
    temperature=0.7,
    max_tokens=512,
    top_p=1,
    n_ctx=1024,
    n_batch=16,
    verbose=False
)

# Load FAISS index
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("model/griffith_vectorstore", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# RAG chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# UI
st.title("📘 Griffith College History – Q&A")
st.write("Ask a question based on the 200 years of campus history.")

query = st.text_input("🔍 Your question")
if query:
    with st.spinner("Generating answer..."):
        result = qa_chain.run(query)
    st.success("✅ Done!")
    st.markdown("### 🧠 Answer")
    st.write(result)
