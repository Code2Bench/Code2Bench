from typing import Dict
from datetime import datetime, date

def _is_annual_period(period: Dict) -> bool:
    """
    Determine if a period is truly annual (300-400 days).

    Annual periods should be approximately one year, allowing for:
    - Leap years (366 days)
    - Slight variations in fiscal year end dates
    - But rejecting multi-year cumulative periods
    """
    try:
        start_date = datetime.strptime(period['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
        duration_days = (end_date - start_date).days
        # Annual periods should be between 300-400 days
        # This rejects quarterly (~90 days) and multi-year (>400 days) periods
        return 300 < duration_days <= 400
    except (ValueError, TypeError, KeyError):
        return False