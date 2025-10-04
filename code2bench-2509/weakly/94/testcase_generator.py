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
def decode_url_params(encoded_map, apply_on_keys=None):
    """Code taken from comments in vizro-core/src/vizro/static/js/models/page.js file."""
    decoded_map = {}
    for key, val in encoded_map.items():
        if val.startswith("b64_") and key in apply_on_keys:
            try:
                # This manual base64 decoding could be simplified with base64.urlsafe_b64decode.
                # It's kept here to match the javascript implementation.
                base64_str = val[4:].replace("-", "+").replace("_", "/")
                base64_str += "=" * ((4 - len(base64_str) % 4) % 4)
                binary_data = base64.b64decode(base64_str)
                json_str = binary_data.decode("utf-8")
                decoded_map[key] = json.loads(json_str)
            except Exception as e:
                print(f"Failed to decode URL parameter: {key}, {val} - {e}")  # noqa
    return decoded_map

# Strategies for generating inputs
def encoded_map_strategy():
    return st.dictionaries(
        keys=st.text(min_size=1, max_size=10),
        values=st.one_of(
            st.text(min_size=1, max_size=20),
            st.builds(
                lambda s: f"b64_{s}",
                st.text(min_size=1, max_size=20).map(
                    lambda x: base64.b64encode(json.dumps(x).encode("utf-8")).decode("utf-8")
                    .replace("+", "-")
                    .replace("/", "_")
                    .replace("=", "")
                )
            )
        ),
        min_size=1, max_size=5
    )

def apply_on_keys_strategy(encoded_map):
    return st.lists(
        st.sampled_from(list(encoded_map.keys())),
        min_size=1, max_size=len(encoded_map)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    encoded_map=encoded_map_strategy(),
    apply_on_keys=st.builds(
        lambda m: apply_on_keys_strategy(m),
        encoded_map_strategy()
    )
)
@example(
    encoded_map={"key1": "b64_eyJ2YWx1ZSI6MX0="},
    apply_on_keys=["key1"]
)
@example(
    encoded_map={"key1": "b64_eyJ2YWx1ZSI6MX0=", "key2": "not_b64"},
    apply_on_keys=["key1"]
)
@example(
    encoded_map={"key1": "b64_invalid", "key2": "b64_eyJ2YWx1ZSI6MX0="},
    apply_on_keys=["key1", "key2"]
)
@example(
    encoded_map={"key1": "b64_eyJ2YWx1ZSI6MX0="},
    apply_on_keys=[]
)
def test_decode_url_params(encoded_map, apply_on_keys):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    encoded_map_copy = copy.deepcopy(encoded_map)
    apply_on_keys_copy = copy.deepcopy(apply_on_keys)

    # Call func0 to verify input validity
    try:
        expected = decode_url_params(encoded_map_copy, apply_on_keys_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "encoded_map": encoded_map_copy,
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