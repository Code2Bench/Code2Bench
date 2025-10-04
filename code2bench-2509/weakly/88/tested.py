import re
from datetime import datetime

def _update_head_date(data: str) -> str:
    current_date = datetime.now().strftime('%d.%m.%Y')
    pattern = r'### HEAD as of (\d{2}\.\d{2}\.\d{4}) ###'
    updated_data = re.sub(pattern, f'### HEAD as of {current_date} ###', data)
    return updated_data