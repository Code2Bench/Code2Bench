from datetime import datetime, date
from typing import Dict

def _is_annual_period(period: Dict) -> bool:
    try:
        start_date = datetime.strptime(period['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
        delta = end_date - start_date
        return 300 <= delta.days <= 400
    except (ValueError, KeyError):
        return False