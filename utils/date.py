from datetime import datetime

import dateparser
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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


def get_date(url, script):
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

    driver = webdriver.Chrome(
        options=options, executable_path="./chromedriver")

    driver.get(url)
    driver.implicitly_wait(5)

    date = driver.execute_script(script)

    driver.close()

    return date
