import os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseScraper:
    def __init__(self, url, exclude_words, headless=True) -> None:
        self.options = Options()
        self.options.add_argument("start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-browser-side-navigation")
        self.options.add_argument(
            "--disable-blink-features=AutomationControlled")

        if headless:
            self.options.add_argument("--headless")

        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        self.driver = webdriver.Chrome(
            options=self.options, executable_path="./chromedriver")

        self.events = []

        self.url = url
        self.exclude_words = exclude_words

        self.num_events = 0

    def open(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(15)

        return self

    def get_events(self):
        pass

    def create_df(self):
        df = pd.DataFrame(self.events)
        return df

    def save_csv(self, name):
        df = self.create_df()
        print(f"Saving {self.num_events} events to ./data/{name}.csv ...")

        if os.path.exists("data"):
            pass
        else:
            os.mkdir("data")

        if df.empty:
            df = generate_blank_df()

        df.to_csv(f"./data/{name}.csv", index=False, header=True)
        print(f"Saved {self.num_events} events to ./data/{name}.csv")

    def close_driver(self):
        self.driver.close()


def exclude(text, exclude_words):
    for word in exclude_words:
        if word in text.lower():
            return True

    return False


def generate_blank_df():
    df = pd.DataFrame(columns=["name", "date", "link"])
    return df
