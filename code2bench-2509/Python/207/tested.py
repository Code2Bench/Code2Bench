from typing import List, Tuple

def parse_expression_response(response: str, chat_id: str) -> List[Tuple[str, str, str]]:
    expressions = []
    for line in response.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("当") and line.endswith("使用"):
            # Extract the situation and style
            situation = line.split('"')[1]
            style = line.split('"')[3]
            expressions.append((chat_id, situation, style))
    return expressions