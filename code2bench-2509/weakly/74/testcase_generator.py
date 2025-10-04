from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Any, Dict

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _parse_json_fields(field: Any) -> Dict[str, Any]:
    """Parse a JSON field from the database, handling potential errors.

    Args:
        field: The field to parse, can be a string or dict

    Returns:
        Parsed dictionary or error dictionary if parsing fails
    """
    if isinstance(field, dict):
        return field
    if isinstance(field, str):
        try:
            return json.loads(field)
        except Exception as e:
            return {"error": f"Unable to parse {field}: {e}"}
    return {"error": f"Invalid {field} format"}

# Strategies for generating inputs
def field_strategy():
    return st.one_of(
        st.dictionaries(
            keys=st.text(min_size=1, max_size=10),
            values=st.one_of(
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(min_size=1, max_size=10),
                st.booleans(),
                st.lists(st.integers(), min_size=1, max_size=5)
            ),
            min_size=1, max_size=5
        ),
        st.text(min_size=1, max_size=50).map(lambda x: json.dumps({"key": x})),
        st.text(min_size=1, max_size=50).filter(lambda x: not x.startswith("{")),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans(),
        st.lists(st.integers(), min_size=1, max_size=5)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(field=field_strategy())
@example(field={"key": "value"})
@example(field='{"key": "value"}')
@example(field="invalid_json")
@example(field=123)
@example(field=True)
@example(field=[1, 2, 3])
def test_parse_json_fields(field: Any):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    field_copy = copy.deepcopy(field)

    # Call func0 to verify input validity
    try:
        result = _parse_json_fields(field_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "field": field_copy
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