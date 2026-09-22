import json
from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

REPORT_PATH = (
    Path(__file__).resolve().parent.parent
    / "reports"
    / "evaluation_report.json"
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI-Guard-Judge Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------------
# Load evaluation report
# ---------------------------------------------------------

if not REPORT_PATH.exists():

    st.error(
        "Evaluation report not found. "
        "Run the evaluation suite first."
    )

    st.stop()


with open(REPORT_PATH, "r", encoding="utf-8") as file:

    report = json.load(file)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🛡️ AI-Guard-Judge Evaluation Dashboard")

st.caption(
    "RAG quality, safety, and automated evaluation monitoring"
)


# ---------------------------------------------------------
# Overall metrics
# ---------------------------------------------------------

total_tests = report["total_tests"]
passed_tests = report["passed_tests"]
failed_tests = report["failed_tests"]
pass_rate = report["pass_rate"]

evaluation_timestamp = report.get(
    "evaluation_timestamp",
    "N/A"
)

duration_seconds = report.get(
    "duration_seconds",
    "N/A"
)

tests = report.get("tests", [])

st.subheader("Overall Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Tests",
        total_tests
    )

with col2:

    st.metric(
        "Passed",
        passed_tests
    )

with col3:

    st.metric(
        "Failed",
        failed_tests
    )

with col4:

    st.metric(
        "Pass Rate",
        f"{pass_rate}%"
    )

st.subheader("Evaluation Run")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Evaluation Duration",
        f"{duration_seconds} seconds"
    )

with col2:

    st.write("**Evaluation Timestamp**")
    st.write(evaluation_timestamp)
# ---------------------------------------------------------
# Average evaluation scores
# ---------------------------------------------------------

st.subheader("AI Evaluation Scores")


if tests:

    avg_faithfulness = round(
        sum(
            test["evaluation"]["faithfulness"]
            for test in tests
        ) / len(tests),
        3
    )

    avg_relevance = round(
        sum(
            test["evaluation"]["relevance"]
            for test in tests
        ) / len(tests),
        3
    )

    avg_safety = round(
        sum(
            test["evaluation"]["safety"]
            for test in tests
        ) / len(tests),
        3
    )

    avg_overall = round(
        sum(
            test["evaluation"]["overall"]
            for test in tests
        ) / len(tests),
        3
    )

else:

    avg_faithfulness = 0
    avg_relevance = 0
    avg_safety = 0
    avg_overall = 0


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Faithfulness",
        f"{avg_faithfulness * 100:.0f}%"
    )

with col2:

    st.metric(
        "Relevance",
        f"{avg_relevance * 100:.0f}%"
    )

with col3:

    st.metric(
        "Safety",
        f"{avg_safety * 100:.0f}%"
    )

with col4:

    st.metric(
        "Overall Score",
        f"{avg_overall * 100:.0f}%"
    )


# ---------------------------------------------------------
# Metrics by test type
# ---------------------------------------------------------

st.subheader("Performance by Test Type")


metrics = report.get(
    "metrics_by_test_type",
    {}
)


if metrics:

    category_rows = []

    for test_type, data in metrics.items():

        category_rows.append(
            {
                "Test Type": test_type,
                "Total": data["total"],
                "Passed": data["passed"],
                "Failed": data["failed"],
                "Pass Rate": data["pass_rate"]
            }
        )

    category_df = pd.DataFrame(category_rows)

    st.dataframe(
        category_df,
        use_container_width=True,
        hide_index=True
    )

    chart_df = category_df[
        ["Test Type", "Pass Rate"]
    ].set_index("Test Type")

    st.bar_chart(chart_df)


# ---------------------------------------------------------
# Test explorer
# ---------------------------------------------------------

st.subheader("Test Explorer")


if tests:

    explorer_rows = []

    for test in tests:

        evaluation = test["evaluation"]

        explorer_rows.append(
            {
                "ID": test["id"],
                "Type": test["test_type"],
                "Question": test["question"],
                "Faithfulness": evaluation["faithfulness"],
                "Relevance": evaluation["relevance"],
                "Safety": evaluation["safety"],
                "Overall": evaluation["overall"],
                "Result": test["result"]
            }
        )

    df = pd.DataFrame(explorer_rows)

    filter_option = st.selectbox(
        "Filter tests",
        [
            "All Tests",
            "Passed Tests",
            "Failed Tests"
        ]
    )

    if filter_option == "Passed Tests":

        filtered_df = df[
            df["Result"] == "PASS"
        ]

    elif filter_option == "Failed Tests":

        filtered_df = df[
            df["Result"] == "FAIL"
        ]

    else:

        filtered_df = df


    display_df = filtered_df.copy()

    for column in [
        "Faithfulness",
        "Relevance",
        "Safety",
        "Overall"
    ]:

        display_df[column] = (
            display_df[column] * 100
        ).round(0).astype(int).astype(str) + "%"


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# Detailed evaluation
# ---------------------------------------------------------

st.subheader("Evaluation Details")


for test in tests:

    evaluation = test["evaluation"]

    with st.expander(
        f"{test['id']} — {test['result']}"
    ):

        st.write(
            "**Question:**",
            test["question"]
        )

        st.write(
            "**Test Type:**",
            test["test_type"]
        )

        st.write(
            "**Answer:**",
            test["answer"]
        )

        st.write(
            "**Faithfulness:**",
            evaluation["faithfulness"]
        )

        st.write(
            "**Relevance:**",
            evaluation["relevance"]
        )

        st.write(
            "**Safety:**",
            evaluation["safety"]
        )

        st.write(
            "**Overall:**",
            evaluation["overall"]
        )

        st.write(
            "**Judge Reason:**",
            evaluation["reason"]
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "AI-Guard-Judge • Automated RAG Evaluation System"
)