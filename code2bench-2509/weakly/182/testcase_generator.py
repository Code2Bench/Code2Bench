from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import struct
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
def tlv(buf):
    n = 4
    t, l_ = struct.unpack('>HH', buf[:n])
    v = buf[n:n + l_]
    pad = (n - l_ % n) % n
    buf = buf[n + l_ + pad:]
    return t, l_, v, buf

# Strategy for generating valid buffers
def buf_strategy():
    # Generate type and length
    t = st.integers(min_value=0, max_value=65535)
    l_ = st.integers(min_value=0, max_value=65535)
    
    # Generate value based on length
    v = st.binary(min_size=0, max_size=65535)
    
    # Generate padding
    pad = st.integers(min_value=0, max_value=3)
    
    # Combine into a buffer
    return st.builds(
        lambda t, l_, v, pad: struct.pack('>HH', t, l_) + v + bytes(pad),
        t, l_, v, pad
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(buf=buf_strategy())
@example(buf=struct.pack('>HH', 0, 0) + b'')
@example(buf=struct.pack('>HH', 65535, 65535) + b'\x00' * 65535 + b'\x00\x00\x00')
@example(buf=struct.pack('>HH', 123, 4) + b'\x01\x02\x03\x04' + b'\x00')
def test_tlv(buf):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    buf_copy = copy.deepcopy(buf)

    # Call func0 to verify input validity
    try:
        t, l_, v, remaining_buf = tlv(buf_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "buf": list(buf_copy)
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