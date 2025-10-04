from typing import List, Dict, Tuple, Optional, Any

def _extract_table(content: List[str], start_idx: int) -> Tuple[Optional[Dict[str, Any]], int]:
    if start_idx < 0 or start_idx >= len(content):
        return None, 0
    
    lines = []
    while start_idx < len(content) and content[start_idx].strip() != "":
        lines.append(content[start_idx])
        start_idx += 1
    
    if len(lines) < 2:
        return None, 1
    
    # Extract headers
    headers = lines[0].split('|')
    if len(headers) == 0:
        return None, len(lines)
    
    # Skip separator line
    if len(lines) > 1 and lines[1].strip() == "":
        lines.pop(0)
    
    # Extract data rows
    rows = []
    for i in range(2, len(lines), 2):
        row = lines[i].split('|')
        if len(row) != len(headers):
            return None, len(lines)
        rows.append(row)
    
    # Return the table structure and number of lines consumed
    return {
        "headers": headers,
        "rows": rows
    }, len(lines)