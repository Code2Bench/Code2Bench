from typing import Any, Optional, Tuple

def _apply_tail(
    current_data: str, n_str: str, mime_type: Optional[str], log_id: str
) -> Tuple[Any, Optional[str], Optional[str]]:
    """
    Returns the last N lines of text data.

    Args:
        current_data: The input data (expected str).
        n_str: String representing the number of lines (N).
        mime_type: The original mime type (passed through).
        log_id: Identifier for logging.

    Returns:
        Tuple: (result_data, original_mime_type, error_string)
               result_data is str containing the last N lines.
    """
    if not isinstance(current_data, str):
        return (
            current_data,
            mime_type,
            f"Input data for 'tail' must be a string, got {type(current_data).__name__}.",
        )

    try:
        n = int(n_str.strip())
        if n < 0:
            return current_data, mime_type, "Tail count N cannot be negative."
        if n == 0:
            return "", mime_type, None

        lines = current_data.splitlines(keepends=True)
        tail_lines = lines[-n:]
        return "".join(tail_lines), mime_type, None
    except (ValueError, TypeError) as e:
        return current_data, mime_type, f"Invalid tail count N '{n_str}': {e}"
    except Exception as e:
        return current_data, mime_type, f"Error applying tail '{n_str}': {e}"