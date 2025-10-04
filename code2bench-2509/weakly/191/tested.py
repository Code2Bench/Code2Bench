from dateutil import parser
import pytz

def validate_and_convert_date(date_input: str) -> str:
    dt = parser.parse(date_input)
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')