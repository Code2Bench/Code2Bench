from datetime import datetime

def human_date(date_value) -> str:
    if date_value is None or date_value == "":
        return "—"
    try:
        if isinstance(date_value, datetime):
            return date_value.strftime("%b %d, %Y at %I:%M %p")
        else:
            parsed_date = datetime.fromisoformat(date_value)
            return parsed_date.strftime("%b %d, %Y at %I:%M %p")
    except (ValueError, TypeError):
        return str(date_value)[:16] if isinstance(date_value, str) else str(date_value)[:16]