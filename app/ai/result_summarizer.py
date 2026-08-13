class ResultSummarizer:

    def summarize(self, website_results):

        summary = {
            "website": website_results["website"],
            "pages_checked": website_results["pages_checked"],
            "failed_pages": [],
            "broken_links": [],
            "broken_images": [],
            "broken_css": [],
            "broken_scripts": []
        }

        for page in website_results["pages"]:

            page_url = page["page_url"]

            # Failed pages
            if page.get("page_failed"):

                summary["failed_pages"].append({
                    "page": page_url,
                    "status": page.get("page_status"),
                    "error": page.get("error")
                })

            # Broken links
            for item in page.get("links", []):

                if item.get("broken"):

                    summary["broken_links"].append({
                        "page": page_url,
                        "url": item.get("url"),
                        "status": item.get("status_code"),
                        "error": item.get("error")
                    })

            # Broken images
            for item in page.get("images", []):

                if item.get("broken"):

                    summary["broken_images"].append({
                        "page": page_url,
                        "url": item.get("url"),
                        "status": item.get("status_code"),
                        "error": item.get("error")
                    })

            # Broken CSS
            for item in page.get("stylesheets", []):

                if item.get("broken"):

                    summary["broken_css"].append({
                        "page": page_url,
                        "url": item.get("url"),
                        "status": item.get("status_code"),
                        "error": item.get("error")
                    })

            # Broken JavaScript
            for item in page.get("scripts", []):

                if item.get("broken"):

                    summary["broken_scripts"].append({
                        "page": page_url,
                        "url": item.get("url"),
                        "status": item.get("status_code"),
                        "error": item.get("error")
                    })

        return summary