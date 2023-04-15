from selenium.webdriver.common.by import By

from utils.date import get_current_year, get_date, greater_than_today, is_date
from utils.utils import BaseScraper


class TheWhiteBox(BaseScraper):
    def __init__(self, url):
        super(TheWhiteBox, self).__init__(url, [])

    def get_events(self):
        divs = self.driver.find_elements(
            by=By.CLASS_NAME, value="grid-product__content")

        for div in divs:
            anchor = div.find_element(by=By.TAG_NAME, value="a")
            event_link = anchor.get_attribute("href")

            div = anchor.find_elements(
                by=By.CLASS_NAME, value="grid-product__meta")[0]
            event_name = div.find_elements(by=By.TAG_NAME, value="div")[0].text

            data = get_date(
                event_link, 'return document.getElementsByClassName(\"product-single__description rte\")[0].innerText')
            data = data.split("\n")

            for d in data:
                if "Date" in d:
                    event_date = d.split(":")[1].strip()
                    break
            else:
                continue

            event_date = event_date.split(", ")[1]
            event_date = event_date.split(" | ")[0]
            event_date = event_date + " " + str(get_current_year())

            print(event_date)

            if is_date(event_date):
                if not greater_than_today(event_date):
                    continue
            else:
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
