import json
import os
import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ---------- Paths ----------
DATA_PATH = r"D:\Advanced_AI\medical_chatbot\data\processed\medical_chatbot_dataset.json"
FAISS_PATH = r"D:\Advanced_AI\medical_chatbot\data\processed\faiss_index.bin"
TEXT_PATH = r"D:\Advanced_AI\medical_chatbot\data\processed\text_data.npy"

# ---------- Load cleaned data ----------
with open(DATA_PATH, "r") as f:
    data = json.load(f)

# Combine disease, symptoms, prevention, solutions into one text per entry
texts = []
for entry in data:
    combined_text = (
        f"Disease: {entry['disease']}. "
        f"Symptoms: {', '.join(entry['symptoms'])}. "
        f"Prevention: {', '.join(entry['prevention'])}. "
        f"Common solutions: {', '.join(entry['common_solutions'])}."
    )
    texts.append(combined_text)

# ---------- Load Sentence-BERT model ----------
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# ---------- Generate embeddings ----------
embeddings = model.encode(texts, show_progress_bar=True)

# ---------- Save text mapping ----------
np.save(TEXT_PATH, texts)

# ---------- Build FAISS index ----------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, FAISS_PATH)

print("✅ Embeddings and FAISS index created successfully.")
print("Using device:", device)
