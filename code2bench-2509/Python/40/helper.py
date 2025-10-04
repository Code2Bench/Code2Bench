import math
from typing import Any, Dict, List



def load_test_cases_from_json() -> List[Dict]:
    # Configure save path
    TEST_CASE_DIR = os.path.abspath("test_cases")
    TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)
    return test_cases

def deep_compare(a, b, tolerance=1e-6):
    if isinstance(a, float) and isinstance(b, float):
        # Compare floats with a tolerance
        return math.isclose(a, b, abs_tol=tolerance)
    elif isinstance(a, dict) and isinstance(b, dict):
        # Compare dictionaries recursively
        return all(
            k in b and deep_compare(a[k], b[k], tolerance)
            for k in a
        ) and len(a) == len(b)
    elif isinstance(a, list) and isinstance(b, list):
        # Compare lists recursively
        return len(a) == len(b) and all(
            deep_compare(ai, bi, tolerance)
            for ai, bi in zip(a, b)
        )
    else:
        # Use strict equality for other types
        return a == b