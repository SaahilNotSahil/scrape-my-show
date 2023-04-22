import json
import threading
from datetime import datetime, timedelta

from scrapers import *

f = open("urls.json", "r")
urls = json.load(f)
f.close()

scrapers = {
    "adidas": AdidasRunners,
    "bic": BangaloreInternationCentre,
    "bms2": BMS2,
    "bngbirds": BngBirds,
    "explocity": ExploCity,
    "insider": Insider,
    "imx": IndianMusicExperience,
    "jagriti": JagritiTheatre,
    "mapindia": MapIndia,
    "meinbhikalakar": MeinBhiKalakar,
    "mello": Mello,
    "paintbarblr": PaintBarBlr,
    "skillboxes": SkillBoxes,
    "sunsetcinema": SunsetCinemaClub,
    "twb": TheWhiteBox
}


def scrape(scraper):
    url = urls[scraper]

    if scraper == "bms":
        today = datetime.now().strftime('%Y%m%d')
        last_day = datetime.now().replace(day=28) + timedelta(days=4)
        last_day = last_day.replace(day=1) - timedelta(days=1)
        last_day = last_day.strftime('%Y%m%d')
        url += today + "-" + last_day

    s = scrapers[scraper](url).open()
    s.get_events()
    s.close_driver()
    s.save_csv(scraper)


def start_scraper():
    for scraper in scrapers:
        print(f"Scraping {scraper} ...")
        thread = threading.Thread(target=scrape, args=(scraper,), name=scraper)
        thread.start()


if __name__ == "__main__":
    start_scraper()
