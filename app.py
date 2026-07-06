import os
import tempfile
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

# ── Debug: confirm env vars loaded ────────────────────────────
print("=" * 50)
print("GEMINI KEY:", "OK" if os.getenv("GEMINI_API_KEY") else "MISSING")
print("QDRANT URL:", os.getenv("QDRANT_URL") or "MISSING")
print("QDRANT KEY:", "OK" if os.getenv("QDRANT_API_KEY") else "MISSING")
print("=" * 50)

# ── Import RAG engine safely ───────────────────────────────────
try:
    from rag_engine import ingest_pdf, generate_answer, ensure_collection
    RAG_READY = True
    RAG_ERROR = "none"
    print("[OK] rag_engine imported successfully")
except Exception as e:
    RAG_READY = False
    RAG_ERROR = str(e)
    print(f"[ERROR] Failed to import rag_engine: {e}")


# ── Routes ─────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/debug")
def debug():
    return jsonify({
        "gemini_key": bool(os.getenv("GEMINI_API_KEY")),
        "qdrant_url": os.getenv("QDRANT_URL", "MISSING"),
        "qdrant_key": bool(os.getenv("QDRANT_API_KEY")),
        "rag_ready": RAG_READY,
        "rag_error": RAG_ERROR
    })


@app.route("/upload", methods=["POST"])
def upload_pdf():
    if not RAG_READY:
        return jsonify({"success": False, "error": f"RAG engine failed to load: {RAG_ERROR}"}), 500

    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file in request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "error": "Only PDF files are supported."}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = ingest_pdf(tmp_path, file.filename)
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.route("/chat", methods=["POST"])
def chat():
    if not RAG_READY:
        return jsonify({"success": False, "error": f"RAG engine failed to load: {RAG_ERROR}"}), 500

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
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "rag_ready": RAG_READY}), 200


if __name__ == "__main__":
    if RAG_READY:
        ensure_collection()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)