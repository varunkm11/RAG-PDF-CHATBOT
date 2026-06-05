import os
import fitz  # PyMuPDF
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, Filter,
    FieldCondition, MatchValue
)
from dotenv import load_dotenv
import uuid
import re

load_dotenv()

# ── Configuration ──────────────────────────────────────────────
GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY")
QDRANT_URL       = os.getenv("QDRANT_URL")
QDRANT_API_KEY   = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME  = os.getenv("COLLECTION_NAME", "pdf_rag_collection")
EMBEDDING_MODEL  = "models/gemini-embedding-001"  # 768-dim, free tier
CHAT_MODEL       = "gemini-2.5-flash"
CHUNK_SIZE       = 500    # characters per chunk
CHUNK_OVERLAP    = 50     # overlap between chunks
TOP_K            = 5      # number of chunks to retrieve

# ── Initialize clients ─────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


def ensure_collection():
    existing = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in existing:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )
        print(f"[RAG] Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"[RAG] Collection '{COLLECTION_NAME}' already exists.")


# ── Text helpers ───────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text


def clean_text(text: str) -> str:
    """Basic text cleaning."""
    text = re.sub(r'\s+', ' ', text)   # collapse whitespace
    text = text.strip()
    return text


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    text = clean_text(text)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap  # move back by overlap for continuity
    return chunks


# ── Embedding ──────────────────────────────────────────────────

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Get embeddings for a list of texts from Gemini."""
    embeddings = []
    for text in texts:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
        )
        embeddings.append(result["embedding"])
    return embeddings


def embed_query(query: str) -> list[float]:
    """Get embedding for a single query string."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=query,
    )
    return result["embedding"]


# ── Ingestion ──────────────────────────────────────────────────

def ingest_pdf(pdf_path: str, filename: str) -> dict:
    """
    Full ingestion pipeline:
      1. Extract text from PDF
      2. Chunk it
      3. Embed chunks
      4. Store in Qdrant
    Returns a summary dict.
    """
    ensure_collection()

    print(f"[RAG] Extracting text from: {filename}")
    raw_text = extract_text_from_pdf(pdf_path)

    if not raw_text.strip():
        return {"success": False, "error": "No text found in PDF. It may be a scanned image."}

    print(f"[RAG] Chunking text ({len(raw_text)} chars)...")
    chunks = chunk_text(raw_text)
    print(f"[RAG] Created {len(chunks)} chunks.")

    print("[RAG] Embedding chunks (this may take a moment)...")
    vectors = embed_texts(chunks)

    print("[RAG] Uploading to Qdrant...")
    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk,
                "filename": filename,
                "chunk_index": i,
            }
        ))

    # Upload in batches of 100
    batch_size = 100
    for i in range(0, len(points), batch_size):
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points[i:i + batch_size],
        )

    print(f"[RAG] Ingestion complete: {len(chunks)} chunks stored.")
    return {
        "success": True,
        "filename": filename,
        "chunks": len(chunks),
        "characters": len(raw_text),
    }


# ── Retrieval ──────────────────────────────────────────────────

def retrieve_chunks(query: str, top_k: int = TOP_K) -> list[str]:
    """Search Qdrant for the most relevant chunks."""
    query_vector = embed_query(query)

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )

    chunks = [hit.payload["text"] for hit in results]
    return chunks


# ── Generation ─────────────────────────────────────────────────

def build_prompt(query: str, context_chunks: list[str]) -> str:
    """Build the RAG prompt from retrieved chunks."""
    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""You are a helpful assistant that answers questions based on the provided document context.
Use ONLY the context below to answer. If the answer is not in the context, say "I couldn't find that in the uploaded document."
Be concise and accurate.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
    return prompt


def generate_answer(query: str) -> str:
    """Full RAG query pipeline: retrieve + generate."""
    # Retrieve relevant chunks
    chunks = retrieve_chunks(query)

    if not chunks:
        return "No documents have been uploaded yet. Please upload a PDF first."

    # Build prompt and call Gemini
    prompt = build_prompt(query, chunks)
    model = genai.GenerativeModel(CHAT_MODEL)
    response = model.generate_content(prompt)

    return response.text