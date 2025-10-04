from typing import List, Dict, Tuple, Any

def _extract_content_and_reasoning(parts: List[Dict[str, Any]]) -> Tuple[str, str]:
    general_content = ""
    reasoning_content = ""

    for part in parts:
        if 'text' in part:
            if 'thought' in part and part['thought']:
                reasoning_content += part['text']
            else:
                general_content += part['text']

    return general_content, reasoning_content