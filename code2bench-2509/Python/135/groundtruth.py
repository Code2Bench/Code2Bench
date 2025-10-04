

def fullwidth_to_halfwidth(s):
    result = []
    for char in s:
        code = ord(char)
        # Convert full-width space to half-width space
        if code == 0x3000:
            code = 0x0020
        # Convert other full-width characters to half-width
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        result.append(chr(code))
    return ''.join(result)