from langchain.chains import RetrievalQA
from services.gemini_chat import get_chat_model


def get_qa_chain(retriever):

    llm = get_chat_model()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    return qa_chain