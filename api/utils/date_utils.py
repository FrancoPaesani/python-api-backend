from datetime import date, datetime


def diff_in_years(date_1: datetime, date_2: datetime):
    """
    date_1: least recent date
    date_2: most recent date
    """
    return abs(date_2.year - date_1.year)


def diff_in_months(date_1: datetime, date_2: datetime):
    """
    date_1: least recent date
    date_2: most recent date
    """
    return abs((date_2.year - date_1.year) * 12 + date_2.month - date_1.month)


def diff_in_years_date(date_1: date, date_2: date):
    """
    date_1: least recent date
    date_2: most recent date
    """
    return abs(date_2.year - date_1.year)


def diff_in_months_date(date_1: date, date_2: date):
    """
    date_1: least recent date
    date_2: most recent date
    """
    return abs((date_2.year - date_1.year) * 12 + date_2.month - date_1.month)
