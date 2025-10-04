from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import codecs
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
def pack_name(name, off, label_ptrs):
    name = codecs.encode(name, 'utf-8')
    if name:
        labels = name.split(b'.')
    else:
        labels = []
    labels.append(b'')
    buf = b''
    for i, label in enumerate(labels):
        key = b'.'.join(labels[i:]).upper()
        ptr = label_ptrs.get(key)
        if ptr is None:
            if len(key) > 1:
                ptr = off + len(buf)
                if ptr < 0xc000:
                    label_ptrs[key] = ptr
            i = len(label)
            buf += struct.pack("B", i) + label
        else:
            buf += struct.pack('>H', (0xc000 | ptr))
            break
    return buf

# Strategies for generating inputs
def name_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P'), min_codepoint=32, max_codepoint=126), min_size=0, max_size=50)

def off_strategy():
    return st.integers(min_value=0, max_value=0xffff)

def label_ptrs_strategy():
    return st.dictionaries(
        keys=st.binary(min_size=1, max_size=50),
        values=st.integers(min_value=0, max_value=0xffff),
        min_size=0, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    name=name_strategy(),
    off=off_strategy(),
    label_ptrs=label_ptrs_strategy()
)
@example(name="", off=0, label_ptrs={})
@example(name="example.com", off=0, label_ptrs={})
@example(name="sub.example.com", off=0, label_ptrs={b'EXAMPLE.COM': 10})
@example(name="a.b.c.d", off=0, label_ptrs={b'C.D': 20, b'B.C.D': 30})
def test_pack_name(name, off, label_ptrs):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    name_copy = copy.deepcopy(name)
    off_copy = copy.deepcopy(off)
    label_ptrs_copy = copy.deepcopy(label_ptrs)

    # Call func0 to verify input validity
    try:
        expected = pack_name(name_copy, off_copy, label_ptrs_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "name": name_copy,
            "off": off_copy,
            "label_ptrs": {k.decode('utf-8', errors='replace'): v for k, v in label_ptrs_copy.items()}
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