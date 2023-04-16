import re
from datetime import datetime

import dateparser
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def date_regex_bms(input_text):
    pattern = r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})"

    match = re.search(pattern, input_text)

    if match:
        date = match.group(2)
        month = match.group(3)
        year = match.group(4)
        return f"{date} {month} {year}"
    else:
        return None


def date_regex_twb(input_text):
    pattern1 = r"(\d{1,2})(st|nd|rd|th)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'(\d{2})"
    pattern2 = r"(\d{1,2})(st|nd|rd|th)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    pattern3 = r"(\d{1,2})(st|nd|rd|th)\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+'?\s+(\d{2})"

    match1 = re.search(pattern1, input_text)
    match2 = re.search(pattern2, input_text)
    match3 = re.search(pattern3, input_text)

    if match1:
        date = match1.group(1)
        month = match1.group(3)
        year = match1.group(4)
        return f"{date} {month} 20{year}"
    elif match2:
        date = match2.group(1)
        month = match2.group(3)
        return f"{date} {month} {get_current_year()}"
    elif match3:
        date = match3.group(1)
        month = match3.group(3)
        year = match3.group(4)
        return f"{date} {month} 20{year}"
    else:
        return None


def is_date(text):
    try:
        parser.parse(text)
        return True
    except ValueError:
        return False


def format_date(datestr):
    if datestr == "None":
        return ""

    return f'{datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S").day} {datetime.strftime(datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S"), "%b %Y")}'


def get_current_year():
    return datetime.now().year


def greater_than_today(datestr):
    if not is_date(datestr):
        return False

    date = datetime.strptime(
        str(dateparser.parse(datestr)), "%Y-%m-%d %H:%M:%S").date()
    date_today = datetime.now().date()

    return date >= date_today


def get_date(url, script, site="bms"):
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if site != "bms":
        options.add_argument("--headless")

    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

    driver = webdriver.Chrome(
        options=options, executable_path="./chromedriver")

    driver.get(url)
    driver.implicitly_wait(5)

    data = driver.execute_script(script)

    driver.close()

    if site == "bms":
        return data
    else:
        return date_regex_twb(data)
