import json
import threading
from time import sleep

from scrapers import *

f = open("urls.json", "r")
urls = json.load(f)
f.close()

scrapers = {
    "adidas": AdidasRunners,
    "bic": BangaloreInternationCentre,
    # "bms": BMS,
    # "bms2": BMS2,
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
    while 1:
        s = scrapers[scraper](urls[scraper]).open()
        s.get_events()
        s.close_driver()
        s.save_csv(scraper)

        sleep(3000)


def start_scraper():
    for scraper in scrapers:
        print(f"Scraping {scraper} ...")
        thread = threading.Thread(target=scrape, args=(scraper,), name=scraper)
        thread.start()


start_scraper()
