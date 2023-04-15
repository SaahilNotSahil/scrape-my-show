from time import sleep

from selenium.webdriver.common.by import By

from utils.date import get_current_year, greater_than_today
from utils.utils import BaseScraper


class BMS2(BaseScraper):
    def __init__(self, url):
        super(BMS2, self).__init__(url, [])

    def get_events(self):
        current_count = 0
        last_count = 0
        second_last_count = 0

        events = []

        # city = self.driver.find_elements(
        #     by=By.CLASS_NAME, value="styles__PopularCityWrapper-ttnkwg-18.jupogi")[2]
        # city.click()

        while 1:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            sleep(2)
            events = self.driver.find_elements(
                by=By.CLASS_NAME, value="df-bv.df-bw.df-bx.df-by.df-bz.df-ca")

            second_last_count = last_count
            last_count = current_count
            current_count = len(events)

            if current_count == last_count == second_last_count:
                break

        self.num_events = current_count

        print(self.num_events)

        for event in events:
            date = event.find_element(
                by=By.CLASS_NAME, value="df-bd.df-bi.df-cp.df-e.df-y").text
            if not date:
                continue

            event_date = ' '.join([date.split("\n")[0], date.split("\n")[
                                  1]]) + f" {get_current_year()}"

            if not greater_than_today(event_date):
                continue

            anchor = event.find_element(by=By.TAG_NAME, value="a")
            event_link = anchor.get_attribute("href")

            div = event.find_element(
                by=By.CLASS_NAME, value="df-bd.df-bi.df-ct.df-e").find_elements(by=By.TAG_NAME, value="div")[0]
            event_name = div.text

            if not event_name:
                continue

            e = {
                "name": event_name,
                "date": event_date,
                "link": event_link
            }

            print(e)

            if e not in self.events:
                self.events.append(e)

        self.num_events = len(self.events)
        print(f"Found {self.num_events} offline events in Bengaluru")
