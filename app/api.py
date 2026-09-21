from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.rag import generate_answer
from app.services.evaluator import evaluate_answer
from app.logging_config import logger


app = FastAPI(
    title="AI-Guard-Judge API",
    description="RAG and AI evaluation backend",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI-Guard-Judge API"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        result = generate_answer(request.question)

        logger.info(
            f"ASK | question={request.question!r} | "
            f"sources={len(result['sources'])} | status=200"
        )

        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"],
            "source_count": len(result["sources"])
        }

    except Exception as e:

        logger.error(
            f"ASK | question={request.question!r} | "
            f"status=500 | error={e}"
        )

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request."
        )


@app.post("/evaluate")
def evaluate_question(request: QuestionRequest):

    try:

        rag_result = generate_answer(request.question)

        evaluation = evaluate_answer(
            request.question,
            rag_result["answer"],
            rag_result["context"],
            "rag"
        )

        logger.info(
            f"EVALUATE | question={request.question!r} | status=200"
        )

        return {
            "question": request.question,
            "answer": rag_result["answer"],
            "sources": rag_result["sources"],
            "evaluation": evaluation
        }

    except Exception as e:

        logger.error(
            f"EVALUATE | question={request.question!r} | "
            f"status=500 | error={e}"
        )

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request."
        )