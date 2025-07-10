from scraper.playwright_scraper import scrape_quotes_and_bios
from summarizer.tagwise_summary import summarize_by_tag
from scraper.utils import load_json
import traceback

def main():
    try:
        print("=== QUOTE ANALYSIS SYSTEM ===")
        print("[1/3] Scraping quotes...")
        scrape_quotes_and_bios(max_quotes=25)
        
        print("\n[2/3] Loading data...")
        quotes = load_json("data/quotes.json")
        if not quotes:
            raise ValueError("No quotes found in the data file")
            
        print("[3/3] Generating summary...")
        summary = summarize_by_tag(quotes, page_num=1)
        
        print("\n=== FINAL SUMMARY ===")
        print(summary)
        
    except Exception as e:
        print(f"\n⚠ ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
