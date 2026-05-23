import streamlit as st


def render_metrics(doc_count, chunk_count):

    col1, col2, col3 = st.columns(3)

    col1.metric("📄 Documents", doc_count)

    col2.metric("🧩 Chunks", chunk_count)

    col3.metric("🤖 Model", "Gemini")