import json

from app.ai.result_summarizer import ResultSummarizer
from app.severity.severity_engine import SeverityEngine


def main():

    print("=" * 70)
    print("             SEVERITY ENGINE TEST")
    print("=" * 70)

    # -----------------------------------------
    # LOAD SCAN
    # -----------------------------------------

    with open(
        "data/reports/raw_scan.json",
        "r",
        encoding="utf-8"
    ) as file:

        website_results = json.load(file)

    print(
        "\nWebsite:",
        website_results["website"]
    )

    # -----------------------------------------
    # SUMMARIZE
    # -----------------------------------------

    summarizer = ResultSummarizer()

    summary = summarizer.summarize(
        website_results
    )

    # -----------------------------------------
    # SEVERITY ENGINE
    # -----------------------------------------

    engine = SeverityEngine()

    result = engine.calculate(
        summary
    )

    # -----------------------------------------
    # DISPLAY
    # -----------------------------------------

    print("\n")
    print("=" * 70)
    print("                 HEALTH RESULT")
    print("=" * 70)

    print(
        "\nHealth Score:",
        result["health_score"],
        "/ 100"
    )

    print(
        "Health Status:",
        result["health_status"]
    )

    print("\nSeverity Counts:")

    print(
        "Critical:",
        result["severity_counts"]["critical"]
    )

    print(
        "High:",
        result["severity_counts"]["high"]
    )

    print(
        "Medium:",
        result["severity_counts"]["medium"]
    )

    print(
        "Low:",
        result["severity_counts"]["low"]
    )

    print("\nPenalties:")

    for name, value in result[
        "penalties"
    ].items():

        print(
            f"{name}: -{value}"
        )


if __name__ == "__main__":
    main()