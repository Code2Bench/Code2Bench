from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from datetime import datetime
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
def human_date(date_value) -> str:
    """Format a date/datetime to be more human-readable.

    Converts datetime objects or ISO strings to a format like:
    "Jan 15, 2024 at 2:30 PM"
    """
    if not date_value:
        return "—"

    # Handle string datetime values (ISO format)
    if isinstance(date_value, str):
        try:
            # Parse common ISO formats
            for fmt in [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
            ]:
                try:
                    date_value = datetime.strptime(date_value, fmt)
                    break
                except ValueError:
                    continue
            else:
                # If we can't parse it, just return the original truncated string
                return date_value[:16] if len(date_value) > 16 else date_value
        except (ValueError, AttributeError):
            return date_value[:16] if len(date_value) > 16 else date_value

    # Handle datetime objects
    if hasattr(date_value, "strftime"):
        return date_value.strftime("%b %-d, %Y at %-I:%M %p")

    # Fallback for unknown types
    return str(date_value)[:16]

# Strategies for generating inputs
def date_value_strategy():
    return st.one_of(
        st.none(),
        st.datetimes(min_value=datetime(1970, 1, 1), max_value=datetime(2100, 1, 1)),
        st.from_regex(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?", fullmatch=True),
        st.from_regex(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}", fullmatch=True),
        st.text(min_size=0, max_size=32)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(date_value=date_value_strategy())
@example(date_value=None)
@example(date_value="2024-01-15 14:30:00")
@example(date_value="2024-01-15T14:30:00")
@example(date_value="2024-01-15T14:30:00.123456")
@example(date_value="2024-01-15 14:30")
@example(date_value="invalid-date-string")
@example(date_value=datetime(2024, 1, 15, 14, 30))
def test_human_date(date_value):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    date_value_copy = copy.deepcopy(date_value)

    # Call func0 to verify input validity
    try:
        expected = human_date(date_value_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "date_value": date_value_copy.strftime("%Y-%m-%d %H:%M:%S") if hasattr(date_value_copy, "strftime") else date_value_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)