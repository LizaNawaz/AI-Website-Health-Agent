import requests
from urllib.parse import urljoin, urlparse


class WebsiteCrawler:

    def __init__(self, timeout=10, max_pages=20):

        self.timeout = timeout
        self.max_pages = max_pages

        self.visited = set()
        self.to_visit = []

    # --------------------------------------------------
    # FETCH A PAGE
    # --------------------------------------------------

    def fetch_page(self, url):

        try:

            response = requests.get(
                url,
                timeout=self.timeout,
                headers={
                    "User-Agent": "AI-Website-Health-Agent/1.0"
                }
            )

            return {
                "url": url,
                "status_code": response.status_code,
                "success": response.ok,
                "html": response.text,
                "content_type": response.headers.get(
                    "Content-Type",
                    ""
                )
            }

        except requests.RequestException as e:

            return {
                "url": url,
                "status_code": None,
                "success": False,
                "html": "",
                "content_type": "",
                "error": str(e)
            }

    # --------------------------------------------------
    # NORMALIZE URL
    # --------------------------------------------------

    def normalize_url(self, base_url, link):

        return urljoin(base_url, link)

    # --------------------------------------------------
    # CHECK INTERNAL URL
    # --------------------------------------------------

    def is_internal_url(self, base_url, url):

        base_domain = urlparse(base_url).netloc
        target_domain = urlparse(url).netloc

        return base_domain == target_domain

    # --------------------------------------------------
    # CLEAN URL
    # --------------------------------------------------

    def clean_url(self, url):

        parsed = urlparse(url)

        # Remove fragment (#section)
        cleaned = parsed._replace(
            fragment=""
        ).geturl()

        return cleaned.rstrip("/")

    # --------------------------------------------------
    # FIND INTERNAL LINKS
    # --------------------------------------------------

    def extract_internal_links(self, base_url, html):

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        links = set()

        for tag in soup.find_all(
            "a",
            href=True
        ):

            href = tag.get("href")

            # Ignore empty links
            if not href:
                continue

            # Ignore special links
            if href.startswith(
                (
                    "mailto:",
                    "tel:",
                    "javascript:",
                    "#"
                )
            ):
                continue

            absolute_url = self.normalize_url(
                base_url,
                href
            )

            # Only crawl same website
            if self.is_internal_url(
                base_url,
                absolute_url
            ):

                absolute_url = self.clean_url(
                    absolute_url
                )

                links.add(
                    absolute_url
                )

        return links

    # --------------------------------------------------
    # CRAWL WEBSITE
    # --------------------------------------------------

    def crawl(self, start_url):

        start_url = self.clean_url(start_url)

        self.to_visit = [start_url]
        self.visited = set()

        pages = []

        while self.to_visit:

            # Stop at maximum page limit
            if len(self.visited) >= self.max_pages:
                break

            current_url = self.to_visit.pop(0)

            if current_url in self.visited:
                continue

            print(
                f"\nCrawling [{len(self.visited) + 1}/{self.max_pages}]: "
                f"{current_url}"
            )

            self.visited.add(current_url)

            page = self.fetch_page(
                current_url
            )

            pages.append(page)

            # If page failed, don't try to extract links
            if not page["success"]:
                continue

            # Find internal pages
            internal_links = self.extract_internal_links(
                current_url,
                page["html"]
            )

            # Add new pages to queue
            for link in internal_links:

                if link not in self.visited:

                    if link not in self.to_visit:

                        self.to_visit.append(link)

        return pages