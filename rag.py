# rag.py - RAG System using Groq

import os
import numpy as np
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = None

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
    print("[INFO] Groq API key loaded successfully")
else:
    print("[WARNING] GROQ_API_KEY not set!")

try:
    import faiss
    FAISS_AVAILABLE = True
    print("[INFO] FAISS available")
except ImportError:
    FAISS_AVAILABLE = False
    print("[INFO] FAISS not found - using cosine similarity")


def _simple_embedding(text):
    # Basic character-frequency embedding (no API needed)
    vec = np.zeros(256, dtype=np.float32)
    for ch in text[:2000]:
        vec[ord(ch) % 256] += 1
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


class RAGSystem:
    def __init__(self):
        self.chunks = []
        self.embeddings = None
        self.index = None
        self.loaded = False

    def is_loaded(self):
        return self.loaded

    def load_chunks(self, chunks):
        self.chunks = chunks
        self.loaded = False
        print(f"[RAG] Creating embeddings for {len(chunks)} chunks...")
        embeddings_list = [_simple_embedding(chunk) for chunk in chunks]
        self.embeddings = np.array(embeddings_list, dtype=np.float32)
        if FAISS_AVAILABLE:
            self._build_faiss_index()
        self.loaded = True
        print("[RAG] Document ready!")

    def _build_faiss_index(self):
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)

    def find_relevant_chunks(self, query, top_k=3):
        query_embedding = np.array([_simple_embedding(query)], dtype=np.float32)
        if FAISS_AVAILABLE and self.index is not None:
            distances, indices = self.index.search(query_embedding, top_k)
            return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]
        else:
            return self._cosine_search(query_embedding[0], top_k)

    def _cosine_search(self, query_vec, top_k):
        def norm(v):
            n = np.linalg.norm(v)
            return v / n if n > 0 else v
        query_norm = norm(query_vec)
        scores = [(np.dot(query_norm, norm(emb)), i)
                  for i, emb in enumerate(self.embeddings)]
        scores.sort(reverse=True)
        return [self.chunks[i] for _, i in scores[:top_k]]

    def _ask_groq(self, prompt):
        if not client:
            return "GROQ_API_KEY not set."
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()

    def answer_question(self, question):
        relevant_chunks = self.find_relevant_chunks(question, top_k=3)
        context = "\n\n---\n\n".join(relevant_chunks)
        prompt = f"""You are a helpful document assistant.
Answer the question based ONLY on the document context below.
If the answer is not in the context, say "I couldn't find that in the document."

Document context:
{context}

Question: {question}
Answer:"""
        answer = self._ask_groq(prompt)
        return {"answer": answer, "source_chunks": relevant_chunks}

    def generate_summary(self):
        sample_text = " ".join(self.chunks[:6])[:2500]
        prompt = f"Summarize this document in 3-4 clear sentences:\n\n{sample_text}"
        return {"summary": self._ask_groq(prompt)}

    def extract_key_points(self):
        sample_text = " ".join(self.chunks[:8])[:3000]
        prompt = f"Extract 5-7 key points as a numbered list:\n\n{sample_text}"
        return {"key_points": self._ask_groq(prompt)}

    def simple_explanation(self):
        sample_text = " ".join(self.chunks[:6])[:2500]
        prompt = f"Explain this document simply, no jargon, short sentences:\n\n{sample_text}"
        return {"explanation": self._ask_groq(prompt)}