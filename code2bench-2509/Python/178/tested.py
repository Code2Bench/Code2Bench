from typing import Any, Optional, Tuple

def _apply_tail(
    current_data: str, n_str: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    # Validate current_data is a string
    if not isinstance(current_data, str):
        return (None, "current_data must be a string", None)
    
    # Validate n_str is a string
    if not isinstance(n_str, str):
        return (None, "n_str must be a string", None)
    
    # Validate n_str is a valid integer
    try:
        n = int(n_str)
    except ValueError:
        return (None, f"n_str must be an integer: {n_str}", None)
    
    # Handle edge case where n is 0
    if n == 0:
        return (current_data, mime_type, None)
    
    # Check if n is negative
    if n < 0:
        return (None, "n_str cannot be negative", None)
    
    # Split current_data into lines
    lines = current_data.splitlines()
    
    # Get the last N lines
    result_data = "\n".join(lines[-n:])
    
    return (result_data, mime_type, None)