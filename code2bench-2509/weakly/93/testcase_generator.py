from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import base64
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
def encode_url_params(decoded_map, apply_on_keys=None):
    """Code taken from comments in vizro-core/src/vizro/static/js/models/page.js file."""
    encoded_map = {}
    for key, value in decoded_map.items():
        if key in apply_on_keys:
            # This manual base64 encoding could be simplified with base64.urlsafe_b64encode.
            # It's kept here to match the javascript implementation.
            json_str = json.dumps(value, separators=(",", ":"))
            encoded_bytes = base64.b64encode(json_str.encode("utf-8"))
            encoded_str = encoded_bytes.decode("utf-8").replace("+", "-").replace("/", "_").rstrip("=")
            encoded_map[key] = "b64_" + encoded_str
    return encoded_map

# Strategies for generating inputs
def decoded_map_strategy():
    return st.dictionaries(
        keys=st.text(min_size=1, max_size=10),
        values=st.one_of(
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(min_size=1, max_size=10),
            st.lists(st.integers(), min_size=1, max_size=5),
            st.dictionaries(st.text(min_size=1, max_size=10), st.integers(), min_size=1, max_size=3)
        ),
        min_size=1, max_size=5
    )

def apply_on_keys_strategy(decoded_map):
    return st.lists(
        st.sampled_from(list(decoded_map.keys())),
        min_size=1, max_size=len(decoded_map)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    decoded_map=decoded_map_strategy(),
    apply_on_keys=st.builds(
        lambda d: apply_on_keys_strategy(d),
        decoded_map_strategy()
    )
)
@example(
    decoded_map={"key1": "value1", "key2": 123},
    apply_on_keys=["key1"]
)
@example(
    decoded_map={"key1": [1, 2, 3], "key2": {"nested": 456}},
    apply_on_keys=["key2"]
)
@example(
    decoded_map={"key1": 1.23, "key2": "text"},
    apply_on_keys=["key1", "key2"]
)
def test_encode_url_params(decoded_map, apply_on_keys):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    decoded_map_copy = copy.deepcopy(decoded_map)
    apply_on_keys_copy = copy.deepcopy(apply_on_keys)

    # Call func0 to verify input validity
    try:
        expected = encode_url_params(decoded_map_copy, apply_on_keys_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "decoded_map": decoded_map_copy,
            "apply_on_keys": apply_on_keys_copy
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