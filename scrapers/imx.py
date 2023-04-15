from selenium.webdriver.common.by import By

from utils.date import greater_than_today
from utils.utils import BaseScraper


class IndianMusicExperience(BaseScraper):
    def __init__(self, url):
        super(IndianMusicExperience, self).__init__(url, [])

    def get_events(self):
        upcoming = self.driver.find_element(
            by=By.CLASS_NAME, value="et_pb_row.et_pb_row_1")

        divs = upcoming.find_elements(
            by=By.CLASS_NAME, value="mec-timeline-event.clearfix ")

        for div in divs:
            event_date = div.find_element(
                by=By.CLASS_NAME, value="mec-timeline-event-date.mec-color").text

            anchor = div.find_element(by=By.CLASS_NAME, value="mec-timeline-event-content").find_element(by=By.CLASS_NAME, value="clearfix").find_element(
                by=By.CLASS_NAME, value="mec-timeline-left-content").find_element(by=By.XPATH, value="//div/h4/a")
            
            event_link = anchor.get_attribute("href")
            event_name = anchor.text

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
