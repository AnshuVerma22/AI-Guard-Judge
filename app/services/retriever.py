from pathlib import Path

import chromadb


DB_DIR = Path("db/chroma")


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path=str(DB_DIR)
)


collection = client.get_collection(
    name="company_policies"
)


def search_documents(query, top_k=3, max_distance=1.10):

    # ChromaDB handles query embedding automatically
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    # Check whether the best retrieved result is relevant
    best_distance = results["distances"][0][0]

    results["is_relevant"] = best_distance <= max_distance

    return results