from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
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

# Strategy for generating page numbers
page_strategy = st.integers(min_value=0, max_value=100)
total_pages_strategy = st.integers(min_value=1, max_value=100)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    start_page=page_strategy,
    end_page=page_strategy,
    total_pages=total_pages_strategy
)
@example(start_page=1, end_page=0, total_pages=10)
@example(start_page=1, end_page=5, total_pages=10)
@example(start_page=5, end_page=5, total_pages=10)
@example(start_page=1, end_page=10, total_pages=10)
@example(start_page=1, end_page=15, total_pages=10)
@example(start_page=0, end_page=5, total_pages=10)
@example(start_page=5, end_page=3, total_pages=10)
@example(start_page=11, end_page=15, total_pages=10)
def test_validate_page_range(start_page, end_page, total_pages):
    global stop_collecting
    if stop_collecting:
        return
    
    try:
        expected = validate_page_range(start_page, end_page, total_pages)
    except ValueError:
        return  # Skip invalid inputs
    
    generated_cases.append({
        "Inputs": {"start_page": start_page, "end_page": end_page, "total_pages": total_pages},
        "Expected": expected
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)