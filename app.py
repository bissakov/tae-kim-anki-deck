from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass, astuple, field

@dataclass()
class Card:
    word:       str
    jisho:      str
    reading:    str
    definition: str

    def __getitem__(self, i):
        return astuple(self)[i]

class Deck_Populator():
    def __init__(self):
        self.deck = []

    def __get_options(self):
        options = Options()
        options.headless = True
        options.add_argument('log-level=3')
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return options

    def __get_table(self):
        url = 'https://itazuraneko.neocities.org/grammar/taekim.html'
        options = self.__get_options()
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
            driver.get(url)
            return driver.execute_script('return document.querySelector("body > div.bodymargin > table:nth-child(3708)").innerHTML')

    def fill_deck(self):
        html = self.__get_table()
        soup = BeautifulSoup(html, 'html.parser')        
        for row in soup.find_all('tr'):
            tags = [col for col in row.find_all('td')]
            if len(tags) == 0: continue
            self.deck.append(Card(word=tags[0].text, jisho=tags[0].find('a')['href'], reading=tags[1].text, definition=tags[2].text))

    def get_deck(self):
        if not self.deck:
            self.fill_deck()
        return self.deck

def main():
    populator = Deck_Populator()
    populator.fill_deck()
    deck = populator.get_deck()
    print(len(deck))
            
if __name__ == '__main__':
    main()