import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "vector_store/chunks.npy"
INDEX_FILE = "vector_store/index.faiss"

print("Loading chunks...")
chunks = np.load(CHUNKS_FILE, allow_pickle=True)

print("Total chunks:", len(chunks))

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating embeddings...")

embeddings = model.encode(chunks, show_progress_bar=True)

dimension = embeddings.shape[1]

print("Embedding dimension:", dimension)

print("Building FAISS index...")

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, INDEX_FILE)

print("Index saved to:", INDEX_FILE)