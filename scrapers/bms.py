from time import sleep

from selenium.webdriver.common.by import By

from utils import (BaseScraper, date_regex_bms, exclude, get_date,
                   greater_than_today)


class BMS(BaseScraper):
    def __init__(self, url):
        super(BMS, self).__init__(url,
                                  "Trek, trekking, Online, Comedy, Kids, Bollywood, Pool Party, Salsa, Bachata, Bhangra, Dj, Open mic, Improv, Networking, Rooftop party, Gokarna, Summer camp, Techno, jokes, Circus, Watch on Zoom, Web designing, Digital marketing, unluclass".lower().split(", "), False)

    def get_events(self):
        current_count = 0
        last_count = 0
        second_last_count = 0

        events = []

        while 1:
            self.driver.execute_script(
                "document.getElementsByClassName(\"sc-eNQAEJ sc-cvbbAY gEQXQu\")[0].scrollIntoView({ block: 'end' });")

            sleep(5)

            events = self.driver.find_elements(
                by=By.CLASS_NAME, value="sc-133848s-11.sc-1ljcxl3-1.eQiiBj")

            second_last_count = last_count
            last_count = current_count
            current_count = len(events)

            if current_count == last_count == second_last_count:
                break

        self.num_events = current_count

        for event in events:
            event_link = event.get_attribute("href")

            event_name = event.find_element(
                by=By.CLASS_NAME, value="sc-7o7nez-0.cBsijw").text

            event_data = get_date(
                event_link, "return document.getElementById(\"app\").innerText")

            if exclude(event_data, self.exclude_words):
                continue

            event_date = date_regex_bms(event_data)

            if event_date is None:
                continue

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
