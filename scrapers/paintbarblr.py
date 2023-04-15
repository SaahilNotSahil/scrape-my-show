from selenium.webdriver.common.by import By

from utils.date import get_current_year, greater_than_today, is_date
from utils.utils import BaseScraper


class PaintBarBlr(BaseScraper):
    def __init__(self, url):
        super(PaintBarBlr, self).__init__(url, [])

    def get_events(self):
        divs = self.driver.execute_script(
            "return document.getElementsByClassName(\"o-layout__item u-1/2 u-1/2@phab u-1/3@tab\")")

        for div in divs:
            div = div.find_element(
                by=By.CLASS_NAME, value="product-card__details")

            anchor = div.find_element(by=By.TAG_NAME, value="a")
            event_link = anchor.get_attribute("href")

            h2 = anchor.find_element(by=By.TAG_NAME, value="h2")

            if "|" not in h2.text:
                continue

            text = h2.text.split("|")

            if is_date(text[0]):
                event_name = text[1].strip()
                event_date = text[0].split(", ")[1]
            else:
                event_name = text[0].strip()
                event_date = text[1].split(", ")[1]

            event_date = event_date + f" {get_current_year()}"

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
