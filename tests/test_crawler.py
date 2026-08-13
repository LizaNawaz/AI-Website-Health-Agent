import os

from dotenv import load_dotenv

from app.crawler.website_crawler import WebsiteCrawler


load_dotenv()


def main():

    url = input(
        "Enter website URL: "
    ).strip()

    max_pages = int(
        os.getenv(
            "MAX_PAGES",
            "20"
        )
    )

    timeout = int(
        os.getenv(
            "REQUEST_TIMEOUT",
            "10"
        )
    )

    crawler = WebsiteCrawler(
        timeout=timeout,
        max_pages=max_pages
    )

    print("\nStarting crawler...")
    print(
        f"Maximum pages: {max_pages}"
    )

    pages = crawler.crawl(url)

    print("\n")
    print("=" * 60)
    print("CRAWL SUMMARY")
    print("=" * 60)

    print(
        "Pages discovered:",
        len(pages)
    )

    successful = 0
    failed = 0

    for page in pages:

        if page["success"]:

            successful += 1

            print(
                f"✓ {page['status_code']} "
                f"{page['url']}"
            )

        else:

            failed += 1

            print(
                f"❌ {page.get('status_code')} "
                f"{page['url']}"
            )

    print("\nSuccessful:", successful)
    print("Failed:", failed)


if __name__ == "__main__":
    main()