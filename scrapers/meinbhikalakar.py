from time import sleep

from selenium.webdriver.common.by import By

from utils.date import get_current_year, greater_than_today
from utils.utils import BaseScraper


class MeinBhiKalakar(BaseScraper):
    def __init__(self, url):
        super(MeinBhiKalakar, self).__init__(url, [])

    def get_events(self):
        divs = self.driver.find_elements(
            by=By.CLASS_NAME, value="Fe2Svm.t6EnES.wixui-gallery__item")

        sleep(5)

        for div in divs:
            anchor = div.find_element(by=By.TAG_NAME, value="a")
            event_link = anchor.get_attribute("href")

            div = anchor.find_element(
                by=By.CLASS_NAME, value="iRSoQ8")

            text = div.text.split("|")

            event_date = text[0].strip() + f" {get_current_year()}"
            event_name = text[2].strip()

            if not greater_than_today(event_date):
                continue

            e = {
                "name": event_name,
                "date": event_date,
                "link": event_link
            }

            if e not in self.events:
                self.events.append(e)

        self.num_events = len(self.events)

        print(f"Found {self.num_events} offline events in Bengaluru")
