from utils import BaseScraper, greater_than_today, is_date


class MapIndia(BaseScraper):
    def __init__(self, url):
        super(MapIndia, self).__init__(url, [])

    def get_events(self):
        articles = self.driver.execute_script(
            "return document.getElementsByClassName(\"row ajax-result\")[0].getElementsByTagName(\"article\")")

        for article in articles:
            para = self.driver.execute_script(
                "return arguments[0].getElementsByClassName(\"card-text\")[0]", article)
            anchor = self.driver.execute_script(
                "return arguments[0].getElementsByTagName(\"a\")[0]", para)

            event_link = anchor.get_attribute("href")
            event_name = anchor.text
            date = self.driver.execute_script(
                "return arguments[0].getElementsByTagName(\"span\")[0]", para).text.split(", ")[0]

            if is_date(date):
                event_date = date
            else:
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
