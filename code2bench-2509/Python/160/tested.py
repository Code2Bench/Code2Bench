import re

def _extract_balanced_json(text: str) -> str:
    # Find the first occurrence of '{'
    open_brace = text.find('{')
    if open_brace == -1:
        return text
    
    # Find the corresponding '}' that balances the braces
    close_brace = text.find('}', open_brace + 1)
    if close_brace == -1 or text[close_brace] != '}':
        return text
    
    # Extract the JSON object between the braces
    json_part = text[open_brace + 1:close_brace]
    
    # Remove escaped characters and strings
    json_part = re.sub(r'({"|}|[^{}])', r'\1', json_part)
    
    return json_part