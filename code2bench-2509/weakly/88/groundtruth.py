
from datetime import datetime
import re

def _update_head_date(data):
    """Parse data and update date of last bump in it
    :param data: String to parse for
    :returns: string with current date instead of old one
    """
    return re.sub(
        r'### HEAD as of [0-9.]{10} ###',
        "### HEAD as of {:%d.%m.%Y} ###".format(datetime.now()),
        data)