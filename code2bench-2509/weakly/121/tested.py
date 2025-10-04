from typing import Dict, List, Tuple, Any

def _parse_principal_entries(principal: Dict) -> List[Tuple[Any, Any]]:
    result = []
    for principal_type, values in principal.items():
        if not isinstance(values, list):
            values = [values]
        for value in values:
            result.append((principal_type, value))
    return result