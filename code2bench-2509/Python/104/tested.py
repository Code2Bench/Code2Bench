from typing import Any, List, Dict

def _convert_dicts_to_rows(data: List[Dict[str, Any]], headers: List[str]) -> List[List[str]]:
    if not headers:
        raise ValueError("headers cannot be empty")
    
    result = []
    for row in data:
        row_list = []
        for header in headers:
            value = row.get(header, None)
            if value is None:
                row_list.append("")
            else:
                row_list.append(str(value))
        result.append(row_list)
    return result