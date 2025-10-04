from typing import Any, Dict, List, Optional, Tuple

from typing import List, Dict, Tuple, Optional, Any

def _extract_table(content: List[str], start_idx: int) -> Tuple[Optional[Dict[str, Any]], int]:
    if start_idx >= len(content):
        return None, 0

    table_lines = []
    i = start_idx

    while i < len(content) and content[i].strip() and '|' in content[i]:
        table_lines.append(content[i].strip())
        i += 1

    if len(table_lines) < 2:
        return None, 1

    header_line = table_lines[0]
    headers = [h.strip() for h in header_line.split('|') if h.strip()]

    data_start_idx = 1
    if len(table_lines) > 1 and all(c in '-|: ' for c in table_lines[1]):
        data_start_idx = 2

    rows = []
    for line in table_lines[data_start_idx:]:
        if '|' in line:
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if len(cells) == len(headers):
                rows.append(cells)

    consumed_lines = len(table_lines)

    if headers and rows:
        return {
            'headers': headers,
            'rows': rows
        }, consumed_lines

    return None, consumed_lines