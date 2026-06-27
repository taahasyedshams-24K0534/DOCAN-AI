# Docan — AI Document Analyzer

An AI-powered document analysis tool that lets you upload PDF files, get instant summaries, extract key points, and ask questions about your documents using RAG (Retrieval-Augmented Generation).

## Features

- Upload PDF files
- AI-generated summaries
- Extract key points from documents
- Ask questions and get precise answers based on document content
- Simple explanation mode for complex documents

## Tech Stack

- **Backend:** Python, Flask
- **AI / LLM:** Groq API
- **Vector Search:** FAISS
- **PDF Processing:** pdfplumber
- **Frontend:** HTML, CSS, JavaScript
- **Architecture:** Retrieval-Augmented Generation (RAG)

## How RAG Works

1. PDF is split into chunks
2. Each chunk is converted to a vector (embedding)
3. When a question is asked, it's converted to a vector too
4. FAISS finds the top 3 most relevant chunks
5. Those chunks + your question are sent to Groq
6. A focused, accurate answer is returned

## Setup

1. Clone the repo
```bash
   git clone https://github.com/taahasyedshams-24K0534/DOCAN-AI.git
   cd DOCAN-AI
```

2. Create and activate virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Add your Groq API key
```bash
   # Windows PowerShell
   $env:GROQ_API_KEY="your_key_here"
```

5. Run the app
```bash
   python app.py
```

6. Open in browser
