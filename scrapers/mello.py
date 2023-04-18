from utils import BaseScraper, exclude, get_current_year, greater_than_today


class Mello(BaseScraper):
    def __init__(self, url):
        super(Mello, self).__init__(url,
                                    "Trek, trekking, Online, Comedy, Kids, Bollywood, Pool Party, Salsa, Bachata, Bhangra, Dj, Open mic, Improv, Networking, Rooftop party, Gokarna, Summer camp, Techno, jokes".lower().split(", "))

    def get_events(self):
        groups = self.driver.execute_script(
            "return document.getElementsByClassName(\"home-widget listify_widget_recent_listings\");")

        for group in groups:
            num_events = len(self.driver.execute_script(
                "return arguments[0].getElementsByClassName(\"job_listing type-job_listing\");", group))

            for i in range(num_events):
                event = self.driver.execute_script(
                    f"return arguments[0].getElementsByClassName(\"job_listing type-job_listing\")[{i}];", group)
                event_details = self.driver.execute_script(
                    f"return arguments[0].getElementsByClassName(\"job_listing type-job_listing\")[{i}].innerText;", group).split("\n")

                event_name = event_details[0]

                if exclude(" ".join(event_details), self.exclude_words):
                    continue

                if len(event_details[-2].split()) >= 2:
                    event_date = ' '.join(
                        [event_details[-2].split()[0], event_details[-2].split()[1]])
                else:
                    event_date = ' '.join(
                        [event_details[-3].split()[0], event_details[-3].split()[1]])

                event_link = self.driver.execute_script(
                    "return arguments[0].getElementsByTagName(\"a\")[0].href;", event)

                event_date = event_date + f" {get_current_year()}"

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
