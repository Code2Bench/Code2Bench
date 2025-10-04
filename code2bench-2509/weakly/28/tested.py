import json
import re

def extract_answer_obj(s: str) -> dict | None:
    pattern = r'<\|begin_of_box\|>(.*?)<\|end_of_box\|>'
    match = re.search(pattern, s, re.DOTALL)
    if not match:
        return None
    
    content = match.group(1).strip()
    
    # Remove leading zeros from numeric arrays
    content = re.sub(r'\s*([0-9]+\s*)', lambda m: m.group(1).lstrip('0') if m.group(1).lstrip('0') else '0', content)
    
    try:
        obj = json.loads(content)
        return obj
    except json.JSONDecodeError:
        # Map 'true', 'false', 'null' to Python's True, False, None
        content = content.replace('true', 'True').replace('false', 'False').replace('null', 'None')
        try:
            obj = eval(content)
            return obj
        except:
            return None