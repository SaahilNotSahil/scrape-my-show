from selenium.webdriver.common.by import By

from utils import BaseScraper, get_current_year, greater_than_today


class SunsetCinemaClub(BaseScraper):
    def __init__(self, url):
        super(SunsetCinemaClub, self).__init__(url, [])

    def get_events(self):
        divs = self.driver.find_elements(
            by=By.CLASS_NAME, value="image-tile.outer-title.mt8")

        for div in divs:
            anchor = div.find_element(by=By.TAG_NAME, value="a")
            event_link = anchor.get_attribute("href")

            div = anchor.find_element(by=By.CLASS_NAME, value="title.mb16")
            h4 = div.find_element(by=By.TAG_NAME, value="h4")
            event_name = h4.text

            event_date = div.find_element(by=By.TAG_NAME, value="span").text
            event_date += f" {get_current_year()}"

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
