from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DB_DIR = Path("db/chroma")


# Load embedding model once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB once
client = chromadb.PersistentClient(
    path=str(DB_DIR)
)


collection = client.get_collection(
    name="company_policies"
)


def search_documents(query, top_k=3, max_distance=1.10):

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Check whether the best retrieved result is relevant
    best_distance = results["distances"][0][0]

    results["is_relevant"] = best_distance <= max_distance

    return results