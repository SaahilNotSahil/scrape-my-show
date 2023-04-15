from selenium.webdriver.common.by import By

from utils.date import get_current_year, greater_than_today
from utils.utils import BaseScraper, exclude


class Insider(BaseScraper):
    def __init__(self, url):
        super(Insider, self).__init__(url,
                                      "Trek, trekking, Online, Comedy, Kids, Bollywood, Pool Party, Salsa, Bachata, Bhangra, Dj, Open mic, Improv, Networking, Rooftop party, Gokarna, Summer camp, Techno, jokes".lower().split(", "))

    def get_events(self):
        self.num_events = int(self.driver.execute_script(
            "return document.getElementsByClassName(\"css-12d1bye\")[0].innerText")[1:-1])

        count = 0
        events = []

        while count < self.num_events:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            events = self.driver.find_elements(
                by=By.XPATH, value="//li[@class='card-list-item']")
            count = len(events)

        assert count == self.num_events

        for event in events:
            anchor = event.find_element(by=By.TAG_NAME, value="a")
            link = anchor.get_attribute("href")

            event_details = event.text.split("\n")
            event_date = event_details[3].split(
                " | ")[0] + f" {get_current_year()}"

            if not greater_than_today(event_date):
                continue
            
            if exclude(" ".join(event_details), self.exclude_words):
                print("Excluding event: ", event_details[2])
                continue

            e = {
                "name": event_details[2],
                "date": event_date,
                "link": link
            }

            if e not in self.events:
                self.events.append(e)

        self.num_events = len(self.events)
        print(f"Found {self.num_events} offline events in Bengaluru")
