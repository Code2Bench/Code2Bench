
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_first_last_day(year_month_str):
    try:
        date_obj = datetime.strptime(year_month_str, "%Y-%m")
        first_day = date_obj.date().replace(day=1)
        last_day = (date_obj + relativedelta(months=1, days=-1)).date()
        return first_day, last_day
    except ValueError:
        raise ValueError("Invalid date format. Please use '%Y-%m'.")