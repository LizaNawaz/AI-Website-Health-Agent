import requests


class ImageChecker:

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

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            is_image = content_type.startswith("image/")

            return {
                "url": url,
                "status_code": response.status_code,
                "content_type": content_type,
                "broken": (
                    response.status_code >= 400
                    or not is_image
                ),
                "error": None
            }

        except requests.RequestException as e:

            return {
                "url": url,
                "status_code": None,
                "content_type": None,
                "broken": True,
                "error": str(e)
            }