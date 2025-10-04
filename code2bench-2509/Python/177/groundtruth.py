from typing import Any, Dict, List, Optional, Tuple

def _apply_filter_rows_eq(
    current_data: List[Dict], filter_spec: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    """
    Filters a list of dictionaries based on a column's value equality.

    Args:
        current_data: The input data (expected List[Dict]).
        filter_spec: String in the format 'column_name:value'.
        mime_type: The original mime type (passed through).
        log_id: Identifier for logging.

    Returns:
        Tuple: (result_data, original_mime_type, error_string)
               result_data is List[Dict] containing only filtered rows.
    """
    if not isinstance(current_data, list) or (
        current_data and not isinstance(current_data[0], dict)
    ):
        return (
            current_data,
            mime_type,
            f"Input data for 'filter_rows_eq' must be a list of dictionaries, got {type(current_data).__name__}.",
        )

    if not current_data:
        return [], mime_type, None

    try:
        parts = filter_spec.split(":", 1)
        if len(parts) != 2:
            return (
                current_data,
                mime_type,
                f"Invalid filter format '{filter_spec}'. Expected 'column_name:value'.",
            )
        col_name, filter_value = parts[0].strip(), parts[1].strip()

        header = list(current_data[0].keys())
        if col_name not in header:
            return (
                current_data,
                mime_type,
                f"Filter column '{col_name}' not found in data keys: {header}",
            )

        output_list = [
            row for row in current_data if str(row.get(col_name)) == filter_value
        ]

        return output_list, mime_type, None

    except Exception as e:
        return current_data, mime_type, f"Error filtering rows by '{filter_spec}': {e}"