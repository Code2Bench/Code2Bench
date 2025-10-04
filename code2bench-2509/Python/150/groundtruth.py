

def format_mins_timer(mins):
    ''' mins --> 4.5 days/min/hrs '''

    try:
        if mins == 0:
            return '0 min'

        if mins >= 86400:
            time_str = f"{mins/1440:.2f} days"
        elif mins < 60:
            time_str = f"{mins:.1f} min"
        elif mins == 60:
            time_str = "1 hr"
        else:
            time_str = f"{mins/60:.1f} hrs"

        # change xx.0 min/hr --> xx min/hr
        time_str = time_str.replace('.0 ', ' ')

    except Exception as err:
        time_str = ''

    return time_str