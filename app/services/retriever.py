from pathlib import Path

import chromadb

from .embedding import MiniLMEmbeddingFunction


DB_DIR = Path("db/chroma")


# Create embedding function
embedding_function = MiniLMEmbeddingFunction()


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path=str(DB_DIR)
)


collection = client.get_collection(
    name="company_policies"
)


def search_documents(query, top_k=3, max_distance=1.10):

    # Generate query embedding locally
    query_embedding = embedding_function([query])[0]

    # Search using the generated embedding
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Check whether the best retrieved result is relevant
    best_distance = results["distances"][0][0]

    results["is_relevant"] = best_distance <= max_distance

    return results