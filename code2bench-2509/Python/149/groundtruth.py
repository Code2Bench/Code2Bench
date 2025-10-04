

def format_timer(secs):
    ''' secs --> 4.5 days/hrs/mins/secs '''

    try:
        if secs < 1:
            return '0 secs'

        if secs >= 86400:
            time_str = f"{secs/86400:.1f} days"
        elif secs < 60:
            time_str = f"{secs:.0f} secs"
        elif secs < 3600:
            time_str = f"{secs/60:.0f} mins"
        elif secs == 3600:
            time_str = "1 hr"
        else:
            time_str = f"{secs/3600:.1f} hrs"

        # change xx.0 min/hr --> xx min/hr
        time_str = time_str.replace('.0 ', ' ')
        if time_str == '1 mins': time_str = '1 min'

    except Exception as err:
        #_LOGGER.exception(err)
        time_str = ''

    return time_str