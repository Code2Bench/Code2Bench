from datetime import datetime

def format_create_date(timestamp: float) -> str:
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "未知时间"