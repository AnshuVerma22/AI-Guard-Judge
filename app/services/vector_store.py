from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingestion import load_documents, split_documents


DB_DIR = Path("db/chroma")


def create_vector_store():
    # Load and split documents
    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks to embed: {len(chunks)}")

    # Load embedding model
    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create ChromaDB client
    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    # Create collection
    collection = client.get_or_create_collection(
        name="company_policies"
    )

    # Prepare data
    ids = []
    texts = []
    metadatas = []

    for chunk in chunks:
        ids.append(
            f"{chunk['source']}_{chunk['chunk_id']}"
        )

        texts.append(chunk["content"])

        metadatas.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        })

    # Generate embeddings
    print("Creating embeddings...")

    embeddings = model.encode(texts).tolist()

    # Store everything in ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Vector database created successfully!")
    print(f"Total vectors stored: {collection.count()}")


if __name__ == "__main__":
    create_vector_store()