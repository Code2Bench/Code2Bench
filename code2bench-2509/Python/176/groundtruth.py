from typing import Any, Dict, List, Optional, Tuple

def _apply_select_cols(
    current_data: List[Dict], cols_str: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    """
    Selects specific columns from data represented as a list of dictionaries.

    Args:
        current_data: The input data (expected List[Dict]).
        cols_str: Comma-separated string of column names to keep.
        mime_type: The original mime type (passed through).
        log_id: Identifier for logging.

    Returns:
        Tuple: (result_data, original_mime_type, error_string)
               result_data is List[Dict] containing only selected columns.
    """
    if not isinstance(current_data, list) or (
        current_data and not isinstance(current_data[0], dict)
    ):
        return (
            current_data,
            mime_type,
            f"Input data for 'select_cols' must be a list of dictionaries, got {type(current_data).__name__}.",
        )

    if not current_data:
        return [], mime_type, None

    try:
        header = list(current_data[0].keys())
        target_cols = [col.strip() for col in cols_str.split(",")]
        output_list = []

        for target_col in target_cols:
            if target_col not in header:
                return (
                    current_data,
                    mime_type,
                    f"Column '{target_col}' not found in data keys: {header}",
                )

        for row_dict in current_data:
            new_row = {col: row_dict.get(col) for col in target_cols}
            output_list.append(new_row)

        return output_list, mime_type, None

    except Exception as e:
        return current_data, mime_type, f"Error selecting columns '{cols_str}': {e}"