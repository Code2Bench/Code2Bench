from typing import Dict, Tuple

def validate_channel_info(channel_info: Dict) -> Tuple[bool, str]:
    required_fields = ['channel_name', 'channel_niche', 'target_audience', 'key_topics', 'unique_points']
    for field in required_fields:
        if field not in channel_info:
            return False, f"Missing required field: {field}"
    
    if len(channel_info['channel_name']) < 3:
        return False, "Channel name must be at least 3 characters long."
    
    if len(channel_info['target_audience']) < 10:
        return False, "Target audience must be at least 10 characters long."
    
    if len(channel_info['key_topics']) < 10:
        return False, "Key topics must be at least 10 characters long."
    
    if len(channel_info['unique_points']) < 10:
        return False, "Unique points must be at least 10 characters long."
    
    return True, "Validation passed."