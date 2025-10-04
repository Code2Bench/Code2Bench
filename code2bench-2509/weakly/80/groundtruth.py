
from datetime import datetime

def format_create_date(timestamp: float) -> str:
    """
    将时间戳格式化为可读的日期字符串
    """
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "未知时间"