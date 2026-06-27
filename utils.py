# utils.py - Utility Functions
# Helper functions for PDF text extraction and text chunking

import re

# Try pdfplumber first (better quality), fall back to PyPDF2
try:
    import pdfplumber
    PDF_LIBRARY = "pdfplumber"
    print("[INFO] Using pdfplumber for PDF extraction")
except ImportError:
    try:
        import PyPDF2
        PDF_LIBRARY = "pypdf2"
        print("[INFO] Using PyPDF2 for PDF extraction")
    except ImportError:
        PDF_LIBRARY = None
        print("[WARNING] No PDF library found! Install pdfplumber or PyPDF2")


# ─────────────────────────────────────────────
# FUNCTION 1: Extract text from PDF file
# ─────────────────────────────────────────────
def extract_text_from_pdf(filepath):
    """
    Read a PDF file and extract all text content.
    Returns a single string with all the text.
    """
    text = ""

    if PDF_LIBRARY == "pdfplumber":
        # pdfplumber is generally more accurate for complex PDFs
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n[Page {page_num + 1}]\n" + page_text

    elif PDF_LIBRARY == "pypdf2":
        # PyPDF2 is lighter but slightly less accurate
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n[Page {page_num + 1}]\n" + page_text

    else:
        return ""

    # Clean up extra whitespace
    text = clean_text(text)
    print(f"[Utils] Extracted {len(text)} characters from PDF")
    return text


# ─────────────────────────────────────────────
# FUNCTION 2: Clean extracted text
# ─────────────────────────────────────────────
def clean_text(text):
    """
    Remove extra spaces, fix newlines, etc.
    Makes the text cleaner before processing.
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)

    # Replace 3+ newlines with 2 newlines (keep paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


# ─────────────────────────────────────────────
# FUNCTION 3: Split text into chunks
# ─────────────────────────────────────────────
def split_into_chunks(text, chunk_size=500, overlap=50):
    """
    Split a long text into smaller overlapping chunks.
    
    Why chunks?
    - AI models have token limits (can't process huge documents at once)
    - Smaller chunks = more precise search results
    
    Why overlap?
    - Overlap ensures that information at chunk boundaries isn't lost
    - e.g. chunk 1 ends at word 500, chunk 2 starts at word 450
    
    Args:
        text: Full document text
        chunk_size: Approx number of words per chunk (default 500)
        overlap: Number of words to overlap between chunks (default 50)
    
    Returns:
        List of text chunk strings
    """
    # Split text into individual words
    words = text.split()
    chunks = []

    if len(words) == 0:
        return []

    # Slide a window across the words list
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        # Only add chunk if it has meaningful content (at least 30 words)
        if len(chunk_words) >= 30:
            chunks.append(chunk_text)

        # Move start forward, but keep some overlap with previous chunk
        start += (chunk_size - overlap)

    print(f"[Utils] Split text into {len(chunks)} chunks (chunk_size={chunk_size}, overlap={overlap})")
    return chunks
