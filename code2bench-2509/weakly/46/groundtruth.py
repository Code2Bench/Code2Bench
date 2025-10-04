
from datetime import date

def gregorian_date(jdn):
    f = jdn + 1401 + (4 * jdn + 274277) // 146097 * 3 // 4 - 38
    e = 4 * f + 3
    h = e % 1461 // 4
    h = 5 * h + 2
    d = (h % 153) // 5 + 1
    m = (h // 153 + 2) % 12 + 1
    y = e // 1461 - 4716 + (14 - m) // 12
    return date(y, m, d)