def split_continuous_references(text: str) -> str:
    # Check if the text meets the conditions
    if '[' in text and ']' in text and text.count(',') == 1:
        # Split the text into parts
        parts = text.split('[', 1)
        if len(parts) != 2:
            return text
        first_part, rest = parts
        # Check if the rest ends with ']'
        if rest.endswith(']'):
            # Split the rest into individual tags
            tags = rest.split(',', 1)
            if len(tags) != 2:
                return text
            tag1, tag2 = tags
            # Combine the parts
            result = f"{first_part}[{tag1}{tag2}]"
            return result
    return text