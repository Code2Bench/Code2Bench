from typing import Dict, Tuple

def validate_script(script: Dict) -> Tuple[bool, str]:
    required_sections = ['introduction', 'body', 'conclusion']
    
    if not all(section in script for section in required_sections):
        return False, "Missing required sections in the script."
    
    for section in required_sections:
        if 'text' not in script[section] or 'duration' not in script[section]:
            return False, f"Section '{section}' is missing 'text' or 'duration' field."
        
        if not isinstance(script[section]['duration'], (int, float)) or script[section]['duration'] <= 0:
            return False, f"Section '{section}' has invalid duration value."
    
    total_duration = sum(script[section]['duration'] for section in required_sections)
    if total_duration > 90:
        return False, "Total duration exceeds 90 seconds."
    
    return True, ""