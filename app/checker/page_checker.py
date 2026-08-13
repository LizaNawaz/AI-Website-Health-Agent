from app.checker.link_checker import LinkChecker
from app.checker.image_checker import ImageChecker
from app.checker.resource_checker import ResourceChecker


class PageChecker:

    def __init__(self, timeout=10):

        self.link_checker = LinkChecker(timeout)
        self.image_checker = ImageChecker(timeout)
        self.resource_checker = ResourceChecker(timeout)

    def check_page(self, page_data):

        results = {
            "links": [],
            "images": [],
            "stylesheets": [],
            "scripts": []
        }

        # -------------------------
        # CHECK LINKS
        # -------------------------

        for link in page_data["links"]:

            result = self.link_checker.check(
                link["url"]
            )

            result["text"] = link["text"]

            results["links"].append(result)

        # -------------------------
        # CHECK IMAGES
        # -------------------------

        for image in page_data["images"]:

            result = self.image_checker.check(
                image["url"]
            )

            result["alt"] = image["alt"]

            results["images"].append(result)

        # -------------------------
        # CHECK CSS
        # -------------------------

        for stylesheet in page_data["stylesheets"]:

            result = self.resource_checker.check(
                stylesheet
            )

            results["stylesheets"].append(result)

        # -------------------------
        # CHECK JAVASCRIPT
        # -------------------------

        for script in page_data["scripts"]:

            result = self.resource_checker.check(
                script
            )

            results["scripts"].append(result)

        return results