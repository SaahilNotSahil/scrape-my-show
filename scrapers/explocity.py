from selenium.webdriver.common.by import By

from utils.date import get_current_year, greater_than_today
from utils.utils import BaseScraper


class ExploCity(BaseScraper):
    def __init__(self, url):
        super(ExploCity, self).__init__(url, [])

    def get_events(self):
        while 1:
            next_button = self.driver.find_element(
                by=By.CLASS_NAME, value="step-links").find_elements(by=By.TAG_NAME, value="a")
            divs = self.driver.find_elements(
                by=By.CLASS_NAME, value="row.news-row")

            for div in divs:
                div = div.find_element(by=By.CLASS_NAME, value="col-xl-6")
                ds = div.find_elements(by=By.TAG_NAME, value="div")

                date = ds[1].text
                anchor = ds[2].find_elements(by=By.TAG_NAME, value="a")[0]

                event_link = anchor.get_attribute("href")
                event_name = anchor.find_element(
                    by=By.TAG_NAME, value="p").text

                event_date = date.split(" -")[0] + f" {get_current_year()}"

                if not greater_than_today(event_date):
                    continue

                e = {
                    "name": event_name,
                    "date": event_date,
                    "link": event_link
                }

                if e not in self.events:
                    self.events.append(e)

            if len(next_button) == 4:
                self.driver.get(next_button[2].get_attribute("href"))
            elif len(next_button) == 2:
                if "next" in next_button[0].text.lower():
                    self.driver.get(next_button[0].get_attribute("href"))
                else:
                    break

        self.num_events = len(self.events)

        print(f"Found {self.num_events} offline events in Bengaluru")
