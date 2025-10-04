from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def get_1d_sincos_pos_embed_from_grid(embed_dim, pos):
    """
    embed_dim: output dimension for each position
    pos: a list of positions to be encoded: size (M,)
    out: (M, D)
    """
    assert embed_dim % 2 == 0
    omega = np.arange(embed_dim // 2, dtype=np.float64)
    omega /= embed_dim / 2.
    omega = 1. / 10000 ** omega  # (D/2,)

    pos = pos.reshape(-1)  # (M,)
    out = np.einsum('m,d->md', pos, omega)  # (M, D/2), outer product

    emb_sin = np.sin(out)  # (M, D/2)
    emb_cos = np.cos(out)  # (M, D/2)

    emb = np.concatenate([emb_sin, emb_cos], axis=1)  # (M, D)
    return emb

# Strategies for generating inputs
def embed_dim_strategy():
    return st.integers(min_value=2, max_value=20).filter(lambda x: x % 2 == 0)

def pos_strategy():
    return hnp.arrays(
        dtype=np.float64,
        shape=st.integers(min_value=1, max_value=10),
        elements=st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(
    embed_dim=embed_dim_strategy(),
    pos=pos_strategy()
)
@example(
    embed_dim=2,
    pos=np.array([0.0])
)
@example(
    embed_dim=4,
    pos=np.array([1.0, -1.0])
)
@example(
    embed_dim=6,
    pos=np.array([0.5, 1.5, 2.5])
)
def test_get_1d_sincos_pos_embed_from_grid(embed_dim: int, pos: np.ndarray):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return

    # Deep copy inputs to avoid modification
    embed_dim_copy = embed_dim
    pos_copy = copy.deepcopy(pos)

    # Call func0 to verify input validity
    try:
        expected = get_1d_sincos_pos_embed_from_grid(embed_dim_copy, pos_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Single position with small embed_dim"
        elif case_count == 1:
            desc = "Multiple positions with medium embed_dim"
        else:
            desc = "Multiple positions with larger embed_dim"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Single position with minimal embed_dim"
        elif case_count == 4:
            desc = "Multiple positions with large embed_dim"
        elif case_count == 5:
            desc = "Single position with large embed_dim"
        elif case_count == 6:
            desc = "Multiple positions with small embed_dim"
        else:
            desc = "Single position with medium embed_dim"

    # Generate usage code
    usage = f"""import numpy as np

# Construct inputs
embed_dim = {embed_dim_copy}
pos = np.array({pos_copy.tolist()})

# Call function
emb = get_1d_sincos_pos_embed_from_grid(embed_dim, pos)
"""

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "embed_dim": embed_dim_copy,
            "pos": pos_copy.tolist()
        },
        "Expected": None,
        "Usage": usage
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)