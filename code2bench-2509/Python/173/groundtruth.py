

def syndrome_booleans(syndrome, measurements):
    if syndrome[0] == 0:
        m = ~measurements[0]
    else:
        m = measurements[0]

    for i, elem in enumerate(syndrome[1:]):
        if elem == 0:
            m = m & ~measurements[i + 1]
        else:
            m = m & measurements[i + 1]

    return m