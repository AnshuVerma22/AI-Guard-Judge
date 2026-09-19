from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCUMENTS_DIR = Path("data/documents")


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": text
        })

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = []

    for document in documents:
        split_texts = splitter.split_text(document["content"])

        for index, chunk in enumerate(split_texts):
            chunks.append({
                "source": document["source"],
                "chunk_id": index,
                "content": chunk
            })

    return chunks


if __name__ == "__main__":
    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    for chunk in chunks[:5]:
        print("\n" + "=" * 60)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["content"])