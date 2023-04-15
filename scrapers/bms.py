from time import sleep

from selenium.webdriver.common.by import By

from utils.date import get_current_year, greater_than_today, get_date
from utils.utils import BaseScraper


class BMS(BaseScraper):
    def __init__(self, url):
        super(BMS, self).__init__(url,
                                  "Trek, trekking, Online, Comedy, Kids, Bollywood, Pool Party, Salsa, Bachata, Bhangra, Dj, Open mic, Improv, Networking, Rooftop party, Gokarna, Summer camp, Techno, jokes, Circus, Watch on Zoom, Web designing, Digital marketing, unluclass".lower().split(", "))

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

        print(self.num_events)

        for event in events:
            event_link = event.get_attribute("href")
            print(event_link)

            event_name = event.find_element(
                by=By.CLASS_NAME, value="sc-7o7nez-0.cBsijw").text

            print(event_name)

            event_date = get_date(
                event_link, "return document.getElementsByClassName(\"df-av df-ay df-az df-ba df-bb\")[1].innerText")
            print(event_date)

            print()
        #     date = event.find_element(
        #         by=By.CLASS_NAME, value="df-bd.df-bi.df-cp.df-e.df-y").text
        #     if not date:
        #         continue

        #     event_date = ' '.join([date.split("\n")[0], date.split("\n")[
        #                           1]]) + f" {get_current_year()}"

        #     if not greater_than_today(event_date):
        #         continue

        #     anchor = event.find_element(by=By.TAG_NAME, value="a")
        #     event_link = anchor.get_attribute("href")

        #     div = event.find_element(
        #         by=By.CLASS_NAME, value="df-bd.df-bi.df-ct.df-e").find_elements(by=By.TAG_NAME, value="div")[0]
        #     event_name = div.text

        #     if not event_name:
        #         continue

        #     e = {
        #         "name": event_name,
        #         "date": event_date,
        #         "link": event_link
        #     }

        #     print(e)

        #     if e not in self.events:
        #         self.events.append(e)

        self.num_events = len(self.events)
        print(f"Found {self.num_events} offline events in Bengaluru")
