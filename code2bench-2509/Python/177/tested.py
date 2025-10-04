from typing import List, Dict, Optional, Tuple, Any

def _apply_filter_rows_eq(
    current_data: List[Dict], 
    filter_spec: str, 
    mime_type: Optional[str], 
    log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    # Split the filter specification into column and value
    try:
        column, value = filter_spec.split(':', 1)
    except ValueError:
        return ([], mime_type, "Invalid filter specification format")
    
    # Filter the current_data based on the column and value
    result_data = [item for item in current_data if item.get(column) == value]
    
    # Return the result, mime type, and error string
    return (result_data, mime_type, None)