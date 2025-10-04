
from datetime import datetime

def ds_format(ds: str, input_format: str, output_format: str) -> str:
    """
    Output datetime string in a given format.

    :param ds: Input string which contains a date.
    :param input_format: Input string format (e.g., '%Y-%m-%d').
    :param output_format: Output string format (e.g., '%Y-%m-%d').

    >>> ds_format("2015-01-01", "%Y-%m-%d", "%m-%d-%y")
    '01-01-15'
    >>> ds_format("1/5/2015", "%m/%d/%Y", "%Y-%m-%d")
    '2015-01-05'
    >>> ds_format("12/07/2024", "%d/%m/%Y", "%A %d %B %Y", "en_US")
    'Friday 12 July 2024'
    """
    return datetime.strptime(str(ds), input_format).strftime(output_format)