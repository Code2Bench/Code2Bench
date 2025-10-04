from typing import List, Dict
from datetime import datetime

def filter_periods_by_document_end_date(periods: List[Dict], document_period_end_date: str, period_type: str) -> List[Dict]:
    if not document_period_end_date:
        return periods
    
    try:
        document_end_date = datetime.strptime(document_period_end_date, '%Y-%m-%d').date()
    except ValueError:
        return periods
    
    filtered_periods = []
    for period in periods:
        if period_type == 'instant':
            date_key = 'date'
        elif period_type == 'duration':
            date_key = 'end_date'
        else:
            continue
        
        if date_key not in period:
            filtered_periods.append(period)
            continue
        
        try:
            period_date = datetime.strptime(period[date_key], '%Y-%m-%d').date()
        except ValueError:
            filtered_periods.append(period)
            continue
        
        if period_date <= document_end_date:
            filtered_periods.append(period)
    
    return filtered_periods