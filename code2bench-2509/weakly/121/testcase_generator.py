from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Any, Dict, List, Tuple

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _parse_principal_entries(principal: Dict) -> List[Tuple[Any, Any]]:
    """
    Returns a list of tuples of the form (principal_type, principal_value)
    e.g. [('AWS', 'example-role-name'), ('Service', 'example-service')]
    """
    principal_entries = []
    for principal_type in principal:
        principal_values = principal[principal_type]
        if not isinstance(principal_values, list):
            principal_values = [principal_values]
        for principal_value in principal_values:
            principal_entries.append((principal_type, principal_value))
    return principal_entries

# Strategies for generating inputs
def principal_type_strategy():
    return st.sampled_from(['AWS', 'Service', 'Federated', 'CanonicalUser'])

def principal_value_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=20)

def principal_strategy():
    return st.dictionaries(
        keys=principal_type_strategy(),
        values=st.one_of(
            principal_value_strategy(),
            st.lists(principal_value_strategy(), min_size=1, max_size=5)
        ),
        min_size=1, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(principal=principal_strategy())
@example(principal={'AWS': 'example-role-name'})
@example(principal={'Service': ['example-service1', 'example-service2']})
@example(principal={'AWS': 'example-role-name', 'Service': 'example-service'})
@example(principal={'Federated': ['example-federated1', 'example-federated2']})
@example(principal={'CanonicalUser': 'example-user'})
def test_parse_principal_entries(principal: Dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    principal_copy = copy.deepcopy(principal)

    # Call func0 to verify input validity
    try:
        expected = _parse_principal_entries(principal_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "principal": principal_copy
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