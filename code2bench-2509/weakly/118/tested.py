import re
import json

def smart_parse(text: str) -> dict:
    # Check for pure JSON
    try:
        parsed = json.loads(text)
        return parsed
    except json.JSONDecodeError:
        pass

    # Check for JSON embedded in text
    json_match = re.search(r'\{.*?\}', text, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group(0))
            remaining_text = text[:json_match.start()] + text[json_match.end():]
            return {**parsed, **{"message": remaining_text.strip()}}
        except json.JSONDecodeError:
            pass

    # Extract key-value pairs in various formats
    kv_pairs = {}
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match key="value" or key='value'
        kv_match = re.match(r'(\w+)\s*=\s*"([^"]*)"$', line)
        if kv_match:
            key, value = kv_match.groups()
            kv_pairs[key.lower()] = value
            continue

        kv_match = re.match(r'(\w+)\s*=\s*([^\s]+)$', line)
        if kv_match:
            key, value = kv_match.groups()
            kv_pairs[key.lower()] = value
            continue

        # Match Key: "value" or Key: value
        kv_match = re.match(r'(\w+)\s*:\s*"([^"]*)"$', line)
        if kv_match:
            key, value = kv_match.groups()
            kv_pairs[key.lower()] = value
            continue

        kv_match = re.match(r'(\w+)\s*:\s*([^\s]+)$', line)
        if kv_match:
            key, value = kv_match.groups()
            kv_pairs[key.lower()] = value
            continue

    # If no structure found, return {'message': text}
    if not kv_pairs:
        return {"message": text}

    # Return the extracted key-value pairs
    return kv_pairs