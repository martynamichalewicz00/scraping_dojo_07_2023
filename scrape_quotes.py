import json
import time 

from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class ScrapeQuotes:
    PROXY = ''
    INPUT_URL='http://quotes.toscrape.com/js-delayed/'
    OUTPUT_FILE='output.jsonl'

    list_of_data = []
    options = webdriver.ChromeOptions() 
    options.add_argument(f"--proxy-server={PROXY}")
    options.headless = True 
    options.page_load_strategy = 'none' 
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 
    driver = Chrome(options=options, service=chrome_service) 
    driver.implicitly_wait(5)


    def __init__(self, proxy=None, input_url=None, output_file=None):
        if proxy is not None:
            ScrapeQuotes.PROXY = proxy
        if input_url is not None:
            ScrapeQuotes.INPUT_URL = input_url
        if output_file is not None:
            ScrapeQuotes.OUTPUT_FILE = output_file

    def find_quotes(self):
        self.driver.get(self.INPUT_URL)
        max_attempts = 5

        while True:
            quotes_per_page = []
            attempts = 0 
            while not quotes_per_page and attempts < max_attempts:
                time.sleep(5)
                quotes_per_page = self.driver.find_elements(By.CSS_SELECTOR, "div.quote")
                attempts += 1
            self.save_quote_from_page(quotes_per_page)
            try:
                next_element = self.driver.find_element(By.XPATH, '//a[text()="Next "]')
                next_element.click()
                continue
            except NoSuchElementException:
                break

    def get_tags(self, element):
        tags = []
        a_tags = element.find_element(By.CSS_SELECTOR, "div.tags").find_elements(By.CSS_SELECTOR, "a.tag")
        for a_tag in a_tags:
            tags.append(self.encode_text(a_tag.text))
        return tags

    def save_to_json_and_quit(self):
        with open(self.OUTPUT_FILE, "w") as json_file:
            json.dump(self.list_of_data, json_file, indent=2)
        self.driver.quit()

    def save_quote_from_page(self,quotes):
        for quote in quotes:
            self.list_of_data.append(
                {
                    "text" : self.encode_text(quote.find_element(By.CSS_SELECTOR, "span.text").text),
                    "by" : self.encode_text(quote.find_element(By.CSS_SELECTOR, "span small.author").text),
                    "tags" : self.get_tags(quote)
                }
            )
    
    @staticmethod
    def encode_text(text):
        return text.encode("ascii", "ignore").decode('utf-8')