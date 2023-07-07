import json
import time 
 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager


class Parser:
    def __init__(self, input, output):
        self.input = input
        self.output = output

class ScrapeQuotes(Parser):
    INPUT_URL='http://quotes.toscrape.com/js-delayed/'
    OUTPUT_FILE='output.jsonl'

    list_of_data = []
    options = webdriver.ChromeOptions() 
    options.headless = True 
    options.page_load_strategy = 'none' 
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 
    driver = Chrome(options=options, service=chrome_service) 
    driver.implicitly_wait(5)

    def __init__(self):
        super().__init__(ScrapeQuotes.INPUT_URL, ScrapeQuotes.OUTPUT_FILE)
    
    def find_quotes(self):
        quotes = self.wait_for_elements(self.driver, self.INPUT_URL)
        for quote in quotes:
            self.list_of_data.append(
                {
                    "text" : self.encode_text(quote.find_element(By.CSS_SELECTOR, "span.text").text),
                    "by" : self.encode_text(quote.find_element(By.CSS_SELECTOR, "span small.author").text),
                    "tags" : self.get_tags(quote)
                }
            )
    def get_tags(self, element):
        tags = []
        a_tags = element.find_element(By.CSS_SELECTOR, "div.tags").find_elements(By.CSS_SELECTOR, "a.tag")
        for a_tag in a_tags:
            tags.append(self.encode_text(a_tag.text))
        return tags

    def save_to_json_and_quit(self):
        with open(self.OUTPUT_FILE, "w") as json_file:
            json.dump(self.list_of_data, json_file, indent=4)
        self.driver.quit()

    @staticmethod
    def wait_for_elements(driver, url):
        all_quotes = []
        driver.get(url)
        while not all_quotes:
            time.sleep(5)
            all_quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
        return all_quotes
    
    @staticmethod
    def encode_text(text):
        return text.encode("ascii", "ignore").decode('utf-8')