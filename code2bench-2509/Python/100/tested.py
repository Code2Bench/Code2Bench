from typing import List, Union, Dict

def extract_weave_refs_from_value(value: Union[str, Dict, List]) -> List[str]:
    result = []
    
    if isinstance(value, str):
        if value.startswith('weave:///'):
            result.append(value)
    elif isinstance(value, (dict, list)):
        if isinstance(value, dict):
            for key, val in value.items():
                result.extend(extract_weave_refs_from_value(val))
        elif isinstance(value, list):
            for item in value:
                result.extend(extract_weave_refs_from_value(item))
    
    return result