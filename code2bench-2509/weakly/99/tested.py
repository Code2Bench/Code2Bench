from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_first_last_day(year_month_str: str) -> tuple:
    try:
        year, month = map(int, year_month_str.split('-'))
    except ValueError:
        raise ValueError("Input string is not in the expected '%Y-%m' format.")
    
    first_day = datetime(year=year, month=month, day=1)
    last_day = first_day + relativedelta(months=1, days=-1)
    
    return first_day.date(), last_day.date()