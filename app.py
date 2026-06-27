# app.py - Main Flask Application
# This is the entry point of our AI Document Analyzer project

from flask import Flask, request, jsonify, render_template, session
import os
from rag import RAGSystem
from utils import extract_text_from_pdf, split_into_chunks

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "student_project_secret_key"  # Needed for session

# Create upload folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global RAG system instance (stores our document data in memory)
rag_system = RAGSystem()


# ─────────────────────────────────────────────
# ROUTE 1: Home page
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────────
# ROUTE 2: Upload and process PDF
# ─────────────────────────────────────────────
@app.route("/upload", methods=["POST"])
def upload_pdf():
    # Check if a file was actually sent
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # Save the uploaded PDF to disk
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Step 1: Extract raw text from PDF
    text = extract_text_from_pdf(filepath)

    if not text or len(text.strip()) < 50:
        return jsonify({"error": "Could not extract text from PDF. Make sure it's not a scanned image."}), 400

    # Step 2: Split text into smaller chunks (for better search)
    chunks = split_into_chunks(text, chunk_size=500)

    # Step 3: Store chunks in our RAG system (builds FAISS index)
    rag_system.load_chunks(chunks)

    return jsonify({
        "message": f"PDF uploaded successfully! Extracted {len(chunks)} text chunks.",
        "filename": file.filename,
        "total_chunks": len(chunks),
        "preview": text[:300] + "..."  # Show first 300 chars as preview
    })


# ─────────────────────────────────────────────
# ROUTE 3: Ask a question about the document
# ─────────────────────────────────────────────
@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question"}), 400

    if not rag_system.is_loaded():
        return jsonify({"error": "Please upload a PDF first"}), 400

    # Use RAG: find relevant chunks + ask OpenAI
    result = rag_system.answer_question(question)
    return jsonify(result)


# ─────────────────────────────────────────────
# ROUTE 4: Generate summary of the document
# ─────────────────────────────────────────────
@app.route("/summarize", methods=["POST"])
def summarize():
    if not rag_system.is_loaded():
        return jsonify({"error": "Please upload a PDF first"}), 400

    result = rag_system.generate_summary()
    return jsonify(result)


# ─────────────────────────────────────────────
# ROUTE 5: Extract key points from the document
# ─────────────────────────────────────────────
@app.route("/keypoints", methods=["POST"])
def key_points():
    if not rag_system.is_loaded():
        return jsonify({"error": "Please upload a PDF first"}), 400

    result = rag_system.extract_key_points()
    return jsonify(result)


# ─────────────────────────────────────────────
# ROUTE 6: Simple explanation of the document
# ─────────────────────────────────────────────
@app.route("/explain", methods=["POST"])
def explain():
    if not rag_system.is_loaded():
        return jsonify({"error": "Please upload a PDF first"}), 400

    result = rag_system.simple_explanation()
    return jsonify(result)


# Run the app
if __name__ == "__main__":
    print("=" * 50)
    print("AI Document Analyzer is running!")
    print("Open http://127.0.0.1:5000 in your browser")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0")
