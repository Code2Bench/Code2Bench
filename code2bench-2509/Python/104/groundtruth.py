from typing import Any

def _convert_dicts_to_rows(
    data: list[dict[str, Any]], headers: list[str]
) -> list[list[str]]:
    """Convert list of dictionaries to list of rows using the specified header order.

    Args:
        data: List of dictionaries to convert
        headers: List of column headers to use for ordering

    Returns:
        List of rows where each row is a list of string values in header order
    """
    if not data:
        return []

    if not headers:
        raise ValueError("Headers are required when using list[dict] format")

    rows = []
    for item in data:
        row = []
        for header in headers:
            value = item.get(header, "")
            row.append(str(value) if value is not None else "")
        rows.append(row)

    return rows