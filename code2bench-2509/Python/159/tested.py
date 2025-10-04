def validate_page_range(start_page: int, end_page: int, total_pages: int) -> tuple[int, int]:
    if start_page < 1:
        raise ValueError("Start page must be at least 1.")
    if end_page < 1:
        raise ValueError("End page must be at least 1.")
    if end_page > total_pages:
        raise ValueError("End page cannot exceed the total number of pages.")
    if start_page > total_pages:
        raise ValueError("Start page cannot exceed the total number of pages.")
    if start_page > end_page:
        start_page, end_page = end_page, start_page
    return (start_page, end_page)