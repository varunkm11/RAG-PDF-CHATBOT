import streamlit as st

from services.qdrant_service import get_qdrant_vectorstore
from services.rag_pipeline import get_qa_chain

from services.chat_memory import (
    initialize_chat,
    add_user_message,
    add_ai_message,
    display_chat_history
)

from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.uploader import process_uploaded_pdfs


st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# Session state
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

initialize_chat()

# Header
st.markdown("""
# 🤖 AI PDF Assistant

Chat with your PDFs using Gemini AI + Qdrant + RAG
""")

# Sidebar
uploaded_files = render_sidebar()

# Display chat history
display_chat_history()

# Process PDFs only ONCE
if uploaded_files and not st.session_state.pdf_processed:

    doc_count, chunk_count = process_uploaded_pdfs(
        uploaded_files
    )

    st.session_state.pdf_processed = True

    render_metrics(
        doc_count=doc_count,
        chunk_count=chunk_count
    )

# Chat Input
question = st.chat_input(
    "Ask something about your PDFs..."
)

if question:

    add_user_message(question)

    with st.chat_message("user"):

        st.markdown(question)

    vectorstore = get_qdrant_vectorstore()

    retriever = vectorstore.as_retriever()

    qa_chain = get_qa_chain(retriever)

    with st.spinner("Thinking..."):

        result = qa_chain.invoke(
            {
                "query": question
            }
        )

    answer = result["result"]

    add_ai_message(answer)

    with st.chat_message("assistant"):

        st.markdown(answer)