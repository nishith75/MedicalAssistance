import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "data", "processed", "faiss_index.bin")
TEXT_PATH = os.path.join(BASE_DIR, "data", "processed", "text_data.npy")

# ---------- LOAD MODEL ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- LOAD FAISS INDEX ----------
index = faiss.read_index(INDEX_PATH)
texts = np.load(TEXT_PATH, allow_pickle=True)

# ---------- SEARCH FUNCTION ----------
def search_medical_query(query, top_k=5):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    seen = set()
    results = []

    for idx in indices[0]:
        text = str(texts[idx])
        if text not in seen:
            seen.add(text)
            results.append(text)

    return results

