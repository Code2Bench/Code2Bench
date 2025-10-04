from typing import Dict

def convert_str_cookie_to_dict(cookie_str: str) -> Dict[str, str]:
    cookie_dict = {}
    if not cookie_str:
        return cookie_dict
    pairs = cookie_str.split(';')
    for pair in pairs:
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            cookie_dict[key.strip()] = value.strip()
    return cookie_dict