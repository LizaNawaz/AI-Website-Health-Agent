from bs4 import BeautifulSoup
from urllib.parse import urljoin


class PageParser:

    def parse(self, html, base_url):

        soup = BeautifulSoup(html, "html.parser")

        links = []
        images = []
        stylesheets = []
        scripts = []

        # -------------------------
        # LINKS
        # -------------------------
        for tag in soup.find_all("a", href=True):

            url = urljoin(base_url, tag["href"])

            links.append({
                "url": url,
                "text": tag.get_text(strip=True)
            })

        # -------------------------
        # IMAGES
        # -------------------------
        for tag in soup.find_all("img", src=True):

            url = urljoin(base_url, tag["src"])

            images.append({
                "url": url,
                "alt": tag.get("alt", "")
            })

        # -------------------------
        # CSS
        # -------------------------
        for tag in soup.find_all("link", href=True):

            rel = tag.get("rel", [])

            if "stylesheet" in rel:

                url = urljoin(base_url, tag["href"])

                stylesheets.append(url)

        # -------------------------
        # JAVASCRIPT
        # -------------------------
        for tag in soup.find_all("script", src=True):

            url = urljoin(base_url, tag["src"])

            scripts.append(url)

        return {
            "links": links,
            "images": images,
            "stylesheets": stylesheets,
            "scripts": scripts
        }