from typing import Any, Dict, Tuple

def validate_operation(operation: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate a batch operation dictionary.

    Args:
        operation: Operation dictionary to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    op_type = operation.get('type')
    if not op_type:
        return False, "Missing 'type' field"

    # Validate required fields for each operation type
    required_fields = {
        'insert_text': ['index', 'text'],
        'delete_text': ['start_index', 'end_index'],
        'replace_text': ['start_index', 'end_index', 'text'],
        'format_text': ['start_index', 'end_index'],
        'insert_table': ['index', 'rows', 'columns'],
        'insert_page_break': ['index'],
        'find_replace': ['find_text', 'replace_text']
    }

    if op_type not in required_fields:
        return False, f"Unsupported operation type: {op_type or 'None'}"

    for field in required_fields[op_type]:
        if field not in operation:
            return False, f"Missing required field: {field}"

    return True, ""