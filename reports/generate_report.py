import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent

JSON_REPORT = BASE_DIR / "evaluation_report.json"
MARKDOWN_REPORT = BASE_DIR / "evaluation_report.md"


with open(JSON_REPORT, "r", encoding="utf-8") as file:
    report = json.load(file)


total_tests = report["total_tests"]
passed_tests = report["passed_tests"]
failed_tests = report["failed_tests"]
pass_rate = report["pass_rate"]

metrics = report.get("metrics_by_test_type", {})
tests = report.get("tests", [])


# Calculate average evaluation scores
if tests:

    avg_faithfulness = round(
        sum(test["evaluation"]["faithfulness"] for test in tests)
        / len(tests),
        3
    )

    avg_relevance = round(
        sum(test["evaluation"]["relevance"] for test in tests)
        / len(tests),
        3
    )

    avg_safety = round(
        sum(test["evaluation"]["safety"] for test in tests)
        / len(tests),
        3
    )

    avg_overall = round(
        sum(test["evaluation"]["overall"] for test in tests)
        / len(tests),
        3
    )

else:

    avg_faithfulness = 0
    avg_relevance = 0
    avg_safety = 0
    avg_overall = 0


generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


lines = []

lines.append("# AI-Guard-Judge Evaluation Report")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(
    "This report summarizes the automated evaluation results "
    "for the AI-Guard-Judge RAG system."
)
lines.append("")

lines.append("## Overall Results")
lines.append("")
lines.append("| Metric | Result |")
lines.append("|---|---:|")
lines.append(f"| Total Tests | {total_tests} |")
lines.append(f"| Passed | {passed_tests} |")
lines.append(f"| Failed | {failed_tests} |")
lines.append(f"| Pass Rate | {pass_rate}% |")
lines.append("")

lines.append("## Average Evaluation Scores")
lines.append("")
lines.append("| Metric | Score |")
lines.append("|---|---:|")
lines.append(f"| Faithfulness | {avg_faithfulness} |")
lines.append(f"| Relevance | {avg_relevance} |")
lines.append(f"| Safety | {avg_safety} |")
lines.append(f"| Overall | {avg_overall} |")
lines.append("")

lines.append("## Metrics by Test Type")
lines.append("")
lines.append("| Test Type | Total | Passed | Failed | Pass Rate |")
lines.append("|---|---:|---:|---:|---:|")

for test_type, data in metrics.items():

    lines.append(
        f"| {test_type} | "
        f"{data['total']} | "
        f"{data['passed']} | "
        f"{data['failed']} | "
        f"{data['pass_rate']}% |"
    )

lines.append("")

lines.append("## Detailed Test Results")
lines.append("")

for test in tests:

    evaluation = test["evaluation"]

    lines.append(f"### {test['id']}")
    lines.append("")
    lines.append(f"**Test Type:** `{test['test_type']}`")
    lines.append("")
    lines.append(f"**Question:** {test['question']}")
    lines.append("")
    lines.append(f"**Result:** `{test['result']}`")
    lines.append("")

    lines.append("**Evaluation Scores:**")
    lines.append("")
    lines.append(
        f"- Faithfulness: {evaluation['faithfulness']}"
    )
    lines.append(
        f"- Relevance: {evaluation['relevance']}"
    )
    lines.append(
        f"- Safety: {evaluation['safety']}"
    )
    lines.append(
        f"- Overall: {evaluation['overall']}"
    )
    lines.append("")

    lines.append("**Judge Reason:**")
    lines.append("")
    lines.append(evaluation["reason"])
    lines.append("")

    lines.append("---")
    lines.append("")


lines.append(f"*Report generated on {generated_time}*")


with open(MARKDOWN_REPORT, "w", encoding="utf-8") as file:
    file.write("\n".join(lines))


print("=" * 60)
print("EVALUATION REPORT GENERATED")
print("=" * 60)
print(f"Report: {MARKDOWN_REPORT}")