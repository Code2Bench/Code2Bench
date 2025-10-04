import urllib.parse

def parse_specific_attributes(specific_attributes: str) -> dict:
    assert isinstance(specific_attributes, str), "specific_attributes must be a string"
    return dict(urllib.parse.parse_qs(specific_attributes)) or {}