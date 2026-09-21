import json
import sys
from pathlib import Path


# Allow importing services from app/services
sys.path.append(
    str(Path(__file__).resolve().parent.parent / "app" / "services")
)

from rag import generate_answer
from evaluator import evaluate_answer


DATASET_PATH = Path(__file__).parent / "evaluation_dataset.json"

RESULTS_PATH = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "evaluation_results.json"
)

METRICS_PATH = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "metrics.json"
)

HISTORY_DIR = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "history"
)
def load_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def run_evaluation():

    dataset = load_dataset()

    results = []

    for test_case in dataset:

        question = test_case["question"]
        expected_answer = test_case["expected_answer"]

        print("=" * 70)
        print(f"Test Case: {test_case['id']}")
        print(f"Type: {test_case['type']}")
        print(f"Question: {question}")

        # Run RAG
        result = generate_answer(question)

        actual_answer = result["answer"]
        context = result["context"]

        # Run AI Judge
        judge_result = evaluate_answer(
            question,
            actual_answer,
            context,
            test_case["type"]
        )

        # Consider score >= 0.8 as passing
        passed = judge_result["overall"] >= 0.8

        results.append({
            "id": test_case["id"],
            "question": question,
            "type": test_case["type"],
            "expected_answer": expected_answer,
            "actual_answer": actual_answer,
            "faithfulness": judge_result["faithfulness"],
            "relevance": judge_result["relevance"],
            "safety": judge_result["safety"],
            "overall": judge_result["overall"],
            "reason": judge_result["reason"],
            "passed": passed
        })

        print(f"Expected: {expected_answer}")
        print(f"Actual:   {actual_answer}")
        print(f"Faithfulness: {judge_result['faithfulness']}")
        print(f"Relevance:    {judge_result['relevance']}")
        print(f"Safety:       {judge_result['safety']}")
        print(f"Overall:      {judge_result['overall']}")
        print(f"Reason:       {judge_result['reason']}")
        print(f"Result:       {'PASS' if passed else 'FAIL'}")

    return results


if __name__ == "__main__":

    results = run_evaluation()

    total = len(results)
    passed = sum(result["passed"] for result in results)
    failed = total - passed

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Total tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print(f"Accuracy    : {(passed / total) * 100:.2f}%")

    # Create results folder if it does not exist
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save detailed evaluation results
    with open(RESULTS_PATH, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nSaved evaluation results to: {RESULTS_PATH}")

    # Calculate average evaluation scores

    average_faithfulness = sum(
        result["faithfulness"] for result in results
    ) / total

    average_relevance = sum(
        result["relevance"] for result in results
    ) / total

    average_safety = sum(
        result["safety"] for result in results
    ) / total

    average_overall = sum(
        result["overall"] for result in results
    ) / total

    # Store metrics

    metrics = {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "accuracy": round(
            (passed / total) * 100,
            2
        ),
        "average_faithfulness": round(
            average_faithfulness,
            2
        ),
        "average_relevance": round(
            average_relevance,
            2
        ),
        "average_safety": round(
            average_safety,
            2
        ),
        "average_overall": round(
            average_overall,
            2
        )
    }

    # Save metrics to metrics.json

    with open(METRICS_PATH, "w", encoding="utf-8") as file:
        json.dump(
            metrics,
            file,
            indent=4
        )

    print(f"Metrics saved to: {METRICS_PATH}")

# Save evaluation history

HISTORY_DIR.mkdir(parents=True, exist_ok=True)

history_file = (
    HISTORY_DIR
    / f"evaluation_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
)

with open(history_file, "w", encoding="utf-8") as file:
    json.dump(
        {
            "metrics": metrics,
            "results": results
        },
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"Evaluation history saved to: {history_file}")