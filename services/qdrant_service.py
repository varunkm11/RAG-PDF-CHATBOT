from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from services.embeddings import get_embedding_model
from dotenv import load_dotenv
import os

load_dotenv()

COLLECTION_NAME = "pdf_chatbot"


def get_qdrant_vectorstore():
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    embeddings = get_embedding_model()

    vectorstore = Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings
    )

    return vectorstore