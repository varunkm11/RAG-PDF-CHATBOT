import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("📚 PDF Assistant")

        st.markdown("---")

        uploaded_files = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True
        )

        st.markdown("---")

        st.subheader("💬 Chat")

        st.button("➕ New Chat")

        st.markdown("---")

        st.caption("Powered by Gemini + Qdrant")

        return uploaded_files