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

    # Check retrieval relevance before calling the LLM
    if not results["is_relevant"]:
        return {
            "answer": "I could not find this information in the company policies.",
            "sources": []
        }

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

Your job is to answer questions ONLY from the provided policy context.

STRICT RULES:

1. Use only information explicitly stated in the policy context.
2. Do NOT use your general knowledge.
3. Do NOT infer missing policy details.
4. Do NOT combine unrelated policy information to create an answer.
5. If the context does not explicitly contain the answer, respond exactly:
"I could not find this information in the company policies."
6. If you are uncertain whether the answer is supported by the context, use the same response above.
7. Keep the answer concise.

Policy Context:
{context}

User Question:
{question}

Answer:
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

    question ="What is the capital of France?"

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