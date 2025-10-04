

def time_str_to_secs(time_str=None) -> int:
    ''' 20 sec/min/hrs --> secs '''

    if time_str is None or time_str == "": return 0

    try:
        s1 = str(time_str).replace('_', ' ') + " min"
        time_part = float((s1.split(" ")[0]))
        text_part = s1.split(" ")[1]

        if text_part in ('sec', 'secs'):
            secs = time_part
        elif text_part in ('min', 'mins'):
            secs = time_part * 60
        elif text_part in ('hr', 'hrs'):
            secs = time_part * 3600
        else:
            secs = 0

        if secs < 0: secs = 0

    except:
        secs = 0

    return secs