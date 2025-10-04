from typing import Dict, Tuple
from typing import Dict, List, Optional, Tuple, Any

def validate_script(script: Dict) -> Tuple[bool, str]:
    """Validate the generated script."""
    required_sections = ['hook', 'introduction', 'showcase', 'value_proposition', 'call_to_action']

    # Check for missing sections
    for section in required_sections:
        if section not in script:
            return False, f"Missing required section: {section}"

    # Validate section content
    for section, content in script.items():
        if not content.get('text'):
            return False, f"Missing text in section: {section}"
        if not content.get('duration'):
            return False, f"Missing duration in section: {section}"

    # Validate total duration
    total_duration = sum(float(content['duration'].split()[0]) for content in script.values())
    if total_duration > 90:  # 90 seconds max
        return False, f"Total duration ({total_duration}s) exceeds maximum allowed (90s)"

    return True, ""