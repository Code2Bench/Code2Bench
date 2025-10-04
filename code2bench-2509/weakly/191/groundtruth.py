
from dateutil import parser
import pytz

def validate_and_convert_date(date_input: str) -> str:
    """
    Converts any recognizable date string into a standardized RFC 3339 format.
    :param date_input: A date string in a recognizable format.
    """
    try:
        dt_object = parser.parse(date_input)
        if dt_object.tzinfo is not None:
            # Convert to UTC if it's in a different timezone
            dt_object = dt_object.astimezone(pytz.utc)
        else:
            # If no timezone info is present, assume it's in local time
            local_tz = pytz.timezone("UTC")
            dt_object = local_tz.localize(dt_object)

        # Convert the datetime object to an RFC 3339-compliant string.
        # RFC 3339 requires timestamps to be in ISO 8601 format with a 'Z' suffix for UTC time.
        # The isoformat() method adds a "+00:00" suffix for UTC by default,
        # so we replace it with "Z" to ensure compliance.
        formatted_date = dt_object.isoformat().replace("+00:00", "Z")
        formatted_date = formatted_date.rstrip("Z") + "Z"

        return formatted_date
    except (ValueError, OverflowError) as e:
        raise ValueError(
            f"Invalid date format: {date_input}."
            f" Date format must adhere to the RFC 3339 standard (e.g., 'YYYY-MM-DDTHH:MM:SSZ' for UTC)."
        ) from e