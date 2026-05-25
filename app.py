import os
import streamlit as st
import tempfile
from services.pdf_loader import load_pdf_text
from services.text_splitter import split_text
from services.embeddings import get_embedding_model
from services.qdrant_service import get_qdrant_vectorstore
from services.rag_pipeline import get_qa_chain
from langchain.schema import Document
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🤖 Gemini RAG PDF Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Processing PDFs..."):

        all_chunks = []

        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name

            text = load_pdf_text(pdf_path)
            chunks = split_text(text)
            all_chunks.extend(chunks)

        docs = [Document(page_content=chunk) for chunk in all_chunks]

        vectorstore = get_qdrant_vectorstore()

        vectorstore.add_documents(docs)

        st.success("PDFs indexed successfully!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask your PDF anything...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            qa_chain = get_qa_chain()

            result = qa_chain(question)

            answer = result["result"]

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
            })