from typing import Dict, Optional, Tuple

def get_contest_data_from_cache(contest_id: int, cached_data: Dict) -> Tuple[Optional[Dict], Optional[Dict]]:
    contest_str_id = str(contest_id)
    if contest_str_id not in cached_data:
        return (None, None)
    
    data = cached_data[contest_str_id]
    if 'standings' not in data or 'rating_changes' not in data:
        raise KeyError("Missing required keys 'standings' or 'rating_changes' in cached data")
    
    standings = data['standings']
    rating_changes = data['rating_changes']
    
    if standings.get('status') == 'OK' and rating_changes.get('status') == 'OK':
        return (standings, rating_changes)
    
    return (None, None)