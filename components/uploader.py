import streamlit as st
import tempfile
import os

from langchain.schema import Document

from services.pdf_loader import load_pdf_text
from services.text_splitter import split_text
from services.qdrant_service import get_qdrant_vectorstore


MAX_FILE_SIZE = 5 * 1024 * 1024

BATCH_SIZE = 20


def process_uploaded_pdfs(uploaded_files):

    if not uploaded_files:

        return 0, 0

    all_chunks = []

    for uploaded_file in uploaded_files:

        if uploaded_file.size > MAX_FILE_SIZE:

            st.error(
                f"{uploaded_file.name} is too large. Upload files under 5MB."
            )

            st.stop()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(uploaded_file.read())

            pdf_path = tmp_file.name

        text = load_pdf_text(pdf_path)

        chunks = split_text(text)

        all_chunks.extend(chunks)

        os.remove(pdf_path)

    docs = [Document(page_content=chunk) for chunk in all_chunks]

    vectorstore = get_qdrant_vectorstore()

    progress_bar = st.progress(0)

    total_batches = len(docs) // BATCH_SIZE + 1

    for i in range(0, len(docs), BATCH_SIZE):

        batch = docs[i:i+BATCH_SIZE]

        vectorstore.add_documents(batch)

        progress = min((i // BATCH_SIZE + 1) / total_batches, 1.0)

        progress_bar.progress(progress)

    st.success("PDFs indexed successfully!")

    return len(uploaded_files), len(all_chunks)