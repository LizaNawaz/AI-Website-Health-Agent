import json

from app.ai.result_summarizer import ResultSummarizer


def main():

    print("=" * 60)
    print("TESTING RESULT SUMMARIZER")
    print("=" * 60)

    # Load real scan
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

    print(
        "Pages:",
        website_results["pages_checked"]
    )

    # Create summarizer
    summarizer = ResultSummarizer()

    summary = summarizer.summarize(
        website_results
    )

    print("\nSUMMARY CREATED")
    print("=" * 60)

    print(
        "Failed pages:",
        len(summary["failed_pages"])
    )

    print(
        "Broken links:",
        len(summary["broken_links"])
    )

    print(
        "Broken images:",
        len(summary["broken_images"])
    )

    print(
        "Broken CSS:",
        len(summary["broken_css"])
    )

    print(
        "Broken JavaScript:",
        len(summary["broken_scripts"])
    )


if __name__ == "__main__":
    main()