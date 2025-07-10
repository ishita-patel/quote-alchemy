from playwright.sync_api import sync_playwright
from scraper.utils import save_json
import time

def scrape_quotes_and_bios(max_quotes=25):
    all_quotes = []
    visited_authors = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto("http://quotes.toscrape.com/", timeout=10000)
            time.sleep(2)

            while len(all_quotes) < max_quotes:
                quotes = page.locator(".quote").all()
                for quote in quotes:
                    if len(all_quotes) >= max_quotes:
                        break

                    try:
                        text = quote.locator(".text").inner_text().strip('“”')
                        author = quote.locator(".author").inner_text().strip()
                        tags = list(set(  # Dedupe tags
                            t.strip() for t in quote.locator(".tag").all_inner_texts()
                        ))

                        if not text or not author or not tags:
                            continue

                        # Get bio only of the author
                        bio = ""
                        if author not in visited_authors:
                            try:
                                author_url = quote.locator("span a").get_attribute("href")
                                author_page = browser.new_page()
                                author_page.goto(
                                    f"http://quotes.toscrape.com{author_url}",
                                    timeout=10000
                                )
                                bio = author_page.locator(".author-description").inner_text().strip()
                                author_page.close()
                                visited_authors.add(author)
                            except:
                                pass

                        all_quotes.append({
                            "text": text,
                            "author": author,
                            "tags": tags,
                            "author_bio": bio
                        })

                    except Exception as e:
                        print(f"Skipping malformed quote: {str(e)}")
                        continue

                # Pagination with timeout
                if len(all_quotes) < max_quotes:
                    try:
                        page.locator(".next > a").first.click(timeout=5000)
                        time.sleep(1)
                    except:
                        break

        finally:
            browser.close()
            save_json(all_quotes, "data/quotes.json")
            print(f"✔ Collected {len(all_quotes)} quotes ({len(visited_authors)} authors)")
