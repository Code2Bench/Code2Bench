from typing import Dict, Optional

def extract_duration_from_data(movie_data: Dict[str, Any]) -> Optional[int]:
    # Check for 'duration_secs' key
    if 'duration_secs' in movie_data:
        return int(movie_data['duration_secs'])
    
    # Check for 'duration' key
    if 'duration' in movie_data:
        duration_str = movie_data['duration']
        
        # Check if the duration is a digit (minutes)
        if duration_str.isdigit():
            return int(duration_str) * 60
        
        # Check for 'HH:MM:SS' format
        if ':' in duration_str:
            hours, minutes, seconds = map(int, duration_str.split(':'))
            return hours * 3600 + minutes * 60 + seconds
        
        # Check for 'MM:SS' format
        elif ':' in duration_str and len(duration_str.split(':')) == 2:
            minutes, seconds = map(int, duration_str.split(':'))
            return minutes * 60 + seconds
        
        # If none of the above, return None
        return None
    
    # If no duration found, return None
    return None