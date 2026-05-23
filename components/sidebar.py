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

        if st.button("➕ New Chat"):

            st.session_state.messages = []

            st.session_state.pdf_processed = False

            st.rerun()

        st.markdown("---")

        st.caption("Powered by Gemini + Qdrant")

        return uploaded_files