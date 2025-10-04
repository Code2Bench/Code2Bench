from dateutil import parser

def iso_to_millis(ts: str) -> int:
    dt = parser.isoparse(ts)
    return int(dt.timestamp() * 1000)