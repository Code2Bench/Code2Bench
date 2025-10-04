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
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

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
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
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
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    embed_dim_copy = embed_dim
    pos_copy = copy.deepcopy(pos)

    # Call func0 to verify input validity
    try:
        expected = get_1d_sincos_pos_embed_from_grid(embed_dim_copy, pos_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "embed_dim": embed_dim_copy,
            "pos": pos_copy.tolist()
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