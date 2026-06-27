============================================================
  AI DOCUMENT ANALYZER - Student Project
  BS Computer Science - RAG Demo
============================================================

WHAT THIS PROJECT DOES:
  - Upload a PDF document
  - Extracts and chunks the text
  - Builds a FAISS vector index for smart search
  - Uses OpenAI GPT to answer questions (RAG pattern)
  - Generates summaries, key points, and simple explanations

------------------------------------------------------------
FOLDER STRUCTURE:
------------------------------------------------------------
  ai_doc_analyzer/
  ├── app.py              ← Flask server (routes/API)
  ├── rag.py              ← RAG logic (embeddings + search)
  ├── utils.py            ← PDF extraction + text chunking
  ├── requirements.txt    ← Python packages to install
  ├── README.txt          ← This file
  ├── sample.pdf          ← Test PDF (included)
  ├── uploads/            ← Uploaded PDFs are saved here
  └── templates/
      └── index.html      ← The web interface

------------------------------------------------------------
STEP-BY-STEP INSTALLATION:
------------------------------------------------------------

STEP 1 — Make sure Python is installed
  Open terminal/command prompt and run:
    python --version
  You need Python 3.9 or higher.

STEP 2 — Create a virtual environment (recommended)
  cd ai_doc_analyzer
  python -m venv venv

  Activate it:
    Windows:  venv\Scripts\activate
    Mac/Linux: source venv/bin/activate

STEP 3 — Install required packages
  pip install -r requirements.txt

  NOTE: If faiss-cpu fails to install, that's okay!
  The project will fall back to simple cosine similarity.
  You can try: pip install faiss-cpu --no-cache-dir

STEP 4 — Set your OpenAI API Key
  You need an OpenAI account and API key.
  Get one at: https://platform.openai.com/api-keys

  Set the key in your terminal:

    Windows (Command Prompt):
      set OPENAI_API_KEY=sk-your-key-here

    Windows (PowerShell):
      $env:OPENAI_API_KEY="sk-your-key-here"

    Mac / Linux:
      export OPENAI_API_KEY="sk-your-key-here"

  ⚠️  IMPORTANT: Never put your API key directly in the code!
      Always use environment variables.

STEP 5 — Run the application
  python app.py

STEP 6 — Open in browser
  Open: http://127.0.0.1:5000

------------------------------------------------------------
HOW TO USE THE APP:
------------------------------------------------------------

1. Click "Upload PDF" and select a PDF file
   (Use the included sample.pdf to test)

2. Wait for processing (30–60 seconds for embedding creation)

3. Click any of the analysis buttons:
   - "Summary"           → 3-4 sentence overview
   - "Key Points"        → Numbered list of main ideas
   - "Simple Explanation"→ Plain language description

4. Type a question in the Q&A box and click "Ask →"
   - The app finds the most relevant chunks using FAISS
   - Sends those chunks + your question to OpenAI
   - Returns a precise answer with source excerpts

------------------------------------------------------------
HOW RAG WORKS (for your understanding):
------------------------------------------------------------

Traditional approach: Send entire document to AI → expensive, limited

RAG approach:
  1. Split doc into chunks (e.g. 500 words each)
  2. Convert each chunk to a vector (embedding)
  3. When question asked → convert question to vector too
  4. Find top 3 chunks closest to question vector (FAISS)
  5. Send only those 3 chunks + question to OpenAI
  6. Get a focused, accurate answer

This is what companies like ChatGPT, Perplexity, etc. use
at a much larger scale!

------------------------------------------------------------
TROUBLESHOOTING:
------------------------------------------------------------

ERROR: "No module named 'pdfplumber'"
  → Run: pip install pdfplumber

ERROR: "Could not extract text from PDF"
  → Your PDF might be a scanned image (not text-based)
  → Try a different PDF with actual text

ERROR: "OpenAI API key not set"
  → Follow STEP 4 above to set your API key

ERROR: faiss-cpu fails to install
  → The project still works without it (slower search)
  → Skip it and proceed

QUESTION: Where are uploaded files saved?
  → In the uploads/ folder inside the project directory

------------------------------------------------------------
TECHNOLOGIES USED:
------------------------------------------------------------

  Flask       → Python web framework (server)
  pdfplumber  → Extract text from PDFs
  OpenAI API  → GPT-3.5-turbo for answers, ada for embeddings
  FAISS       → Fast vector similarity search (Facebook AI)
  NumPy       → Matrix operations for embeddings
  HTML/CSS/JS → Simple frontend (no React, no frameworks)

------------------------------------------------------------
PROJECT CONCEPTS DEMONSTRATED:
------------------------------------------------------------

  ✓ RAG (Retrieval-Augmented Generation)
  ✓ Text Embeddings & Vector Search
  ✓ Chunking Strategy with Overlap
  ✓ REST API Design (Flask routes)
  ✓ NLP via OpenAI API
  ✓ Document Understanding

============================================================
  Made for BS CS Academic Project — Keep it simple! 🎓
============================================================
