from selenium.webdriver.common.by import By

from utils import BaseScraper, greater_than_today


class BngBirds(BaseScraper):
    def __init__(self, url):
        super(BngBirds, self).__init__(url, [])

    def get_events(self):
        divs = self.driver.execute_script(
            "return document.getElementsByClassName(\"dp_pec_content\")[0].getElementsByTagName(\"div\")[1].querySelectorAll(\"div.dp_pec_isotope\")")

        dates = []
        data = []

        for div in divs:
            if "dp_pec_date_block_wrap" in div.get_attribute("class"):
                dates.append(div)
            else:
                data.append(div)

        for divs in zip(dates, data):
            event_date = divs[0].find_element(
                by=By.CLASS_NAME, value="dp_pec_date_block").text

            h2 = divs[1].find_element(by=By.TAG_NAME, value="h2")
            anchor = h2.find_element(by=By.TAG_NAME, value="a")

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
