from typing import Dict, Any, Tuple

def validate_operation(operation: Dict[str, Any]) -> Tuple[bool, str]:
    if 'type' not in operation:
        return False, "Operation must contain a 'type' field."
    
    # Define required fields based on operation type
    required_fields = {
        'create': ['name', 'description'],
        'update': ['id', 'name', 'description'],
        'delete': ['id']
    }
    
    # Check if the operation type is supported
    if operation['type'] not in required_fields:
        return False, f"Unsupported operation type: {operation['type']}"
    
    # Check if all required fields are present
    for field in required_fields[operation['type']]:
        if field not in operation:
            return False, f"Missing required field: {field}"
    
    return True, ""