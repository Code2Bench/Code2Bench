from datetime import date

def gregorian_date(jdn: int) -> date:
    jdn += 1867216.5
    if jdn < 2432119.5:
        j = jdn + 1401
        m = (j // 36524 + 1) * 30
        d = (j // 36524 + 1) * 30
    else:
        j = jdn + 1401
        m = (j // 36524 + 1) * 30
        d = (j // 36524 + 1) * 30
    return date(int(d), int(m), int(j))