import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INDEX_PATH = "vector_store/index.faiss"
CHUNKS_PATH = "vector_store/chunks.npy"

print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("Loading chunks...")
chunks = np.load(CHUNKS_PATH, allow_pickle=True)

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, subject=None, k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k * 3)

    results = []

    for d, i in zip(distances[0], indices[0]):

        chunk = chunks[i]

        # subject filter
        if subject is not None and chunk["subject"] != subject:
            continue

        #  RELAX threshold
        if d > 1.3:
            continue

        results.append(chunk["text"])

        if len(results) >= k:
            break

    #  fallback 
    if len(results) == 0:
        for i in indices[0][:k]:
            results.append(chunks[i]["text"])

    return results
