import os
import json

from app.crawler.website_crawler import WebsiteCrawler
from app.crawler.page_parser import PageParser
from app.checker.page_checker import PageChecker
from app.ai.result_summarizer import ResultSummarizer
from app.ai.ollama_agent import OllamaAgent
from app.severity.severity_engine import SeverityEngine


class WebsiteScanner:

    def __init__(
        self,
        max_pages=5,
        timeout=10,
        ollama_model="llama3.2:latest"
    ):

        self.max_pages = max_pages
        self.timeout = timeout
        self.ollama_model = ollama_model

        self.crawler = WebsiteCrawler(
            timeout=timeout,
            max_pages=max_pages
        )

        self.parser = PageParser()

        self.checker = PageChecker(
            timeout=timeout
        )

        self.summarizer = ResultSummarizer()

        self.severity_engine = SeverityEngine()

        self.ai_agent = OllamaAgent(
            model=ollama_model
        )

    # ============================================================
    # MAIN SCAN
    # ============================================================

    def scan(self, url):

        # --------------------------------------------------------
        # STEP 1 — CRAWL
        # --------------------------------------------------------

        pages = self.crawler.crawl(url)

        if not pages:
            raise Exception(
                "No pages were discovered."
            )

        # --------------------------------------------------------
        # STEP 2 — PARSE + CHECK
        # --------------------------------------------------------

        all_results = []

        for page in pages:

            # Failed page
            if not page["success"]:

                all_results.append({

                    "page_url": page["url"],

                    "page_status": page.get(
                        "status_code"
                    ),

                    "page_failed": True,

                    "error": page.get(
                        "error"
                    ),

                    "links": [],

                    "images": [],

                    "stylesheets": [],

                    "scripts": []
                })

                continue

            # Parse
            page_data = self.parser.parse(
                page["html"],
                page["url"]
            )

            # Check
            results = self.checker.check_page(
                page_data
            )

            results["page_url"] = page["url"]

            results["page_status"] = (
                page["status_code"]
            )

            results["page_failed"] = False

            all_results.append(
                results
            )

        # --------------------------------------------------------
        # STEP 3 — RAW RESULTS
        # --------------------------------------------------------

        website_results = {

            "website": url,

            "pages_checked": len(
                all_results
            ),

            "pages": all_results
        }

        # --------------------------------------------------------
        # SAVE RAW JSON
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # STEP 4 — SUMMARY
        # --------------------------------------------------------

        summary = self.summarizer.summarize(
            website_results
        )

        # --------------------------------------------------------
        # STEP 5 — HEALTH SCORE
        # --------------------------------------------------------

        health_result = (
            self.severity_engine.calculate(
                summary
            )
        )

        # --------------------------------------------------------
        # STEP 6 — OLLAMA
        # --------------------------------------------------------

        ai_report = self.ai_agent.analyze(
            summary,
            health_result
        )

        # --------------------------------------------------------
        # SAVE AI REPORT
        # --------------------------------------------------------

        ai_report_file = os.path.join(
            report_folder,
            "ai_health_report.txt"
        )

        with open(
            ai_report_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                ai_report
            )

        # --------------------------------------------------------
        # RETURN EVERYTHING
        # --------------------------------------------------------

        return {

            "website": url,

            "pages": pages,

            "website_results": website_results,

            "summary": summary,

            "health_result": health_result,

            "ai_report": ai_report,

            "raw_report_file": raw_report_file,

            "ai_report_file": ai_report_file
        }