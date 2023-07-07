import os
from dotenv import load_dotenv
from scrape_quotes import ScrapeQuotes


if __name__ == '__main__':
    load_dotenv()
    PROXY = os.getenv("PROXY")
    INPUT_URL = os.getenv("INPUT_URL")
    OUTPUT_FILE = os.getenv("OUTPUT_FILE")

    scrape = ScrapeQuotes(PROXY, INPUT_URL, OUTPUT_FILE)
    scrape.find_quotes()
    scrape.save_to_json_and_quit()