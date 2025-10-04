

def format_dict_to_string(data: dict, indent_level=0, use_colon=True):
    """
    Recursively formats a dictionary into a multi-line string.

    Args:
        data (dict): The dictionary to format
        indent_level (int): Current indentation level for nested structures
        use_colon (bool): Whether to use "key: value" or "key value" format

    Returns:
        str: Formatted string representation of the dictionary
    """
    if not isinstance(data, dict):
        return str(data)

    lines = []
    indent = "  " * indent_level  # 2 spaces per indentation level
    separator = ": " if use_colon else " "

    for key, value in data.items():
        if isinstance(value, dict):
            # Recursive case: nested dictionary
            lines.append(f"{indent}{key}:")
            nested_string = format_dict_to_string(
                value, indent_level + 1, use_colon
            )
            lines.append(nested_string)
        else:
            # Base case: simple key-value pair
            lines.append(f"{indent}{key}{separator}{value}")

    return "\n".join(lines)