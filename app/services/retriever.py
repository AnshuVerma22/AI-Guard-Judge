from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DB_DIR = Path("db/chroma")


def search_documents(query, top_k=3, max_distance=1.10):
    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Connect to existing ChromaDB
    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    collection = client.get_collection(
        name="company_policies"
    )

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


if __name__ == "__main__":

    query = "How much is the domestic travel allowance?"

    print(f"\nQuery: {query}\n")

    results = search_documents(query)

    for i, document in enumerate(results["documents"][0]):

        print("=" * 60)

        print(f"Result {i + 1}")

        print(f"Source: {results['metadatas'][0][i]['source']}")

        print(f"Chunk ID: {results['metadatas'][0][i]['chunk_id']}")

        print("\nContent:")

        print(document)