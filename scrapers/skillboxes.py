from time import sleep

from selenium.webdriver.common.by import By

from utils.date import greater_than_today, is_date
from utils.utils import BaseScraper, exclude


class SkillBoxes(BaseScraper):
    def __init__(self, url):
        super(SkillBoxes, self).__init__(
            url, "Comedy, Online".lower().split(", "))

    def get_events(self):
        current_count = 0
        last_count = 0
        second_last_count = 0

        events = []

        while 1:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            sleep(2)
            events = self.driver.find_elements(
                by=By.CLASS_NAME, value="event-result-box")

            second_last_count = last_count
            last_count = current_count
            current_count = len(events)

            if current_count == last_count == second_last_count:
                break

        self.num_events = current_count

        for event in events:
            div = event.find_element(by=By.CLASS_NAME, value="result_text2")
            h2 = div.find_element(by=By.TAG_NAME, value="h2")
            anchor = h2.find_element(by=By.TAG_NAME, value="a")
            link = anchor.get_attribute("href")
            event_name = anchor.text
            para = div.find_elements(by=By.TAG_NAME, value="p")[1]

            if exclude(event.text, self.exclude_words):
                print("Excluding event: ", event_name)
                continue

            event_date = para.text.split(" | ")[0].split(" - ")[0]
            if len(para.text.split(" | ")[0].split(" - ")) == 2:
                event_date += f" {para.text.split(' | ')[0].split(' - ')[1].split()[2]}"

            if len(event_date.split()) > 3:
                event_date = event_date.split(", ")[0].split()[
                    0] + f" {event_date.split(', ')[0].split()[3]}" + f" {event_date.split(', ')[1]}"

            if is_date(event_date):
                if not greater_than_today(event_date):
                    continue
            else:
                continue

            e = {
                "name": event_name,
                "date": event_date,
                "link": link
            }

            if e not in self.events:
                self.events.append(e)

        self.num_events = len(self.events)
        print(f"Found {self.num_events} offline events in Bengaluru")
