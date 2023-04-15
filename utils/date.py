from datetime import datetime

import dateparser

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

months.extend(months_short)


def is_date(text):
    for month in months:
        if month.lower() in text.lower():
            return True
    return False


def format_date(datestr):
    if datestr == "None":
        return ""

    return f'{datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S").day} {datetime.strftime(datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S"), "%b")}'


def get_current_year():
    return datetime.now().year


def greater_than_today(datestr):
    if not is_date(datestr):
        return False

    date = datetime.strptime(
        str(dateparser.parse(datestr)), "%Y-%m-%d %H:%M:%S").date()
    date_today = datetime.now().date()

    return date >= date_today
