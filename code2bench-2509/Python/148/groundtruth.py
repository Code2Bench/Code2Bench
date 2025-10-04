

def time_to_24hrtime(hhmmss):
    ''' (h)h:mm:ssa or (h)h:mm:ssp --> hh:mm:ss '''

    hhmm_colon = hhmmss.find(':')
    if hhmm_colon == -1: return hhmmss

    ap = hhmmss[-1].lower()                # Get last character of time (#, a, p).lower()
    if ap not in ['a', 'p']:
        return hhmmss

    hh = int(hhmmss[:hhmm_colon])
    if hh == 12 and ap == 'a':
        hh = 0
    elif hh <= 11 and ap == 'p':
        hh += 12

    hhmmss24 = f"{hh:0>2}{hhmmss[hhmm_colon:-1]}"

    return hhmmss24