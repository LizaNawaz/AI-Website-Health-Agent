import json

from app.ai.result_summarizer import ResultSummarizer
from app.ai.ollama_agent import OllamaAgent


def main():

    print("=" * 70)
    print("       AI WEBSITE HEALTH REPORT TEST")
    print("=" * 70)

    # -----------------------------------------
    # LOAD REAL SCAN
    # -----------------------------------------

    print("\n[1] Loading website scan...")

    with open(
        "data/reports/raw_scan.json",
        "r",
        encoding="utf-8"
    ) as file:

        website_results = json.load(file)

    print(
        "Website:",
        website_results["website"]
    )

    print(
        "Pages checked:",
        website_results["pages_checked"]
    )

    # -----------------------------------------
    # SUMMARIZE
    # -----------------------------------------

    print("\n[2] Creating AI summary...")

    summarizer = ResultSummarizer()

    summary = summarizer.summarize(
        website_results
    )

    print("✓ Summary created")

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

    # -----------------------------------------
    # OLLAMA
    # -----------------------------------------

    print("\n[3] Sending results to Ollama...")

    agent = OllamaAgent(
        model="llama3.2:latest"
    )

    report = agent.analyze(summary)

    # -----------------------------------------
    # DISPLAY REPORT
    # -----------------------------------------

    print("\n")
    print("=" * 70)
    print("              AI WEBSITE HEALTH REPORT")
    print("=" * 70)

    print(report)

    # -----------------------------------------
    # SAVE REPORT
    # -----------------------------------------

    report_path = (
        "data/reports/ai_health_report.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print("\n")
    print("=" * 70)
    print("✓ AI REPORT SAVED")
    print("=" * 70)

    print(report_path)


if __name__ == "__main__":
    main()