# 📄 RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with Flask. Upload any PDF and ask questions about it using Google Gemini AI and Qdrant vector database.

---

## ✨ Features

- 📁 Upload PDF documents and chat with their contents
- 🌙 Dark / Light mode toggle
- 📌 Collapsible sidebar panel
- 🗑️ Clear chat history and uploaded PDF list
- ❌ Remove individual PDFs from the session
- ☁️ One-click deploy to Render

---

## 🛠️ Tech Stack

- **Backend** — Python 3.12, Flask, Gunicorn
- **LLM** — Google Gemini 2.0 Flash
- **Embeddings** — Google Gemini Embedding 001
- **Vector Store** — Qdrant Cloud
- **PDF Parsing** — PyMuPDF
- **Deployment** — Render

---

## 📁 Project Structure

```
rag-pdf-chatbot/
│
├── app.py                  # Flask routes
├── rag_engine.py           # RAG logic — embed, store, retrieve, generate
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── .env                    # Local secrets (never commit this)
├── .gitignore
│
├── templates/
│   └── index.html          # Frontend UI
│
└── static/
    └── style.css           # Styles with dark / light theme
```

---

## ⚙️ Local Setup

**1. Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/rag-pdf-chatbot.git
cd rag-pdf-chatbot
```

**2. Create a virtual environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Create your `.env` file**

Create a file named `.env` in the project root and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=https://your-cluster-url.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
COLLECTION_NAME=pdf_rag_collection
```

**5. Run the app**

```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 🔑 Getting API Keys

**Gemini API Key**

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** → **Create API Key**
3. Copy the key into your `.env`

**Qdrant Cloud**

1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Sign up and click **Create Cluster** (free tier available)
3. Copy the **Cluster URL** and generate an **API Key**
4. Paste both into your `.env`

---

## 🚀 Deploy to Render

**1. Push your code to GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rag-pdf-chatbot.git
git push -u origin main
```

**2. Create a Web Service on Render**

1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub repository
3. Render will auto-detect `render.yaml`
4. Go to the **Environment** tab and add these variables:

| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | your Gemini API key |
| `QDRANT_URL` | your Qdrant cluster URL |
| `QDRANT_API_KEY` | your Qdrant API key |
| `COLLECTION_NAME` | `pdf_rag_collection` |

5. Click **Deploy** and wait 2–3 minutes

Your live URL will look like:

```
https://rag-pdf-chatbot.onrender.com
```

---

## 💡 How It Works

**Ingestion Pipeline**

```
PDF Upload → Extract Text → Split into Chunks → Embed with Gemini → Store in Qdrant
```

**Query Pipeline**

```
User Question → Embed with Gemini → Search Qdrant → Top 5 Chunks → Gemini LLM → Answer
```

---

## ⚠️ Known Limitations

| Problem | Solution |
|---------|----------|
| Scanned / image-based PDFs not supported | PDF must contain selectable text |
| Gemini free tier quota error (429) | Wait 24 hours or create a new API key |
| Render free tier cold start (~30s delay) | Upgrade to a paid Render plan |
| Chat history is session-only | Refreshing the page resets the chat |

---

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ |
| `QDRANT_URL` | Qdrant Cloud cluster URL | ✅ |
| `QDRANT_API_KEY` | Qdrant Cloud API key | ✅ |
| `COLLECTION_NAME` | Name of the Qdrant collection | ✅ |

---

## 👤 Author

**Varun Kumar Singh**
GitHub: [varunkm11](https://github.com/varunkm11)

---

## 📄 License

MIT License — free to use and modify.
