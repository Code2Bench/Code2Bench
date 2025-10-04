

def extract_duration_from_data(movie_data):
    """Extract duration in seconds from movie data"""
    duration_secs = None

    # Try to extract duration from various possible fields
    if movie_data.get('duration_secs'):
        duration_secs = int(movie_data.get('duration_secs'))
    elif movie_data.get('duration'):
        # Handle duration that might be in different formats
        duration_str = str(movie_data.get('duration'))
        if duration_str.isdigit():
            duration_secs = int(duration_str) * 60  # Assume minutes if just a number
        else:
            # Try to parse time format like "01:30:00"
            try:
                time_parts = duration_str.split(':')
                if len(time_parts) == 3:
                    hours, minutes, seconds = map(int, time_parts)
                    duration_secs = (hours * 3600) + (minutes * 60) + seconds
                elif len(time_parts) == 2:
                    minutes, seconds = map(int, time_parts)
                    duration_secs = minutes * 60 + seconds
            except (ValueError, AttributeError):
                pass

    return duration_secs