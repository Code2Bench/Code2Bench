import json
import ast

def parse_tool_result(result: dict) -> dict:
    if result.get('status') != 'success':
        return result
    content = result.get('content', [])
    if not content:
        return result
    text = content[0].get('text')
    if not text:
        return result
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return result