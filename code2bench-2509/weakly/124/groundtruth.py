from typing import Dict, List
from datetime import datetime

def filter_periods_by_document_end_date(periods: List[Dict], document_period_end_date: str, period_type: str) -> List[Dict]:
    """Filter periods to only include those that end on or before the document period end date."""
    if not document_period_end_date:
        return periods

    try:
        doc_end_date = datetime.strptime(document_period_end_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        # If we can't parse the document end date, return all periods
        return periods

    filtered_periods = []
    for period in periods:
        try:
            if period_type == 'instant':
                period_date = datetime.strptime(period['date'], '%Y-%m-%d').date()
                if period_date <= doc_end_date:
                    filtered_periods.append(period)
            else:  # duration
                period_end_date = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
                if period_end_date <= doc_end_date:
                    filtered_periods.append(period)
        except (ValueError, TypeError):
            # If we can't parse the period date, include it to be safe
            filtered_periods.append(period)

    return filtered_periods