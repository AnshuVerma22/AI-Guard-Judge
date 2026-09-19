import os

from dotenv import load_dotenv
from groq import Groq

from retriever import search_documents


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question):

    # Retrieve relevant documents
    results = search_documents(question, top_k=3)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Build context
    context_parts = []

    for i, document in enumerate(documents):
        source = metadatas[i]["source"]
        chunk_id = metadatas[i]["chunk_id"]

        context_parts.append(
            f"[Source: {source}, Chunk: {chunk_id}]\n"
            f"{document}"
        )

    context = "\n\n".join(context_parts)

    # Prompt
    prompt = f"""
You are a company policy assistant.

Answer the user's question using ONLY the provided policy context.

If the answer is not available in the context, say:
"I could not find this information in the company policies."

Do not invent or assume information.

Policy Context:
{context}

User Question:
{question}

Answer clearly and concisely.
"""

    # Call LLM
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": metadatas
    }


if __name__ == "__main__":

    question = "How much is the domestic travel allowance?"

    result = generate_answer(question)

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(result["answer"])

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(Chunk {source['chunk_id']})"
        )