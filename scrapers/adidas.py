from time import sleep

from selenium.webdriver.common.by import By

from utils.date import get_current_year, greater_than_today
from utils.utils import BaseScraper


class AdidasRunners(BaseScraper):
    def __init__(self, url):
        super(AdidasRunners, self).__init__(url, [])

    def get_events(self):
        sleep(5)

        anchors = self.driver.find_elements(
            by=By.XPATH, value="//a[@class=\"button event-card-1Qm2Tuk event-23RVlnk\"]")

        sleep(5)

        for anchor in anchors:
            event_link = anchor.get_attribute("href")

            h3 = anchor.find_element(by=By.TAG_NAME, value="h3")
            paras = anchor.find_elements(by=By.TAG_NAME, value="p")
            event_name = h3.text + f" - {paras[1].text}"

            event_date = paras[0].text.split(
                ", ")[0] + f" {get_current_year()}"

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
