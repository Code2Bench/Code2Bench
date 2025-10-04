from typing import List, Tuple

from typing import List, Tuple

def parse_expression_response(response: str, chat_id: str) -> List[Tuple[str, str, str]]:
    expressions: List[Tuple[str, str, str]] = []
    for line in response.splitlines():
        line = line.strip()
        if not line:
            continue
        idx_when = line.find('当"')
        if idx_when == -1:
            continue
        idx_quote1 = idx_when + 1
        idx_quote2 = line.find('"', idx_quote1 + 1)
        if idx_quote2 == -1:
            continue
        situation = line[idx_quote1 + 1 : idx_quote2]
        idx_use = line.find('使用"', idx_quote2)
        if idx_use == -1:
            continue
        idx_quote3 = idx_use + 2
        idx_quote4 = line.find('"', idx_quote3 + 1)
        if idx_quote4 == -1:
            continue
        style = line[idx_quote3 + 1 : idx_quote4]
        expressions.append((chat_id, situation, style))
    return expressions