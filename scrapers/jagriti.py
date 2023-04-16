from selenium.webdriver.common.by import By

from utils import BaseScraper, greater_than_today


class JagritiTheatre(BaseScraper):
    def __init__(self, url):
        super(JagritiTheatre, self).__init__(url, [])

    def get_events(self):
        while 1:
            next_button = self.driver.find_elements(
                by=By.CSS_SELECTOR, value="a.next")
            divs = self.driver.find_elements(
                by=By.CLASS_NAME, value="evtabrow")

            for div in divs:
                date = div.find_element(
                    by=By.CLASS_NAME, value="evtabdat").text

                anchor = div.find_element(by=By.CLASS_NAME, value="tevtit").find_element(
                    by=By.TAG_NAME, value="a")

                event_link = anchor.get_attribute("href")
                event_name = anchor.text

                event_date = date.split("-")
                event_date = ' '.join(
                    [event_date[0], event_date[1], event_date[2]])
                
                if not greater_than_today(event_date):
                    continue

                e = {
                    "name": event_name,
                    "date": event_date,
                    "link": event_link
                }

                if e not in self.events:
                    self.events.append(e)

            if len(next_button) == 0:
                break

            self.driver.get(next_button[0].get_attribute("href"))

        self.num_events = len(self.events)

        print(f"Found {self.num_events} offline events in Bengaluru")
