import requests


class LinkChecker:

    def __init__(self, timeout=10):
        self.timeout = timeout

    def check(self, url):

        try:

            response = requests.get(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                headers={
                    "User-Agent": "AI-Website-Health-Agent/1.0"
                }
            )

            return {
                "url": url,
                "status_code": response.status_code,
                "final_url": response.url,
                "broken": response.status_code >= 400,
                "error": None
            }

        except requests.RequestException as e:

            return {
                "url": url,
                "status_code": None,
                "final_url": None,
                "broken": True,
                "error": str(e)
            }