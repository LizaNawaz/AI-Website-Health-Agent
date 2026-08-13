import json
import ollama


class OllamaAgent:

    def __init__(self, model="llama3.2:latest"):
        self.model = model

    def analyze(
        self,
        scan_summary,
        health_result
    ):

        # ============================================================
        # PREPARE VERIFIED DATA
        # ============================================================

        data = {
            "website": scan_summary.get(
                "website"
            ),

            "pages_checked": scan_summary.get(
                "pages_checked",
                0
            ),

            "failed_pages": scan_summary.get(
                "failed_pages",
                []
            )[:10],

            "broken_links": scan_summary.get(
                "broken_links",
                []
            )[:20],

            "broken_images": scan_summary.get(
                "broken_images",
                []
            )[:20],

            "broken_css": scan_summary.get(
                "broken_css",
                []
            )[:20],

            "broken_scripts": scan_summary.get(
                "broken_scripts",
                []
            )[:20],

            # --------------------------------------------------------
            # DETERMINISTIC HEALTH RESULT
            # --------------------------------------------------------

            "health_result": {

                "health_score": health_result.get(
                    "health_score"
                ),

                "health_status": health_result.get(
                    "health_status"
                ),

                "severity_counts": health_result.get(
                    "severity_counts",
                    {}
                ),

                "penalties": health_result.get(
                    "penalties",
                    {}
                ),

                "metrics": health_result.get(
                    "metrics",
                    {}
                )
            }
        }

        # ============================================================
        # OLLAMA PROMPT
        # ============================================================

        prompt = f"""
You are a professional Website Health Analysis Agent.

Your job is to analyze VERIFIED website scan results
collected by a Python website monitoring system.

The Python scanner has already checked the website.

The Python Severity Engine has already calculated the
official health score and health status.

You are NOT responsible for calculating the health score.

Your job is ONLY to:

- understand the verified scan results
- explain important problems
- explain their severity
- explain possible causes
- recommend practical fixes
- provide an overall assessment

IMPORTANT HEALTH SCORE RULE:

The health score and health status provided inside
"health_result" are the OFFICIAL values.

You MUST use those exact values.

DO NOT calculate another health score.

DO NOT change the health score.

DO NOT change the health status.

STRICT RULES:

1. Only use information present in the scan data.
2. Never invent URLs.
3. Never invent HTTP status codes.
4. Never invent errors.
5. Never write JavaScript code.
6. Never write Python code.
7. Do not explain how JSON works.
8. Do not say "the provided JSON".
9. Do not repeat the complete input data.
10. Do not give generic programming tutorials.
11. If there are no issues in a category, write
    "None detected".
12. Possible causes must clearly be described as
    possible causes.
13. Keep the report professional.
14. Keep the report easy to understand.
15. Use the exact numbers from the verified scan.
16. Do not create fake examples.
17. Do not claim that a possible cause is confirmed.
18. Do not modify the verified health score.

Use this EXACT report structure:

WEBSITE HEALTH REPORT
=====================

Website:
<website>

Pages Checked:
<number>

OVERALL HEALTH
--------------
<2-4 sentence assessment based only on verified data>

HEALTH SCORE
------------
<EXACT health_score from health_result>/100

HEALTH STATUS
-------------
<EXACT health_status from health_result>

CRITICAL ISSUES
---------------
<List confirmed critical issues>

HIGH SEVERITY ISSUES
--------------------
<List confirmed high severity issues>

MEDIUM SEVERITY ISSUES
----------------------
<List confirmed medium severity issues>

LOW SEVERITY ISSUES
-------------------
<List confirmed low severity issues>

BROKEN RESOURCES
----------------

Broken Links:
<number>
<List only important confirmed examples>

Broken Images:
<number>
<List only important confirmed examples>

Broken CSS:
<number>
<List only important confirmed examples>

Broken JavaScript:
<number>
<List only important confirmed examples>

FAILED PAGES
------------
<number>
<List important failed pages>

IMPORTANT FINDINGS
------------------
<List the most important confirmed findings>

LIKELY CAUSES
-------------
<List possible technical causes>

Clearly label these as possible causes.
Do not present possible causes as confirmed facts.

RECOMMENDED FIXES
-----------------
1. <practical recommendation>
2. <practical recommendation>
3. <practical recommendation>

PRIORITY ACTION
---------------
<State what should be fixed first based on severity>

FINAL SUMMARY
-------------
<3-5 sentence professional conclusion>

Remember:

The health score is calculated by Python.

Use the EXACT health score and status provided by
health_result.

Do not calculate your own score.

VERIFIED SCAN DATA
==================

{json.dumps(data, indent=2)}
"""

        # ============================================================
        # SEND TO OLLAMA
        # ============================================================

        print(
            "\n🤖 Ollama is analyzing the website..."
        )

        response = ollama.chat(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional "
                        "website health analysis agent. "
                        "Analyze only verified scan data. "
                        "Never invent technical facts. "
                        "Use the exact health score "
                        "provided by the Python "
                        "Severity Engine."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            options={
                "temperature": 0.2
            }
        )

        # ============================================================
        # RETURN REPORT
        # ============================================================

        return response[
            "message"
        ][
            "content"
        ]