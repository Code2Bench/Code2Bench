from typing import List, Dict, Optional, Tuple, Any

def _apply_select_cols(
    current_data: List[Dict], cols_str: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    # Validate input data
    if not isinstance(current_data, list):
        return current_data, mime_type, f"Input data is not a list: {current_data}"

    # Validate cols_str
    if not isinstance(cols_str, str):
        return current_data, mime_type, f"cols_str is not a string: {cols_str}"

    # Split the column string into a list
    selected_cols = cols_str.split(',')

    # Validate that all selected columns exist in the data
    valid_cols = [col for col in selected_cols if col in current_data[0].keys()]
    if len(valid_cols) != len(selected_cols):
        return current_data, mime_type, f"Invalid column(s): {', '.join(selected_cols)}"

    # Filter the data to include only the selected columns
    result_data = [dict(row[col] for col in valid_cols) for row in current_data]

    # Return the result
    return result_data, mime_type, None