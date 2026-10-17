from pathlib import Path

import chromadb

from .ingestion import load_documents, split_documents
from .embedding import MiniLMEmbeddingFunction


DB_DIR = Path("db/chroma")


def create_vector_store():

    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks to store: {len(chunks)}")

    embedding_function = MiniLMEmbeddingFunction()

    client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    collection = client.get_or_create_collection(
        name="company_policies",
    )

    ids = []
    texts = []
    metadatas = []

    for chunk in chunks:

        ids.append(
            f"{chunk['source']}_{chunk['chunk_id']}"
        )

        texts.append(
            chunk["content"]
        )

        metadatas.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        })

    print("Creating embeddings and storing documents...")

    embeddings = embedding_function(texts)

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print("Vector database created successfully!")
    print(f"Total vectors stored: {collection.count()}")


if __name__ == "__main__":
    create_vector_store()