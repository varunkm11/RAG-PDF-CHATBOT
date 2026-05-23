import streamlit as st
import tempfile
import os

from langchain.schema import Document

from services.pdf_loader import load_pdf_text
from services.text_splitter import split_text
from services.qdrant_service import get_qdrant_vectorstore


def process_uploaded_pdfs(uploaded_files):

    if not uploaded_files:

        return 0, 0

    all_chunks = []

    for uploaded_file in uploaded_files:

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

    with st.spinner("Indexing PDFs..."):

        vectorstore.add_documents(docs)

    st.success("PDFs indexed successfully!")

    return len(uploaded_files), len(all_chunks)