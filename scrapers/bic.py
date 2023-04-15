from selenium.webdriver.common.by import By

from utils.date import greater_than_today
from utils.utils import BaseScraper


class BangaloreInternationCentre(BaseScraper):
    def __init__(self, url):
        super(BangaloreInternationCentre, self).__init__(url, [])

    def get_events(self):
        while 1:
            next_button = self.driver.find_elements(
                by=By.CLASS_NAME, value="button.button-override.hollow")
            divs = self.driver.find_elements(
                by=By.CLASS_NAME, value="large-4.medium-4.small-12.columns")

            divs = divs[:-1]

            for div in divs:
                anchor = div.find_element(
                    by=By.CLASS_NAME, value="tribe-event-url")

                event_link = anchor.get_attribute("href")
                event_name = anchor.text

                try:
                    date = div.find_element(
                        by=By.CLASS_NAME, value="tribe-event-dates")
                except:
                    date = div.find_element(
                        by=By.CLASS_NAME, value="event-meta-inner")

                event_date = date.text.split(", ")[1]
                event_date = ' '.join(
                    [event_date.split()[0], event_date.split()[1], event_date.split()[2]])

                if not greater_than_today(event_date):
                    continue

                e = {
                    "name": event_name,
                    "date": event_date,
                    "link": event_link
                }

                if e not in self.events:
                    self.events.append(e)

            if len(next_button) != 6:
                break

            self.driver.get(next_button[3].get_attribute("href"))

        self.num_events = len(self.events)

        print(f"Found {self.num_events} offline events in Bengaluru")
