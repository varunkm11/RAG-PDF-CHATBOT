import os
import streamlit as st
import tempfile
from services.pdf_loader import load_pdf_text
from services.text_splitter import split_text
from services.embeddings import get_embedding_model
from services.qdrant_service import get_qdrant_vectorstore
from services.rag_pipeline import get_qa_chain
from langchain.schema import Document

# Page Configuration
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files_names" not in st.session_state:
    st.session_state.uploaded_files_names = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Sidebar
with st.sidebar:
    st.markdown("### 📄 Document Manager")
    
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader"
    )
    
    if uploaded_files:
        with st.spinner("📥 Processing PDFs..."):
            all_chunks = []
            
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    pdf_path = tmp_file.name
                
                text = load_pdf_text(pdf_path)
                chunks = split_text(text)
                all_chunks.extend(chunks)
                
                st.session_state.uploaded_files_names.append(uploaded_file.name)
            
            docs = [Document(page_content=chunk) for chunk in all_chunks]
            vectorstore = get_qdrant_vectorstore()
            vectorstore.add_documents(docs)
            st.session_state.vectorstore = vectorstore
            
            st.success("✅ PDFs indexed successfully!")
    
    # Display uploaded files
    if st.session_state.uploaded_files_names:
        st.markdown("#### 📚 Indexed Documents:")
        for i, file_name in enumerate(st.session_state.uploaded_files_names, 1):
            st.markdown(f"<div class='file-badge'>📖 {file_name}</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Suggested Questions
    st.markdown("### 💡 Suggested Questions")
    suggested = [
        "What is the main topic?",
        "Summarize the key points",
        "What are the conclusions?",
        "Explain the methodology",
        "Who are the authors?"
    ]
    
    if st.session_state.uploaded_files_names:
        for q in suggested:
            if st.button(q, key=q, use_container_width=True):
                st.session_state.suggested_question = q
    
    st.divider()
    
    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.uploaded_files_names = []
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    st.markdown("### 📊 Statistics")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Documents", len(st.session_state.uploaded_files_names))

# Main Content
col_main = st.columns([1])

with col_main[0]:
    # Header
    st.markdown("""
    <div class='header-container'>
        <h1>🤖 Gemini RAG PDF Chatbot</h1>
        <p>Ask unlimited questions about your PDFs with AI-powered answers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat Container
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Display chat messages
    if st.session_state.messages:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    else:
        st.info("👋 Upload PDFs and start asking questions!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat Input
    st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
    
    # Check if there's a suggested question
    default_input = ""
    if "suggested_question" in st.session_state:
        default_input = st.session_state.suggested_question
        del st.session_state.suggested_question
    
    question = st.chat_input(
        "Ask your PDF anything...",
        key="chat_input"
    )
    
    if question and st.session_state.uploaded_files_names:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    qa_chain = get_qa_chain()
                    result = qa_chain(question)
                    answer = result["result"]
                    st.markdown(answer)
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    elif question and not st.session_state.uploaded_files_names:
        st.warning("⚠️ Please upload a PDF first!")
    
    st.markdown("</div>", unsafe_allow_html=True)