# README.md

````md
# 🤖 Gemini RAG PDF Chatbot

An AI-powered RAG (Retrieval-Augmented Generation) PDF chatbot built using Gemini, Qdrant, Streamlit, and LangChain.

Users can upload PDFs and ask questions about their documents using natural language.

---

# 🚀 Features

- 📄 Upload multiple PDFs
- 🤖 AI-powered question answering
- 🔍 Semantic search using vector embeddings
- 🧠 Gemini 2.5 Flash integration
- 🗂️ Qdrant vector database
- ⚡ Fast retrieval pipeline
- 🌙 Modern Streamlit UI
- 📚 Multi-document support
- ☁️ Deployment-ready architecture

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend |
| Streamlit | Frontend |
| Gemini API | LLM Responses |
| HuggingFace Embeddings | Vector Embeddings |
| Qdrant | Vector Database |
| LangChain | RAG Pipeline |
| PyMuPDF | PDF Processing |

---

# 🧠 Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embeddings Generation
    ↓
Qdrant Vector Storage
    ↓
Similarity Search
    ↓
Gemini Response Generation
    ↓
Final Answer
````

---

# 📂 Project Structure

```text
rag-pdf-chatbot/
│
├── app.py
├── requirements.txt
├── .env
├── README.md
│
├── services/
│   ├── pdf_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── qdrant_service.py
│   ├── rag_pipeline.py
│   └── gemini_chat.py
│
├── uploads/
├── assets/
└── .gitignore
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
cd rag-pdf-chatbot
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=your_google_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

---

# ▶️ Run The Application

```bash
streamlit run app.py
```

---

# 🌐 Qdrant Setup

Create a collection in Qdrant Cloud with:

| Setting         | Value       |
| --------------- | ----------- |
| Collection Name | pdf_chatbot |
| Dimension       | 384         |
| Distance Metric | Cosine      |

---

# 🤖 Embedding Model

Using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

---

# 🧠 LLM Model

Using:

```text
gemini-2.5-flash
```

---

# 📦 Requirements

```txt
streamlit==1.37.1
langchain==0.2.16
langchain-community==0.2.16
langchain-core==0.2.38
langchain-google-genai==1.0.8
langchain-text-splitters==0.2.4
qdrant-client==1.10.1
python-dotenv
PyMuPDF
pypdf
sentence-transformers
fastapi
uvicorn
inngest
```

---

# 💡 Future Improvements

* Chat history
* Streaming responses
* Authentication
* OCR support
* Multi-user workspace
* Voice assistant
* Citations with page numbers
* Docker deployment
* Hybrid search

---

# 📸 Screenshots

Add screenshots here after completing UI.

---

# 🚀 Deployment

Recommended deployment stack:

| Service         | Platform     |
| --------------- | ------------ |
| Frontend        | Streamlit    |
| Hosting         | Render       |
| Vector Database | Qdrant Cloud |
| Source Code     | GitHub       |

---

# 🎯 Real-World Applications

* AI study assistant
* Research paper chatbot
* Internal company knowledge assistant
* Resume analyzer
* Legal document assistant
* Medical document search

---

# 👨‍💻 Author

Varun

---

# ⭐ If You Like This Project

Give this repository a star ⭐

````

---

# .gitignore

```gitignore
# Virtual Environment
.venv/
venv/

# Python Cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Environment Variables
.env

# Streamlit
.streamlit/

# IDE Files
.idea/
.vscode/

# Uploaded Files
uploads/

# Logs
*.log

# OS Files
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Build Files
build/
dist/

# Temporary Files
*.tmp
*.temp
````

---

# Commands For GitHub Push

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Initial commit"
```

```bash
git branch -M main
```

```bash
git remote add origin YOUR_REPOSITORY_URL
```

```bash
git push -u origin main
```
