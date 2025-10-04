from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Any, Dict, Optional
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
def _extract_publication_date(result: Dict[str, Any]) -> Optional[str]:
    # Check for various date fields
    date_fields = ["pagemap", "metatags", "date"]

    for field in date_fields:
        if field in result:
            date_value = result[field]
            if isinstance(date_value, dict):
                # Look for common date keys
                for date_key in ["date", "pubdate", "article:published_time"]:
                    if date_key in date_value:
                        return date_value[date_key]
            elif isinstance(date_value, str):
                return date_value

    return None

# Strategy for generating nested dictionaries with date fields
def result_strategy():
    date_keys = ["date", "pubdate", "article:published_time"]
    date_value = st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    
    return st.one_of([
        st.fixed_dictionaries({
            "pagemap": st.dictionaries(keys=st.sampled_from(date_keys), values=date_value, max_size=3)
        }),
        st.fixed_dictionaries({
            "metatags": st.dictionaries(keys=st.sampled_from(date_keys), values=date_value, max_size=3)
        }),
        st.fixed_dictionaries({
            "date": date_value
        }),
        st.dictionaries(keys=st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10),
                        values=st.one_of([st.integers(), st.floats(), st.text(), st.booleans()]), max_size=5)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(result=result_strategy())
@example(result={"pagemap": {"date": "2023-10-01"}})
@example(result={"metatags": {"article:published_time": "2023-10-01"}})
@example(result={"date": "2023-10-01"})
@example(result={"pagemap": {"pubdate": "2023-10-01"}})
@example(result={"metatags": {"date": "2023-10-01"}})
@example(result={"pagemap": {"other_key": "value"}})
@example(result={"other_key": "value"})
def test_extract_publication_date(result: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    result_copy = copy.deepcopy(result)
    try:
        expected = _extract_publication_date(result_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize meaningful cases
    if any(field in result for field in ["pagemap", "metatags", "date"]):
        generated_cases.append({
            "Inputs": {"result": result},
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