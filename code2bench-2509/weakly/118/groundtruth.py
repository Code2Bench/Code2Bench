
import re
import json

def smart_parse(text: str) -> dict:
    """
    Smart parser that attempts to extract structured data from a string using multiple approaches.

    Handles:
    1. Pure JSON objects
    2. JSON embedded in text
    3. Key-value pairs in formats like:
       - key="value"
       - key=value
       - Key: "value"
       - key: value
    4. Plain text (stored under 'message' key)

    Args:
        text (str): Input text to parse

    Returns:
        dict: Parsed data or {'message': text} if no structure found
    """

    # First try: Parse as pure JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Second try: Look for JSON within text
        json_match = re.search(r'{.*}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        # Third try: Parse key-value pairs
        pattern = re.findall(
            r'(\w+)=["\']([^"\']+)["\']|'  # key="value"
            r'(\w+)=([\w.]+)|'  # key=value
            r'(\w+):\s*["\']([^"\']+)["\']|'  # Key: "value"
            r'(\w+):\s*([\w.]+)',  # key: value
            text)

        if pattern:
            parsed_data = {}
            remaining_str = text

            for match in pattern:
                key = next(m for m in [match[0], match[2], match[4], match[6]] if m)
                value = next(m for m in [match[1], match[3], match[5], match[7]] if m)
                parsed_data[key.lower()] = value
                # Remove matched text from remaining string
                for possible_format in [f'{key}={value}', f'{key}: {value}', f'{key}="{value}"', f'{key}: "{value}"']:
                    remaining_str = remaining_str.replace(possible_format, '')

            # Add remaining text as message if it exists
            remaining_str = remaining_str.strip().strip(',').strip()
            if remaining_str:
                parsed_data['message'] = remaining_str

            return parsed_data

        # Fallback: Return plain text as message
        return {'message': text}