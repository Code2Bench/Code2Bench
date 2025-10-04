from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from datetime import datetime
from typing import Any

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _prepare_node_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Ensure metadata has proper datetime fields and normalized types.

    - Fill `created_at` and `updated_at` if missing (in ISO 8601 format).
    - Convert embedding to list of float if present.
    """
    now = datetime.utcnow().isoformat()

    # Fill timestamps if missing
    metadata.setdefault("created_at", now)
    metadata.setdefault("updated_at", now)

    # Normalize embedding type
    embedding = metadata.get("embedding")
    if embedding and isinstance(embedding, list):
        metadata["embedding"] = [float(x) for x in embedding]

    return metadata

# Strategies for generating metadata
def metadata_strategy():
    # Generate a dictionary with optional fields
    return st.dictionaries(
        keys=st.sampled_from(["created_at", "updated_at", "embedding", "other_field"]),
        values=st.one_of(
            st.datetimes().map(lambda dt: dt.isoformat()),
            st.lists(st.one_of(st.floats(allow_nan=False, allow_infinity=False), st.integers()), min_size=1, max_size=10),
            st.text(min_size=1, max_size=10)
        ),
        min_size=0, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(metadata=metadata_strategy())
@example(metadata={})
@example(metadata={"created_at": "2023-01-01T00:00:00"})
@example(metadata={"updated_at": "2023-01-01T00:00:00"})
@example(metadata={"embedding": [1.0, 2.0, 3.0]})
@example(metadata={"embedding": [1, 2, 3]})
@example(metadata={"created_at": "2023-01-01T00:00:00", "updated_at": "2023-01-01T00:00:00", "embedding": [1.0, 2.0, 3.0]})
def test_prepare_node_metadata(metadata: dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    metadata_copy = copy.deepcopy(metadata)

    # Call func0 to verify input validity
    try:
        result = _prepare_node_metadata(metadata_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "metadata": metadata_copy
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