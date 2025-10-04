from configparser import ConfigParser

def entry_points(text: str, text_source: str = "entry-points") -> dict[str, dict[str, str]]:
    config = ConfigParser()
    config.read_string(text)
    result = {}
    for section in config.sections():
        result[section] = {key: value for key, value in config.items(section)}
    return result