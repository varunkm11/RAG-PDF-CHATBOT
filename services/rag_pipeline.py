from langchain.chains import RetrievalQA
from services.qdrant_service import get_qdrant_vectorstore
from services.gemini_chat import get_chat_model


def get_qa_chain():
    vectorstore = get_qdrant_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    llm = get_chat_model()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain