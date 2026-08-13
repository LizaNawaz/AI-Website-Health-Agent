import os
import json

from dotenv import load_dotenv

from app.crawler.website_crawler import WebsiteCrawler
from app.crawler.page_parser import PageParser
from app.checker.page_checker import PageChecker
from app.ai.result_summarizer import ResultSummarizer
from app.ai.ollama_agent import OllamaAgent
from app.severity.severity_engine import SeverityEngine


load_dotenv()


def main():

    print("=" * 70)
    print("              AI WEBSITE HEALTH AGENT")
    print("=" * 70)

    url = input("\nEnter website URL: ").strip()

    if not url:
        print("❌ URL cannot be empty.")
        return

    # ============================================================
    # CONFIGURATION
    # ============================================================

    max_pages = int(
        os.getenv("MAX_PAGES", "5")
    )

    timeout = int(
        os.getenv("REQUEST_TIMEOUT", "10")
    )

    print("\nConfiguration")
    print("-" * 70)
    print("Website:", url)
    print("Maximum pages:", max_pages)
    print("Timeout:", timeout)

    # ============================================================
    # STEP 1 — CRAWLER
    # ============================================================

    print("\n")
    print("=" * 70)
    print("[1/5] WEBSITE CRAWLING")
    print("=" * 70)

    crawler = WebsiteCrawler(
        timeout=timeout,
        max_pages=max_pages
    )

    pages = crawler.crawl(url)

    print("\n✓ Crawling completed")
    print("Pages discovered:", len(pages))

    if not pages:
        print("❌ No pages were discovered.")
        return

    # ============================================================
    # STEP 2 — PARSER + CHECKER
    # ============================================================

    print("\n")
    print("=" * 70)
    print("[2/5] CHECKING WEBSITE RESOURCES")
    print("=" * 70)

    parser = PageParser()

    checker = PageChecker(
        timeout=timeout
    )

    all_results = []

    for number, page in enumerate(
        pages,
        start=1
    ):

        print(
            f"\n[{number}/{len(pages)}] {page['url']}"
        )

        # --------------------------------------------------------
        # FAILED PAGE
        # --------------------------------------------------------

        if not page["success"]:

            print(
                "❌ Page failed:",
                page.get("status_code")
            )

            all_results.append({
                "page_url": page["url"],
                "page_status": page.get(
                    "status_code"
                ),
                "page_failed": True,
                "error": page.get("error"),
                "links": [],
                "images": [],
                "stylesheets": [],
                "scripts": []
            })

            continue

        # --------------------------------------------------------
        # PARSE PAGE
        # --------------------------------------------------------

        page_data = parser.parse(
            page["html"],
            page["url"]
        )

        print(
            "Links:",
            len(page_data["links"])
        )

        print(
            "Images:",
            len(page_data["images"])
        )

        print(
            "CSS:",
            len(page_data["stylesheets"])
        )

        print(
            "JS:",
            len(page_data["scripts"])
        )

        # --------------------------------------------------------
        # CHECK RESOURCES
        # --------------------------------------------------------

        results = checker.check_page(
            page_data
        )

        results["page_url"] = page["url"]

        results["page_status"] = (
            page["status_code"]
        )

        results["page_failed"] = False

        all_results.append(results)

    # ============================================================
    # STEP 3 — SAVE RAW SCAN
    # ============================================================

    print("\n")
    print("=" * 70)
    print("[3/5] SAVING RAW SCAN")
    print("=" * 70)

    website_results = {
        "website": url,
        "pages_checked": len(all_results),
        "pages": all_results
    }

    report_folder = os.path.join(
        os.getcwd(),
        "data",
        "reports"
    )

    os.makedirs(
        report_folder,
        exist_ok=True
    )

    raw_report_file = os.path.join(
        report_folder,
        "raw_scan.json"
    )

    with open(
        raw_report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            website_results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "✓ Raw scan saved:"
    )

    print(
        os.path.abspath(
            raw_report_file
        )
    )

    # ============================================================
    # STEP 4 — SUMMARIZE RESULTS
    # ============================================================

    print("\n")
    print("=" * 70)
    print("[4/5] PREPARING AI ANALYSIS")
    print("=" * 70)

    summarizer = ResultSummarizer()

    summary = summarizer.summarize(
        website_results
    )

    print(
        "✓ Scan summary created"
    )

    print("\nVerified problems:")

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

    # ============================================================
    # STEP 4.5 — SEVERITY + HEALTH SCORE
    # ============================================================

    print("\n")
    print("=" * 70)
    print("[4.5/5] CALCULATING WEBSITE HEALTH SCORE")
    print("=" * 70)

    severity_engine = SeverityEngine()

    health_result = severity_engine.calculate(
        summary
    )

    print(
        "\nHealth Score:",
        health_result["health_score"],
        "/ 100"
    )

    print(
        "Health Status:",
        health_result["health_status"]
    )

    print(
        "Critical:",
        health_result["severity_counts"]["critical"]
    )

    print(
        "High:",
        health_result["severity_counts"]["high"]
    )

    print(
        "Medium:",
        health_result["severity_counts"]["medium"]
    )

    print(
        "Low:",
        health_result["severity_counts"]["low"]
    )

    # ============================================================
    # STEP 5 — OLLAMA AI ANALYSIS
    # ============================================================

    print("\n")
    print("=" * 70)
    print("[5/5] OLLAMA AI ANALYSIS")
    print("=" * 70)

    print(
        "\nSending verified results to Ollama..."
    )

    print(
        "Model: llama3.2:latest"
    )

    agent = OllamaAgent(
        model="llama3.2:latest"
    )

    # IMPORTANT:
    # Send both the verified scan summary
    # and the deterministic health result.

    report = agent.analyze(
        summary,
        health_result
    )

    # ============================================================
    # SAVE AI REPORT
    # ============================================================

    ai_report_file = os.path.join(
        report_folder,
        "ai_health_report.txt"
    )

    with open(
        ai_report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    # ============================================================
    # FINAL OUTPUT
    # ============================================================

    print("\n")
    print("=" * 70)
    print("             AI WEBSITE HEALTH REPORT")
    print("=" * 70)

    print("\n")

    print(report)

    print("\n")
    print("=" * 70)
    print("                    COMPLETE")
    print("=" * 70)

    print(
        "\nRaw scan:"
    )

    print(
        os.path.abspath(
            raw_report_file
        )
    )

    print(
        "\nAI report:"
    )

    print(
        os.path.abspath(
            ai_report_file
        )
    )


if __name__ == "__main__":
    main()