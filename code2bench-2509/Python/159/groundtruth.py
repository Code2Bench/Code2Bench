

def validate_page_range(
    start_page: int, end_page: int, total_pages: int
) -> tuple[int, int]:
    """
    Validate and normalize page range

    Args:
        start_page: Starting page number (1-based)
        end_page: Ending page number (1-based, 0 means last page)
        total_pages: Total number of pages in document

    Returns:
        Tuple of (normalized_start, normalized_end)

    Raises:
        ValueError: If page range is invalid
    """
    if start_page < 1:
        raise ValueError("Start page must be >= 1")

    if start_page > total_pages:
        raise ValueError(f"Start page {start_page} exceeds total pages {total_pages}")

    # Handle end_page = 0 (means last page)
    if end_page == 0:
        end_page = total_pages

    if end_page < start_page:
        raise ValueError(f"End page {end_page} must be >= start page {start_page}")

    if end_page > total_pages:
        end_page = total_pages

    return start_page, end_page