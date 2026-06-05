import os
import tempfile
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from rag_engine import ingest_pdf, generate_answer, ensure_collection

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB limit


# ── Routes ─────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    """Receive a PDF, ingest it into Qdrant."""
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "error": "Only PDF files are supported."}), 400

    # Save to a temp file and ingest
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = ingest_pdf(tmp_path, file.filename)
    finally:
        os.unlink(tmp_path)  # always clean up temp file

    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@app.route("/chat", methods=["POST"])
def chat():
    """Receive a question, return an answer from the RAG pipeline."""
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"success": False, "error": "Missing 'question' field."}), 400

    question = data["question"].strip()

    if not question:
        return jsonify({"success": False, "error": "Question cannot be empty."}), 400

    try:
        answer = generate_answer(question)
        return jsonify({"success": True, "answer": answer}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/debug")
def debug():
    return jsonify({
        "gemini_key": bool(os.getenv("GEMINI_API_KEY")),
        "qdrant_url": os.getenv("QDRANT_URL", "MISSING"),
        "qdrant_key": bool(os.getenv("QDRANT_API_KEY")),
        "rag_ready": RAG_READY,
        "rag_error": RAG_ERROR if not RAG_READY else "none"
    })

# ── Entry point ────────────────────────────────────────────────

if __name__ == "__main__":
    ensure_collection()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)