class SeverityEngine:

    def calculate(self, summary):

        failed_pages = len(
            summary.get("failed_pages", [])
        )

        broken_links = len(
            summary.get("broken_links", [])
        )

        broken_images = len(
            summary.get("broken_images", [])
        )

        broken_css = len(
            summary.get("broken_css", [])
        )

        broken_scripts = len(
            summary.get("broken_scripts", [])
        )

        pages_checked = summary.get(
            "pages_checked",
            0
        )

        # -------------------------------------------------
        # START WITH PERFECT SCORE
        # -------------------------------------------------

        score = 100

        # -------------------------------------------------
        # PAGE FAILURE PENALTY
        # -------------------------------------------------

        page_penalty = min(
            failed_pages * 15,
            40
        )

        # -------------------------------------------------
        # LINK PENALTY
        # -------------------------------------------------

        link_penalty = min(
            broken_links * 0.20,
            25
        )

        # -------------------------------------------------
        # IMAGE PENALTY
        # -------------------------------------------------

        image_penalty = min(
            broken_images * 0.10,
            15
        )

        # -------------------------------------------------
        # CSS PENALTY
        # -------------------------------------------------

        css_penalty = min(
            broken_css * 0.20,
            10
        )

        # -------------------------------------------------
        # JAVASCRIPT PENALTY
        # -------------------------------------------------

        script_penalty = min(
            broken_scripts * 0.50,
            10
        )

        # -------------------------------------------------
        # TOTAL
        # -------------------------------------------------

        total_penalty = (
            page_penalty
            + link_penalty
            + image_penalty
            + css_penalty
            + script_penalty
        )

        score -= total_penalty

        # Keep score between 0 and 100
        score = max(
            0,
            min(
                100,
                round(score)
            )
        )

        # -------------------------------------------------
        # DETERMINE STATUS
        # -------------------------------------------------

        if score >= 90:

            status = "Excellent"

        elif score >= 75:

            status = "Good"

        elif score >= 50:

            status = "Needs Attention"

        elif score >= 25:

            status = "Poor"

        else:

            status = "Critical"

        # -------------------------------------------------
        # SEVERITY COUNTS
        # -------------------------------------------------

        critical = 0
        high = 0
        medium = 0
        low = 0

        # Failed pages
        if failed_pages > 0:
            critical += failed_pages

        # Broken links
        if broken_links >= 50:
            high += broken_links

        elif broken_links > 10:
            medium += broken_links

        elif broken_links > 0:
            low += broken_links

        # Broken images
        if broken_images >= 50:
            high += broken_images

        elif broken_images > 10:
            medium += broken_images

        elif broken_images > 0:
            low += broken_images

        # Broken CSS
        if broken_css >= 20:
            high += broken_css

        elif broken_css > 5:
            medium += broken_css

        elif broken_css > 0:
            low += broken_css

        # Broken JS
        if broken_scripts >= 10:
            high += broken_scripts

        elif broken_scripts > 0:
            medium += broken_scripts

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        return {

            "health_score": score,

            "health_status": status,

            "penalties": {
                "failed_pages": round(
                    page_penalty,
                    2
                ),

                "broken_links": round(
                    link_penalty,
                    2
                ),

                "broken_images": round(
                    image_penalty,
                    2
                ),

                "broken_css": round(
                    css_penalty,
                    2
                ),

                "broken_scripts": round(
                    script_penalty,
                    2
                )
            },

            "severity_counts": {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },

            "metrics": {
                "pages_checked": pages_checked,
                "failed_pages": failed_pages,
                "broken_links": broken_links,
                "broken_images": broken_images,
                "broken_css": broken_css,
                "broken_scripts": broken_scripts
            }
        }