import datetime

def epoch_ms_to_utc_iso(ms: int) -> str:
    dt = datetime.datetime.utcfromtimestamp(ms / 1000.0)
    return dt.strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'